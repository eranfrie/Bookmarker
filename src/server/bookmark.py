from utils.html_utils import html_escape, split_escaped_text
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

        # don't be sensitive around / separators
        sub_sections = self.section.split("/")
        sub_sections = [s.strip() for s in sub_sections]
        self.section = " / ".join(sub_sections)

        self.title_lower = self.title.lower()
        self.description_lower = self.description.lower()
        self.url_lower = self.url.lower()
        self.section_lower = self.section.lower()

        self.escaped_title = html_escape(self.title)
        self.escaped_description = html_escape(self.description)
        self.escaped_url = html_escape(self.url)
        self.escaped_section = html_escape(self.section)

        self.escaped_chars_title = split_escaped_text(self.escaped_title)
        assert len(self.escaped_chars_title) == len(self.title)
        self.escaped_chars_description = split_escaped_text(self.escaped_description)
        assert len(self.escaped_chars_description) == len(self.description)
        self.escaped_chars_url = split_escaped_text(self.escaped_url)
        assert len(self.escaped_chars_url) == len(self.url)

        self.title_indexes = None
        self.description_indexes = None
        self.url_indexes = None

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
        self.title_indexes = is_match(pattern, self.title_lower)
        self.description_indexes = is_match(pattern, self.description_lower)
        self.url_indexes = is_match(pattern, self.url_lower)
        return self.title_indexes is not None or \
            self.description_indexes is not None or \
            self.url_indexes is not None
