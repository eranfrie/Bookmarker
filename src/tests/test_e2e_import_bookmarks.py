import requests

from tests.test_e2e_base import TestE2eBase, NUM_MENU_LINKS, URL


# pylint: disable=R0201 (no-self-use)
class TestE2eImportBookmarks(TestE2eBase):
    # pylint: disable=R0913 (too-many-arguments)
    def _test_response(self, response, internal_err, num_added, num_failed, total):
        assert response.status_code == 200
        if not internal_err:
            assert "Failed to import bookmarks" not in response.text

            if num_added > 0:
                assert f"Imported {num_added} bookmarks" in response.text
            else:
                assert "Imported" not in response.text

            if num_failed > 0:
                assert f"Failed to import {num_failed} bookmarks" in response.text
            else:
                assert "Failed to import" not in response.text
        else:  # internal error
            assert "Failed to import bookmarks" in response.text
            assert "Imported" not in response.text

        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, total)

    def test_import_page(self):
        response = requests.get(URL.IMPORT.value)
        assert response.status_code == 200
        assert response.text.count("Import") == 2  # menu + sub-header
        assert response.text.count("href") == NUM_MENU_LINKS
        assert "Import bookmarks" in response.text  # sub-header

    def test_import_success(self):
        with open("src/tests/chrome_bookmarks_test.html", "rb") as f:
            files = {"bookmarks_html": f}
            response = requests.post(URL.IMPORT.value, files=files)
        self._test_response(response, False, 6, 0, 6)

    def test_import_hebew(self):
        with open("src/tests/chrome_bookmarks_hebrew.html", "rb") as f:
            files = {"bookmarks_html": f}
            response = requests.post(URL.IMPORT.value, files=files)
        self._test_response(response, False, 1, 0, 1)

    def test_import_internal_err(self):
        with open("src/tests/chrome_bookmarks_hebrew.html", "rb") as f:
            # cause internal error by changing the name
            files = {"wrong_name": f}
            response = requests.post(URL.IMPORT.value, files=files)
        self._test_response(response, True, None, None, 0)

    def test_import_partial(self):
        """
        using a file that contains both good and bad bookmarks.
        """
        with open("src/tests/chrome_bookmarks_partial.html", "rb") as f:
            files = {"bookmarks_html": f}
            response = requests.post(URL.IMPORT.value, files=files)
        self._test_response(response, False, 2, 1, 2)

    def test_two_imports(self):
        """
        test that the second imported file overrides the first one
        (in the server filesystem).
        """
        # first file
        with open("src/tests/chrome_bookmarks_test.html", "rb") as f:
            files = {"bookmarks_html": f}
            response = requests.post(URL.IMPORT.value, files=files)
        self._test_response(response, False, 6, 0, 6)

        # second file
        with open("src/tests/chrome_bookmarks_partial.html", "rb") as f:
            files = {"bookmarks_html": f}
            response = requests.post(URL.IMPORT.value, files=files)
        self._test_response(response, False, 2, 1, 8)
