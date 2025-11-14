import requests

from tests.test_e2e_base import TestE2eBase, URL


class TestE2eSearch(TestE2eBase):
    def test_complete_match_title(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "test_title_1"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_complete_match_description(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "test_description_1"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_complete_match_url(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "test_1.com"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_include_url(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "test_1.com"
        params = {"pattern": pattern, "includeurl": "false"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 0, db_avail=False)

    def test_fuzzy_title(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "testtitle1"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_fuzzy_description(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "tstdescription_1"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_fuzzy_url(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "test1com"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_fuzzy_ignore_case_title(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "TESTtitle1"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_fuzzy_ignore_case_description(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "TSTdescription_1"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_fuzzy_ignore_case_url(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "TEST1com"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_html_escaping_title(self):
        self._add_bookmark_to_db("<>test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("<>test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "<>TESTtitle1"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_html_escaping_description(self):
        self._add_bookmark_to_db("test_title_1", "<>test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "<>test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "<>TSTdescription1"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_html_escaping_url(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1<>.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2<>.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "TEST1<>com"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_sql_escaping_title(self):
        self._add_bookmark_to_db("\"'test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("\"'test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "\"'TESTtitle1"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_sql_escaping_description(self):
        self._add_bookmark_to_db("test_title_1", "\"'test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "\"'test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "\"'TSTdescription_1"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_sql_escaping_url(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1\"'.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2\"'.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "TEST1\"'com"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_regular_search(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "test_title_1"
        params = {"pattern": pattern, "includeurl": "true", "fuzzy": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_regular_search_no_match(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "tsttitle1"
        params = {"pattern": pattern, "includeurl": "true", "fuzzy": "false"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 0, db_avail=False)

    def test_section_filter_only(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        self._add_bookmark_to_db("test_title_3", "test_description_3",
                                 "https://www.test_3.com", "test_section_1")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 3)

        params = {"sectionPattern": "test_section_1"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 2, db_avail=False)

    def test_section_filter_case_insensitive(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "Test_Section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        params = {"sectionPattern": "test_section_1"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_section_filter_with_pattern(self):
        self._add_bookmark_to_db("title_a", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("title_b", "test_description_2",
                                 "https://www.test_2.com", "test_section_1")
        self._add_bookmark_to_db("title_c", "test_description_3",
                                 "https://www.test_3.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 3)

        # Filter by section and pattern
        pattern = "title_a"
        params = {"pattern": pattern, "sectionPattern": "test_section_1", "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1, db_avail=False)

    def test_section_filter_no_match(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        params = {"sectionPattern": "nonexistent_section"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 0, db_avail=False)
