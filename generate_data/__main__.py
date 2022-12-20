import os

from get_original_ucd_xml_file import (
    download_original_ucd_xml_zip_file,
    unzip_to_ucd_xml_file,
)
from process_ucd_xml_file import process_ucd_xml_file
from assert_characters_for_test import assert_characters_for_test
from save_unicode_data_to_json_file import save_unicode_data_to_json_file

from process_ucd_xml_file import UnicodeBlock, UnicodeCharacter


def main():
    """Generate Data (unicode_data.json for UnicodeExtension)"""

    ORIGINAL_DATA_DIR = "original_data"

    ORIGINAL_UCD_ZIP_FILENAME = "ucd.all.flat.zip"
    ORIGINAL_UCD_ZIP_PATH = f"{ORIGINAL_DATA_DIR}/{ORIGINAL_UCD_ZIP_FILENAME}"

    ORIGINAL_UCD_ALL_FLAT_XML_FILENAME = "ucd.all.flat.xml"
    ORIGINAL_UCD_ALL_FLAT_XML_PATH = (
        f"{ORIGINAL_DATA_DIR}/{ORIGINAL_UCD_ALL_FLAT_XML_FILENAME}"
    )

    OUTPUT_DIR = "data"

    OUTPUT_JSON_FILENAME = "unicode_data.json"
    OUTPUT_JSON_FILE_PATH = f"{OUTPUT_DIR}/{OUTPUT_JSON_FILENAME}"

    if not os.path.isdir(ORIGINAL_DATA_DIR):
        print(
            f"generate_data - `{ORIGINAL_DATA_DIR}` directory is not exist. Create Directory."
        )
        os.mkdir(ORIGINAL_DATA_DIR)

    download_original_ucd_xml_zip_file(save_file_path=ORIGINAL_UCD_ZIP_PATH)

    unzip_to_ucd_xml_file(
        original_zip_file_path=ORIGINAL_UCD_ZIP_PATH,
        save_xml_file_dir_path=ORIGINAL_DATA_DIR,
    )

    if not os.path.exists(ORIGINAL_UCD_ALL_FLAT_XML_PATH):
        raise FileNotFoundError(
            f"`{ORIGINAL_UCD_ALL_FLAT_XML_FILENAME}` not exist. Something is wrong"
        )

    def process_and_save():
        process_result = process_ucd_xml_file(ORIGINAL_UCD_ALL_FLAT_XML_PATH)

        UNICODE_BLOCK_ARRAY: list[UnicodeBlock] = process_result["UNICODE_BLOCK_ARRAY"]
        UNICODE_CHARACTER_DICT: dict[str, UnicodeCharacter] = process_result[
            "UNICODE_CHARACTER_DICT"
        ]
        UNICODE_CHARACTER_LIST: list[UnicodeCharacter] = list(
            UNICODE_CHARACTER_DICT.values()
        )
        ALL_CHARACTERS_PROCESSED: bool = process_result["ALL_CHARACTERS_PROCESSED"]

        if not ALL_CHARACTERS_PROCESSED:
            print("generate_data - ALL_CHARACTERS_PROCESSED is False. Stop Process.")
            return

        print("")
        print("generate_data - ALL Characters Processed. Run Assertion Test.")
        assert_characters_for_test(UNICODE_CHARACTER_DICT)
        print("generate_data - Assertion Test Complete.")
        print("")

        if not os.path.isdir(OUTPUT_DIR):
            print(f"`{OUTPUT_DIR}` directory is not exist. Create Directory.")
            os.mkdir(OUTPUT_DIR)

        save_unicode_data_to_json_file(
            unicode_data_list=UNICODE_CHARACTER_LIST,
            output_json_file_path=OUTPUT_JSON_FILE_PATH,
            output_json_indent=None,
        )

        print(f"")
        print(f"")
        print(f"==============")
        print(f"Process Result")
        print(f"==============")
        print(f"")
        print(f"Unicode Blocks")
        print(f"==============")
        print(f"Block Number: {len(UNICODE_BLOCK_ARRAY):,}")
        print(f"First Block : {UNICODE_BLOCK_ARRAY[0]}")
        print(f"Last  Block : {UNICODE_BLOCK_ARRAY[-1]}")
        print(f"")
        print(f"Unicode Characters")
        print(f"==================")
        print(
            f"Character Number: {len(UNICODE_CHARACTER_LIST):,} ({hex(len(UNICODE_CHARACTER_LIST))})"
        )
        print(f"First Character : {UNICODE_CHARACTER_LIST[0]}")
        print(f"Last  Character : {UNICODE_CHARACTER_LIST[-1]}")
        print(f"")

    while True:
        print("")
        print("Ready to process original Unicode XML file.")
        print("")

        user_input = input("Process Unicode XML file [y: default/n]: ")

        if user_input.lower() == "y" or user_input.lower() == "":
            process_and_save()
            return
        elif user_input.lower() == "n":
            return
        else:
            continue


if __name__ == "__main__":
    main()
