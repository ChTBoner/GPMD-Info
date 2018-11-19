#!/usr/bin/env python3

from getpass import getuser
from json import load
from sys import argv
from platform import system
from requests import get
import base64
import os
import psutil

APP_NAME = 'Google Play Music Desktop Player'

'''
    Finding the correct json file depending on the OS
    GPMDP only supported on Linux, MacOS
'''


def json_location(user):
    json_dir = 'json_store'
    filename = 'playback.json'

    if system() == 'Darwin':
        return os.path.join('/Users', user, 'Library/Application Support', APP_NAME, json_dir, filename)
    elif system() == 'Linux':
        return os.path.join('/home', user, '.config', APP_NAME, json_dir, filename)


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


def string_format(icon, song_info, time):
    return " {}{} {}".format(icon, song_info, time)


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


def single_print(info):
    song_info = format_song_info(info['song']['title'], info['song']['artist'], info['song']['album'])
    time = format_time(human_time(info['time']['current']), human_time(info['time']['total']))

    if "short" in argv:
        song_info = song_info[0:20]
        time = ""

    icon = show_icon()

    if info['song']['title'] is not None:
        print(string_format(icon, song_info, time))


def print_image(link):
    encoded_image = base64.b64encode(get(link).content).decode()
    print("| image=" + encoded_image + "imageWidth=200 imageHeight=200")


def main():
    json_info = json_location(getuser())

    with open(json_info, 'r') as json_file:
        info = load(json_file)

    single_print(info)

    print('---')
    print_image(info['song']["albumArt"])
    print('---')
    if info['songLyrics'] is not None and info['songLyrics'] != '':
        print(info['songLyrics'])


if __name__ == '__main__':
    if gpm_run_check():
        main()
    else:
        print(" ")
