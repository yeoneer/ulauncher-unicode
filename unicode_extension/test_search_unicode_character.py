import unittest

import os
import sys
import logging

from .load_unicode_data import load_unicode_data
from .search_unicode_character import search_unicode_character
from .unicode_character import UnicodeCharacter
from .unicode_extension_feature import UnicodeExtensionFeature


class SearchUnicodeCharacterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.UNICODE_CHARACTER_DICT: dict[str, UnicodeCharacter] = {}
        cls.UNICODE_CHARACTER_LIST: list[UnicodeCharacter] = []

        loaded_unicode_data = load_unicode_data()

        cls.UNICODE_CHARACTER_DICT = loaded_unicode_data["UNICODE_CHARACTER_DICT"]
        cls.UNICODE_CHARACTER_LIST = loaded_unicode_data["UNICODE_CHARACTER_LIST"]

    def search_one_character(self, query: str) -> UnicodeCharacter:

        search_result = search_unicode_character(query, self.UNICODE_CHARACTER_LIST, 10)

        # for result_item in search_result_list:
        #     (unicode_character, _, _) = result_item
        #     unicode_character: UnicodeCharacter = unicode_character

        #     print(result_item, " - ", " ".join(unicode_character.aliases))
        (unicode_character, _, _) = search_result[0]
        unicode_character: UnicodeCharacter = unicode_character

        return unicode_character

    def check_search(
        self,
        expected_character_u_code_point: str,
        query: str,
    ):
        searched_character = self.search_one_character(query)

        self.assertEqual(
            searched_character.u_code_point,
            expected_character_u_code_point,
            f"Query: `{query}`, Searched Character: {searched_character}",
        )

    def test_unicode_search_000a(self):
        self.check_search("U+000A", "end of line")
        self.check_search("U+000A", "line feed lf")

    def test_unicode_search_0041(self):
        # self.check_search("U+0041", "capital latin a")
        self.check_search("U+0041", "capital letter latin a")

    def test_unicode_search_00b7(self):
        self.check_search("U+00B7", "00b7")
        self.check_search("U+00B7", "middle dot")


if __name__ == "__main__":
    unittest.main()
