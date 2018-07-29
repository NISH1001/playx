<h1 align=center>
<img src="logo/1024 bg.svg" width=100%>
</h1>

## Search and play any song from terminal.

# playx in action

![GIF](https://i.imgur.com/42mEHQ5.gif)

# playx  

1. [Philosophy](#philosophy)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Features](#features)
5. [Usage](#usage)
6. [TO-DO](#to-do)
7. [Acknowledgements](#acknowledgements)

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

## Features

- play by query
- play by youtube url
- cache support
- CLI using `mpv`
------------

## Usage
For now, the application is in development phase.  

```sh
usage: main.py [-h] [-p] [-n] [-d] [-l] [song [song ...]]

positional arguments:
  song                  Name or youtube link of song to download

optional arguments:
  -h, --help            show this help message and exit
  -p, --play-cache      Play all songs from the cache.
  -n, --no-cache        Don't download the song for later use.
  -d, --dont-cache-search
                        Don't search the song in the cache.
  -l, --lyrics          Show lyircs of the song.

```

------------

## TO-DO
- ~~caching of downloaded songs (if the song exists locally, play it right away else play from youtube)~~
- ~~speed up the whole **search->download->convert->play** process~~
- ~~stream/play while downloading the song~~
- ~~play all the songs from the cache~~
- ~~search lyrics~~
- log activity
- use logs to create simple recommendations


## Acknowledgements
- Thanks to [Deepjyoti Barman](https://github.com/deepjyoti30) for parallelizing streaming + downloading (and other improvements)
- Thanks to [Mirza Zulfan](https://github.com/mirzazulfan) for logo for `playx`. It's neat (and cool)
