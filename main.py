#!/usr/bin/env python3

from youtube import get_youtube_streams, search_youtube
from utility import download, download2, convert_to_mp3, run_cvlc

import sys

def main():
    args = sys.argv[1:]
    if len(args) > 0:
        song_name = ' '.join(args)
        videos = search_youtube(song_name)
        video = videos[0]
        url = video.url
        print(url)
        stream = get_youtube_streams(url)
        print(stream)
        filename = "test"
        download(stream['audio'], filename)
        convert_to_mp3(filename + ".mp3")
        run_cvlc(filename + ".mp3")

    else:
        print("Lol! That is a retarded command just like me...")

if __name__ == "__main__":
    main()

