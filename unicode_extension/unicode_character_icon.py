import os
import shutil

from .unicode_character import UnicodeCharacter
from .util import get_project_path


PROJECT_PATH = get_project_path()
UNICODE_CHARACTER_ICON_DIR = ".unicode_character_icon"
UNICODE_CHARACTER_ICON_DIR_PATH = f"{PROJECT_PATH}/{UNICODE_CHARACTER_ICON_DIR}"

# Associated code with generate Unicode Character Icon is come from
# [GitHub - zensoup/ulauncher-unicode](https://github.com/zensoup/ulauncher-unicode) (GPL-3.0 license)
#
# More Detail: [ulauncher-unicode/main.py at master · zensoup/ulauncher-unicode · GitHub](https://github.com/zensoup/ulauncher-unicode/blob/master/main.py)
#
# Most of code is modified, but not all

ICON_WITHOUT_BACKGROUND_TEMPLATE = """
<svg  width="100" height="100">
    <text x="50" y="50" dy=".35em" text-anchor="middle" dominant-baseline="middle" font-family="{font}" font-size="80">{symbol}</text>
</svg>
"""

ICON_WITH_WHITE_BACKGROUND_TEMPLATE = """
<svg  width="100" height="100">
    <rect x="0" y="0" rx="10" ry="10" width="100" height="100" style="fill:rgb(255,255,255)" />
    <text x="50" y="50" dy=".35em" text-anchor="middle" dominant-baseline="middle" font-family="{font}" font-size="80">{symbol}</text>
</svg>
"""


def generate_unicode_character_icon(
    unicode_character: UnicodeCharacter,
    background: None | str = None,
    font: str = "sans-serif",
):
    """Get Unicode Character Icon

    Warning: Create File.
    The general use of this extension involves the creation of **many** files.

    This problem might be resolved if Ulauncher produce an API that allows icons to be
    loaded without actual image files (such as generated image data).
    """

    character_icon_file_path = f"{UNICODE_CHARACTER_ICON_DIR_PATH}/u_{unicode_character.code_point.lower()}.svg"

    # 1. Font preference(`unicode_character_icon_font`) changes are not affected
    #    properly until Ulauncher is restarted.
    # 2. When Ulauncher is restarted, in other words, when this extension is restarted,
    #    all existed icon file wll be removed. (`reset_unicode_character_icon_dir`)
    #
    # So it makes sense not to create a new file every time.
    #
    # If font preference changes are affected immediately, it should be create file in
    # every time, but it isn't. (maybe the reason is GTK pixbuf loader cache)
    if os.path.isfile(character_icon_file_path):
        return character_icon_file_path

    icon_content = None

    if background is None:
        icon_content = ICON_WITHOUT_BACKGROUND_TEMPLATE.replace(
            "{symbol}", unicode_character.character
        ).replace("{font}", font)
    elif background == "white":
        icon_content = ICON_WITH_WHITE_BACKGROUND_TEMPLATE.replace(
            "{symbol}", unicode_character.character
        ).replace("{font}", font)

    if icon_content is None:
        raise ValueError(
            f"Unknown background value. current background value: `{background}`"
        )

    def create_icon_file(icon_file_path: str, content: str):
        icon_file = open(icon_file_path, "w")
        icon_file.write(content)
        icon_file.close()

    try:
        create_icon_file(character_icon_file_path, icon_content)
    except FileNotFoundError:
        prepare_unicode_character_icon_dir()
        create_icon_file(character_icon_file_path, icon_content)

    return character_icon_file_path


# This(`generate_unicode_character_icon_without_file`) is not work.
#
# Ulauncher API is require real file's path(str) to icon of ExtensionResultItem.
# There is no way to display icon image to Ulauncher Result List without real file.
# String image path is the only way to display icon in User Extension.
#
# The method of creating data and passing only data such as GTK Image instances,
# PixBuf(This is the way Ulauncher internally uses to display icon image), bytes, etc.
# without creating actual files cannot be used to display the ExtensionResultItem icon
# in User Extension.
#
# Ulauncher v5.15.0(latest release), v6(latest dev) both are same. (tested in 2022-12-18)

# def generate_unicode_character_icon_without_file(
#     unicode_character: UnicodeCharacter,
#     background: None | str = None,
#     font: str = "sans-serif",
# ):
#     from gi.repository import Gtk, GLib, GdkPixbuf
#
#     icon_content = ICON_WITHOUT_BACKGROUND_TEMPLATE.replace(
#         "{symbol}", unicode_character.character
#     ).replace("{font}", font)
#
#     def create_icon_data(content: str):
#         loader = GdkPixbuf.PixbufLoader()
#         loader.write(content.encode())
#         loader.close()
#
#         pixbuf = loader.get_pixbuf()  # Pixbuf
#         image = Gtk.Image.new_from_pixbuf(pixbuf)  # GTK Image
#         pixels = pixbuf.get_pixels()  # bytes
#
#         return pixbuf
#
#     data = create_icon_data(icon_content)
#
#     return data


def prepare_unicode_character_icon_dir():
    if not os.path.isdir(UNICODE_CHARACTER_ICON_DIR_PATH):
        os.mkdir(UNICODE_CHARACTER_ICON_DIR_PATH)


def reset_unicode_character_icon_dir():
    if os.path.isdir(UNICODE_CHARACTER_ICON_DIR_PATH):
        shutil.rmtree(UNICODE_CHARACTER_ICON_DIR_PATH)
    prepare_unicode_character_icon_dir()
