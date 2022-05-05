from utils import html_utils


# pylint: disable=R0201 (no-self-use)
class TestHTMLUtils:
    def test_html_escape(self):
        assert html_utils.html_escape("<>") == "&lt;&gt;"
        assert html_utils.html_escape("&") == "&amp;"
        assert html_utils.html_escape("") == ""
        assert html_utils.html_escape(None) is None

    def test_split_escaped_text(self):
        assert not html_utils.split_escaped_text("")

        assert html_utils.split_escaped_text("a") == ["a"]
        assert html_utils.split_escaped_text("ab") == ["a", "b"]
        assert html_utils.split_escaped_text("&lt;ab") == ["&lt;", "a", "b"]
        assert html_utils.split_escaped_text("ab&gt;") == ["a", "b", "&gt;"]
        assert html_utils.split_escaped_text("a&amp;b") == ["a", "&amp;", "b"]

    def test_highlight(self):
        assert html_utils.highlight(None,
                                    None) == ""
        assert html_utils.highlight([],
                                    None) == ""

        assert html_utils.highlight(["a", "b", "c"],
                                    None) == "abc"
        assert html_utils.highlight(["a", "b", "c"],
                                    {}) == "abc"
        assert html_utils.highlight(["a", "b", "c"],
                                    {}) == "abc"

        assert html_utils.highlight(["a"],
                                    {}) == "a"
        assert html_utils.highlight(["a"],
                                    {0}) == "<mark>a</mark>"
        assert html_utils.highlight(["a", "b", "c"],
                                    {0}) == "<mark>a</mark>bc"
        assert html_utils.highlight(["a", "b", "c"],
                                    {0, 2}) == "<mark>a</mark>b<mark>c</mark>"
        assert html_utils.highlight(["a", "b", "c"],
                                    {0, 2, 1}) == "<mark>a</mark><mark>b</mark><mark>c</mark>"

        assert html_utils.highlight(["a", "&amp;", "c"],
                                    {0}) == "<mark>a</mark>&amp;c"
        assert html_utils.highlight(["a", "&amp;", "c"],
                                    {1}) == "a<mark>&amp;</mark>c"
