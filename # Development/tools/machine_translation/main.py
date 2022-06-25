"""Translates one or all of the english source files to target language
"""

from argparse import ArgumentParser, ArgumentTypeError, Namespace
from dataclasses import dataclass, fields
from pathlib import Path
from typing import List, Union

from languages import Language, LanguageCollection, source_language, target_language
from tqdm import tqdm
from translation import initialize_translation, translate
from utils import initialize_yaml, replace_clrf_with_lf, replace_whitespace_before_keys, save_as_utf_8_bom
from ruamel.yaml.scalarstring import DoubleQuotedScalarString
#from filtering import split_into_translatable_and_untranslatable_parts
from pathlib import Path

from backoff import expo, on_exception
from easynmt import EasyNMT
from languages import Language, is_key_ignored, is_value_ignored, source_language
from nltk import download
from typing import List
from requests.exceptions import HTTPError
from ruamel.yaml.scalarstring import DoubleQuotedScalarString
from utils import (
    is_just_icon_like_structure,
    split_because_of_start_icon_like_structure,
    starts_with_icon_like_structure,
)


def _args() -> Namespace:
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--source-file",
        type=Path,
        help="Translates source file into all target languages",
    )
    group.add_argument(
        "--update-all-localizations",
        action="store_true",
        help="Translates every language file in localisation to target languages",
    )
    parser.add_argument("--target-language", type=target_language, required=True)
    parser.add_argument("--translation-model-cache-dir", type=Path, required=True)
    return parser.parse_args()


def _calculate_destination_path(source_file: Path, target_language: Language) -> Path:
    return (
        source_file.parent
        / str(source_file.name).replace(
            source_language().paradox_localization_key,
            target_language.paradox_localization_key,
        )
    ).resolve()

@dataclass
class DoNotTranslateThis:
    string: str

@dataclass
class TranslateThis:
    string: str

@dataclass
class ToBeTranslated:
    key: str
    sub_strings: List[Union[DoNotTranslateThis, TranslateThis]]

@dataclass
class Translated:
    key: str
    value: str

def split_into_translatable_and_untranslatable_parts(
    key: str, value: str, target_language: Language, #translation_model_cache_dir: Path
) -> bool:#-> tuple[str, DoubleQuotedScalarString]:
    if is_key_ignored(key, target_language):
        return [DoNotTranslateThis(value)]
        #return key, DoubleQuotedScalarString(value)
    if is_value_ignored(value, target_language):
        #return key, DoubleQuotedScalarString(value)
        return [DoNotTranslateThis(value)]
    if starts_with_icon_like_structure(value):
        if is_just_icon_like_structure(value):
            #return key, DoubleQuotedScalarString(value)
            return [DoNotTranslateThis(value)]
        split_string = split_because_of_start_icon_like_structure(value)
        icon = split_string[0]
        separators = split_string[1]
        rest = split_string[2]
        if is_value_ignored(rest, target_language):
            #return key, DoubleQuotedScalarString(value)
            return [DoNotTranslateThis(value)]
        #result = translate(rest, target_language.code, translation_model_cache_dir)
        #return key, DoubleQuotedScalarString(f"{icon}{separators}{result}")
        #return False # not correct
        return [DoNotTranslateThis(icon), DoNotTranslateThis(separators), TranslateThis(rest)]

    #return key, DoubleQuotedScalarString(translate(value, target_language.code, translation_model_cache_dir))
    return [TranslateThis(value)]

#def split_into_translatable_blocks(source_value: str):
#    return split_into_translatable_and_untranslatable_parts(source_value)


def _main() -> None:
    args = _args()
    repo_root = Path(__file__).parent.parent.parent.parent.resolve()

    if args.source_file:
        paths = [args.source_file.resolve()]
    elif args.update_all_localizations:
        paths = sorted(
            list(
                (repo_root / "localisation")
                .resolve(strict=True)
                .rglob(pattern=f"*{source_language().paradox_localization_key}.yml")
            )
        )
    else:
        raise RuntimeError("Invalid argument, expected a source file or all files")
    target_language = args.target_language

    print("Setup models before translation, otherwise the translation might be unstable")
    initialize_translation(
        target_language=target_language, translation_model_cache_dir=args.translation_model_cache_dir.resolve()
    )

    for path in paths:
        data = initialize_yaml().load(path)

        if source_language().paradox_localization_key not in data:
            raise RuntimeError(f"{path} does not contain the '{source_language()=}'s key")

        destination = _calculate_destination_path(source_file=path, target_language=target_language)

        print(
            f"Translating '{path}' to {target_language.name}",
            flush=True,
        )

        source_data = data[source_language().paradox_localization_key]
        translation_entry_collection = []

        # create list of to_be_translated entries key + list[translate_this,do_not_translate_this]
        for source_key, source_value in source_data.items():
            source_split_into_translateable_and_untranslateable_parts = split_into_translatable_and_untranslatable_parts(key=source_key, value=source_value, target_language=target_language)
            translation_entry_collection.append(ToBeTranslated(key=source_key, sub_strings=source_split_into_translateable_and_untranslateable_parts))
        
        # if to_be_translated contains just do_not_translate_this -> convert to translated
        for translation_entry in translation_entry_collection:
            requires_translation = False
            for substring in translation_entry.sub_strings:
                if isinstance(substring, TranslateThis):
                    requires_translation = True
                    break
            if not requires_translation:
                translation_entry = Translated(translation_entry.key, " ".join([e.string for e in translation_entry.sub_strings]))
        
        # for all to_be_translated, create list of all translate_this
        strings_to_be_translated = []
        for translation_entry in translation_entry_collection:
            if isinstance(translation_entry, ToBeTranslated):
                for sub_string in translation_entry.sub_strings:
                    if isinstance(sub_string, TranslateThis):
                        strings_to_be_translated.append(sub_string.string)

        # translate list of translate_this
        result = translate(strings_to_be_translated, target_language.code, args.translation_model_cache_dir.resolve())

        # for all to_be_translated, get the translated text and convert to translated
        new_collection = []
        for translation_entry in translation_entry_collection:
            if isinstance(translation_entry, ToBeTranslated):
                new_sub_strings = []
                for sub_string in translation_entry.sub_strings:
                    if isinstance(sub_string, TranslateThis):
                        sub_string = DoNotTranslateThis(result.pop(0))
                    new_sub_strings.append(sub_string)
                translation_entry.sub_strings = new_sub_strings
                translation_entry = Translated(translation_entry.key, " ".join([e.string for e in translation_entry.sub_strings]))
            new_collection.append(translation_entry)
       
        # write to file
        translated_data = {}
        for translation_entry in new_collection:
            translated_data[translation_entry.key] = DoubleQuotedScalarString(translation_entry.value)

#        translated = {}
#
#        if not data[source_language().paradox_localization_key]:
#            continue
#        list_2 = []
#
#        for key, value in tqdm(
#            data[source_language().paradox_localization_key].items(),
#            total=len(data[source_language().paradox_localization_key]),
#        ):
#            list_2.append(translate_or_skip_value(
#                key, value, target_language, args.translation_model_cache_dir.resolve()
#            ))
#            #translated[key] = value
#
#        print("translating", flush=True)
#        to_be_translated = []
#        for count, key_value in enumerate(data[source_language().paradox_localization_key].items()):
#            key = key_value[0]
#            value = key_value[1]
#            if list_2[count]:
#                to_be_translated.append(value)
#        
#        res = translate(to_be_translated, target_language.code, args.translation_model_cache_dir.resolve())
#        count_2 = 0
#
#        for count, key_value in enumerate(data[source_language().paradox_localization_key].items()):
#            key = key_value[0]
#            value = key_value[1]
#            if list_2[count]:
#                translated[key] = DoubleQuotedScalarString(res[count_2])
#                count_2 += 1
#            else:
#                translated[key] = DoubleQuotedScalarString(value)
#


        translation = {target_language.paradox_localization_key: translated_data}
        initialize_yaml().dump(translation, destination)

        replace_whitespace_before_keys(destination)
        replace_clrf_with_lf(destination)
        save_as_utf_8_bom(destination)


if __name__ == "__main__":
    _main()
