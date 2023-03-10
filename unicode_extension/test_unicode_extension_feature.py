import unittest

import os
import sys

from .load_unicode_data import load_unicode_data
from .unicode_character_icon import reset_unicode_character_icon_dir
from .unicode_character import UnicodeCharacter
from .unicode_extension_feature import UnicodeExtensionFeature
from .util import get_project_path

from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem


class UnicodeExtensionFeatureTest(unittest.TestCase):
    def setUp(self):
        reset_unicode_character_icon_dir()

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
        test("???", "CJK UNIFIED IDEOGRAPH-4E00", "U+4E00 CJK UNIFIED IDEOGRAPH-4E00")

        # U+3042 HIRAGANA LETTER A
        test("???", "HIRAGANA LETTER A", "U+3042 HIRAGANA LETTER A")

        # U+AC00 HANGUL SYLLABLE GA
        test("???", "HANGUL SYLLABLE GA", "U+AC00 HANGUL SYLLABLE GA")

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
            "??????",
            "U+4F60 U+597D",
            "???(U+4F60) ???(U+597D)",
        )

        # Japanese - Konnichiwa
        test(
            "???????????????",
            "U+3053 U+3093 U+306B U+3061 U+306F",
            "???(U+3053) ???(U+3093) ???(U+306B) ???(U+3061) ???(U+306F)",
        )

        # Korean - Annyeonghaseyo
        test(
            "???????????????",
            "U+C548 U+B155 U+D558 U+C138 U+C694",
            "???(U+C548) ???(U+B155) ???(U+D558) ???(U+C138) ???(U+C694)",
        )

    def test_generate_search_result_item_type_default(self):

        search_result = self.feature.generate_search_result("latin capital letter a")

        self.assertIsInstance(search_result[0], ExtensionResultItem)
        self.assertNotIsInstance(search_result[0], ExtensionSmallResultItem)

    def test_generate_search_result_item_type_small(self):
        self.feature.preferences.update_search_result_view_type("small")

        search_result = self.feature.generate_search_result("latin capital letter a")

        # `ExtensionSmallResultItem` is subclass of `ExtensionResultItem`
        self.assertIsInstance(search_result[0], ExtensionResultItem)
        self.assertIsInstance(search_result[0], ExtensionSmallResultItem)

    def test_generate_search_result_item_size(self):
        SIZE_A = 15

        self.feature.preferences.update_search_result_list_size(str(SIZE_A))
        search_result = self.feature.generate_search_result("latin")
        self.assertEqual(len(search_result), SIZE_A)

        SIZE_B = 5

        self.feature.preferences.update_search_result_list_size(str(SIZE_B))
        search_result = self.feature.generate_search_result("latin")
        self.assertEqual(len(search_result), SIZE_B)

    def test_generate_search_result(self):
        # TODO: improve

        search_result = self.feature.generate_search_result("latin capital letter a")

        self.assertEqual(search_result[0].get_name(), "LATIN CAPITAL LETTER A")

    def test_handle_keyword_query_event(self):
        # TODO: improve
        from ulauncher.api.shared.action.RenderResultListAction import (
            RenderResultListAction,
        )
        from ulauncher.api.shared.event import KeywordQueryEvent
        from ulauncher.search.Query import Query

        def create_keyword_query_event(query: str) -> KeywordQueryEvent:
            return KeywordQueryEvent(Query(query))

        def get_result_list_from_render_result_list_action(
            render_result_list_action: RenderResultListAction,
        ) -> list[ExtensionResultItem]:
            return render_result_list_action.result_list

        def simulate_query(query: str) -> list[ExtensionResultItem]:
            return get_result_list_from_render_result_list_action(
                self.feature.handle_keyword_query_event(
                    create_keyword_query_event(query)
                )
            )

        result = simulate_query("u latin capital letter a")

        self.assertEqual(result[1].get_name(), "LATIN CAPITAL LETTER A")


if __name__ == "__main__":
    unittest.main()
