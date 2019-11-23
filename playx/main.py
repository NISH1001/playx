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

from playx.playlist.autoplaylist import (
    CountBasedAutoPlaylist,
    MarkovBasedAutoPlaylist
)


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
                        The cache is located at [~/.playx/songs/] by default")
    parser.add_argument('-n', '--no-cache',
                        action='store_true',
                        help="Don't download the song for later use.")
    parser.add_argument('-a', '--auto',
                        action='store_true',
                        help="Auto generate playlist")
    parser.add_argument('-d', '--skip-cached',
                        action='store_true',
                        help="Don't search the song in the cache.")
    parser.add_argument('-r', '--no-related',
                        action='store_true',
                        help="Disable playing related songs extracted\
                            from YouTube")
    parser.add_argument('-k', '--disable-kw',
                        action='store_true',
                        help="Disable addition of keywords while\
                            searching the song on YouTube.")
    parser.add_argument('--sync-pl',
                        default=None, type=str,
                        help="Sync the playlists. Pass the name as\
                        arguement. If all the playlists are to be \
                        synced, just pass [All].", metavar="PLAYLIST")
    parser.add_argument('-l', '--lyrics',
                        action='store_true',
                        help="Show lyircs of the song.")
    parser.add_argument('--shuffle', help="Shuffle the playlist in case\
                        it is one, else the option will have no effect.",
                        action="store_true")
    parser.add_argument('--repeat', help="Put the passed entity on repeat\
                        , be it a playlist or a song. If an arg is not\
                        passed, infinite loop is considered. (default = \
                        Infinite)",
                        type=int, nargs='?', choices=range(1, 5000),
                        metavar="NUMBER", default=1)
    parser.add_argument('--pl-start', help="Start position in case a\
                         playlist is passed. If passed without a playlist\
                         it has no effect.", default=None, type=int,
                         metavar="START")
    parser.add_argument('--pl-end', help="End position in case a \
                        playlist is passed. If passed without a playlist\
                        it has no effect." + "\n", default=None, type=int,
                        metavar="END")
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


def stream_cache_all(cache):
    run_mpv_dir(cache.dir)


def playx(parser, args, song):
    """Search the song in youtube and stream through mpd."""
    if not song and args.play_cache:
        cache = Cache("~/.playx/songs")
        return stream_cache_all(cache)
    # Check if its a playlist
    logger.debug(args.no_related)
    playlist = Playlist(song, args.pl_start, args.pl_end, args.shuffle)
    if playlist.is_playlist():
        data = playlist.get_data()
        player = Player(
                        data,
                        playlisttype=playlist.type,
                        show_lyrics=args.lyrics,
                        dont_cache_search=args.skip_cached,
                        no_cache=args.no_cache,
                        no_related=args.no_related,
                        on_repeat=args.repeat
                        )
        player.play()
    elif not song:
        parser.print_help()
    else:
        player = Player(
                        song,
                        show_lyrics=args.lyrics,
                        dont_cache_search=args.skip_cached,
                        no_cache=args.no_cache,
                        no_related=args.no_related,
                        on_repeat=args.repeat,
                        disable_kw=args.disable_kw
                        )
        player.play()


def main():
    # Before doing anything, make sure all songs are in the new song dir
    # move_songs()
    parser, args = parse()
    song = ' '.join(args.song)
    # first check for auto playlist
    if args.auto:
        # ap = CountBasedAutoPlaylist('~/.playx/logs/log.cat')
        ap = MarkovBasedAutoPlaylist('~/.playx/logs/log.cat')
        song = ap.generate()

    # Check if sync-playlists is passed
    if args.sync_pl is not None:
        pl = Playlist(None, None, None)
        pl.sync_playlist(args.sync_pl)
        exit(0)

    # Put a check to see if the passed arg is a list
    playx_list = Playxlist(song, args.pl_start, args.pl_end)
    if not playx_list.is_playx_list():
        playx(parser, args, song)
    else:
        for s in playx_list.get_list_contents():
            playx(parser, args, s)


if __name__ == "__main__":
    main()
