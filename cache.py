"""Definitions related to caching the song."""

import youtube_dl
import os
import threading


class Cache:
    """Class to cache the song to a directory for quick acces."""

    def __init__(self, link, dir='~/.playx'):
        """Init the stuff."""
        self.link = link
        dir = os.path.expanduser(dir)
        self.dir = dir
        self.create_cache_dir()

    def create_cache_dir(self):
        """If cache dir is not already present make it."""
        if not os.path.isdir(self.dir):
            # Make the dir
            os.mkdirs(self.dir)

    def dw(link):
        """Download the song."""
        dw = Cache(link)
        print("Downloading from {}".format(link))
        dw_thread = threading.Thread(target=dw.GRAB_SONG)
        dw_thread.start()

    def GRAB_SONG(self):
        """Return true if the song is downloaded else false."""
        ydl_opts = {
            'format': 'bestaudio',
            'quiet': True,
            'outtmpl': os.path.join(self.dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec':  'mp3',
                'preferredquality': '320'
            }]
        }

        # Download the song with youtube-dl
        try:
            ydl = youtube_dl.YoutubeDL(ydl_opts)
            ydl.download([self.link])
            return True
        except TimeoutError:
            print('Timed Out! Are you connected to internet?\a')
            return False
        else:
            return False
