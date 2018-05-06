#!/usr/bin/env python3

from getpass import getuser
from json import load
from time import sleep
from sys import argv
from subprocess import getoutput
from platform import system

'''
    Finding the correct json file depending on the OS
    GPMDP only supported on Linux, MacOS and windows
'''


def json_location(user):
    dir1 = 'Google Play Music Desktop Player'
    dir2 = 'json_store'
    filename = 'playback.json'

    if system() == 'Darwin':
        return "/Users/{0}/Library/Application Support/{1}/{2}/{3}".format(user, dir1, dir2, filename)
    elif system() == 'Linux':
        return "/home/{0}/.config/{1}/{2}/{3}".format(user, dir1, dir2, filename)
    # elif system() == 'Windows':
    #     return "%APPDATA%\\{}\\{}\\{}".format(dir1, dir2, filename)


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
    command = "ps -Aef | grep -i \"Google Play Music Desktop Player\" | grep -v grep | wc -l"
    if int(getoutput(command)) > 0:
        return True
    else:
        return False


def format_song_info(title, artist, ablum):
    return "{}, {}, {}".format(title, artist, ablum)


def string_format(icon, song_info, time):
    return " {}{} {}".format(icon, song_info, time)


def show_icon():
    if "noicon" in argv:
        return ""
    else:
        return " "


def format_time(current, total):
    time = "| {}/{} ".format(current, total)
    if "shorttime" in argv:
        time = "| {} ".format(current)
    elif "notime" in argv:
        time = ""

    return time


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


def cont_print():
    json_info = json_location(getuser())

    current_song = CurrentSong()
    i = 0

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
            song_info = song_info[0:20]
        
        icon = show_icon()

        time = format_time(human_time(info['time']['current']), human_time(info['time']['total']))
        
        print(string_format(icon, song_info, time))

        sleep(1)


def single_print():
    json_info = json_location(getuser())

    with open(json_info, 'r') as json_file:
        info = load(json_file)
    
    song_info = format_song_info(info['song']['title'], info['song']['artist'], info['song']['album'])

    time = format_time(human_time(info['time']['current']), human_time(info['time']['total']))
    icon = show_icon()

    if info['song']['title'] is not None:
        print(string_format(icon, song_info, time))


def main():
    if "cont" in argv or "clear" in argv or "rotate" in argv:
        cont_print()
    else:
        single_print()


if __name__ == '__main__':
    if gpm_run_check():
        main()
    else:
        print()
