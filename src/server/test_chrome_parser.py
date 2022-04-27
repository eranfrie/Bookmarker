from server.chrome_parser import ChromeParser


# pylint: disable=R0201 (no-self-use)
class TestFuzzySearch:
    def test_invalid_html(self):
        with open("src/tests/chrome_bookmarks_invalid.html", "r", encoding="ascii") as f:
            html_data = f.read()

        bookmarks = ChromeParser().get_bookmarks(html_data)
        assert len(bookmarks) == 0
