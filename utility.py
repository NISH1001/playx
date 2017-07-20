#!/usr/bin/env python3


"""
    A utility module for misc operations
"""

import subprocess
import sys
import os
import shutil
import time

import urllib.request
import requests

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
    print("Playing using vlc command line...")
    cli = "cvlc '{}'".format(stream_url)
    os.system(cli)

def download(url, filename='test'):
    # download the song here
    print(url)
    print("... download in progress... :D ")
    try:
        urllib.request.urlretrieve(url, filename+'.mp3')
    except KeyboardInterrupt:
        print(" -_- why y no wait for completion -_-")
        return False
    print("... downloaded 100%, perhaps ... :P")
    return True

def download2(url, filename="test"):
    print(url)
    data = requests.get(url).content
    with open(filename+".mp3", "wb") as f:
        f.write(data)

def convert_to_mp3(filename):
    print("Converting to mp3...Have patience...")
    new_file = str(time.time()) + filename
    cli = "ffmpeg -i {0} {1}".format(filename, new_file)
    #cli = "ffmpeg -i {0} -map 0:a:0 -b:a 96k {1}".format(filename, new_file)
    output, error = exe(cli)
    shutil.move(new_file, filename)

def main():
    pass

if __name__ == "__main__":
    main()

