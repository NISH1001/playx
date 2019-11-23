"""File to handle all other playlists"""


from playx.playlist.billboard import (
    get_chart_names,
    get_chart_names_online,
    dump_to_file
)

from playx.playlist import (
    spotify,
    youtube,
    billboard,
    soundcloud,
    jiosaavn,
    gaana,
    playlistcache,
    ytmusic
)

import re
from random import shuffle
from playx.logger import Logger

# Get the logger
logger = Logger('Playlist')


"""
__author__ = Deepjyoti Barman
__github__ = github.com/deepjyoti30
"""


class Playlist:
    """Class for every kind of playlist supported."""

    def __init__(self, URL, pl_start, pl_end, is_shuffle):
        """
        URL: Passed URL
        pl_start: Playlist start index.
        pl_end: Playlist end index.
        """
        self.URL = URL
        self.file_path = None  # Used for cached playlists
        self.temp_type = None  # Used for cached playlists
        self.pl_start = pl_start
        self.pl_end = pl_end
        self.is_shuffle = is_shuffle
        self.type = 'N/A'
        self.dict = {
                    'spotify': spotify,
                    'youtube': youtube,
                    'billboard': billboard,
                    'soundcloud': soundcloud,
                    'jiosaavn': jiosaavn,
                    'gaana': gaana,
                    'cached': playlistcache,
                    'youtubeMusic': ytmusic
                    }

    def _is_spotify(self):
        """Check if URL is a spotify playlist."""
        # playlist_part = 'open.spotify.com/playlist/'
        match = re.match(r'^(https://)?open.spotify.com/(user/.*/)?playlist/.*?$', self.URL)
        if match:
            self.type = 'spotify'

    def _is_youtube(self):
        """Check if URL is a youtube playlist."""
        playlist_part = 'https://www.youtube.com/playlist?list'
        if playlist_part in self.URL:
            self.type = 'youtube'

    def _is_billboard(self):
        """Check if URL is a billboard chart."""
        # First check online. If internet error then try to search offline.
        # If its found online then
        # We will check if we have an offline copy of the billboard charts

        CHART_NAMES = get_chart_names_online()

        # Check if CHART_NAMES are present or not.
        if len(CHART_NAMES):
            # Before returning dump the charts to a file
            dump_to_file(CHART_NAMES)
            if self.URL.lower() in CHART_NAMES:
                self.type = 'billboard'
        else:
            try:
                chart_names = get_chart_names('~/.playx/logs/billboard')
            except FileNotFoundError:
                logger.error("No internet connection!\nNo local billboard chart list found! Cannot check if passed name is a chart.\a")
                return False
            if not chart_names:
                return False
            else:
                if self.URL.lower in chart_names:
                    self.type = 'billboard'

    def _is_soundcloud(self):
        """Check if URL is a soundcloud set."""
        match = re.findall(r'https://soundcloud\.com.*?/sets/.*?$', self.URL)
        if len(match):
            self.type = 'soundcloud'

    def _is_jiosaavn(self):
        """
        Check if the passed URL is a jiosaavn playlist.
        """
        match = re.findall(r'^(https://)?(www.)?(jio)?saavn.com/(s/playlist|featured)/.*?', self.URL)
        if len(match):
            self.type = 'jiosaavn'

    def _is_gaana(self):
        """
        Check if passed URL is a gaana playlist.
        """
        match = re.findall(r'^(https://)?gaana.com/playlist.*?$', self.URL)
        if len(match):
            self.type = 'gaana'

    def _is_cached(self):
        """
        Check if the playlist is cached.
        """
        playlist_cache = playlistcache.PlaylistCache(self.URL)
        if playlist_cache.is_cached():
            self.type = 'cached'
            self.temp_type = playlist_cache.extract_playlist_type()
            self.URL = playlist_cache.file_path

    def _is_ytmusic(self):
        """
        Check if the passed URL is youtube music URL.
        """
        playlist_part = "https://music.youtube.com/playlist?list"
        if playlist_part in str(self.URL):
            self.type = "youtubeMusic"

    def _get_data(self):
        """
        Internal function to call get_data of type and get the
        data and name of the playlist.
        """
        data, name = self.dict[self.type].get_data(
                                                self.URL,
                                                self.pl_start,
                                                self.pl_end
                                                )
        return data, name

    def sync_playlist(self, value):
        """
        Sync the playlists saved in the playlists dir.
        """
        playlists = playlistcache.list_all()

        if value.lower() == 'all':
            for playlist in playlists:
                self.type = playlist[2]
                self.URL = playlist[1]
                logger.info("Syncing {} with {}".format(playlist[0], self.type))
                data, name = self._get_data()
                playlistcache.save_data(name, self.URL, self.type, data)
        else:
            for playlist in playlists:
                logger.debug('{}:{}'.format(playlist[0], value))
                req_pl = playlist if playlist[0] == value else None
                if req_pl is not None:
                    logger.debug(req_pl[1])
                    self.type = req_pl[2]
                    self.URL = req_pl[1]
                    logger.info("Syncing {} with {}".format(req_pl[0], self.type))
                    data, name = self._get_data()
                    playlistcache.save_data(name, self.URL, self.type, data)
                    return

            logger.error('{}: Not found in cached playlists'.format(value))

    def _shuffle(self, data):
        """Shuffle the data in case is_shuffle is True."""
        if not self.is_shuffle:
            return data
        else:
            logger.info("Shuffling the playlist...")
            shuffle(data)
            return data

    def is_playlist(self):
        """Check if the playlist is valid."""

        self._is_billboard()
        self._is_spotify()
        self._is_youtube()
        self._is_soundcloud()
        self._is_jiosaavn()
        self._is_gaana()
        self._is_cached()
        self._is_ytmusic()

        if self.type != 'N/A':
            return True
        else:
            return False

    def get_data(self):
        """
        Extract the data according to the playlist
        and return the data.
        """
        if self.type == 'N/A':
            return []

        logger.info("{} Playlist passed.".format(self.type[0].upper() + self.type[1:]))
        data, name = self._get_data()
        logger.info("{}: {} {}".format(
                                        name,
                                        len(data),
                                        'song' if len(data) < 2 else 'songs'
                                    ))
        logger.debug(data[0].content())
        # Cache the playlist if its not already there
        if self.type != 'cached':
            playlistcache.save_data(name, self.URL, self.type, data)
        else:
            self.type = self.temp_type

        # Shuffle the data in case is_shuffle is True
        data = self._shuffle(data)

        return data
