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
        time_for_humanz =  str(minutes) + ':0' + str(seconds)
    else: time_for_humanz =  str(minutes) + ':' + str(seconds)

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
