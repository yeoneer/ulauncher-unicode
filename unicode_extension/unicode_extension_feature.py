import logging
import os
import sys

from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.item.ExtensionSmallResultItem import ExtensionSmallResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.event import PreferencesEvent
from ulauncher.api.shared.event import PreferencesUpdateEvent

from .search_unicode_character import search_unicode_character
from .unicode_character_icon import generate_unicode_character_icon

from .unicode_character import UnicodeCharacter

logger = logging.getLogger(__name__)


class UnicodeExtensionFeature:
    def __init__(
        self,
        project_path: str,
        unicode_character_list: list,
        unicode_character_dict: dict,
    ):
        self.project_path: str = project_path

        self.icon_extension = f"{self.project_path}/images/icon.png"
        self.icon_non_printable = f"{self.project_path}/images/non-printable-icon.png"
        self.icon_convert = f"{self.project_path}/images/convert-icon.png"

        self.preferences: UnicodeExtensionPreferences = UnicodeExtensionPreferences()

        self.unicode_character_dict: dict[
            str, UnicodeCharacter
        ] = unicode_character_dict
        self.unicode_character_list: list[UnicodeCharacter] = unicode_character_list

    def process_keyword_query_event(
        self, event: KeywordQueryEvent
    ) -> RenderResultListAction:
        content: str = event.get_argument()

        if not content:
            return RenderResultListAction([])

        extension_result_list: list = []

        if len(content) == 1:
            result_item = self.convert_one_letter_to_unicode_info(content)

            extension_result_list.append(result_item)

        if len(content) >= 1:
            result_item = self.convert_all_letter_to_unicode_info(content)

            extension_result_list.append(result_item)

        search_result_list = self.get_search_result(content)
        extension_result_list.extend(search_result_list)

        return RenderResultListAction(extension_result_list)

    def process_preferences_event(self, event: PreferencesEvent):
        self.preferences.update(event.preferences)  # type: ignore

    def process_preferences_update_event(self, event: PreferencesUpdateEvent):
        preference_id = event.id
        new_value = event.new_value

        self.preferences.update({preference_id: new_value})

    def get_unicode_character_icon(
        self,
        unicode_character: UnicodeCharacter,
    ) -> str:
        if not unicode_character.character.isprintable():
            return self.icon_non_printable

        unicode_character_icon = generate_unicode_character_icon(
            unicode_character,
            background=self.preferences.unicode_character_icon_background,
            font=self.preferences.unicode_character_icon_font,
        )

        return unicode_character_icon

    def get_search_result(self, query: str) -> list[ExtensionResultItem]:
        extension_result_item_list: list = []

        search_result_list = search_unicode_character(
            query=query,
            unicode_character_list=self.unicode_character_list,
            limit=self.preferences.search_result_list_size,
        )

        for index, result_item in enumerate(search_result_list):
            (unicode_character, score, _) = result_item
            unicode_character: UnicodeCharacter = unicode_character

            extension_result_item = self.generate_search_result_item_view(
                unicode_character
            )

            extension_result_item_list.append(extension_result_item)

        return extension_result_item_list

    def generate_search_result_item_view(
        self, unicode_character: UnicodeCharacter
    ) -> ExtensionResultItem | ExtensionSmallResultItem:
        def generate_extension_result_item(
            unicode_character: UnicodeCharacter,
        ) -> ExtensionResultItem:
            unicode_character_icon = self.get_unicode_character_icon(unicode_character)
            name = f"{unicode_character.name}"
            description: str = f"{unicode_character.u_code_point} {unicode_character.name} ({unicode_character.block})"

            if len(unicode_character.aliases) > 0:
                alias: str = ", ".join(unicode_character.aliases)
                description = f"{description} [{alias}]"

            result_item = ExtensionResultItem(
                icon=unicode_character_icon,
                name=name,
                description=description,
                on_enter=CopyToClipboardAction(unicode_character.character),
            )
            return result_item

        def generate_extension_small_result_item(
            unicode_character: UnicodeCharacter,
        ) -> ExtensionSmallResultItem:
            name = f"{unicode_character.name} ({unicode_character.u_code_point})"

            small_result_item = ExtensionSmallResultItem(
                icon=self.get_unicode_character_icon(unicode_character),
                name=name,
                on_enter=CopyToClipboardAction(unicode_character.character),
            )

            return small_result_item

        if self.preferences.search_result_view_type == "default":
            return generate_extension_result_item(unicode_character)
        elif self.preferences.search_result_view_type == "small":
            return generate_extension_small_result_item(unicode_character)
        else:
            raise ValueError(
                f"`search_result_view_type` is wrong. Current value: `{self.preferences.search_result_view_type}`"
            )

    def get_unicode_character_from_letter(self, character: str) -> UnicodeCharacter:
        if len(character) > 1:
            raise ValueError(
                f"Character should be one letter. current 'character' value: `{character}`"
            )

        hex_code_str = f"{ord(character):X}"
        code_point = f"U+{hex_code_str.zfill(4)}"

        unicode_character = self.unicode_character_dict[code_point]

        return unicode_character

    def convert_one_letter_to_unicode_info(self, letter: str) -> ExtensionResultItem:
        unicode_character = self.get_unicode_character_from_letter(letter)

        name = f"{unicode_character.name}"
        description = f"`{letter}` is {unicode_character.u_code_point}"

        result_item = ExtensionResultItem(
            icon=self.icon_convert,
            name=name,
            description=description,
            on_enter=CopyToClipboardAction(name),
        )

        return result_item

    def convert_all_letter_to_unicode_info(self, content: str) -> ExtensionResultItem:
        letter_info_list: list[str] = []

        for letter in content:
            unicode_character = self.get_unicode_character_from_letter(letter)

            letter_info = f"{letter}({unicode_character.u_code_point})"
            letter_info_list.append(letter_info)

        name = " ".join(letter_info_list)
        description = f"`{content}` to Unicode code point"

        result_item = ExtensionResultItem(
            icon=self.icon_convert,
            name=name,
            description=description,
            on_enter=CopyToClipboardAction(name),
        )

        return result_item


class UnicodeExtensionPreferences:
    DEFAULT_KEYWORD: str = "u"
    DEFAULT_SEARCH_RESULT_LIST_SIZE: int = 10
    DEFAULT_SEARCH_RESULT_VIEW_TYPE: str = "default"
    DEFAULT_UNICODE_CHARACTER_ICON_FONT: str = "sans-serif"
    DEFAULT_UNICODE_CHARACTER_ICON_BACKGROUND = None

    keyword: str
    search_result_list_size: int
    search_result_view_type: str
    unicode_character_icon_font: str
    unicode_character_icon_background: None | str

    def __init__(self):
        self.keyword: str = self.DEFAULT_KEYWORD
        self.search_result_list_size: int = self.DEFAULT_SEARCH_RESULT_LIST_SIZE
        self.search_result_view_type: str = self.DEFAULT_SEARCH_RESULT_VIEW_TYPE
        self.unicode_character_icon_font: str = self.DEFAULT_UNICODE_CHARACTER_ICON_FONT
        self.unicode_character_icon_background: None | str = (
            self.DEFAULT_UNICODE_CHARACTER_ICON_BACKGROUND
        )

    def update(self, new_preferences: dict):
        if "keyword" in new_preferences.keys():
            self.update_keyword(new_preferences["keyword"])
        if "search_result_list_size" in new_preferences.keys():
            self.update_search_result_list_size(
                new_preferences["search_result_list_size"]
            )
        if "search_result_view_type" in new_preferences.keys():
            self.update_search_result_view_type(
                new_preferences["search_result_view_type"]
            )
        if "unicode_character_icon_font" in new_preferences.keys():
            self.update_unicode_character_icon_font(
                new_preferences["unicode_character_icon_font"]
            )
        if "unicode_character_icon_background" in new_preferences.keys():
            self.update_unicode_character_icon_background(
                new_preferences["unicode_character_icon_background"]
            )

    def update_keyword(self, new_value: str):
        self.keyword = new_value

    def update_search_result_list_size(self, new_value: str):
        # Handle cases where `search_result_list_size` preference value
        # is look like `asdf` instead of `{number}` that it should be.
        try:
            self.search_result_list_size = int(new_value)
        except ValueError:
            self.search_result_list_size = self.DEFAULT_SEARCH_RESULT_LIST_SIZE

        if self.search_result_list_size < 0:
            self.search_result_list_size = self.DEFAULT_SEARCH_RESULT_LIST_SIZE

    def update_search_result_view_type(self, new_value: str):
        self.search_result_view_type = new_value

    def update_unicode_character_icon_font(self, new_value: str):
        self.unicode_character_icon_font = new_value

        if new_value == "":
            self.unicode_character_icon_font = self.DEFAULT_UNICODE_CHARACTER_ICON_FONT

    def update_unicode_character_icon_background(self, new_value: str):
        if new_value == "none":
            self.unicode_character_icon_background = None
        elif new_value == "white":
            self.unicode_character_icon_background = "white"
        else:
            self.unicode_character_icon_background = (
                self.DEFAULT_UNICODE_CHARACTER_ICON_BACKGROUND
            )
