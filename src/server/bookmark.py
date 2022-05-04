from server.fuzzy_search import is_match


# pylint: disable=R0902 (too-many-instance-attributes)
class Bookmark:
    # pylint: disable=R0913 (too-many-arguments)
    def __init__(self, bookmark_id, title, description, url, section):
        self.id = bookmark_id
        self.title = title if title else ""
        self.description = description if description else ""
        self.url = url if url else ""
        self.section = section if section else ""

        self.title_lower = self.title.lower()
        self.description_lower = self.description.lower()
        self.url_lower = self.url.lower()
        self.section_lower = self.section.lower()

    def __lt__(self, other):
        if self.section_lower != other.section_lower:
            return self.section_lower < other.section_lower
        if self.title_lower != other.title_lower:
            return self.title_lower < other.title_lower
        if self.description_lower != other.description_lower:
            return self.description_lower < other.description_lower
        return self.url_lower < other.url_lower

    def match(self, pattern):
        """
        Assumptions:
            pattern is not None
            pattern is lower case
        """
        return is_match(pattern, self.title_lower) or \
            is_match(pattern, self.description_lower) or \
            is_match(pattern, self.url_lower)
