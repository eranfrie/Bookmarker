import requests

from tests.test_e2e_base import TestE2eBase, URL
from app import app


class TestE2eEdit(TestE2eBase):
    # pylint: disable=R0201 (no-self-use)
    def _edit_bookmark(self, bookmark_id, title, description, url, section):
        payload = {
            "bookmark_id": bookmark_id,
            "title": title,
            "description": description,
            "url": url,
            "section": section,
        }
        response = requests.post(URL.EDIT_BOOKMARK.value, data=payload)
        return response

    def test_edit_success(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "http://www.test_1.com", "test_section_1")
        response = self._edit_bookmark(1, "test_title_2", "test_description_2", "http://www.test_2.com", "test_section_2")
        self._compare_num_bookmarks(response, 1)
        assert "test_title_2" in response.text and "test_description_2" in response.text \
                and "http://www.test_2.com" in response.text and "test_section_2" in response.text
        assert app.EDIT_BOOKMARK_OK_MSG in response.text
        assert "Add a bookmark" in response.text

    def test_edit_fail_title_required(self):
        """Edit fails because title is a required field."""
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "http://www.test_1.com", "test_section_1")
        response = self._edit_bookmark(1, "", "test_description_2", "http://www.test_2.com", "test_section_2")
        assert "test_title_1" not in response.text
        assert "test_description_2" in response.text and "http://www.test_2.com" in response.text \
                and "test_section_2" in response.text
        assert app.BOOKMARK_TITLE_REQUIRED_MSG in response.text
        # stay in edit form
        assert "Edit a bookmark" in response.text

    def test_edit_fail_title_required(self):
        """Edit fails because URL is a required field."""
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "http://www.test_1.com", "test_section_1")
        response = self._edit_bookmark(1, "test_title_2", "test_description_2", "", "test_section_2")
        assert "http://www.test_1.com" not in response.text
        assert "test_title_2" in response.text and  "test_description_2" in response.text \
                and "test_section_2" in response.text
        assert app.BOOKMARK_URL_REQUIRED_MSG in response.text
        # stay in edit form
        assert "Edit a bookmark" in response.text

    def test_edit_fail_db_not_accessible(self):
        self._delete_db()
        response = self._edit_bookmark(1, "test_title_2", "test_description_2", "http://www.test_2.com", "test_section_2")
        assert "test_title_2" in response.text and "test_description_2" in response.text \
                and "http://www.test_2.com" in response.text and "test_section_2" in response.text
        assert app.EDIT_BOOKMARK_ERR_MSG in response.text
        # stay in edit form
        assert "Edit a bookmark" in response.text
