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
        response = requests.get(URL.INDEX.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1, db_avail=False)
        assert response.text.count("mark") == len(pattern) * 2 + 3  # 3 because of Bookmarker header, etc

    def test_complete_match_description(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "test_description_1"
        response = requests.get(URL.INDEX.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1, db_avail=False)
        assert response.text.count("mark") == len(pattern) * 2 + 3  # 3 because of Bookmarker header, etc

    def test_complete_match_url(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "test_1.com"
        response = requests.get(URL.INDEX.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1, db_avail=False)
        assert response.text.count("mark") == len(pattern) * 2 + 3  # 3 because of Bookmarker header, etc

    def test_fuzzy_title(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "testtitle1"
        response = requests.get(URL.INDEX.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1, db_avail=False)
        assert response.text.count("mark") == len(pattern) * 2 + 3  # 3 because of Bookmarker header, etc

    def test_fuzzy_description(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "tstdescription_1"
        response = requests.get(URL.INDEX.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1, db_avail=False)
        assert response.text.count("mark") == len(pattern) * 2 + 3  # 3 because of Bookmarker header, etc

    def test_fuzzy_url(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "test1com"
        response = requests.get(URL.INDEX.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1, db_avail=False)
        assert response.text.count("mark") == len(pattern) * 2 + 3  # 3 because of Bookmarker header, etc

    def test_fuzzy_ignore_case_title(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "TESTtitle1"
        response = requests.get(URL.INDEX.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1, db_avail=False)
        assert response.text.count("mark") == len(pattern) * 2 + 3  # 3 because of Bookmarker header, etc

    def test_fuzzy_ignore_case_description(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "TSTdescription_1"
        response = requests.get(URL.INDEX.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1, db_avail=False)
        assert response.text.count("mark") == len(pattern) * 2 + 3  # 3 because of Bookmarker header, etc

    def test_fuzzy_ignore_case_url(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "TEST1com"
        response = requests.get(URL.INDEX.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1, db_avail=False)
        assert response.text.count("mark") == len(pattern) * 2 + 3  # 3 because of Bookmarker header, etc

    def test_html_escaping_title(self):
        self._add_bookmark_to_db("<>test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("<>test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "<>TESTtitle1"
        response = requests.get(URL.INDEX.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1, db_avail=False)
        assert response.text.count("mark") == len(pattern) * 2 + 3  # 3 because of Bookmarker header, etc

    def test_html_escaping_description(self):
        self._add_bookmark_to_db("test_title_1", "<>test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "<>test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "<>TSTdescription1"
        response = requests.get(URL.INDEX.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1, db_avail=False)
        assert response.text.count("mark") == len(pattern) * 2 + 3  # 3 because of Bookmarker header, etc

    def test_html_escaping_url(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1<>.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2<>.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "TEST1<>com"
        response = requests.get(URL.INDEX.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1, db_avail=False)
        assert response.text.count("mark") == len(pattern) * 2 + 3  # 3 because of Bookmarker header, etc

    def test_sql_escaping_title(self):
        self._add_bookmark_to_db("\"'test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("\"'test_title_2", "test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "\"'TESTtitle1"
        response = requests.get(URL.INDEX.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1, db_avail=False)
        assert response.text.count("mark") == len(pattern) * 2 + 3  # 3 because of Bookmarker header, etc

    def test_sql_escaping_description(self):
        self._add_bookmark_to_db("test_title_1", "\"'test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "\"'test_description_2",
                                 "https://www.test_2.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "\"'TSTdescription_1"
        response = requests.get(URL.INDEX.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1, db_avail=False)
        assert response.text.count("mark") == len(pattern) * 2 + 3  # 3 because of Bookmarker header, etc

    def test_sql_escaping_url(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1\"'.com", "test_section_1")
        self._add_bookmark_to_db("test_title_2", "test_description_2",
                                 "https://www.test_2\"'.com", "test_section_2")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 2)

        pattern = "TEST1\"'com"
        response = requests.get(URL.INDEX.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1, db_avail=False)
        assert response.text.count("mark") == len(pattern) * 2 + 3  # 3 because of Bookmarker header, etc

    # pylint: disable=R0201 (no-self-use)
    def test_last_search_in_input_field(self):
        response = requests.get(URL.INDEX.value, params={"pattern": "last_search_pattern"})
        assert 'value="last_search_pattern"' in response.text
        assert response.text.count("mark") == 3  # 3 because of Bookmarker header, etc

    # pylint: disable=R0201 (no-self-use)
    def test_last_search_in_input_field_escaped(self):
        response = requests.get(URL.INDEX.value, params={"pattern": "last_search_pattern<>"})
        assert 'value="last_search_pattern&lt;&gt;"' in response.text
        assert response.text.count("mark") == 3  # 3 because of Bookmarker header, etc

    def test_clear_search_no_highlight(self):
        self._add_bookmark_to_db("test_title_1", "test_description_1",
                                 "https://www.test_1.com", "test_section_1")
        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 1)

        pattern = "test_title_1"
        response = requests.get(URL.INDEX.value, params={"pattern": pattern})
        self._compare_num_bookmarks(response, 1)
        assert response.text.count("mark") == len(pattern) * 2 + 3  # 3 because of Bookmarker header, etc

        response = requests.get(URL.INDEX.value)
        self._compare_num_bookmarks(response, 1)
        assert response.text.count("mark") == 3  # 3 because of Bookmarker header, etc
