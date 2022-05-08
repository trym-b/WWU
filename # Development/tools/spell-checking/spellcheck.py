"""
Spell checks all localisation files that ends with `l_english.yml`
"""

from pathlib import Path
from subprocess import check_call, CalledProcessError
from sys import exit


def _main() -> None:
    repo_root = Path(__file__).parent.parent.parent.parent
    localisation_directory = repo_root / "localisation"
    localisation_files = sorted(
        [str(path) for path in localisation_directory.rglob("*l_english.yml")]
    )
    if len(localisation_files) < 1:
        raise RuntimeError(f"No localisation files found in {localisation_directory}")
    try:
        check_call(
            args=[
                "cspell",
                "--no-summary",
                "--no-progress",
                f"--config={repo_root/'# Development'/'tools'/'spell-checking'/'cspell.json'}",
                *localisation_files,
            ]
        )
    except CalledProcessError:
        print("Spell checking failed", flush=True)
        exit(1)
    print("No spelling errors found", flush=True)



if __name__ == "__main__":
    _main()
