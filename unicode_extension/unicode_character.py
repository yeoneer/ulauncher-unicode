class UnicodeCharacter:
    """
    UnicodeCharacter

    Attributes:
        code_point (str): Code point with only number string.
            Example: `"0041"`
        u_code_point (str): Code point starts with 'U+'
            Example: `"U+0041"`
        name (str): Character name
            Example: `"LATIN CAPITAL LETTER A"`
        block (str): Unicode Block of character
            Example: `"Basic Latin"`
        aliases (list[str]): Aliases of Character
            Most of characters has empty aliases

            U+000A aliases: `["END OF LINE", "EOL", "LF", "LINE FEED", "NEW LINE", "NL"]`
            U+0041 aliases: `[]`
        character (str): Real character
            Example: `"A"`
    """

    code_point: str
    u_code_point: str
    name: str
    block: str
    aliases: list[str]
    character: str

    def __init__(self, code_point: str, name: str, block: str, aliases: list[str]):

        if not (isinstance(code_point, str) and (code_point != "")):
            raise ValueError(
                f"UnicodeCharacter init - `code_point` value error. Should be `XXXX` (Hex number string). Current `code_point`: `{code_point}`"
            )
        if not (isinstance(name, str) and (name != "")):
            raise ValueError(
                f"UnicodeCharacter init - `name` value error. Current `name`: `{name}`"
            )
        if not (isinstance(block, str) and (block != "")):
            raise ValueError(
                f"UnicodeCharacter init - `block` value error. Current `block`: `{block}`"
            )
        if not isinstance(aliases, list):
            raise ValueError(
                f"UnicodeCharacter init - `aliases` value error. Current `aliases`: `{aliases}`"
            )

        self.code_point = code_point
        self.u_code_point = f"U+{code_point}"
        self.name = name
        self.block = block
        self.aliases = aliases
        self.character = chr(int(code_point, base=16))

        self._string_data_for_search = self.__convert_for_search()

    def __str__(self):
        return f"{self.u_code_point} - '{self.name}' ({self.block})"

    def __repr__(self):
        return str(self)

    # Preprocess for `search_unicode_character`
    def __convert_for_search(self):
        string_list: list[str] = []

        string_list.append(self.u_code_point)

        string_list.append(self.name)

        string_list.extend(self.aliases)

        # When block information is added, the quality of search results significantly decreases.
        #
        # string_list.append(self.block)

        def remove_duplicate_in_list(original_list: list) -> list:
            new_list: list = []

            for item in original_list:
                if item not in new_list:
                    new_list.append(item)

            return new_list

        result = " ".join(remove_duplicate_in_list(string_list)).upper()

        return result
