from server.chrome_parser import ChromeParser


# pylint: disable=R0201 (no-self-use)
class TestFuzzySearch:
    def test_chrome_bookmarks(self):
        with open("src/tests/chrome_bookmarks_test.html", "r", encoding="ascii") as f:
            html_data = f.read()

        expected_bookmarks = [
            {"section": "", "title": "n1"},
            {"section": "s1", "title": "n1_1"},
            {"section": "s1", "title": "n1_2"},
            {"section": "s1 / s1_2", "title": "n1_2_1"},
            {"section": "", "title": "n2"},
            {"section": "s2", "title": "n2_1"},
        ]

        bookmarks = ChromeParser().get_bookmarks(html_data)

        for b, e in zip(bookmarks, expected_bookmarks):
            assert b["section"] == e["section"]
            assert b["title"] == e["title"]

    def test_chrome_bookmarks_invalid_html(self):
        with open("src/tests/chrome_bookmarks_invalid.html", "r", encoding="ascii") as f:
            html_data = f.read()

        bookmarks = ChromeParser().get_bookmarks(html_data)
        assert len(bookmarks) == 0
