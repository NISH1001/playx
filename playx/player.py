"""File to handle player related functions."""

from playx.utility import (
    direct_to_play
)

from playx.cache import (
    search_locally
)

from playx.youtube import (
    grab_link, dw
)

from playx.songfinder import (
    search
)

from playx.logger import (
    get_logger
)

from playx.stringutils import (
    is_song_url, url_type
)

from playx.soundcloud import (
    get_track_info
)


# Setup logger
logger = get_logger('player')


class URLPlayer():
    """
    Currently support for soundcloud and youtube URL's are added.
    """

    def __init__(
                self,
                URL=None,
                songObj=None,
                dont_cache_search=False,
                show_lyrics=False,
                no_cache=False
                ):
        self.URL = URL
        self.stream_url = ''
        self.title = ''
        self.URL_type = url_type(self.URL) if self.URL is not None else None
        self.songObj = songObj
        self.dont_cache_search = dont_cache_search
        self.show_lyrics = show_lyrics
        self.no_cache = no_cache

    def _dw(self):
        """
        Add the song to download.
        """
        if not self.no_cache:
            dw(self.title, self.stream_url)

    def _update_URL(self, URL):
        """
        Update the URL. Useful if the URL is to be updated later
        during the class call.
        """
        self.URL = URL
        self.URL_type = url_type(self.URL)

    def _update_songObj(self, songObj):
        self.songObj = songObj

    def _get_soundcloud_data(self):
        """
        Extract the data for the soundcloud track.
        """
        self.title, self.stream_url = get_track_info(self.URL)

    def _get_youtube_data(self):
        """
        Search youtube and get its data.
        """
        data = search(self.URL)
        self.title = data.title
        self.stream_url = grab_link(self.URL)

    def _extract_data(self):
        """
        Extract the song data according to type
        """
        if self.URL_type == 'youtube':
            self._get_youtube_data()
        elif self.URL_type == 'soundcloud':
            self._get_soundcloud_data()

    def _extract_songObj(self):
        """
        Extract the data from the songObj.
        """
        if self.URL_type == 'youtube':
            self.title = self.songObj.title
            self.stream_url = self.songObj.URL
        elif self.URL_type == 'soundcloud':
            self.title = self.songObj.title
            self.stream_url = self.songObj.stream_url

    def _stream_from_url(self):
        """Stream the song using the url.

        Before searching the stream, get the title of the song
        If local search is not forbidden, search it locally
        """
        if self.songObj is None:
            self._extract_data()
        else:
            self._extract_songObj()

        # Now search the song locally
        if not self.dont_cache_search:
            match = search_locally(self.title)
            if match:
                # Change the value to local path
                self.stream_url = match[1]
            else:
                self._dw()

        direct_to_play(self.stream_url, self.show_lyrics, self.title)

    def play(self, URL, songObj=None):
        """
        Play the song by using the URL.
        """
        self._update_URL(URL)
        if songObj is not None:
            self._update_songObj(songObj)
        self._stream_from_url()


class NamePlayer():
    """
    Player to particularly play songs by name.
    """

    def __init__(
                self,
                name=None,
                dont_cache_search=False,
                show_lyrics=False,
                no_cache=False
                ):
        self.name = name
        self.dont_cache_search = dont_cache_search
        self.no_cache = no_cache
        self.show_lyrics = show_lyrics
        self.title = ''
        self.stream_url = ''

    def _update_name(self, name):
        """
        Update the name of the song.
        """
        self.name = name

    def _get_youtube_data(self):
        """
        Search youtube and get its data.
        """
        data = search(self.name)
        self.title = data.title
        self.stream_url = grab_link(data.url)

    def _stream_from_name(self):
        """Start streaming the song.

        First search in the local cache.
        If no song is found in the cache, search in the youtube.
        """
        # Need to check if searching locally is forbidden
        if not self.dont_cache_search:
            match = search_locally(self.name)
            if match:
                self.title = match[0]
                self.stream_url = match[1]
            else:
                self._get_youtube_data()
        else:
            self._get_youtube_data()
        direct_to_play(self.stream_url, self.show_lyrics, self.title)

    def play(self, name):
        """
        Start playing the song.
        """
        self._update_name(name)
        self._stream_from_name()


class Player(URLPlayer, NamePlayer):
    """
    Base class to play songs.

    Player will take different types of data,
    recognize them and play accordingly.

    Supported data types would be:
    Playlist
    URL
    Songname
    """

    def __init__(
                self,
                data,
                datatype=None,
                playlisttype=None,
                show_lyrics=False,
                dont_cache_search=False,
                no_cache=False
                ):
        """
        data can be anything of the above supported
        types.
        If playlist then it is iterated over,
        if it is some other type then its simply
        sent to be played according to the player.

        datatype supports the following types:
        - playlist
        - song
        - URL
        """
        URLPlayer.__init__(
                            self,
                            show_lyrics=show_lyrics,
                            dont_cache_search=dont_cache_search,
                            no_cache=no_cache
                            )
        NamePlayer.__init__(
                            self,
                            show_lyrics=show_lyrics,
                            dont_cache_search=dont_cache_search,
                            no_cache=no_cache
                            )
        self._iterable_list = []
        self.data = data
        self.datatype = datatype
        self.playlisttype = playlisttype
        self._playlist_names = [
                                'spotify',
                                'youtube',
                                'soundcloud',
                                'billboard',
                              ]
        self._datatypes = [
                            'playlist',
                            'song',
                            'URL'
                          ]
        self.show_lyrics = show_lyrics
        self.dont_cache_search = dont_cache_search
        self.no_cache = no_cache

    def _determine_datatype(self):
        """Determine the datatype of the passed data."""
        if is_song_url(self.data):
            self.datatype = "URL"
        else:
            self.datatype = "song"

    def _check_type(self):
        """Check the type of the data"""

        if self.playlisttype is not None:
            if self.playlisttype not in self._playlist_names:
                logger.critical('Passed playlist is not supported yet')
            else:
                self.datatype = "playlist"
                self._iterable_list = self.data
        elif self.datatype is not None:
            if self.datatype not in self._datatypes:
                logger.warning('Datatype of playlist not within supported ones.')
        else:
            self._determine_datatype()

    def play(self):
        """Play the data."""
        self._check_type()

        if self.datatype == 'URL':
            URLPlayer().play(self.data)
        elif self.datatype == "song":
            NamePlayer().play(self.data)
        elif self.datatype == 'playlist':
            logger.debug(len(self._iterable_list))
            for i in self._iterable_list:
                # For different playlists the player needs to act
                # differently
                if self.playlisttype == 'soundcloud':
                    URLPlayer().play(i.stream_url, i)
                elif self.playlisttype == 'spotify':
                    NamePlayer().play(i.title + ' ' + i.artist)
                elif self.playlisttype == 'billboard':
                    NamePlayer().play(i.title)
                elif self.playlisttype == 'youtube':
                    URLPlayer().play(i.URL, i)
