#!/usr/bin/env python3

from youtube import get_youtube_streams
from utility import download, download2, convert_to_mp3


def main():
    print("processing... :D")
    url = "https://www.youtube.com/watch?v=-qfCrYwdqCA"
    stream = get_youtube_streams(url)
    filename = "test"
    download(stream['audio'], filename)
    convert_to_mp3(filename + ".mp3")


if __name__ == "__main__":
    main()

