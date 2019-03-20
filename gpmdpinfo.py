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


def truncate(string, width):
    if len(string) > width:
        string = string[:width-3] + '...'
    return string


def format_song_info(title, artist, album, chars_to_remove):
    # not cutting already short data
    if chars_to_remove > 0:
        array = (title, artist, album)
        average = int((len(title) + len(artist) + len(album)) / 3)
        print("av", average)
        for item in array:
            if len(item) > average:
                print(item, int(chars_to_remove/3))
    return "{}, {}, {}".format(title, artist, album)


def resize_song_info(size, icon, status, title, artist, album, time):
    song_info_len = size - len(icon) - len(status) - len(time) - 3
    chars_to_remove = (len(title) + len(artist) + len(album)) - song_info_len
    print("song_info_len", song_info_len)
    print("chars_to_remove", chars_to_remove)
    #
    # print(title[0:int(song_info_len/3)])


def string_format(icon, status, title, artist, album, time):
    chars_to_remove = 0
    for arg in argv:
        if arg.isdigit():
            size = int(arg)
            str_len = len(icon) + len(status) + len(title) + len(artist) + len(album) + len(time) + 3
            song_info_len = size - len(icon) - len(status) - len(time) - 3
            chars_to_remove = (len(title) + len(artist) + len(album)) - song_info_len

            print("str_len", str_len)
            if str_len > size:
                resize_song_info(size, icon, status, title, artist, album, time)

    print(" {} {} {} {}".format(icon, status, format_song_info(title, artist, album, chars_to_remove), time))
    # print(len(" {} {} {} {}".format(icon, status, song_info, time)))


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

            string_format(show_icon(),
                          get_status(info['playing']),
                          info['song']['title'],
                          info['song']['artist'],
                          info['song']['album'],
                          format_time(human_time(info['time']['current']), human_time(info['time']['total']))
                          )
            stdout.flush()
        sleep(1)


def single_print(json_info):
    with open(json_info, 'r') as json_file:
        info = load(json_file)

    if info['song']['title'] is not None:
        # song_info = format_song_info(info['song']['title'], info['song']['artist'], info['song']['album'])

        # time = format_time(human_time(info['time']['current']), human_time(info['time']['total']))

        string_format(show_icon(),
                      get_status(info['playing']),
                      info['song']['title'],
                      info['song']['artist'],
                      info['song']['album'],
                      format_time(human_time(info['time']['current']), human_time(info['time']['total']))
                )


def main():
    try:
        json_info = json_location(getuser()) 
        if "cont" in argv or "clear" in argv or "rotate" in argv:
            cont_print(json_info)
        else:
            single_print(json_info)
    except:
        return 0
    

if __name__ == '__main__':
    if gpm_run_check():
        main()
    else:
        print(" ")
