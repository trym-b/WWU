"""Translates one or all of the english source files to target language
"""

from argparse import ArgumentParser, ArgumentTypeError, Namespace
from dataclasses import fields
from pathlib import Path

from languages import Language, LanguageCollection, source_language, target_language
from tqdm import tqdm
from translation import initialize_translation, translate_or_skip_value, translate
from utils import initialize_yaml, replace_clrf_with_lf, replace_whitespace_before_keys, save_as_utf_8_bom
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

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
            continue

        destination = _calculate_destination_path(source_file=path, target_language=target_language)

        print(
            f"Translating '{path}' to {target_language.name}",
            flush=True,
        )
        translated = {}

        if not data[source_language().paradox_localization_key]:
            continue
        list_2 = []

        for key, value in tqdm(
            data[source_language().paradox_localization_key].items(),
            total=len(data[source_language().paradox_localization_key]),
        ):
            list_2.append(translate_or_skip_value(
                key, value, target_language, args.translation_model_cache_dir.resolve()
            ))
            #translated[key] = value

        print("translating", flush=True)
        to_be_translated = []
        for count, key_value in enumerate(data[source_language().paradox_localization_key].items()):
            key = key_value[0]
            value = key_value[1]
            if list_2[count]:
                to_be_translated.append(value)
        
        res = translate(to_be_translated, target_language.code, args.translation_model_cache_dir.resolve())
        count_2 = 0

        for count, key_value in enumerate(data[source_language().paradox_localization_key].items()):
            key = key_value[0]
            value = key_value[1]
            if list_2[count]:
                translated[key] = DoubleQuotedScalarString(res[count_2])
                count_2 += 1
            else:
                translated[key] = DoubleQuotedScalarString(value)



        translation = {target_language.paradox_localization_key: translated}
        initialize_yaml().dump(translation, destination)

        replace_whitespace_before_keys(destination)
        replace_clrf_with_lf(destination)
        save_as_utf_8_bom(destination)


if __name__ == "__main__":
    _main()
