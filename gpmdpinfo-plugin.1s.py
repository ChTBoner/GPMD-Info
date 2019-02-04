#!/usr/bin/env python3

# <bitbar.title>gpmdpinfo.py</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>ChTBoner</bitbar.author>
# <bitbar.author.github>chtboner</bitbar.author.github>
# <bitbar.desc>Displays currently playing song from Google Play Music Desktop Player.</bitbar.desc>
# <bitbar.image>https://imgur.com/qDPtOxl</bitbar.image>
# <bitbar.dependencies>python3, psutil, requests</bitbar.dependencies>
#
# by ChTBoner


"""
    Displays currently playing song info and status from Google Play Music Desktop Player
    https://www.googleplaymusicdesktopplayer.com/

    Plugin made for BitBar for MacOS X and Argos for Gnome Desktop
"""

from getpass import getuser
from json import load
from platform import system
import os
import psutil
import base64
import requests

APP_NAME = 'Google Play Music Desktop Player'
MAX_INFO_LEN = 30
IMAGE_SIZE = 150


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


def gpm_run_check():
    """ Run program only if google play music is up. """

    for p in psutil.process_iter():
        if APP_NAME in p.name():
            return True

    return False


def human_time(time_in_ms):
    """ converts time in human readable time """

    minutes = int(time_in_ms / 60000)
    seconds = int((time_in_ms - (int(minutes) * 60000)) / 1000)

    if seconds < 10:
        time_for_humanz = str(minutes) + ':0' + str(seconds)
    else:
        time_for_humanz = str(minutes) + ':' + str(seconds)

    return time_for_humanz


def format_time(current, total):
    time = "- {}/{} ".format(current, total)

    return time


def format_song_info(title, artist, ablum):
    """ 
        Formats the song info
        "|" needs to be changed as it is used to pipe parameters
         Maximum number of chars can be set with the global MAX_INFO_LEN variable, to avoid occupying the full bar
    """
    
    if title.find('|') != -1:
        s = list(title)
        s[title.find('|')] = "-"
        title = ''.join(s)

    song_info = "{}, {}, {}".format(title, artist, ablum)

    if len(song_info) > MAX_INFO_LEN:
        song_info = song_info[0:MAX_INFO_LEN - 3] + '...'

    return song_info


def get_status(status):
    """ returns the correct icon if a song is playing or in pause"""
    
    if status is False:
        return '❚❚'
    else:
        return '▶'


def print_image(url):
    """ get the base64 data from the image url """
    base_image = base64.b64encode(requests.get(url).content).decode()
    print('| image={} imageWidth={} imageHeight={}'.format(base_image, IMAGE_SIZE, IMAGE_SIZE))


def main():
    # find the json info file and open it
    json_info = json_location(getuser())

    with open(json_info, 'r') as json_file:
        info = load(json_file)

    # info will be none if no songs where played yet
    if info['song']['title'] is not None:
        # formating the data before printing
        song_info = format_song_info(info['song']['title'], info['song']['artist'], info['song']['album'])
        time = format_time(human_time(info['time']['current']), human_time(info['time']['total']))
        status_icon = get_status(info['playing'])

        print(" ♫ {} {} {}".format(status_icon, song_info, time))

    print('---')
    # print the full data
    print("Song:    {}".format(info['song']['title']))
    print("Artist:  {}".format(info['song']['artist']))
    print("Album:   {}".format(info['song']['album']))

#    if info['song']['albumArt'] is not None:
#        print('---')
#        print_image(info['song']['albumArt'])

    #  if lyrics are available in the json file, print them in the dropdown menu if not empty
    if info['songLyrics'] is not None and info['songLyrics'] != '':
        print('---')
        print("Lyrics:")
        print(info['songLyrics'])


if __name__ == '__main__':
    if gpm_run_check():
        main()
