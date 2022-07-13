"""
Naively verifies that every event and mission modifier in `common/event_modifiers`
are at least referenced in some `*.txt` or `*.yml` file outside of abovementioned
directory.

One major drawback to this script is that it is not able to determine if a event/mission
modifier which name is simply a subset of another event/mission modifier's name
will not cause a failure.

A more robust and sophisticated solution should ideally be used instead. However,
such a solution might require a complete EU4 syntax parser.
"""

from pathlib import Path

from modifier_parser import parse_text, transform


def _main() -> None:
    repo_root = Path(__file__).parent.parent.parent.parent.resolve()
    all_text_and_yaml_files = list(repo_root.rglob("*.txt")) + list(
        repo_root.rglob("*.yml")
    )
    for dir in all_text_and_yaml_files:
        if "/map/" in dir:
            all_text_and_yaml_files.remove(dir)
    if not all_text_and_yaml_files:
        raise RuntimeError(f"{repo_root} globbed no '*.txt' or '*.yml*' files")
    relevant_files = sorted(
        [
            file
            for file in all_text_and_yaml_files
            if not file.is_relative_to(repo_root / "common" / "event_modifiers")
        ]
    )
    if not relevant_files:
        raise RuntimeError("The filtered files after globbing contains no entries")
    modifier_files = sorted(repo_root.rglob("common/event_modifiers/*.txt"))
    if not modifier_files:
        raise RuntimeError("No relevant files found in 'common/event_modifiers'")
    for modifier_file in modifier_files:
        res = transform(parse_text(modifier_file.read_text(encoding="utf-8")))
        for key in res:
            found = False
            for file in relevant_files:
                file_content = file.read_text(encoding="utf-8")
                if key in file_content:
                    print(
                        f"Potential reference to '{key}' found in '{file}'", flush=True
                    )
                    found = True
                    break
            if not found:
                raise RuntimeError(
                    f"Modifier '{key}' not found. Source file: '{modifier_file}'"
                )


if __name__ == "__main__":
    _main()
