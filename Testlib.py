import youtube_dl
from bs4 import BeautifulSoup

DL = youtube_dl.YoutubeDL()


def start():
    url = input("Link: ")
    # info = DL.extract_info(url=url, download=False,)

    print(info)

if __name__ == "__main__":
    start()
