#!/usr/bin/env python3
"""A utility module for misc operations."""

import os
import subprocess
import time
from shutil import copy


def exe(command):
    """Execute the command externally."""
    command = command.strip()
    c = command.split()
    output, error = subprocess.Popen(c,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE).communicate()
    output = output.decode('utf-8').strip()
    error = error.decode('utf-8').strip()
    return (output, error)


def run_mpd(url, play_type):
    """Run the song in mpd."""
    # Pause mpd
    cm1 = 'mpc pause'
    exe(cm1)
    # Clear the playlist
    cm2 = 'mpc clear'
    exe(cm2)
    # Insert the song
    if play_type == 'local':
        # Move the song to mpd dir
        move_to_mpd_dir(url)
        os.chdir(find_mpd_dir())
        cm3 = 'mpc insert {}'.format('temp.mp3')
    else:
        cm3 = 'mpc insert {}'.format(url)
    exe(cm3)
    # Play the song
    cm4 = 'mpc play'
    exe(cm4)
    if play_type == 'local':
        os.remove(os.path.join(find_mpd_dir(), 'temp.mp3'))


def find_mpd_dir():
    """Find the mpd music directory."""
    home = os.path.expanduser('~')
    path = os.path.join(home, '.config', 'mpd', 'mpd.conf')

    stream = open(path, 'r')
    while True:
        nana = stream.readline()
        if not nana:
            break
        if 'music_directory' in nana and '#' not in nana:
            nana = nana[nana.index('"') + 1:-2]
            nana = os.path.expanduser(nana)
            return nana

    return False


def move_to_mpd_dir(name):
    """Move the song to mpd_dir."""
    mpd_dir = find_mpd_dir()

    if not mpd_dir:
        pass
    else:
        copy(name, os.path.join(mpd_dir, 'temp.mp3'))


def toggle():
    """Toggle mpd."""
    cm = 'mpc toggle'
    os.system(cm)


def get_status():
    """Return the status of mpd."""
    status, error = exe('mpc status')

    if 'playing' in status:
        return 'Playing'
    elif 'paused' in status:
        return 'Paused'
    else:
        return False


def is_on():
    """Check if mpc is on."""
    status = get_status()
    if status == 'Playing' or status == 'Paused':
        return True
    else:
        return False

    time.sleep(0.5)


if __name__ == '__main__':
    print(is_on())
