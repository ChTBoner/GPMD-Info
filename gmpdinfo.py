#!/usr/bin/env python3

from getpass import getuser
from json import load
from helpers import json_location, human_time, gpm_run_check
from time import sleep
from sys import argv

def format_time(current, total):
    time = "| {}/{} ".format(current, total)
    if "shorttime" in argv:
        time = "| {} ".format(current)
    elif "notime" in argv:
        time = ""

    return time

class CurrentSong:
    def __init__(self):
        self.title = ''
        self.artist = ''
        self.album = ''


'''
    print continuously if "clear or "rotate" option is set
    "rotate" option will print song info, rotating from right to left
    "clear" clears the terminal
'''


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

        song_info = "{}, {}, {}".format(info['song']['title'], info['song']['artist'], info['song']['album'])
        # if loop over chars is over, reset i to 0
        if i < len(song_info):
            i += 1
        else:
            i = 0

        if "clear" in argv:
            print("\033[H\033[J")

        if "rotate" in argv:
            song_info = "{} | {}".format(song_info[i:], song_info[:i])
        if "short" in argv:
            song_info = song_info[0:20]

        time = format_time(human_time(info['time']['current']), human_time(info['time']['total']))

        print(" ", song_info, time)

        sleep(0.3)


def single_print():
    json_info = json_location(getuser())

    with open(json_info, 'r') as json_file:
        info = load(json_file)

    time = format_time(human_time(info['time']['current']), human_time(info['time']['total']))

    if info['song']['title'] is not None:
        # print("\033[H\033[J")
        print("  {}, {}, {}".format(info['song']['title'], info['song']['artist'], info['song']['album']), time)


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
