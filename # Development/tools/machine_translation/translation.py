from backoff import expo, on_exception
from easynmt import EasyNMT
from languages import Language, is_key_ignored, is_value_ignored, source_language
from nltk import download
from requests.exceptions import HTTPError
from ruamel.yaml.scalarstring import DoubleQuotedScalarString
from utils import (
    is_just_icon_like_structure,
    split_because_of_start_icon_like_structure,
    starts_with_icon_like_structure,
)


@on_exception(expo, HTTPError, max_time=120)
def initialize_translation(target_language: Language) -> None:
    download("punkt")
    print("Dummy translation to ensure translation data has been setup properly")
    _translate("hello", language_code=target_language.code)


def translate_or_skip_value(key: str, value: str, target_language: Language) -> tuple[str, DoubleQuotedScalarString]:
    if is_key_ignored(key, target_language):
        return key, DoubleQuotedScalarString(value)
    if is_value_ignored(value, target_language):
        return key, DoubleQuotedScalarString(value)
    if starts_with_icon_like_structure(value):
        if is_just_icon_like_structure(value):
            return key, DoubleQuotedScalarString(value)
        split_string = split_because_of_start_icon_like_structure(value)
        icon = split_string[0]
        separators = split_string[1]
        rest = split_string[2]
        if is_value_ignored(rest, target_language):
            return key, DoubleQuotedScalarString(value)
        result = _translate(rest, target_language.code)
        return key, DoubleQuotedScalarString(f"{icon}{separators}{result}")
    return key, DoubleQuotedScalarString(_translate(value, target_language.code))


def _translate(to_be_translated: str, language_code: str) -> str:
    """Translate a single string into the target language"""
    model = EasyNMT("opus-mt", max_loaded_models=10)

    translated = model.translate(
        to_be_translated,
        target_lang=language_code,
        source_lang=source_language().code,
    )

    return translated
