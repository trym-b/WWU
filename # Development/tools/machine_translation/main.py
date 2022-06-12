"""Translates one or all of the english source files to target language
"""

from argparse import ArgumentParser, ArgumentTypeError, Namespace
from dataclasses import fields
from pathlib import Path

from languages import Language, LanguageCollection, source_language
from tqdm import tqdm
from translation import initialize_translation, translate_or_skip_value
from utils import initialize_yaml, replace_clrf_with_lf, replace_whitespace_before_keys, save_as_utf_8_bom


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
    parser.add_argument("--target-language", type=_target_language, required=True)
    return parser.parse_args()


def _target_language(language_as_string: str) -> Language:
    if language_as_string == LanguageCollection.german.name:
        return LanguageCollection.german
    if language_as_string == LanguageCollection.spanish.name:
        return LanguageCollection.spanish
    if language_as_string == LanguageCollection.french.name:
        return LanguageCollection.french
    raise ArgumentTypeError(
        f"Invalid language: {language_as_string}, valid options: {' '.join([f.name for f in fields(LanguageCollection)])}"
    )


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
    initialize_translation(target_language=target_language)

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

        for key, value in tqdm(
            data[source_language().paradox_localization_key].items(),
            total=len(data[source_language().paradox_localization_key]),
        ):
            key, value = translate_or_skip_value(key, value, target_language)
            translated[key] = value

        translation = {target_language.paradox_localization_key: translated}
        initialize_yaml().dump(translation, destination)

        replace_whitespace_before_keys(destination)
        replace_clrf_with_lf(destination)
        save_as_utf_8_bom(destination)


if __name__ == "__main__":
    _main()
