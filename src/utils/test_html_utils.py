from utils import html_utils


# pylint: disable=R0201 (no-self-use)
class TestHTMLUtils:
    def test_html_escape(self):
        assert html_utils.html_escape("<>") == "&lt;&gt;"
        assert html_utils.html_escape("&") == "&amp;"
        assert html_utils.html_escape("") == ""
        assert html_utils.html_escape(None) is None
