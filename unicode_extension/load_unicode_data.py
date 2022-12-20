import json
from .unicode_character import UnicodeCharacter
from .util import get_project_path


PROJECT_PATH = get_project_path()


def load_unicode_data() -> dict:
    """Load Unicode Data (`unicode_data.json`)

    Returns:

        {
            UNICODE_CHARACTER_LIST: list[UnicodeCharacter],
            UNICODE_CHARACTER_DICT: dict[str, UnicodeCharacter],
        }

    """

    UNICODE_DATA_JSON_PATH = f"{PROJECT_PATH}/data/unicode_data.json"

    unicode_character_list: list[UnicodeCharacter] = []
    unicode_character_dict: dict[str, UnicodeCharacter] = {}

    with open(UNICODE_DATA_JSON_PATH) as json_file:
        unicode_data_json: list = json.load(json_file)

        for character_data in unicode_data_json:
            character_data: dict = character_data  # for IntelliSense

            code_point: str = character_data["cp"]
            name: str = character_data["na"]
            block: str = character_data["blk"]
            aliases: list[str] = []

            # `als` is optional in data file.
            if "als" in character_data.keys():
                aliases = character_data["als"]

            unicode_character = UnicodeCharacter(
                code_point=code_point, name=name, block=block, aliases=aliases
            )

            unicode_character_list.append(unicode_character)
            unicode_character_dict[unicode_character.u_code_point] = unicode_character

    result = {
        "UNICODE_CHARACTER_LIST": unicode_character_list,
        "UNICODE_CHARACTER_DICT": unicode_character_dict,
    }

    return result


if __name__ == "__main__":
    load_unicode_data()
