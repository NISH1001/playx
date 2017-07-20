#!/usr/bin/env python3
"""
    Module for caching songs.
"""

import os

class Cache:
    def __init__(self, directory="~/Music/"):
        self.create_cache_directory(directory)

    def create_cache_directory(self, directory):
        print("Creating the cache directory...")
        directory = directory.strip()
        directory = os.path.abspath(os.path.expanduser(directory))

        # Create the directory if doesn't exist.
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.directory = directory

    def __str__(self):
        string = "Directory : {}".format(self.directory)
        return string

def main():
    cache = Cache("~/.playx")
    print(cache)

if __name__ == "__main__":
    main()

