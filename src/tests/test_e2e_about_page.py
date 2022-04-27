import requests

from tests.test_e2e_base import TestE2eBase, NUM_MENU_LINKS
from utils import version, opts


URL = "http://localhost:8000/about"


# pylint: disable=R0201 (no-self-use)
class TestE2eAboutPage(TestE2eBase):
    def test_about_page(self):
        response = requests.get(URL)
        assert response.status_code == 200
        assert response.text.count("About") == 2  # menu + sub-header
        assert response.text.count("href") == NUM_MENU_LINKS + 1  # 1 for github link

        ver = version.get_version()
        assert f"{opts.PROD_NAME} Version {ver}" in response.text
