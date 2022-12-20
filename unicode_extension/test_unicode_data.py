import unittest

import os
import sys
import logging

from .load_unicode_data import load_unicode_data
from .unicode_character import UnicodeCharacter

logger = logging.getLogger()
logger.level = logging.DEBUG

PROJECT_PATH = os.getcwd()

UNICODE_DATA_JSON_PATH = f"{PROJECT_PATH}/data/unicode_data.json"


class UnicodeDataJsonTest(unittest.TestCase):
    def test_unicode_data_json_is_exist(self):
        self.assertTrue(os.path.exists(UNICODE_DATA_JSON_PATH))

    def test_can_load_unicode_data(self):
        load_unicode_data()


class UnicodeDataVerificationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.UNICODE_CHARACTER_DICT: dict[str, UnicodeCharacter] = {}
        cls.UNICODE_CHARACTER_LIST: list[UnicodeCharacter] = []

        loaded_unicode_data = load_unicode_data()

        cls.UNICODE_CHARACTER_DICT = loaded_unicode_data["UNICODE_CHARACTER_DICT"]
        cls.UNICODE_CHARACTER_LIST = loaded_unicode_data["UNICODE_CHARACTER_LIST"]

    def get_unicode_character(self, code: str) -> UnicodeCharacter:
        """Get Unicode Character From UNICODE_CHARACTER_DICT

        Args:
            code_str: Example: `U+0041`

        Returns:
            UnicodeCharacter
        """

        character: UnicodeCharacter = self.UNICODE_CHARACTER_DICT[code]

        return character

    def get_unicode_character_name(self, code: str) -> str:
        """Get Unicode Character's Character Name.

        Args:
            code_str: Example: `U+0041`

        Returns:
            Example: `LATIN CAPITAL LETTER A`
        """

        character: UnicodeCharacter = self.get_unicode_character(code)
        name = character.name

        return name

    def get_unicode_character_block(self, code: str) -> str:
        """Get Unicode Character's Block.

        Args:
            code_str: Example: `U+0041`

        Returns:
            Example: `Basic Latin`
        """

        character: UnicodeCharacter = self.get_unicode_character(code)
        block = character.block

        return block

    def test_unicode_character_name_latin_capital(self):
        # Block

        # Latin Capital `A`, `B`, `Z`
        self.assertEqual(
            self.get_unicode_character_name("U+0041"), "LATIN CAPITAL LETTER A"
        )
        self.assertEqual(
            self.get_unicode_character_name("U+0042"), "LATIN CAPITAL LETTER B"
        )
        self.assertEqual(
            self.get_unicode_character_name("U+005A"), "LATIN CAPITAL LETTER Z"
        )

    def test_unicode_character_name_latin_small_letter(self):

        # Small letter `a`, `b`, `z`
        self.assertEqual(
            self.get_unicode_character_name("U+0061"), "LATIN SMALL LETTER A"
        )
        self.assertEqual(
            self.get_unicode_character_name("U+0062"), "LATIN SMALL LETTER B"
        )
        self.assertEqual(
            self.get_unicode_character_name("U+007A"), "LATIN SMALL LETTER Z"
        )

    def test_unicode_character_name_cjk_unified(self):

        # CJK Unified Ideograph `一`
        self.assertEqual(
            self.get_unicode_character_name("U+4E00"), "CJK UNIFIED IDEOGRAPH-4E00"
        )
        # CJK Unified Ideograph `漢`
        self.assertEqual(
            self.get_unicode_character_name("U+6F22"), "CJK UNIFIED IDEOGRAPH-6F22"
        )

    def test_unicode_character_name_hangul_syllable(self):

        # Hangul Syllable `가`, `나`, `힣`
        self.assertEqual(
            self.get_unicode_character_name("U+AC00"), "HANGUL SYLLABLE GA"
        )
        self.assertEqual(
            self.get_unicode_character_name("U+B098"), "HANGUL SYLLABLE NA"
        )
        self.assertEqual(
            self.get_unicode_character_name("U+D7A3"), "HANGUL SYLLABLE HIH"
        )

    def test_unicode_character_name_special_letter(self):

        # Special letter
        self.assertEqual(
            self.get_unicode_character_name("U+3008"), "LEFT ANGLE BRACKET"
        )
        self.assertEqual(
            self.get_unicode_character_name("U+300C"), "LEFT CORNER BRACKET"
        )

    def test_unicode_block(self):

        self.assertEqual(self.get_unicode_character_block("U+0000"), "Basic Latin")
        self.assertEqual(self.get_unicode_character_block("U+0041"), "Basic Latin")
        self.assertEqual(
            self.get_unicode_character_block("U+4E00"), "CJK Unified Ideographs"
        )
        self.assertEqual(self.get_unicode_character_block("U+AC00"), "Hangul Syllables")


if __name__ == "__main__":
    unittest.main()
