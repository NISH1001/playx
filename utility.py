#!/usr/bin/env python3

import subprocess
import sys
import os

def exe(command):
    command = command.strip()
    c = command.split()
    output, error = subprocess.Popen(c,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE).communicate()
    output = output.decode('utf-8').strip()
    error = error.decode('utf-8').strip()
    return (output, error)

def run_cvlc(stream_url):
    cli = "cvlc '{}'".format(stream_url)
    os.system(cli)


def main():
    pass

if __name__ == "__main__":
    main()

