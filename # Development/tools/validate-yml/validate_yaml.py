"""
Validates that all localisation files are complying with YAML format
"""

from pathlib import Path

from pdxloc.util import read_localisation


def _main() -> None:
    repo_root = Path(__file__).parent.parent.parent.parent
    localisation_directory = repo_root / "localisation"
    localisation_files = sorted(list(localisation_directory.rglob("*.yml")))
    if len(localisation_files) < 1:
        raise RuntimeError(f"No localisation files found in {localisation_directory}")
    for localisation_file in localisation_files:
        print(f"Validating yml syntax in file: {localisation_file}", flush=True)
        read_localisation(localisation_file)


if __name__ == "__main__":
    _main()
