#!/usr/bin/env python3

from cache import Cache
from songfinder import search_song, SongSource
from utility import download, download2, convert_to_mp3, run_cvlc
from youtube import get_youtube_streams, search_youtube

import sys

def main():
    args = sys.argv[1:]
    cache = Cache("~/.playx/")
    if len(args) > 0:
        song = ' '.join(args)
        source, result = search_song(song)
        url = ""
        if source == SongSource.CACHE:
            print("Song found in the cache...")
            url = result
        elif source == SongSource.NETWORK:
            print("Song found in youtube...")
            stream = get_youtube_streams(result.url)
            print(stream)
            filename = cache.directory + "/" + result.get_hash() + ".mp3"
            url = filename
            download2(stream['audio'], filename)
            convert_to_mp3(filename)
        else:
            return
        run_cvlc(url)


    else:
        print("Lol! That is a retarded command just like me...")

if __name__ == "__main__":
    main()

