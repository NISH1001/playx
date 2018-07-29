#!/usr/bin/env python3

"""
    Main function for playx.
"""

import argparse

from cache import (
    Cache, search_locally
)

from utility import (
    direct_to_play, run_mpv_dir
)

from youtube import (
    grab_link, get_youtube_title
)

from songfinder import search
from lyrics import search_lyricswikia
from stringutils import is_song_url

def parse():
    """Parse the arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('song',
                        help="Name or youtube link of song to download",
                        default=None, type=str, nargs="*")
    parser.add_argument('--play-cache',
                        action='store_true',
                        help="Play all songs from the cache.")
    parser.add_argument('--lyrics', '-l',
                        action='store_true',
                        help="Show lyircs of the song.")
    args = parser.parse_args()
    return parser, args

def stream(search_type, value=None, show_lyrics=False):
    """
        Start streaming the song.
        First search in the local cache.
        If no song is found in the cache, search in the youtube.

        Fow now, the search in the cache happens based on individual words.
        This will be later improved
    """
    # if query by name -> search locally
    if search_type == 'name':
        match = search_locally(value)
        if match:
            value = match[1]
            title = match[0]
        else:
            result = search(value)
            result.display()
            title = result.title
            value = grab_link(result.url, title)

        if show_lyrics:
            lyric = search_lyricswikia(title)
            print("----\n{}\n----".format(lyric))
    else:
        # if url just grab the stream url (no caching is done)
        title = get_youtube_title(value)
        value = grab_link(value, title)

    direct_to_play(value)


def stream_cache_all(cache):
    run_mpv_dir(cache.dir)


def main():
    """Search the song in youtube and stream through mpd."""
    parser, args = parse()
    args.song = ' '.join(args.song)
    if not args.song and args.play_cache:
        cache = Cache("~/.playx/")
        stream_cache_all(cache)
    if is_song_url(args.song):
        stream('url', args.song, args.lyrics)
    elif not args.song:
        parser.print_help()
    else:
        stream('name', args.song, args.lyrics)


if __name__ == "__main__":
    main()
