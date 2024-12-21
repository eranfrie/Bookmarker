from utils.html_utils import html_escape
from server.fuzzy_search import is_match


def _regular_search(pattern, line):
    """
    Assumptions:
        pattern is not None
        pattern is lower case
        line is lower case

    Returns:
        indexes (set) of matched indexes
            if pattern is contained in line
        None otherwise
    """
    try:
        first_indes = line.index(pattern)
    except ValueError:
        return None
    return set(range(first_indes, first_indes + len(pattern)))


# pylint: disable=R0902 (too-many-instance-attributes)
class Bookmark:
    # pylint: disable=R0913 (too-many-arguments)
    def __init__(self, bookmark_id, title, description, url, section):
        self.id = bookmark_id
        self.title = title if title else ""
        self.description = description if description else ""
        self.url = url if url else ""
        self.section = section.lower() if section else ""  # section always lower case

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

    def __lt__(self, other):
        if self.section_lower != other.section_lower:
            return self.section_lower < other.section_lower
        if self.title_lower != other.title_lower:
            return self.title_lower < other.title_lower
        if self.description_lower != other.description_lower:
            return self.description_lower < other.description_lower
        return self.url_lower < other.url_lower

    def match(self, pattern, is_fuzzy, include_url):
        """
        Assumptions:
            pattern is not None
            pattern is lower case
        """
        search_method = is_match if is_fuzzy else _regular_search
        return search_method(pattern, self.title_lower) is not None \
            or search_method(pattern, self.description_lower) is not None \
            or (search_method(pattern, self.url_lower) is not None and include_url)
