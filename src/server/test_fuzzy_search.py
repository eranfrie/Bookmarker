from server.fuzzy_search import is_match


# pylint: disable=R0201 (no-self-use)
class TestFuzzySearch:
    def test_match(self):
        assert is_match("abc", "abc") == {0, 1, 2}
        assert is_match("abc", "aabbccdd") == {0, 2, 4}
        assert is_match("aaabbb", "aaa-bbb") == {0, 1, 2, 4, 5, 6}
        assert is_match("a", "a") == {0}
        assert is_match("a", " -. a") == {4}

        assert is_match("123", "44142434") == {2, 4, 6}
        assert is_match("123", "1243") == {0, 1, 3}

    def test_not_match(self):
        assert is_match("b", "") is None

        assert is_match("b", "a") is None
        assert is_match("d", "abc") is None
        assert is_match("123", "143") is None
        assert is_match("123", "124") is None
