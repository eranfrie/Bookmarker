import re

import requests

from app import app
from tests.test_e2e_base import TestE2eBase, URL


# pylint: disable=R0904 (too-many-public-methods)
class TestE2eAddBookmark(TestE2eBase):
    def test_add_bookmark(self):
        # add a bookmark
        response = self._add_bookmark("test_title", "test_description", "http://www.test.com", "test_section")
        self._compare_num_bookmarks(response, 1)

        # add another bookmark
        response = self._add_bookmark("test_title_2", "test_description_2",
                                      "http://www.test_2.com", "test_section_2")
        self._compare_num_bookmarks(response, 2)

        # validate fields order
        pattern = "test_title.*test_description.*http://www\\.test\\.com.*" \
                  "test_title_2.*test_description_2.*http://www\\.test_2\\.com"
        assert re.search(pattern, response.text)

    def test_add_bookmark_with_missing_description(self):
        """
        description is optional field - adding a bookmark should succeed.
        """
        response = self._add_bookmark("test_title", "", "http://www.test.com", "test_section")
        self._compare_num_bookmarks(response, 1)

    def test_add_bookmark_with_missing_section(self):
        """
        section is optional field - adding a bookmark should succeed.
        """
        response = self._add_bookmark("test_title", "test_description", "http://www.test.com", "")
        self._compare_num_bookmarks(response, 1)

    def test_add_bookmark_with_missing_description_and_section(self):
        response = self._add_bookmark("test_title", "", "http://www.test.com", "")
        self._compare_num_bookmarks(response, 1)

    def test_not_displaying_missing_description(self):
        """
        a missing (optional) description should not be displayed as "None".
        """
        response = self._add_bookmark("test_title", "", "http://www.test.com", "test_section")
        self._compare_num_bookmarks(response, 1)
        assert "None" not in response.text

    def test_add_bookmark_internal_err(self):
        # delete the db in order to get an internal error.
        self._delete_db()

        response = self._add_bookmark("test_title", "test_description", "http://www.test.com", "test_section")
        self._compare_num_bookmarks(response, 0, db_avail=False)
        assert response.text.count(app.ADD_BOOKMARK_ERR_MSG) == 1
        assert response.text.count(app.GET_BOOKMARKS_ERR_MSG) == 1

        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 0, db_avail=False)
        assert response.text.count(app.ADD_BOOKMARK_ERR_MSG) == 0
        assert response.text.count(app.GET_BOOKMARKS_ERR_MSG) == 1

    def test_add_bookmark_success_msg(self):
        # add a bookmark
        response = self._add_bookmark("test_title", "test_description", "http://www.test.com", "test_section")
        self._compare_num_bookmarks(response, 1)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1

        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 1)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 0

        # add another bookmark
        response = self._add_bookmark("test_title_2", "test_description_2",
                                      "http://www.test_2.com", "test_section_2")
        self._compare_num_bookmarks(response, 2)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1

        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 0

    def test_add_bookmark_title_required(self):
        response = self._add_bookmark("", "test_description", "http://www.test.com", "test_section")
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_TITLE_REQUIRED_MSG) == 1

    def test_add_bookmark_url_required(self):
        response = self._add_bookmark("test_title_2", "test_description", "", "test_section")
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_URL_REQUIRED_MSG) == 1

    def test_add_bookmark_description_only(self):
        response = self._add_bookmark("", "test_description", "", "")
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_TITLE_REQUIRED_MSG) == 1

    def test_add_bookmark_no_fields(self):
        response = self._add_bookmark("", "", "", "")
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_TITLE_REQUIRED_MSG) == 1

    def test_add_bookmark_title_whitespace(self):
        response = self._add_bookmark(" ", "", "test_url", "")
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_TITLE_REQUIRED_MSG) == 1

    def test_add_bookmark_title_tab(self):
        response = self._add_bookmark("\t", "", "test_url", "")
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_TITLE_REQUIRED_MSG) == 1

    def test_add_bookmark_title_newline(self):
        response = self._add_bookmark("\n", "", "test_url", "")
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_TITLE_REQUIRED_MSG) == 1

    def test_add_bookmark_url_whitespace(self):
        response = self._add_bookmark("test_title", "", " ", "")
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_URL_REQUIRED_MSG) == 1

    def test_add_bookmark_url_tab(self):
        response = self._add_bookmark("test_title", "", "\t", "")
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_URL_REQUIRED_MSG) == 1

    def test_add_bookmark_url_newline(self):
        response = self._add_bookmark("test_title", "", "\n", "")
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_URL_REQUIRED_MSG) == 1

    def test_html_escaping(self):
        response = self._add_bookmark("<>test_title", "<>test_description",
                                      "<>http://www.test.com", "<>test_section")
        self._compare_num_bookmarks(response, 1)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1
        pattern = "&lt;&gt;test_section.*&lt;&gt;test_title.*" \
            "&lt;&gt;test_description.*&lt;&gt;http://www\\.test\\.com"
        assert re.search(pattern, response.text)

    def test_sql_escaping(self):
        # test single quote
        response = self._add_bookmark("'select *'", "'select *'", "'select *'", "'select *'")
        self._compare_num_bookmarks(response, 1)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1

        # test double quote
        response = self._add_bookmark('"select *"', '"select *"', '"select *"', '"select *"')
        self._compare_num_bookmarks(response, 2)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1

    def test_whitespace(self):
        response = self._add_bookmark("test title", "test description", "test url", "test section")
        self._compare_num_bookmarks(response, 1)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1
        assert "test title" in response.text \
            and "test description" in response.text \
            and "test url" in response.text \
            and "test section" in response.text

    def test_input_values_on_err(self):
        """
        If "add bookmark" operation fail,
        fields that were entered by user should still show up.
        """
        # error due to missing title
        response = self._add_bookmark("", "test_description", "test_url", "test_section")
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_TITLE_REQUIRED_MSG) == 1
        assert 'value="test_description"' in response.text \
            and 'value="test_url"' in response.text \
            and 'value="test_section"' in response.text

        # error due to missing url
        response = self._add_bookmark("test_title", "test_description", "", "test_section")
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_URL_REQUIRED_MSG) == 1
        assert 'value="test_description"' in response.text \
            and 'value="test_title"' in response.text \
            and 'value="test_section"' in response.text

        # internal error
        self._delete_db()
        response = self._add_bookmark("test_title", "test_description", "test_url", "test_section")
        self._compare_num_bookmarks(response, 0, db_avail=False)
        assert response.text.count(app.ADD_BOOKMARK_ERR_MSG) == 1
        assert response.text.count(app.GET_BOOKMARKS_ERR_MSG) == 1
        assert 'value="test_description"' in response.text \
            and 'value="test_title"' in response.text \
            and 'value="test_url"' in response.text \
            and 'value="test_section"' in response.text

    def test_escaped_input_values_on_err(self):
        """
        If "add bookmark" operation fail,
        fields that were entered by user should still show up.

        test that the values are escaped.
        """
        self._delete_db()
        response = self._add_bookmark("<test_title>", "<test_description>", "<test_url>", "<test_section>")
        self._compare_num_bookmarks(response, 0, db_avail=False)
        assert response.text.count(app.ADD_BOOKMARK_ERR_MSG) == 1
        assert response.text.count(app.GET_BOOKMARKS_ERR_MSG) == 1
        assert 'value="&lt;test_description&gt;"' in response.text \
            and 'value="&lt;test_title&gt;"' in response.text \
            and 'value="&lt;test_url&gt;"' in response.text \
            and 'value="&lt;test_section&gt;"' in response.text

    def test_no_input_values_on_success(self):
        """
        If "add bookmark" operation fail,
        fields that were entered by user should still show up.

        test that there are no values on success.
        """
        response = self._add_bookmark("<test_title>", "<test_description>", "<test_url>", "<test_section>")
        self._compare_num_bookmarks(response, 1)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1
        assert 'value="&lt;test_description&gt;"' not in response.text \
            and 'value="&lt;test_title&gt;"' not in response.text \
            and 'value="&lt;test_url&gt;"' not in response.text \
            and 'value="&lt;test_section&gt;"' not in response.text
