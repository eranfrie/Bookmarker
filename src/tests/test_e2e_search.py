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
        assert response.text.count("mark>") == len(pattern) * 2

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
        assert response.text.count("mark>") == len(pattern) * 2

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
        assert response.text.count("mark>") == len(pattern) * 2

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
        assert response.text.count("mark>") == len(pattern) * 2

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
        assert response.text.count("mark>") == len(pattern) * 2

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
        assert response.text.count("mark>") == len(pattern) * 2

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
        assert response.text.count("mark>") == len(pattern) * 2

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
        assert response.text.count("mark>") == len(pattern) * 2

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
        assert response.text.count("mark>") == len(pattern) * 2

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
        assert response.text.count("mark>") == len(pattern) * 2

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
        assert response.text.count("mark>") == len(pattern) * 2

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
        assert response.text.count("mark>") == len(pattern) * 2

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
        assert response.text.count("mark>") == len(pattern) * 2

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
        assert response.text.count("mark>") == len(pattern) * 2

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
        assert response.text.count("mark>") == len(pattern) * 2

    def test_clear_search_no_highlight(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 1)

        pattern = "test_title_1"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1)
        assert response.text.count("mark>") == len(pattern) * 2

        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 1)
        assert response.text.count("mark>") == 0

    def test_highlight_section(self):
        self._add_bookmark_to_db("test_highlight", "",
                                 "https://www.test_1.com", "test_highlight")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 1)

        pattern = "testhghlgt"
        params = {"pattern": pattern, "includeurl": "true"}
        response = requests.get(URL.INDEX.value, params=params)
        self._compare_num_bookmarks(response, 1)
        assert response.text.count("mark>") == len(pattern) * 2 * 2
