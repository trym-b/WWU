from pathlib import Path

from backoff import expo, on_exception
from easynmt import EasyNMT
from languages import Language, is_key_ignored, is_value_ignored, source_language
from nltk import download
from typing import List, Sequence
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



def translate(to_be_translated: Sequence[str], language_code: str, translation_model_cache_dir: Path) -> List[str]:
    """Translate a sequence of strings into the target language"""
    model = EasyNMT(model_name="opus-mt", cache_folder=str(translation_model_cache_dir))

    translated = model.translate(
        to_be_translated,
        target_lang=language_code,
        source_lang=source_language().code,
    )

    return translated
