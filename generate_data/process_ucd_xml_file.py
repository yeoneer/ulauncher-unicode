import xml.etree.ElementTree
from xml.etree.ElementTree import Element


class UnicodeBlock:
    def __init__(self, first_cp: str, last_cp: str, name: str):

        if type(first_cp) is int:
            raise TypeError
        if type(last_cp) is int:
            raise TypeError

        self.first_code_point: int = int(first_cp, base=16)
        self.last_code_point: int = int(last_cp, base=16)
        self.name = name

    def __str__(self):
        return (
            f"U+{self.first_code_point:X}..U+{self.last_code_point:X}"
            + " - "
            + f"{self.name} (CP: {self.last_code_point - self.first_code_point})"
        )


class UnicodeCharacter:
    def __init__(self, code_point: str, name: str, block: str, aliases: list[str]):
        """`code_point`, `block` is str, because it's more convenience."""

        if type(code_point) is int:
            raise TypeError("UnicodeCharacter - `code_point` should be string. not int")
        if type(block) is UnicodeBlock:
            raise TypeError(
                "UnicodeCharacter - `block` should be string. not UnicodeBlock"
            )

        self.code_point = code_point
        self.name = name
        self.block = block
        self.aliases = aliases

    def __str__(self):
        return f"U+{self.code_point} - '{self.name}' ({self.block})"


def get_character_block(
    UNICODE_BLOCK_ARRAY: list[UnicodeBlock], character_code: int
) -> UnicodeBlock:
    filtered_block_list = list(
        filter(
            lambda block: (
                (block.first_code_point <= character_code)
                and (block.last_code_point >= character_code)
            ),
            UNICODE_BLOCK_ARRAY,
        )
    )

    block_of_character = filtered_block_list[0]

    return block_of_character


def get_character_name(character_element: Element) -> str:
    """Get Unicode Character's Character Name.

    Args:
        character_element: XMLElement(`char`) of `ucd.all.flat.xml` file

    Returns:
        Unicode Character's Character Name

        Example:

        - `LATIN CAPITAL LETTER A` (U+0041)
        - `CJK UNIFIED IDEOGRAPH-4E00` (U+4E00)
    """

    def get_character_name_from_element(character_element: Element) -> str:
        # Main Character Name Candidate.
        #
        # 'Character Name' of Unicode Character can be found in below way:
        #
        # - 'na' attribute
        # - 'na1' attribute (for Unicode 1.0 characters, other characters 'na' attribute is '', not every Unicode 1.0 characters have this attribute, and sometimes duplicate with other name)

        character_attrib_code_point: str = character_element.attrib["cp"]

        character_attrib_name: str = character_element.attrib["na"]

        if character_attrib_name != "":
            return character_attrib_name

        character_attrib_age: str = character_element.attrib["age"]
        character_attrib_name_of_unicode_v1: str = character_element.attrib["na1"]

        if (
            character_attrib_age.startswith("1")
            and character_attrib_name_of_unicode_v1 != ""
        ):
            return character_attrib_name_of_unicode_v1

        # Character that has name in `figment` type `name-alias`
        #
        # E.g., `<name-alias alias="PADDING CHARACTER" type="figment"/>`
        def handle_special_case(code: str) -> str | None:
            match code:
                case "U+0080":
                    return "PADDING CHARACTER"
                case "U+0081":
                    return "HIGH OCTET PRESET"
                case "U+0084":
                    return "INDEX"
                case "U+0099":
                    return "SINGLE GRAPHIC CHARACTER INTRODUCER"
                case _:
                    return None

        special_case_result = handle_special_case(f"U+{character_attrib_code_point}")

        if special_case_result is not None:
            return special_case_result

        raise RuntimeError(
            "Unhandled Character's Character Name",
            f"U+{character_attrib_code_point}",
        )

    def replace_number_sign_with_code_point(
        character_name: str, code_point: str
    ) -> str:
        """Replace NUMBER SIGN with code point.

        Q: Why this is needed?
        A: [UAX #42: Unicode Character Database in XML - 4.4.2 Name Properties](https://www.unicode.org/reports/tr42/#d1e2784)

        Args:
            character_name: Character Name. (e.g., 'CJK UNIFIED IDEOGRAPH-#')
            code_point: Code point. (e.g., '4E00')

        Returns:
            Replaced String (e.g., `CJK UNIFIED IDEOGRAPH-4E00`)
        """

        # Starting with below character name
        # is look like `CJK UNIFIED IDEOGRAPH-#`:
        # (number in parentheses is number of character)
        #
        # - `CJK UNIFIED IDEOGRAPH` (97046)
        # - `CJK COMPATIBILITY IDEOGRAPH` (1014)
        # - `TANGUT IDEOGRAPH` (6145)
        # - `KHITAN SMALL SCRIPT CHARACTER` (470)
        # - `NUSHU CHARACTER` (396)
        #
        # Specific code Example(U+6F22):
        # `char cp="6F22" age="1.1" na="CJK UNIFIED IDEOGRAPH-#" ...`

        if "#" in character_name:
            return character_name.replace("#", code_point)

        return character_name

    character_name = get_character_name_from_element(character_element)

    character_name = replace_number_sign_with_code_point(
        character_name, character_element.attrib["cp"]
    )

    return character_name


def get_character_aliases(character_element: Element) -> list[str]:
    """Get Unicode Character's Character Alias.

    Args:
        character_element: XMLElement(`char`) of `ucd.all.flat.xml` file

    Returns:
        Unicode Character's Aliases

        Example:

        - U+000A (LINE FEED (LF): [`END OF LINE`, `EOL`, `LF`, `LINE FEED`, `NEW LINE`, `NL`]
        - U+0041 (LATIN CAPITAL LETTER A): []
    """

    alias_list: list[str] = []

    for child_element in character_element:
        if "name-alias" in child_element.tag:
            alias: str = child_element.attrib["alias"]

            alias_list.append(alias)

    def remove_duplicate_in_list(original_list: list) -> list:
        new_list: list = []

        for item in original_list:
            if item not in new_list:
                new_list.append(item)

        return new_list

    alias_list = remove_duplicate_in_list(alias_list)

    return alias_list


def process_ucd_xml_file(unicode_xml_file_path: str) -> dict:
    """Process original Unicode XML file (`ucd.all.flat.xml`)

    Args:
        unicode_xml_file_path: E.g., `original_data/ucd.all.flat.xml`

    Returns:
    {
        "UNICODE_BLOCK_ARRAY": list[UnicodeBlock]
        "UNICODE_CHARACTER_DICT": dict[str, UnicodeCharacter]
        "ALL_CHARACTERS_PROCESSED": bool
    }
    """
    unicode_xml_tree = xml.etree.ElementTree.parse(unicode_xml_file_path)
    unicode_xml_root = unicode_xml_tree.getroot()

    XML_UNICODE_REPERTOIRE = unicode_xml_root[1]
    XML_UNICODE_BLOCKS = unicode_xml_root[2]

    block_array: list[UnicodeBlock] = []

    print(f"Processing Unicode Blocks")

    mark_for_all_processed_without_break: bool = True

    for block_item in XML_UNICODE_BLOCKS:
        # Block Example (Basic Latin):
        # `<block first-cp="0000" last-cp="007F" name="Basic Latin"/>`

        block_first_cp: str = block_item.attrib["first-cp"]
        block_last_cp: str = block_item.attrib["last-cp"]
        block_name: str = block_item.attrib["name"]

        block = UnicodeBlock(block_first_cp, block_last_cp, block_name)

        block_array.append(block)

        # Print Block Processing process
        print(f"Block Processing: {block}")

    # Already sorted in XML file, but for verification
    block_array.sort(key=lambda block: block.first_code_point)

    UNICODE_BLOCK_ARRAY: list[UnicodeBlock] = block_array

    print(f"Number of Blocks: {len(UNICODE_BLOCK_ARRAY)}")

    def condition_for_break(code: int) -> bool:
        # For Small Test
        # if code > 32:
        #     return True
        return False

    print(f"Processing Unicode Characters")

    unicode_character_dict: dict[str, UnicodeCharacter] = {}

    for character_element in XML_UNICODE_REPERTOIRE:

        # Unicode XML
        #
        # `repertoire`
        # - char (most of it)
        # - noncharacter
        # - reserved

        # `tag` string startswith xml namespace
        if character_element.tag != "{http://www.unicode.org/ns/2003/ucd/1.0}char":
            continue

        try:
            character_code_point: str = character_element.attrib["cp"]
            character_code_point_in_num: int = int(character_code_point, base=16)

            if condition_for_break(character_code_point_in_num) == True:
                mark_for_all_processed_without_break = False
                break

            character_name: str = get_character_name(character_element)

            character_block = get_character_block(
                UNICODE_BLOCK_ARRAY, character_code_point_in_num
            )

            character_alias_list: list[str] = get_character_aliases(character_element)

            unicode_character: UnicodeCharacter = UnicodeCharacter(
                character_code_point,
                character_name,
                character_block.name,
                character_alias_list,
            )

            unicode_character_dict[f"{character_code_point}"] = unicode_character

            # Print Character Processing process
            print(f"Character Processing: {unicode_character}")
        except KeyError:
            # print(character_item.tag, character_item.attrib)
            if "PUA" in character_element.attrib["blk"]:
                continue
            else:
                raise KeyError

    print(f"")
    print(f"Processing Unicode characters complete")

    result = {
        "UNICODE_BLOCK_ARRAY": UNICODE_BLOCK_ARRAY,
        "UNICODE_CHARACTER_DICT": unicode_character_dict,
        "ALL_CHARACTERS_PROCESSED": mark_for_all_processed_without_break,
    }

    return result


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
    assert_character_alias("0000", "U+0000")
    assert_character_alias("0000", "NULL")
    # Assert Alias - U+000A
    assert_character_alias("000A", "U+000A")
    assert_character_alias("000A", "LINE FEED (LF)")
    assert_character_alias("000A", "END OF LINE")
    assert_character_alias("000A", "EOL")
    assert_character_alias("000A", "LF")
    assert_character_alias("000A", "LINE FEED")
    assert_character_alias("000A", "NEW LINE")
    assert_character_alias("000A", "NL")
    # Assert Alias - U+0041
    assert_character_alias("0041", "U+0041")
    assert_character_alias("0041", "LATIN CAPITAL LETTER A")
    # Assert Alias - U+00B7
    assert_character_alias("00B7", "U+00B7")
    assert_character_alias("00B7", "MIDDLE DOT")

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


if __name__ == "__main__":
    # Process Full Unicode Characters
    process_result = process_ucd_xml_file("original_data/ucd.all.flat.xml")

    UNICODE_BLOCK_ARRAY: list[UnicodeBlock] = process_result["UNICODE_BLOCK_ARRAY"]
    UNICODE_CHARACTER_DICT: dict[str, UnicodeCharacter] = process_result[
        "UNICODE_CHARACTER_DICT"
    ]
    UNICODE_CHARACTER_LIST: list[UnicodeCharacter] = list(
        UNICODE_CHARACTER_DICT.values()
    )
    ALL_CHARACTERS_PROCESSED: bool = process_result["ALL_CHARACTERS_PROCESSED"]

    print(f"")
    print(f"")
    print(f"Process Result")
    print(f"======")
    print(f"")
    print(f"Unicode Blocks:")
    print(f"===")
    print(f"Block Number : {len(UNICODE_BLOCK_ARRAY)}")
    print(f"First Block: {UNICODE_BLOCK_ARRAY[0]}")
    print(f"Last  Block: {UNICODE_BLOCK_ARRAY[-1]}")
    print(f"")
    print(f"Unicode Characters:")
    print(f"===")
    print(
        f"Character Number : {len(UNICODE_CHARACTER_LIST):,} ({hex(len(UNICODE_CHARACTER_LIST))})"
    )
    print(f"First Character: {UNICODE_CHARACTER_LIST[0]}")
    print(f"Last  Character: {UNICODE_CHARACTER_LIST[-1]}")
    print(f"")

    if ALL_CHARACTERS_PROCESSED:
        print("All characters processed. Run assertion test.")
        print("")

        assert_characters_for_test(UNICODE_CHARACTER_DICT)

        print("Assertion Unicode Characters Data Success")
        print("")

    else:
        print("All characters not processed. Assertion test skipped.")
        print("")

    # Check for all characters have Character Name. (not empty)
    for character in UNICODE_CHARACTER_LIST:
        if character.name == "":
            print(f"Warning: U+{character.code_point} - Character Name is Empty")
            raise ValueError(
                f"U+{character.code_point} - Character Name is Empty", character
            )
