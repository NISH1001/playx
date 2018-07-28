<h1 align=center>
<img src="logo/1024 bg.svg" width=100%>
</h1>

# playx  

Search and play any song from terminal.

---------

# Philosophy
Play any songs that come in your mind.
> Hoping to make it an awesome music assistant
---------

## Requirements

1. Python3.x

2. pip3

3. MPV

## Installation

 * Run following to install python modules

```sh
pip install -r requirements.txt
```

 * Get <a href = https://mpv.io/>MPV (website)</a> from here.

 * Get <a href = https://github.com/mpv-player/mpv>MPV (github)</a> from here.

> **Note**: These dependencies in linux can be installed in other variants.  
> For *arch linux*, you can use **pacman** package manager accordingly.

------------

## Feaures

- play by query
- play by youtube url
- cache support
- CLI using `mpv`
------------

## Usage
For now, the application is in development phase.  

```sh
usage: main.py [-h] [--name NAME [NAME ...]] [--url URL]

optional arguments:
  -h, --help            show this help message and exit
  --name NAME [NAME ...], -n NAME [NAME ...]
                        Name of the song to download. Words separated by space
  --url URL, -u URL     Youtube song link.
  --play-cache          Play all songs from the cache.
  --lyrics, -l          Show lyircs of the song.
```

------------

## TO-DO
- ~~caching of downloaded songs (if the song exists locally, play it right away else play from youtube)~~
- ~~speed up the whole **search->download->convert->play** process~~
- ~~stream/play while downloading the song~~
- ~~play all the songs from the cache~~
- ~~search lyrics~~
