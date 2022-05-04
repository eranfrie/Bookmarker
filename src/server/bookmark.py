class Bookmark:
    # pylint: disable=R0913 (too-many-arguments)
    def __init__(self, bookmark_id, title, description, url, section):
        self.id = bookmark_id
        self.title = title
        self.description = description
        self.url = url
        self.section = section

    def __lt__(self, other):
        if self.section.lower() != other.section.lower():
            return self.section.lower() < other.section.lower()
        if self.title.lower() != other.title.lower():
            return self.title.lower() < other.title.lower()
        if self.description.lower() != other.description.lower():
            return self.description.lower() < other.description.lower()
        return self.url.lower() < other.url.lower()

    def match(self, pattern):
        """
        Assumptions:
            pattern is not None
            pattern already lowered
        """
        return pattern in self.title.lower() or \
            pattern in self.description.lower() or \
            pattern in self.url.lower()
