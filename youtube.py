#!/usr/bin/env python3

from utility import exe

class YoutubeMetadata:
    def __init__self(self):
        self.title = ""
        self.url = ""
        self.description = ""
        self.duration = ""

    def display(self):
        print("title : ", self.title)
        print("url : ", self.url)
        print("description : ", self.description)
        print("duration : ", self.duration)

def get_youtube_streams(url):
    print("Getting stream urls...")
    cli = "youtube-dl -g {}".format(url)
    output, error = exe(cli)
    stream_urls = output.split("\n")
    url = {}
    url['audio'] = stream_urls[1]
    url['video'] = stream_urls[0]
    print("Fetched stream urls...")
    return url

def main():
    url = "https://www.youtube.com/watch?v=-qfCrYwdqCA"
    urls = get_youtube_streams(url)
    print(urls)

if __name__ == "__main__":
    main()

