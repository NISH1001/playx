"""File to handle player related functions."""

from playx.utility import (
    direct_to_play
)

from playx.cache import (
    search_locally, update_URL_cache, search_URL
)

from playx.youtube import (
    grab_link, dw, get_youtube_title
)

from playx.songfinder import (
    search
)

from playx.logger import (
    Logger
)

from playx.stringutils import (
    is_song_url, url_type
)

from playx.soundcloud import (
    get_track_info
)

from playx.playlist.ytrelated import (
    get_data
)

from playx.playlist import (
    playlistcache
)

from os.path import basename


# Setup logger
logger = Logger('player')


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
            # Update the cache.
            update_URL_cache(self.title, self.URL)
        else:
            logger.info('Caching is disabled')

    def _get_soundcloud_data(self):
        """
        Extract the data for the soundcloud track.
        """
        self.title, self.stream_url = get_track_info(self.URL)

    def _get_youtube_data_url(self):
        """
        Search youtube and get its data.
        """
        self.title = get_youtube_title(self.URL)
        self.stream_url = grab_link(self.URL)

    def _extract_data(self):
        """
        Extract the song data according to type
        """
        if self.URL_type == 'youtube':
            self._get_youtube_data_url()
        elif self.URL_type == 'soundcloud':
            self._get_soundcloud_data()

    def _extract_songObj(self):
        """
        Extract the data from the songObj.
        """
        if self.URL_type == 'youtube':
            self.title = self.songObj.title
            self.URL = self.songObj.URL
            self._get_youtube_data_url()
        elif self.URL_type == 'soundcloud':
            self.title = self.songObj.title
            self.stream_url = self.songObj.URL

    def _stream_from_url(self):
        """Stream the song using the url.

        Before searching the stream, get the title of the song
        If local search is not forbidden, search it locally
        """
        if self.songObj is None:
            self._extract_data()
        else:
            self._extract_songObj()

        logger.debug(self.title)

        # Now search the song locally
        if not self.dont_cache_search:
            match = search_locally(self.title)
            if match:
                # Update the URL cache. This is necessary for the old songs.
                update_URL_cache(self.title, self.URL)
                # Change the value to local path
                self.stream_url = match[1]
            else:
                self._dw()
        else:
            logger.info("Searching locally disabled.")
            if self.stream_url == '':
                self._get_youtube_data_url()

        direct_to_play(self.stream_url, self.show_lyrics, self.title)

    def play_url(self, URL, songObj=None):
        """
        Play the song by using the URL.
        """
        self.URL = URL

        # Make a search locally to see if the song is already cached.
        if not self.dont_cache_search:
            song_path = search_URL(self.URL)
            if song_path is not None:
                self.stream_url = song_path
                self.title = basename(song_path)
                direct_to_play(song_path, self.show_lyrics, self.title)
                return self.URL

        self.URL_type = url_type(self.URL)
        if songObj is not None:
            self.songObj = songObj
        self._stream_from_url()
        return self.URL


class NamePlayer():
    """
    Player to particularly play songs by name.
    """

    def __init__(
                self,
                name=None,
                dont_cache_search=False,
                show_lyrics=False,
                no_cache=False,
                disable_kw=False
                ):
        self.name = name
        self.URL = ''
        self.dont_cache_search = dont_cache_search
        self.no_cache = no_cache
        self.show_lyrics = show_lyrics
        self.title = ''
        self.stream_url = ''
        self.disable_kw = disable_kw

    def _get_youtube_data_name(self):
        """
        Search youtube and get its data.
        """
        data = search(self.name, self.disable_kw)
        self.title = data.title
        self.URL = data.url
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
                self._get_youtube_data_name()
                local_path = search_URL(self.URL)

                # Try to check if the URL is mapped locally.
                if local_path is not None:
                    logger.debug("Replacing the stream URL with the local.")
                    self.stream_url = local_path
                else:
                    # Update the URL cache
                    update_URL_cache(self.title, self.URL)
                    self._dw()
        else:
            self._get_youtube_data_name()
        direct_to_play(self.stream_url, self.show_lyrics, self.title)

    def play_name(self, name):
        """
        Start playing the song.
        """
        self.name = name
        self._stream_from_name()
        return self.URL


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
                on_repeat,
                datatype=None,
                playlisttype=None,
                show_lyrics=False,
                dont_cache_search=False,
                no_cache=False,
                no_related=False,
                disable_kw=False,
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
                            no_cache=no_cache,
                            disable_kw=disable_kw
                            )
        self._iterable_list = []
        self.data = data
        self.datatype = datatype
        self.playlisttype = playlisttype
        self.no_related = no_related
        self.on_repeat = on_repeat
        self._playlist_names = [
                                'spotify',
                                'youtube',
                                'soundcloud',
                                'billboard',
                                'jiosaavn',
                                'gaana',
                                'cached'
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

    def _play_related(self, url):
        """
        Play related songs.
        """
        if self.no_related:
            return

        # Check if URL is not path
        logger.debug(url)
        if url != '':
            related_songs = get_data(url)
        else:
            return

        if len(related_songs) != 0:
            logger.info("Playing related songs")
            for i in related_songs:
                self.play_name(i.search_querry)

    def _check_type(self):
        """Check the type of the data"""

        if self.playlisttype is not None:
            logger.debug(self.playlisttype)
            logger.hold()
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

    def _get_repeat_times(self):
        """Return the number of times the song is supposed to repeat."""
        # The passed arg on_repeat is used to check that.

        # The arg passes 1 in case the --repeat flag is not passed
        # which means we simply need to loop for once.

        # The arg passes None in case the --repeat flag is passed but
        # without a value. In this case, we need to make sure the song goes
        # on an infinite loop. Though, in our case, we will make the loop run
        # for a really large value like 1000

        # The arg passes the number of times the loop is supposed the run in
        # case the value is passed by the user.

        if self.on_repeat == 1:
            return 1
        elif self.on_repeat is None:
            logger.info("Repeating indefinitely")
            return 5000
        else:
            logger.info("Repeating {} {}".format(
                    self.on_repeat,
                    'time' if self.on_repeat == 1 else 'times'
            ))
            return self.on_repeat

    def play(self):
        """Play the data."""
        self._check_type()

        # Stored the returned URL, useful for playing related songs.
        URL = None

        on_repeat_time = self._get_repeat_times()

        while on_repeat_time > 0:
            try:
                if self.datatype == 'URL':
                    URL = self.play_url(self.data)
                elif self.datatype == "song":
                    URL = self.play_name(self.data)
                elif self.datatype == 'playlist':
                    for i in self._iterable_list:
                        # For different playlists the player needs to act
                        # differently
                        if self.playlisttype == 'soundcloud':
                            self.play_url(i.URL, i)
                        elif self.playlisttype == 'youtube':
                            self.play_url(i.search_querry, i)
                        else:
                            self.play_name(i.search_querry)
                on_repeat_time -= 1
            except KeyboardInterrupt:
                on_repeat_time = -1
                logger.info("Exitting peacefully")

        if URL is not None:
            self._play_related(URL)
