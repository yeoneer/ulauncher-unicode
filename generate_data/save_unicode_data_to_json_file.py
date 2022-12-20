import os
import sys
import json

from process_ucd_xml_file import process_ucd_xml_file
from process_ucd_xml_file import UnicodeCharacter, UnicodeBlock


def save_unicode_data_to_json_file(
    unicode_data_list: list[UnicodeCharacter],
    output_json_file_path: str,
    output_json_indent: int | None,
):
    """Save Unicode data to JSON file

    Args:
        unicode_data_dictionary: Process result of `process_unicode_xml`.
        output_json_file_path: Output JSON file path.
        output_json_indent: Output JSON file indent. `2` for prettier, `None` for compress
    """

    def custom_json_serializer(data):
        if isinstance(data, UnicodeCharacter):
            unicode_character_data: UnicodeCharacter = data  # for IntelliSense

            if len(unicode_character_data.aliases) > 0:
                return {
                    "cp": unicode_character_data.code_point,
                    "na": unicode_character_data.name,
                    "blk": unicode_character_data.block,
                    "als": unicode_character_data.aliases,
                }
            else:
                return {
                    "cp": unicode_character_data.code_point,
                    "na": unicode_character_data.name,
                    "blk": unicode_character_data.block,
                }
        else:
            return data.__dict__

    print(
        f"save_unicode_data_to_json_file - Save Unicode data to `{output_json_file_path}`"
    )
    with open(output_json_file_path, "w") as file:
        json.dump(
            unicode_data_list,
            file,
            indent=output_json_indent,
            default=custom_json_serializer,
        )


if __name__ == "__main__":

    ORIGINAL_UCD_ALL_FLAT_XML_PATH = "original_data/ucd.all.flat.xml"
    OUTPUT_DIR = "data"
    OUTPUT_JSON_FILE_PATH = f"{OUTPUT_DIR}/unicode_data.json"

    if not os.path.exists(ORIGINAL_UCD_ALL_FLAT_XML_PATH):
        raise FileNotFoundError(f"`{ORIGINAL_UCD_ALL_FLAT_XML_PATH}` not exist.")

    # Process Full Unicode Characters
    process_result = process_ucd_xml_file(ORIGINAL_UCD_ALL_FLAT_XML_PATH)

    UNICODE_CHARACTER_DICT: dict[str, UnicodeCharacter] = process_result[
        "UNICODE_CHARACTER_DICT"
    ]
    UNICODE_CHARACTER_LIST: list[UnicodeCharacter] = list(
        UNICODE_CHARACTER_DICT.values()
    )
    ALL_CHARACTERS_PROCESSED: bool = process_result["ALL_CHARACTERS_PROCESSED"]

    if not os.path.isdir(OUTPUT_DIR):
        print(f"`{OUTPUT_DIR}` directory is not exist. Create Directory.")
        os.mkdir(OUTPUT_DIR)

    save_unicode_data_to_json_file(
        unicode_data_list=UNICODE_CHARACTER_LIST,
        output_json_file_path=OUTPUT_JSON_FILE_PATH,
        output_json_indent=2,
    )
