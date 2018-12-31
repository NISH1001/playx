"""File to handle all other playlists"""


from playlist.billboard import (
    get_chart_names,
    get_chart_names_online,
    dump_to_file
)

from playlist import (
    spotify,
    youtube,
    billboard
)

from playx.logger import get_logger

# Get the logger
logger = get_logger('Playlist')


"""
__author__ = Deepjyoti Barman
__github__ = github.com/deepjyoti30
"""


class Playlist():
    """Class for every kind of playlist supported."""

    def __init__(self, URL, pl_start, pl_end):
        """
        URL: Passed URL
        pl_start: Playlist start index.
        pl_end: Playlist end index.
        """
        self.URL = URL
        self.pl_start = pl_start
        self.pl_end = pl_end
        self.type = 'N/A'
        self.dict = {
                    'spotify': spotify,
                    'youtube': youtube,
                    'billboard': billboard
                    }

    def _is_spotify(self):
        """Check if URL is a spotify playlist."""
        playlist_part = 'open.spotify.com/playlist/'
        if playlist_part in self.URL:
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

    def is_playlist(self):
        """Check if the playlist is valid."""
        self._is_billboard()
        self._is_spotify()
        self._is_youtube()

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

        logger.info("{} playlist passed.".format(self.type))
        data, name = self.dict[self.type].get_data(
                                                self.URL,
                                                self.pl_start,
                                                self.pl_end
                                                )
        logger.info("{}: {} {}".format(
                                        name,
                                        len(data),
                                        'song' if len(data) < 2 else 'songs'
                                    ))
        return data