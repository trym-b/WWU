from argparse import ArgumentParser, Namespace
from pathlib import Path

from backoff import expo, on_exception
from easynmt import EasyNMT
from languages import Language, source_language, target_language
from nltk import download
from requests.exceptions import HTTPError


def _args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--target-language", type=target_language, required=True)
    return parser.parse_args()


@on_exception(expo, HTTPError, max_time=120)
def _download_model(destination: Path, target_language: Language) -> EasyNMT:
    model = EasyNMT("opus-mt", max_loaded_models=10)
    model.translate(
        "hello",
        target_lang=target_language.code,
        source_lang=source_language().code,
    )
    model.save(str(destination.resolve()))


def _main() -> None:
    args = _args()
    _download_model(destination=args.destination, target_language=args.target_language)


if __name__ == "__main__":
    _main()
