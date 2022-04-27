import requests

from tests.test_e2e_base import TestE2eBase, NUM_MENU_LINKS


URL = "http://localhost:8000/import"


# pylint: disable=R0201 (no-self-use)
class TestE2eImportPage(TestE2eBase):
    def test_import_page(self):
        response = requests.get(URL)
        assert response.status_code == 200
        assert response.text.count("Import") == 2  # menu + sub-header
        assert response.text.count("href") == NUM_MENU_LINKS
        assert "Import bookmarks" in response.text  # sub-header
