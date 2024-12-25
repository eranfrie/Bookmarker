import requests

from tests.test_e2e_base import TestE2eBase, URL


# pylint: disable=R0201 (no-self-use)
class TestE2eEditForm(TestE2eBase):
    def test_edit_form(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "http://www.test_1.com", "test_section_1")
        response = requests.get(URL.EDIT_FORM.value + "?id=1")
        assert response.status_code == 200
        assert "test_title_1" in response.text and "test_description_1" in response.text \
                and "http://www.test_1.com" in response.text and "test_section_1" in response.text

        assert "Edit a bookmark" in response.text

    def test_edit_form_invalid_bookmark_id(self):
        """In case of invalid bookmark id, main page is presented."""
        response = requests.get(URL.EDIT_FORM.value + "?id=1234")
        assert response.status_code == 200
        assert "Add a bookmark" in response.text

    def test_edit_form_bookmark_id_missing_in_url(self):
        """In case of missing bookmark id, main page is presented."""
        response = requests.get(URL.EDIT_FORM.value)
        assert response.status_code == 200
        assert "Add a bookmark" in response.text

    def test_edit_form_db_not_accessible(self):
        """In case of no DB, main page is presented."""
        self._delete_db()
        response = requests.get(URL.EDIT_FORM.value + "?id=1")
        assert response.status_code == 200
        assert "Add a bookmark" in response.text
