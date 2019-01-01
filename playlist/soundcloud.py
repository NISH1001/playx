"""Functions related to soundcloud playlists."""

import requests
import re


class SoundCloudTrack():

    def __init__(self):
        self.title = ''
        self.download_url = ''
        self.stream_url = ''


class SoundCloudPlaylistExtractor():
    """
    Class to scrap Soundcloud playlists.

    We need to get the set(playlist) id by scraping
    the page.
    Using that id we can use the api of soundcloud
    to get the tracks data.
    """

    def __init__(self, URL, pl_start, pl_end):
        self._clientID = 'LvWovRaJZlWCHql0bISuum8Bd2KX79mb'
        self.URL = URL
        self.set_ID = ''
        self.API_URL = 'http://api.soundcloud.com/playlists/{}?client_id={}'
        self.song_tuple = []
        self.set_name = ''
        self.pl_end = pl_end
        self.pl_start = pl_start
        self.default_end = 0
        self.default_start = 1
        self.is_valid_start = False
        self.is_valid_end = False

    def _is_valid(self):
        """Check if pl_start and pl_end are valid."""
        self.is_valid_start = True if self.pl_start in range(
                                            self.default_start,
                                            self.default_end + 1) else False
        self.is_valid_end = True if self.pl_end in range(
                                            self.default_start,
                                            self.default_end + 1) else False

    def _strip_to_start_end(self):
        """Strip the tuple to positions passed by the user."""
        # Before doing anything check if the passed numbers are valid
        self._is_valid()
        if self.pl_start is not None and self.is_valid_start:
            self.default_start = self.pl_start
        if self.pl_end is not None and self.is_valid_end:
            self.default_end = self.pl_end
        self.song_tuple = self.song_tuple[self.default_start - 1: self.default_end]

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
            sound_cloud_track = SoundCloudTrack()
            sound_cloud_track.title = i['title']
            sound_cloud_track.download_url = i['download_url'] + '?client_id=' + self._clientID
            sound_cloud_track.stream_url = i['stream_url'] + '?client_id=' + self._clientID
            self.song_tuple.append(sound_cloud_track)

        self.default_end = len(self.song_tuple)
        self._strip_to_start_end()


def get_data(URL, pl_start, pl_end):
    """Generic function. Should be called only when
    it is checked if the URL is a spotify playlist.

    Returns a tuple containing the songs and name of
    the playlist.
    """
    sound_cloud_playlist = SoundCloudPlaylistExtractor(URL, pl_start, pl_end)
    sound_cloud_playlist.get_tracks()
    return sound_cloud_playlist.song_tuple, sound_cloud_playlist.set_name
