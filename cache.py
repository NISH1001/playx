#!/usr/bin/env python3
"""
    Module for caching songs.
"""

import glob
import os

class Cache:
    def __init__(self, directory="~/.playx/"):
        self.directory = directory
        self.create_directory(directory)

    def create_directory(self, directory):
        print("Creating the cache directory...")
        directory = directory.strip()
        directory = os.path.abspath(os.path.expanduser(directory))

        # Create the directory if doesn't exist.
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.directory = directory

    def list_mp3(self):
        os.chdir(self.directory)
        for file in glob.glob("*.mp3"):
            print(file)

    def __str__(self):
        string = "Directory : {}".format(self.directory)
        return string

def main():
    cache = Cache("~/.playx")
    cache.list_mp3()
    print(cache)

if __name__ == "__main__":
    main()

