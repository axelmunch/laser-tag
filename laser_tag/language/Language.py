import json

from ..configuration import LANGUAGE_FILE, VARIABLES
from .LanguageKey import LanguageKey


class Language:
    """Language manager"""

    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)

            cls.__instance.language_content = {}
            cls.__instance.load()
            cls.__instance.set_language(VARIABLES.language)

        return cls.__instance

    def load(self):
        try:
            with open(LANGUAGE_FILE, "r", encoding="utf-8") as file:
                self.language_content = json.load(file)
        except FileNotFoundError:
            if VARIABLES.debug:
                print("Language file not found")

    def set_language(self, language):
        self.language = language

    def get_language_list(self):
        try:
            return self.language_content["index"]
        except KeyError:
            return {}

    def get(self, key: LanguageKey) -> str:
        try:
            return self.language_content[self.language][str(key)]
        except KeyError:
            if VARIABLES.debug:
                print(f"Language key {key} not found for language {self.language}")
            return ""
