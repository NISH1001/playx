#!/usr/bin/env python3


"""
    A utility module for misc operations
"""

import os
import subprocess


def exe(command):
    command = command.strip()
    c = command.split()
    output, error = subprocess.Popen(c,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE).communicate()
    output = output.decode('utf-8').strip()
    error = error.decode('utf-8').strip()
    return (output, error)


def run_mpd(url):
    """Nana."""
    cm1 = 'mpc pause'
    cm2 = 'mpc clear'
    cm3 = 'mpc insert "{}"'.format(url)
    cm4 = 'mpc play'
    anda = '&&'
    cli = cm1 + '&&' + cm2 + '&&' + cm3 + '&&' + cm4
    os.system(cli)


def main():
    pass

if __name__ == "__main__":
    main()
