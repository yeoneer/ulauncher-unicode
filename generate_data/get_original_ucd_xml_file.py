import os
import sys

import zipfile
import urllib.request

# Reference: [Unicode Character Database](https://www.unicode.org/ucd/)

# [Unicode 15.0.0](https://www.unicode.org/versions/Unicode15.0.0/) (Released on 2022-09-13)

UNICODE_CHARACTER_DATABASE_URL = "https://www.unicode.org/Public"
UNICODE_VERSION = "15.0.0"
UCD_ALL_FLAT_ZIP_PATH = "ucdxml/ucd.all.flat.zip"

# URL Example: `https://www.unicode.org/Public/15.0.0/ucdxml/ucd.all.flat.zip`


def download_original_ucd_xml_zip_file(
    save_file_path: str = "original_data/ucd.all.flat.zip",
):
    """Download Original `ucd.all.flat.zip` file from unicode.org

    Args:

        save_file_path (str): e.g.,: `original_data/ucd.all.flat.zip`
    """

    if os.path.exists(save_file_path):
        print(
            f"download_original_ucd_xml_zip_file - Download skipped. `{save_file_path}` file is already exist."
        )
        return

    url = f"{UNICODE_CHARACTER_DATABASE_URL}/{UNICODE_VERSION}/{UCD_ALL_FLAT_ZIP_PATH}"
    req = urllib.request.urlopen(url)

    content = req.read()

    print(
        f"download_original_ucd_xml_zip_file - Download Complete. Save to `{save_file_path}`"
    )
    open(save_file_path, "wb").write(content)


def unzip_to_ucd_xml_file(
    original_zip_file_path: str = "original_data/ucd.all.flat.zip",
    save_xml_file_dir_path: str = "original_data",
):
    """Unzip `ucd.all.flat.zip` zip file to `ucd.all.flat.xml` file.

    Args:

        original_zip_file_path: `original_data/ucd.all.flat.zip`
        save_xml_file_dir_path: `original_data/`
    """

    if not os.path.exists(original_zip_file_path):
        print(
            f"unzip_to_ucd_xml_file - Unzip skipped. `{original_zip_file_path}` file does not exist."
        )
        return

    if os.path.exists(f"{save_xml_file_dir_path}/ucd.all.flat.xml"):
        print(
            f"unzip_to_ucd_xml_file - Unzip skipped. `{save_xml_file_dir_path}/ucd.all.flat.xml` file already exist."
        )
        return

    with zipfile.ZipFile(original_zip_file_path, "r") as zipfile_object:
        RESULT_FILENAME = "ucd.all.flat.xml"
        result_file_path = f"{save_xml_file_dir_path}/{RESULT_FILENAME}"
        print(
            f"unzip_to_ucd_xml_file - Extract `{original_zip_file_path}` zip to `{result_file_path}`"
        )
        zipfile_object.extract(RESULT_FILENAME, save_xml_file_dir_path)


if __name__ == "__main__":
    DIR_PATH = "original_data"
    FILE_NAME_WITH_EXT = "ucd.all.flat.zip"

    FILE_PATH = f"{DIR_PATH}/{FILE_NAME_WITH_EXT}"

    if not os.path.isdir(DIR_PATH):
        print(f"`{DIR_PATH}` directory is not exist. Create Directory.")
        os.mkdir(DIR_PATH)

    download_original_ucd_xml_zip_file(save_file_path=FILE_PATH)

    ORIGINAL_ZIP_FILE_PATH = "original_data/ucd.all.flat.zip"
    SAVE_XML_FILE_DIR_PATH = "original_data"

    print("unzip")
    unzip_to_ucd_xml_file(
        original_zip_file_path=ORIGINAL_ZIP_FILE_PATH,
        save_xml_file_dir_path=SAVE_XML_FILE_DIR_PATH,
    )
