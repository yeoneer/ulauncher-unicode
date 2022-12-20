import unittest

import os
import sys

from .load_unicode_data import load_unicode_data
from .unicode_character import UnicodeCharacter
from .unicode_extension_feature import UnicodeExtensionFeature
from .util import get_project_path


class UnicodeExtensionFeatureTest(unittest.TestCase):
    def setUp(self):
        loaded_unicode_data = load_unicode_data()

        self.feature: UnicodeExtensionFeature = UnicodeExtensionFeature(
            project_path=get_project_path(),
            unicode_character_list=loaded_unicode_data["UNICODE_CHARACTER_LIST"],
            unicode_character_dict=loaded_unicode_data["UNICODE_CHARACTER_DICT"],
        )

    def test_weird_preferences_value_update(self):
        self.feature.preferences.update({"search_result_list_size": "asdf"})
        self.assertIsInstance(
            self.feature.preferences.search_result_list_size,
            int,
            "'search_result_list_size' should be a number",
        )

        self.feature.preferences.update({"search_result_list_size": "-1"})
        self.assertNotEqual(
            -1,
            self.feature.preferences.search_result_list_size,
            "'search_result_list_size' can't be lower than 0",
        )

        # Allow '0' if user want
        self.feature.preferences.update({"search_result_list_size": "0"})
        self.assertEqual(0, self.feature.preferences.search_result_list_size)

        self.feature.preferences.update({"unicode_character_icon_font": ""})
        self.assertNotEqual(
            "",
            self.feature.preferences.unicode_character_icon_font,
            "'unicode_character_icon_font' can't be empty",
        )
        self.assertEqual(
            "sans-serif",
            self.feature.preferences.unicode_character_icon_font,
            "'unicode_character_icon_font' default value is `sans-serif` ",
        )

    def test_proper_preferences_value_update_type_a(self):
        PREFERENCES: dict = {
            "search_result_list_size": "20",
            "search_result_view_type": "small",
            "unicode_character_icon_font": "Open Sans, sans-serif",
            "unicode_character_icon_background": "none",
        }

        self.feature.preferences.update(PREFERENCES)

        self.assertEqual(self.feature.preferences.search_result_list_size, 20)
        self.assertEqual(self.feature.preferences.search_result_view_type, "small")
        self.assertEqual(
            self.feature.preferences.unicode_character_icon_font,
            "Open Sans, sans-serif",
        )
        self.assertEqual(
            self.feature.preferences.unicode_character_icon_background, None
        )

    def test_proper_preferences_value_update_type_b(self):
        PREFERENCES: dict = {
            "search_result_list_size": "11",
            "search_result_view_type": "default",
            "unicode_character_icon_font": "Noto Serif, serif",
            "unicode_character_icon_background": "white",
        }

        self.feature.preferences.update(PREFERENCES)

        self.assertEqual(self.feature.preferences.search_result_list_size, 11)
        self.assertEqual(self.feature.preferences.search_result_view_type, "default")
        self.assertEqual(
            self.feature.preferences.unicode_character_icon_font,
            "Noto Serif, serif",
        )
        self.assertEqual(
            self.feature.preferences.unicode_character_icon_background, "white"
        )

    def test_get_unicode_character_from_letter(self):
        self.assertRaises(
            ValueError, self.feature.get_unicode_character_from_letter, "Hello"
        )

        self.assertEqual(
            "0041", self.feature.get_unicode_character_from_letter("A").code_point
        )
        self.assertEqual(
            "0042", self.feature.get_unicode_character_from_letter("B").code_point
        )


if __name__ == "__main__":
    unittest.main()
