from html.parser import HTMLParser


# pylint: disable=W0223
class ChromeParser(HTMLParser):
    def __init__(self):
        super().__init__()

        self.bookmarks = []

        self.a_tag = False
        self.url = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.a_tag = True
            for k, v in attrs:
                if k == "href":
                    self.url = v

    def handle_data(self, data):
        if self.a_tag:
            self.bookmarks.append(
                {
                    "title": data,
                    "url": self.url,
                }
            )
            self.a_tag = False

    def get_bookmarks(self, html):
        self.feed(html)
        return self.bookmarks
