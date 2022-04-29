from html.parser import HTMLParser


# pylint: disable=W0223 (abstract-method)
class ChromeParser(HTMLParser):
    def __init__(self):
        super().__init__()

        self.bookmarks = []

        self.h3_tag = False
        self.first_h3_tag = True
        self.sections = []

        self.a_tag = False
        self.url = None

    def _get_section(self):
        section = ""
        first_section = True
        for s in self.sections:
            if first_section:
                first_section = False
                section += s
            else:
                section += " / " + s
        return section

    def handle_starttag(self, tag, attrs):
        # bookmark
        if tag == "a":
            self.a_tag = True
            for k, v in attrs:
                if k == "href":
                    self.url = v

        # new folder
        if tag == "h3":
            # ignore first H3 tag
            if self.first_h3_tag:
                self.first_h3_tag = False
            else:
                self.h3_tag = True

    def handle_endtag(self, tag):
        # end of folder
        if tag == "dl":
            # there are few unrelated DL tags at the beginning
            # which we ignore when building the section list
            # so we ignore them at the end too
            if self.sections:
                self.sections.pop()

    def handle_data(self, data):
        # bookmark
        if self.a_tag:
            self.a_tag = False
            self.bookmarks.append(
                {
                    "section": self._get_section(),
                    "title": data,
                    "url": self.url,
                }
            )

        # folder
        if self.h3_tag:
            self.h3_tag = False
            self.sections.append(data)

    def get_bookmarks(self, html):
        self.feed(html)
        return self.bookmarks
