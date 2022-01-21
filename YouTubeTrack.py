import youtube_dl


class YouTubeTrack:
    music_url = ""
    _url = ""
    name = ""
    _duration = 0
    channel = ""
    _params = {'format': 'bestaudio'}
    info = []
    image_link = ""

    def __init__(self, url):
        self._url = url
        self.info = youtube_dl.YoutubeDL(self._params).extract_info(self._url, download=False)
        self.name = self.info['track']
        self.channel = self.info['channel']
        self._duration = self.info['duration']
        self.image_link = self.info['thumbnails'][0]['url']
        self.music_url = self.info['formats'][0]['url']

    def get_duration(self):
        hours = self._duration // 3600
        hours_str = "0" + str(hours) if hours < 10 else str(hours)
        mins = self._duration // 60
        mins_str = "0" + str(mins) if mins < 10 else str(mins)
        secs = self._duration % 60
        secs_str = "0" + str(secs) if secs < 10 else str(secs)
        return hours_str + ":" + mins_str + ":" + secs_str
