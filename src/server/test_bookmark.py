from server.bookmark import Bookmark


values = ["test", "Test_1", "", "Test", "", "test_1"]
sorted_values = ["", "", "test", "Test", "Test_1", "test_1"]


# pylint: disable=R0201 (no-self-use)
class TestFuzzySearch:
    def test_sort_by_section(self):
        bookmarks = []
        for v in values:
            bookmarks.append(
                Bookmark(1, "", "", "", v),
            )
        bookmarks.sort()
        for v, b in zip(sorted_values, bookmarks):
            assert v == b.section

    def test_sort_by_title(self):
        bookmarks = []
        for v in values:
            bookmarks.append(
                Bookmark(1, v, "", "", ""),
            )
        bookmarks.sort()
        for v, b in zip(sorted_values, bookmarks):
            assert v == b.title

    def test_sort_by_description(self):
        bookmarks = []
        for v in values:
            bookmarks.append(
                Bookmark(1, "", v, "", ""),
            )
        bookmarks.sort()
        for v, b in zip(sorted_values, bookmarks):
            assert v == b.description

    def test_sort_by_url(self):
        bookmarks = []
        for v in values:
            bookmarks.append(
                Bookmark(1, "", "", v, ""),
            )
        bookmarks.sort()
        for v, b in zip(sorted_values, bookmarks):
            assert v == b.url
