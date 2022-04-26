import re

import requests

from app import app
from tests.test_e2e_base import TestE2eBase


URL = "http://localhost:8000"
ADD_BOOKMARK_URL = f"{URL}/add_bookmark"


class TestE2e(TestE2eBase):
    def test_add_bookmark(self):
        # add a bookmark
        payload = {
            "title": "test_title",
            "description": "test_description",
            "url": "http://www.test.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 1)

        # add another bookmark
        payload = {
            "title": "test_title_2",
            "description": "test_description_2",
            "url": "http://www.test_2.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 2)

        # validate fields order
        pattern = "test_title.*test_description.*http://www\\.test\\.com.*" \
                  "test_title_2.*test_description_2.*http://www\\.test_2\\.com"
        assert re.search(pattern, response.text)

    def test_add_bookmark_with_missing_description(self):
        """
        description is optional field - adding a bookmark should succeed.
        """
        payload = {
            "title": "test_title",
            "url": "http://www.test.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 1)

    def test_not_desplaying_missing_description(self):
        """
        a missing (optional) description should not be displayed as "None".
        """
        payload = {
            "title": "test_title",
            "url": "http://www.test.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 1)
        assert "None" not in response.text

    def test_add_bookmark_internal_err(self):
        # delete the db in order to get an internal error.
        self._delete_db()

        payload = {
            "title": "test_title",
            "description": "test_description",
            "url": "http://www.test.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 0, db_avail=False)
        assert response.text.count(app.ADD_BOOKMARK_ERR_MSG) == 1
        assert response.text.count(app.GET_BOOKMARKS_ERR_MSG) == 1

        response = requests.get(URL)
        self._compare_num_bookmarks(response, 0, db_avail=False)
        assert response.text.count(app.ADD_BOOKMARK_ERR_MSG) == 0
        assert response.text.count(app.GET_BOOKMARKS_ERR_MSG) == 1

    def test_add_bookmark_success_msg(self):
        # add a bookmark
        payload = {
            "title": "test_title",
            "description": "test_description",
            "url": "http://www.test.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 1)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1

        response = requests.get(URL)
        self._compare_num_bookmarks(response, 1)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 0

        # add another bookmark
        payload = {
            "title": "test_title_2",
            "description": "test_description_2",
            "url": "http://www.test_2.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 2)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1

        response = requests.get(URL)
        self._compare_num_bookmarks(response, 2)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 0

    def test_add_bookmark_title_required(self):
        payload = {
            "description": "test_description",
            "url": "http://www.test.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_TITLE_REQUIRED_MSG) == 1

    def test_add_bookmark_url_required(self):
        payload = {
            "title": "test_title_2",
            "description": "test_description",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_URL_REQUIRED_MSG) == 1

    def test_html_escaping(self):
        payload = {
            "title": "<>test_title",
            "description": "<>test_description",
            "url": "<>http://www.test.com",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 1)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1
        pattern = "&lt;&gt;test_title.*&lt;&gt;test_description.*&lt;&gt;http://www\\.test\\.com"
        assert re.search(pattern, response.text)

    def test_sql_escaping(self):
        # test single quote
        payload = {
            "title": "'select *'",
            "description": "'select *'",
            "url": "'select *'",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 1)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1

        # test double quote
        payload = {
            "title": '"select *"',
            "description": '"select *"',
            "url": '"select *"',
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 2)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1

    def test_whitespace(self):
        payload = {
            "title": "test title",
            "description": "test description",
            "url": "test url",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 1)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1
        assert "test title" in response.text \
            and "test description" in response.text \
            and "test url" in response.text

    def test_input_values_on_err(self):
        """
        If "add bookmark" operation fail,
        fields that were entered by user should still show up.
        """
        # error due to missing title
        payload = {
            "description": "test_description",
            "url": "test_url",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_TITLE_REQUIRED_MSG) == 1
        assert 'value="test_description"' in response.text \
            and 'value="test_url"' in response.text

        # error due to missing url
        payload = {
            "title": "test_title",
            "description": "test_description",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 0)
        assert response.text.count(app.ADD_BOOKMARK_URL_REQUIRED_MSG) == 1
        assert 'value="test_description"' in response.text \
            and 'value="test_title"' in response.text

        # internal error
        self._delete_db()
        payload = {
            "title": "test_title",
            "description": "test_description",
            "url": "test_url",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 0, db_avail=False)
        assert response.text.count(app.ADD_BOOKMARK_ERR_MSG) == 1
        assert response.text.count(app.GET_BOOKMARKS_ERR_MSG) == 1
        assert 'value="test_description"' in response.text \
            and 'value="test_title"' in response.text \
            and 'value="test_url"' in response.text

    def test_escaped_input_values_on_err(self):
        """
        If "add bookmark" operation fail,
        fields that were entered by user should still show up.

        test that the values are escaped.
        """
        self._delete_db()
        payload = {
            "title": "<test_title>",
            "description": "<test_description>",
            "url": "<test_url>",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 0, db_avail=False)
        assert response.text.count(app.ADD_BOOKMARK_ERR_MSG) == 1
        assert response.text.count(app.GET_BOOKMARKS_ERR_MSG) == 1
        assert 'value="&lt;test_description&gt;"' in response.text \
            and 'value="&lt;test_title&gt;"' in response.text \
            and 'value="&lt;test_url&gt;"' in response.text

    def test_no_input_values_on_success(self):
        """
        If "add bookmark" operation fail,
        fields that were entered by user should still show up.

        test that there are no values on success.
        """
        payload = {
            "title": "<test_title>",
            "description": "<test_description>",
            "url": "<test_url>",
        }
        response = requests.post(ADD_BOOKMARK_URL, data=payload)
        self._compare_num_bookmarks(response, 1)
        assert response.text.count(app.ADD_BOOKMARK_OK_MSG) == 1
        assert 'value="&lt;test_description&gt;"' not in response.text \
            and 'value="&lt;test_title&gt;"' not in response.text \
            and 'value="&lt;test_url&gt;"' not in response.text
