#!/usr/bin/env python3

from getpass import getuser
from json import load
from time import sleep
from sys import argv, stdout
from platform import system
import os
import psutil

APP_NAME = 'Google Play Music Desktop Player'

'''
    Finding the correct json file depending on the OS
    GPMDP only supported on Linux, MacOS and windows
    Be careful if 
'''


def json_location(user):
    json_dir = 'json_store'
    filename = 'playback.json'

    if system() == 'Darwin':
        return os.path.join('/Users', user, 'Library/Application Support', APP_NAME, json_dir, filename)
    elif system() == 'Linux':
        # runs in flatpack
        if os.path.isfile(os.path.join('/home', user, '.var/app/com.googleplaymusicdesktopplayer.GPMDP', 'config', APP_NAME, json_dir, filename)):
            return os.path.join('/home', user, '.var/app/com.googleplaymusicdesktopplayer.GPMDP', 'config', APP_NAME, json_dir, filename)
        else:
            return os.path.join('/home', user, '.config', APP_NAME, json_dir, filename)
    # elif system() == 'Windows':
    #     return "%APPDATA%\\{}\\{}\\{}".format(APP_NAME, dir2, filename)
    return "OS not supported yet"


'''
    converts time in human readable time
'''


def human_time(time_in_ms):
    minutes = int(time_in_ms / 60000)
    seconds = int((time_in_ms - (int(minutes) * 60000)) / 1000)

    if seconds < 10:
        time_for_humanz = str(minutes) + ':0' + str(seconds)
    else:
        time_for_humanz = str(minutes) + ':' + str(seconds)

    return time_for_humanz


'''
    Run program only if google play music is up.
'''


def gpm_run_check():
    for p in psutil.process_iter():
        if APP_NAME in p.name():
            return True

    return False


def format_song_info(title, artist, ablum):
    if title.find('|') != -1:
        s = list(title)
        s[title.find('|')] = "-"
        title = ''.join(s)
    return "{}, {}, {}".format(title, artist, ablum)


def string_format(icon, status, song_info, time):
    print(" {} {} {} {}".format(icon, status, song_info, time))


def show_icon():
    if "noicon" in argv:
        return ""
    else:
        return " "


def format_time(current, total):
    time = "- {}/{} ".format(current, total)
    if "shorttime" in argv:
        time = "- {} ".format(current)
    elif "notime" in argv:
        time = ""

    return time


def get_status(status):
    """ returns the correct icon if a song is playing or in pause"""

    if status is False:
        return '❚❚'
    else:
        return '▶'


'''
    print continuously if "clear or "rotate" option is set
    "rotate" option will print song info, rotating from right to left
    "clear" clears the terminal
'''


class CurrentSong:
    def __init__(self):
        self.title = ''
        self.artist = ''
        self.album = ''


def cont_print(json_info):
    i = 0

    current_song = CurrentSong()

    while True:
        with open(json_info, 'r') as json_file:
            info = load(json_file)

        if info['song']['title'] is not None:
            # reset counter if song changed
            if info['song']['title'] != current_song.title or \
                    info['song']['artist'] != current_song.artist or info['song']['album'] != current_song.album:
                current_song.title = info['song']['title']
                current_song.artist = info['song']['artist']
                current_song.album = info['song']['album']
                i = 0

            song_info = format_song_info(info['song']['title'], info['song']['artist'], info['song']['album'])

            if "rotate" in argv:
                song_info = "{} | {}".format(song_info[i:], song_info[:i])

            if i < len(song_info):
                i += 1
            else:
                i = 0

            if "clear" in argv:
                print("\033[H\033[J")

            if "short" in argv:
                song_info = song_info[0:50]

            time = format_time(human_time(info['time']['current']), human_time(info['time']['total']))
            
            string_format(show_icon(), get_status(info['playing']), song_info, time)
            stdout.flush()
        sleep(1)


def single_print(json_info):
    with open(json_info, 'r') as json_file:
        info = load(json_file)

    song_info = format_song_info(info['song']['title'], info['song']['artist'], info['song']['album'])

    time = format_time(human_time(info['time']['current']), human_time(info['time']['total']))

    if "short" in argv:
        song_info = song_info[0:50]
        time = ""

    icon = show_icon()

    if info['song']['title'] is not None:
        string_format(icon, get_status(info['playing']), song_info, time)


def main():
    json_info = json_location(getuser())

    if "cont" in argv or "clear" in argv or "rotate" in argv:
        cont_print(json_info)
    else:
        single_print(json_info)


if __name__ == '__main__':
    if gpm_run_check():
        try:
            main()
        except Exception:
            print("")
    else:
        print(" ")
