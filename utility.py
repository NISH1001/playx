#!/usr/bin/env python3
"""A utility module for misc operations."""

import os
import subprocess
import time


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


def run_mpd(url):
    """Run the song in mpd."""
    # Pause mpd
    cm1 = 'mpc pause'
    # Clear the playlist
    cm2 = 'mpc clear'
    # Insert the song
    cm3 = 'mpc insert "{}"'.format(url)
    # Play the song
    cm4 = 'mpc play'
    cli = cm1 + '&&' + cm2 + '&&' + cm3 + '&&' + cm4
    os.system(cli)


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
