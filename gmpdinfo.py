#!/usr/bin/env python3

from getpass import getuser
from json import load
from helpers import json_location, human_time, gpm_run_check
from time import sleep
from sys import argv

class CurrentSong:
    def __init__(self):
        self.title = ''
        self.artist = ''
        self.album = ''

def rotate(song_info, i):
    rotated = song_info[i:] + ' | ' + song_info[:i]
    return rotated


def rotation_print(json_info):
    current_song = CurrentSong()
    i = 0
    while True:
        with open(json_info, 'r') as json_file:
            info = load(json_file)

        if info['song']['title'] is not None:
            if info['song']['title'] != current_song.title or info['song']['artist'] != current_song.artist or info['song']['album'] != current_song.album:
                current_song.title = info['song']['title']
                current_song.artist = info['song']['artist']
                current_song.album = info['song']['album']
                # reset counter
                i = 0

        print("\033[H\033[J")
        song_info = "{}, {}, {}".format(info['song']['title'],
                                            info['song']['artist'],
                                            info['song']['album'])
        rotated = rotate(song_info, i)

        print(i, len(song_info))

        if i < len(song_info):
            i += 1
        else:
            i = 0

        print(" ", rotated + " | {}/{} ".format(human_time(info['time']['current']), human_time(info['time']['total'])))

        sleep(0.3)



def line_print(json_info):
    with open(json_info, 'r') as json_file:
        info = load(json_file)

    if info['song']['title'] is not None:
        # print("\033[H\033[J")
        print("  {}, {}, {} | {}/{} ".format(info['song']['title'], info['song']['artist'], info['song']['album'],
                                              human_time(info['time']['current']), human_time(info['time']['total'])))

def main():
    json_info = json_location(getuser())

    if len(argv) >= 2 and "rotate" in argv:
        rotation_print(json_info)
    else:
        line_print(json_info)


if __name__ == '__main__':
    if gpm_run_check():
        main()
    else:
        print()
