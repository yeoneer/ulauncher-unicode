import unittest

import os
import sys

from .load_unicode_data import load_unicode_data
from .unicode_character import UnicodeCharacter
from .unicode_extension_feature import UnicodeExtensionFeature
from .util import get_project_path

from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem


class UnicodeExtensionFeatureTest(unittest.TestCase):
    def setUp(self):
        loaded_unicode_data = load_unicode_data()

        self.feature: UnicodeExtensionFeature = UnicodeExtensionFeature(
            project_path=get_project_path(),
            unicode_character_list=loaded_unicode_data["UNICODE_CHARACTER_LIST"],
            unicode_character_dict=loaded_unicode_data["UNICODE_CHARACTER_DICT"],
        )

    def get_copy_value_of_extension_result_item(
        self, extension_result_item: ExtensionResultItem
    ):
        value = extension_result_item._on_enter.text  # type: ignore

        return value

    def test_preferences_weird_value_update(self):
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

    def test_preferences_proper_value_update_type_a(self):
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

    def test_preferences_proper_value_update_type_b(self):
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

    def test_convert_one_letter_to_unicode_info(self):
        def test(letter: str, item_name: str, copy_value: str):
            extension_item = self.feature.convert_one_letter_to_unicode_info(letter)

            self.assertEqual(extension_item.get_name(), item_name)
            self.assertEqual(
                self.get_copy_value_of_extension_result_item(extension_item),
                copy_value,
            )

        # U+0041 LATIN CAPITAL LETTER A
        test("A", "LATIN CAPITAL LETTER A", "U+0041 LATIN CAPITAL LETTER A")

        # U+4E00 CJK UNIFIED IDEOGRAPH-4E00
        test("一", "CJK UNIFIED IDEOGRAPH-4E00", "U+4E00 CJK UNIFIED IDEOGRAPH-4E00")

        # U+3042 HIRAGANA LETTER A
        test("あ", "HIRAGANA LETTER A", "U+3042 HIRAGANA LETTER A")

        # U+AC00 HANGUL SYLLABLE GA
        test("가", "HANGUL SYLLABLE GA", "U+AC00 HANGUL SYLLABLE GA")

    def test_convert_all_letter_to_unicode_info(self):
        def test(content: str, item_name: str, copy_value: str):
            extension_item = self.feature.convert_all_letter_to_unicode_info(content)

            self.assertEqual(extension_item.get_name(), item_name)
            self.assertEqual(
                self.get_copy_value_of_extension_result_item(extension_item),
                copy_value,
            )

        # English - Hello
        test(
            "Hello",
            "U+0048 U+0065 U+006C U+006C U+006F",
            "H(U+0048) e(U+0065) l(U+006C) l(U+006C) o(U+006F)",
        )

        # Chinese - Nihao
        test(
            "你好",
            "U+4F60 U+597D",
            "你(U+4F60) 好(U+597D)",
        )

        # Japanese - Konnichiwa
        test(
            "こんにちは",
            "U+3053 U+3093 U+306B U+3061 U+306F",
            "こ(U+3053) ん(U+3093) に(U+306B) ち(U+3061) は(U+306F)",
        )

        # Korean - Annyeonghaseyo
        test(
            "안녕하세요",
            "U+C548 U+B155 U+D558 U+C138 U+C694",
            "안(U+C548) 녕(U+B155) 하(U+D558) 세(U+C138) 요(U+C694)",
        )


if __name__ == "__main__":
    unittest.main()
