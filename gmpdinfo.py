#!/usr/bin/env python3

from getpass import getuser
from json import load
from helpers import json_location, human_time, gpm_run_check


def main():
    json_info = json_location(getuser())

    with open(json_info, 'r') as json_file:
        info = load(json_file)

    if info['song']['title'] != None:
        print("  {}, {}, {} | {}:{} ".format(info['song']['title'], info['song']['artist'], info['song']['album'],
                                              human_time(info['time']['current']), human_time(info['time']['total'])))


if __name__ == '__main__':
    if gpm_run_check():
        main()
    else:
        print()
