"""Functions related to soundcloud playlists."""

import requests
import re

from playx.playlist.playlistbase import (
    PlaylistBase
)

from playx.logger import (
    Logger
)

# Setup logger
logger = Logger("Soundcloud")


class SoundCloudTrack:

    def __init__(self, title, download_url, stream_url):
        self.title = title
        self.download_url = download_url
        self.stream_url = stream_url


class SoundCloudPlaylistExtractor(PlaylistBase):
    """
    Class to scrap Soundcloud playlists.

    We need to get the set(playlist) id by scraping
    the page.
    Using that id we can use the api of soundcloud
    to get the tracks data.
    """

    def __init__(self, URL, pl_start, pl_end):
        super().__init__(pl_start, pl_end)
        self._clientID = 'LvWovRaJZlWCHql0bISuum8Bd2KX79mb'
        self.URL = URL
        self.set_ID = ''
        self.API_URL = 'http://api.soundcloud.com/playlists/{}?client_id={}'
        self.list_content_tuple = []
        self.set_name = ''

    def _get_ID(self):
        """Get the playlists id."""
        r = requests.get(self.URL)
        match = re.findall(
                r'href="android-app://com\.soundcloud\.android.*?"',
                r.text
                )
        self.set_ID = re.sub(
                r'playlists:|"',
                '',
                re.findall(r'playlists:.*?"', str(match))[0]
                )

    def get_tracks(self):
        """Get the tracks on the playlist by using the API."""
        self._get_ID()
        r = requests.get(self.API_URL.format(self.set_ID, self._clientID)).json()
        self.set_name = r['permalink']
        tracks = r['tracks']

        for i in tracks:
            title = i['title']
            download_url = i['download_url'] + '?client_id=' + self._clientID
            stream_url = i['stream_url'] + '?client_id=' + self._clientID
            self.list_content_tuple.append(SoundCloudTrack(title, download_url, stream_url))

        self.strip_to_start_end()


def get_data(URL, pl_start, pl_end):
    """Generic function. Should be called only when
    it is checked if the URL is a spotify playlist.

    Returns a tuple containing the songs and name of
    the playlist.
    """
    logger.info("Extracting Playlist Contents")
    sound_cloud_playlist = SoundCloudPlaylistExtractor(URL, pl_start, pl_end)
    sound_cloud_playlist.get_tracks()
    return sound_cloud_playlist.list_content_tuple, sound_cloud_playlist.set_name
