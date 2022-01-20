class Track:
    name = ""
    duration = 0
    url = ""

    def __init__(self, name, duration, url):
        self.name = name
        self.duration = duration
        self.url = url

    def get_duration(self):
        return self.duration

    def get_name(self):
        return self.name

    def get_url(self):
        return self.url
