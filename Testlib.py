import re

import bs4
import requests
import youtube_dl
from bs4 import BeautifulSoup
import urllib.request

DL = youtube_dl.YoutubeDL()


def start():
    url = input("Link: ")
    html = urllib.request.urlopen(url)
    video_IDS = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    print(video_IDS[0], sep="\n")
    link = "https://www.youtube.com/watch?v=" + video_IDS[0]
    print(link)

if __name__ == "__main__":
    start()
