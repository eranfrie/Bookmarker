from server.chrome_parser import ChromeParser


# pylint: disable=R0201 (no-self-use)
class TestFuzzySearch:
    def _read_file(self, filename):
        with open(filename, "r", encoding="ascii") as f:
            return f.read()

    def test_chrome_bookmarks(self):
        expected_bookmarks = [
            {"section": "", "title": "n1"},
            {"section": "s1", "title": "n1_1"},
            {"section": "s1", "title": "n1_2"},
            {"section": "s1 / s1_2", "title": "n1_2_1"},
            {"section": "", "title": "n2"},
            {"section": "s2", "title": "n2_1"},
        ]

        html_data = self._read_file("src/tests/chrome_bookmarks_test.html")
        bookmarks = ChromeParser().get_bookmarks(html_data)

        for b, e in zip(bookmarks, expected_bookmarks):
            assert b["section"] == e["section"]
            assert b["title"] == e["title"]

    def test_chrome_bookmarks_invalid_html(self):
        html_data = self._read_file("src/tests/chrome_bookmarks_invalid.html",)
        bookmarks = ChromeParser().get_bookmarks(html_data)
        assert len(bookmarks) == 0
