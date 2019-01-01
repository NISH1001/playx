#!/usr/bin/env python3
"""A utility module for misc operations."""

import os
import subprocess
from shutil import move
from playx.lyrics import search_lyricswikia
from playx.logger import get_logger
import threading

# Setup logger
logger = get_logger('utility')


class MPVThread(threading.Thread):

    def __init__(self, URL, title=None):
        threading.Thread.__init__(self)
        self.songURL = URL
        self.title = title

    def run(self):
        logger.info("Playing [{}]".format(self.title))
        cli = 'mpv "{}" --really-quiet'.format(self.songURL)
        os.system(cli)


def exe(command):
    """Execute the command externally."""
    command = command.strip()
    c = command.split()
    output, error = subprocess.Popen(c,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE).communicate()
    output = output.decode('utf-8').strip()
    error = error.decode('utf-8').strip()
    return (output, error)


def direct_to_play(url, show_lyrics, title):
    """Direct the song to be played according to the play_type."""
    if show_lyrics:
        lyric = search_lyricswikia(title)
        print("----\n{}\n----".format(lyric))

    run_mpv(url, title)

def run_mpv(stream_url, title=None):
    # print("Playing using mpv...")
    logger.info("Playing [{}]".format(title))
    cli = 'mpv "{}" --really-quiet'.format(stream_url)
    os.system(cli)
    """
    mpv_thread = MPVThread(stream_url, title)
    mpv_thread.start()
    mpv_thread.join()
    """


def run_mpv_dir(directory):
    logger.info("Playing using mpv from directory :: {}".format(directory))
    cli = 'mpv "{}"'.format(directory)
    os.system(cli)

if __name__ == '__main__':
    url = "https://r7---sn-bvvbax-3uhl.googlevideo.com/videoplayback?ip=110.44.120.206&ei=qsFSW7DmE6jMoQP3ppSICg&sparams=clen%2Cdur%2Cei%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cnh%2Cpl%2Crequiressl%2Csource%2Cexpire&id=o-ANRsypPRJvgkydFW-5_ZV_zCT8JsLhV5Unh1mGiXB0WR&keepalive=yes&clen=3253260&requiressl=yes&gir=yes&nh=EAQ%2C&initcwndbps=427500&pl=23&dur=208.881&source=youtube&lmt=1468126594841376&ipbits=0&itag=251&fvip=1&mime=audio%2Fwebm&key=yt6&expire=1532171786&mm=31%2C26&mn=sn-bvvbax-3uhl%2Csn-i3beln7s&c=WEB&ms=au%2Conr&mt=1532150082&mv=m&signature=8D3E161749FBB351BACDC6AB97DF578C330E5A7F.85CA648C3E09F32DE7F882023747D84D8D288C1A&ratebypass=yes"
    run_mpv(url)


def move_songs():
    """Recent changes moved the song directory to ~/.playx/songs
    from ~/.playx.
    Function to make sure the migration is done properly.
    Disable after a few days."""

    OLD_DIR = os.path.expanduser("~/.playx")
    NEW_DIR = os.path.expanduser("~/.playx/songs")

    if not os.path.isdir(NEW_DIR):
        os.makedirs(NEW_DIR)

    for file in os.listdir(OLD_DIR):
        if file.endswith('mp3'):
            move(os.path.join(OLD_DIR, file),
                os.path.join(NEW_DIR, file))
