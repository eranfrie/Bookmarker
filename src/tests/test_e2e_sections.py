import re

import requests

from tests.test_e2e_base import TestE2eBase, URL


class TestE2eSections(TestE2eBase):
    def test_section_appears_once(self):
        """
        tests that links with the same section are grouped together
        and each section appears only once.
        """
        self._add_bookmark_to_db("test_title", "test_description",
                                 "http://www.test.com", "test_section_1")
        self._add_bookmark_to_db("test_title", "test_description",
                                 "http://www.test.com", "test_section_2")
        self._add_bookmark_to_db("test_title", "test_description",
                                 "http://www.test.com", "test_section_3")
        self._add_bookmark_to_db("test_title", "test_description",
                                 "http://www.test.com", "test_section_1")
        self._add_bookmark_to_db("test_title", "test_description",
                                 "http://www.test.com", "test_section_2")

        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 5)
        assert response.text.count("test_section_1") == 1
        assert response.text.count("test_section_2") == 1
        assert response.text.count("test_section_3") == 1

    def test_no_section_first(self):
        self._add_bookmark("test_title_3", "test_description",
                           "http://www.test.com", "test_section_1")
        # special case - test that " " is treated as ""
        # so when sorting, it should come before the next bookmark (with "" section)
        self._add_bookmark("test_title_1", "test_description",
                           "http://www.test.com", " ")
        self._add_bookmark("test_title_2", "test_description",
                           "http://www.test.com", "")

        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 3)
        pattern = "test_title_1.*test_title_2.*test_section_1.*test_title_3"
        assert re.search(pattern, response.text)

    def test_section_ignore_case(self):
        self._add_bookmark_to_db("test_title", "test_description",
                                 "http://www.test.com", "Test_section")
        self._add_bookmark_to_db("test_title", "test_description",
                                 "http://www.test.com", "test_section")

        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)
        assert response.text.count("est_section") == 1
