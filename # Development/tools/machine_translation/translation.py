from pathlib import Path

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
def initialize_translation(target_language: Language, translation_model_cache_dir: Path) -> None:
    download("punkt")
    print("Dummy translation to ensure translation data has been setup properly")
    translate("hello", language_code=target_language.code, translation_model_cache_dir=translation_model_cache_dir)


def translate_or_skip_value(
    key: str, value: str, target_language: Language, translation_model_cache_dir: Path
) -> bool:#-> tuple[str, DoubleQuotedScalarString]:
    if is_key_ignored(key, target_language):
        return False
        #return key, DoubleQuotedScalarString(value)
    if is_value_ignored(value, target_language):
        #return key, DoubleQuotedScalarString(value)
        return False
    if starts_with_icon_like_structure(value):
        if is_just_icon_like_structure(value):
            #return key, DoubleQuotedScalarString(value)
            return False
        split_string = split_because_of_start_icon_like_structure(value)
        icon = split_string[0]
        separators = split_string[1]
        rest = split_string[2]
        if is_value_ignored(rest, target_language):
            #return key, DoubleQuotedScalarString(value)
            return False
        #result = translate(rest, target_language.code, translation_model_cache_dir)
        #return key, DoubleQuotedScalarString(f"{icon}{separators}{result}")
        return False # not correct
    #return key, DoubleQuotedScalarString(translate(value, target_language.code, translation_model_cache_dir))
    return True


def translate(to_be_translated: str, language_code: str, translation_model_cache_dir: Path) -> str:
    """Translate a single string into the target language"""
    model = EasyNMT(model_name="opus-mt", cache_folder=str(translation_model_cache_dir))

    translated = model.translate(
        to_be_translated,
        target_lang=language_code,
        source_lang=source_language().code,
    )

    return translated
