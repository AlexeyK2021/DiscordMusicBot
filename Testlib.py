import youtube_dl

DL = youtube_dl.YoutubeDL()


def start():
    url = input("Link: ")
    info = DL.extract_info(url=url, download=False,)
    print(info)

if __name__ == "__main__":
    start()
