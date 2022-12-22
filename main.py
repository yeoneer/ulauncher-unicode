import logging
import os
import sys

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener

from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.event import PreferencesEvent
from ulauncher.api.shared.event import PreferencesUpdateEvent

from unicode_extension.load_unicode_data import load_unicode_data
from unicode_extension.unicode_character_icon import reset_unicode_character_icon_dir
from unicode_extension.unicode_extension_feature import UnicodeExtensionFeature
from unicode_extension.util import get_project_path

logger = logging.getLogger(__name__)


class UlauncherUnicodeExtension(Extension):
    def __init__(self):
        super().__init__()

        reset_unicode_character_icon_dir()

        self.subscribe(KeywordQueryEvent, UlauncherKeywordQueryEventListener())
        self.subscribe(PreferencesEvent, UlauncherPreferencesEventListener())
        self.subscribe(
            PreferencesUpdateEvent, UlauncherPreferencesUpdateEventListener()
        )

        unicode_data = load_unicode_data()

        self.feature: UnicodeExtensionFeature = UnicodeExtensionFeature(
            project_path=get_project_path(),
            unicode_character_list=unicode_data["UNICODE_CHARACTER_LIST"],
            unicode_character_dict=unicode_data["UNICODE_CHARACTER_DICT"],
        )


class UlauncherKeywordQueryEventListener(EventListener):
    def on_event(self, event: KeywordQueryEvent, extension: UlauncherUnicodeExtension):
        return extension.feature.handle_keyword_query_event(event)


class UlauncherPreferencesEventListener(EventListener):
    def on_event(self, event: PreferencesEvent, extension: UlauncherUnicodeExtension):
        extension.feature.handle_preferences_event(event)


class UlauncherPreferencesUpdateEventListener(EventListener):
    def on_event(
        self, event: PreferencesUpdateEvent, extension: UlauncherUnicodeExtension
    ):
        extension.feature.handle_preferences_update_event(event)


if __name__ == "__main__":
    UlauncherUnicodeExtension().run()
