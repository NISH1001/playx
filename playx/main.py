#!/usr/bin/env python3

"""
    Main function for playx.
"""

import argparse

from playx.cache import (
    Cache, search_locally
)

from playx.utility import (
    direct_to_play, run_mpv_dir, move_songs
)

from playx.youtube import (
    grab_link
)

from playx.playlist.playlist import (
    Playlist
)

from playx.playlist.playxlist import (
    Playxlist
)

from playx.player import (
    Player
)

from playx.logger import Logger
from playx.songfinder import search
from playx.stringutils import is_song_url

from playx.playlist.autoplaylist import (
    CountBasedAutoPlaylist
)

from random import shuffle


# Get the logger
logger = Logger('main')


def parse():
    """Parse the arguments."""
    parser = argparse.ArgumentParser(description="playx - Search and play\
                                     any song that comes to your mind.\n\
                                     If you have any issues, raise an issue in\
                                     the github\
                                     (https://github.com/NISH1001/playx) page")
    parser.add_argument('song',
                        help="Name or youtube link of song to download",
                        default=None, type=str, nargs="*")
    parser.add_argument('-p', '--play-cache',
                        action='store_true',
                        help="Play all songs from the cache.\
                        The cache is located at ~/.playx/songs/ by default")
    parser.add_argument('-n', '--no-cache',
                        action='store_true',
                        help="Don't download the song for later use.")
    parser.add_argument('-auto', '--auto',
                        action='store_true',
                        help="Auto generate playlist")
    parser.add_argument('-s', '--shuffle',
                        action='store_true',
                        help='Shuffle the playlist. Not applicbble if playlist\
                        not passed.')
    parser.add_argument('-d', '--dont-cache-search',
                        action='store_true',
                        help="Don't search the song in the cache.")
    parser.add_argument('-l', '--lyrics',
                        action='store_true',
                        help="Show lyircs of the song.")
    parser.add_argument('--pl-start', help="Start position in case a\
                         playlist is passed. If passed without a playlist\
                         it has no effect.", default=None, type=int)
    parser.add_argument('--pl-end', help="End position in case a \
                        playlist is passed. If passed without a playlist\
                        it has no effect.", default=None, type=int)
    args = parser.parse_args()
    return parser, args


def online_search(value, no_cache):
    """Search the song online."""
    result = search(value)
    if result is None:
        return print("No results found")
    result.display()
    title = result.title
    value = grab_link(result.url, title, no_cache)
    return value, title


def get_value(value, no_cache):
    """Get the value of the song."""
    value = online_search(value, no_cache)
    if value is None:
        print("No audio attached to video")
        exit(-1)
    else:
        return value[0], value[1]


def stream_from_name(value=None, show_lyrics=False, no_cache=False,
                     dont_cache_search=False):
    """Start streaming the song.

    First search in the local cache.
    If no song is found in the cache, search in the youtube.
    """
    # Need to check if searching locally is forbidden
    if not dont_cache_search:
        match = search_locally(value)
        if match:
            value = match[1]
            title = match[0]
        else:
            value, title = get_value(value, no_cache)
    else:
        value, title = get_value(value, no_cache)

    direct_to_play(value, show_lyrics, title)


def stream_from_url(url, show_lyrics=False, no_cache=False,
                    dont_cache_search=False, ytObj=None):
    """Stream the song using the url.

    Before searching the stream, get the title of the song
    If local search is not forbidden, search it locally
    """
    if ytObj is None:
        result = search(url)
        if result is None:
            return print("No results found")
    else:
        result = ytObj
    result.display()
    title = result.title

    # Now search the song locally
    if not dont_cache_search:
        match = search_locally(title)
        if match:
            # Change the value to local path
            value = match[1]
        else:
            value = grab_link(result.url, title, no_cache)
    else:
        value = grab_link(result.url, title, no_cache)

    direct_to_play(value, show_lyrics, title)


def stream_cache_all(cache):
    run_mpv_dir(cache.dir)


def playx(parser, args, song):
    """Search the song in youtube and stream through mpd."""
    if not song and args.play_cache:
        cache = Cache("~/.playx/songs")
        return stream_cache_all(cache)
    # Check if its a playlist
    playlist = Playlist(song, args.pl_start, args.pl_end)
    if playlist.is_playlist():
        data = playlist.get_data()
        if args.shuffle:
            shuffle(data)
        player = Player(
                        data,
                        playlisttype=playlist.type,
                        show_lyrics=args.lyrics,
                        dont_cache_search=args.dont_cache_search,
                        no_cache=args.no_cache
                        )
        player.play()
    elif not song:
        parser.print_help()
    else:
        player = Player(
                        song,
                        show_lyrics=args.lyrics,
                        dont_cache_search=args.dont_cache_search,
                        no_cache=args.no_cache
                        )
        player.play()


def main():
    # Before doing anything, make sure all songs are in the new song dir
    # move_songs()
    parser, args = parse()
    song = ' '.join(args.song)
    # first check for auto playlist
    if args.auto:
        ap = CountBasedAutoPlaylist('~/.playx/logs/log.cat')
        song = ap.generate()
    # Put a check to see if the passed arg is a list
    playx_list = Playxlist(song, args.pl_start, args.pl_end)
    if not playx_list.is_playx_list():
        playx(parser, args, song)
    else:
        for s in playx_list.get_list_contents():
            playx(parser, args, s)


if __name__ == "__main__":
    main()
