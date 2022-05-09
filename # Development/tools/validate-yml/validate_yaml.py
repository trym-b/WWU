"""
Validates that all localisation files are complying with YAML format
"""

from pathlib import Path
from typing import List

from yaml import safe_load


def _ignored_files() -> List[Path]:
    """These files globbed by the file patterns in this function are ignored
    because they do not conform to yaml syntax
    Ideally this function should be deleted when all the file patterns has been deleted
    """
    invalid_file_patterns = [
        "localisation/WWU_ruler_personalities_l_*.yml",
        "localisation/replace/loadingtips_l_*.yml",
        "localisation/replace/generic_events_l_*.yml",
        "localisation/replace/WWU_replacements_l_*.yml",
        "localisation/events/WWU_event_consort_l_*.yml",
        "localisation/WWU_estate_agenda_l_*.yml",
    ]
    repo_root = Path(__file__).parent.parent.parent.parent
    invalid_files = []
    for pattern in invalid_file_patterns:
        invalid_files.extend(list(repo_root.rglob(pattern=pattern)))
    return invalid_files


def _main() -> None:
    repo_root = Path(__file__).parent.parent.parent.parent
    localisation_directory = repo_root / "localisation"
    localisation_files = sorted(list(localisation_directory.rglob("*.yml")))
    if len(localisation_files) < 1:
        raise RuntimeError(f"No localisation files found in {localisation_directory}")
    for localisation_file in localisation_files:
        if localisation_file in _ignored_files():
            print(f"Skipping file {localisation_file}", flush=True)
            continue
        print(f"Validating yml syntax in file: {localisation_file}", flush=True)
        with localisation_file.open(encoding="utf-8") as file_pointer:
            safe_load(file_pointer)


if __name__ == "__main__":
    _main()
