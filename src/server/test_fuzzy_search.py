from server.fuzzy_search import is_match


# pylint: disable=R0201
class TestFuzzySearch:
    def test_match(self):
        assert is_match("", "")
        assert is_match("", "a")

        assert is_match("abc", "ABC")
        assert is_match("ABC", "abc")
        assert is_match("abc", "aabbccdd")
        assert is_match("abC", "AAbbccdd")
        assert is_match("aaabbb", "Aaa-bbB")
        assert is_match("A", "a")
        assert is_match("A", " -. a")

        assert is_match("123", "44142434")
        assert is_match("123", "1243")

    def test_not_match(self):
        assert not is_match("b", "")

        assert not is_match("b", "a")
        assert not is_match("d", "abc")
        assert not is_match("123", "143")
        assert not is_match("123", "124")
