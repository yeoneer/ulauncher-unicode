from process_ucd_xml_file import UnicodeCharacter


def assert_characters_for_test(UNICODE_CHARACTER_DICT: dict[str, UnicodeCharacter]):
    def assert_character_name(code_point: str, expect: str):
        unicode_character = UNICODE_CHARACTER_DICT[code_point]
        assert (
            unicode_character.name == expect
        ), f"Character Name AssertionError: U+{code_point} - Real Character Name: '{unicode_character.name}', Expect: '{expect}'"

    def assert_character_block(code_point: str, expect: str):
        unicode_character = UNICODE_CHARACTER_DICT[code_point]
        assert (
            unicode_character.block == expect
        ), f"Character Block AssertionError: U+{code_point} - Real Block Name: '{unicode_character.block}', Expect: '{expect}'"

    def assert_character_alias(code_point: str, expect: str):
        unicode_character = UNICODE_CHARACTER_DICT[code_point]
        assert (
            expect in unicode_character.aliases
        ), f"Character Alias AssertionError: U+{code_point} - '{expect}' is not in {unicode_character.aliases}. Real Aliases: {unicode_character.aliases}, Expect: '{expect}'."

    # Assert Character Name
    # Assert Character Name - 'Basic Latin'
    assert_character_name("0000", "NULL")
    assert_character_name("000A", "LINE FEED (LF)")
    assert_character_name("0041", "LATIN CAPITAL LETTER A")
    # Assert Character Name - 'General Punctuation'
    assert_character_name("2014", "EM DASH")

    # Assert Character Name - 'CJK UNIFIED IDEOGRAPHS'
    assert_character_name("4E00", "CJK UNIFIED IDEOGRAPH-4E00")
    assert_character_name("6F22", "CJK UNIFIED IDEOGRAPH-6F22")

    # Assert Character Name - 'HANGUL SYLLABLES'
    assert_character_name("AC00", "HANGUL SYLLABLE GA")
    assert_character_name("B098", "HANGUL SYLLABLE NA")
    assert_character_name("D7A3", "HANGUL SYLLABLE HIH")

    # Assert Block
    assert_character_block("0000", "Basic Latin")
    assert_character_block("2014", "General Punctuation")
    assert_character_block("4E00", "CJK Unified Ideographs")
    assert_character_block("AC00", "Hangul Syllables")

    # Assert Alias
    # Assert Alias - U+0000
    assert_character_alias("0000", "NULL")
    # Assert Alias - U+000A
    assert_character_alias("000A", "END OF LINE")
    assert_character_alias("000A", "EOL")
    assert_character_alias("000A", "LF")
    assert_character_alias("000A", "LINE FEED")
    assert_character_alias("000A", "NEW LINE")
    assert_character_alias("000A", "NL")

    # Special Case
    #
    # See also:
    # - [UTN #27: Known anomalies in Unicode Character Names](https://unicode.org/notes/tn27/)
    # - [Unicode - Wikipedia](https://en.wikipedia.org/wiki/Unicode#Anomalies)

    # U+FE18 - Misspelling of "BRACKET" in Character Name, and mitigate in name alias
    assert_character_name(
        "FE18", "PRESENTATION FORM FOR VERTICAL RIGHT WHITE LENTICULAR BRAKCET"
    )
    assert_character_alias(
        "FE18", "PRESENTATION FORM FOR VERTICAL RIGHT WHITE LENTICULAR BRACKET"
    )
