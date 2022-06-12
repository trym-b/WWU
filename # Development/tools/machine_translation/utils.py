from pathlib import Path
from re import search, split, sub

from ruamel.yaml import YAML


def starts_with_icon_like_structure(value: str) -> bool:
    result = search(r"(^[\[£]\S+[\]£]+)", value)
    if result:
        return True
    return False


def is_just_icon_like_structure(value: str) -> bool:
    result = search(r"(^[\[£]\S+[\]£]+$)", value)
    if result:
        return True
    return False


def replace_whitespace_before_keys(path: Path) -> None:
    content = path.read_bytes()
    new_content = []
    for line in content.split(b"\n"):
        new_content.append(sub(rb"^(\s\s)", b" ", line, count=1))
    path.write_bytes(b"\n".join(new_content))


def replace_clrf_with_lf(path: Path) -> None:
    content = path.read_bytes()
    crlf_as_bytes = b"\r\n"
    lf_as_bytes = b"\n"
    content = content.replace(crlf_as_bytes, lf_as_bytes)
    path.write_bytes(content)


def save_as_utf_8_bom(path: Path) -> None:
    path.write_text(path.read_text(encoding="utf-8-sig"), encoding="utf-8-sig")


def initialize_yaml() -> YAML:
    yaml = YAML()
    yaml.width = float("inf")
    yaml.allow_unicode = True
    yaml.encoding = "utf-8"
    yaml.indent = 2
    yaml.preserve_quotes = True
    yaml.line_break = "\n"
    yaml.block_seq_indent = 2
    yaml.allow_duplicate_keys = True
    return yaml


def split_because_of_start_icon_like_structure(value: str) -> tuple[str, str, str]:
    icon_lie_start_pattern = r"(^[\[£]\S+[\]£]+)"
    result = split(icon_lie_start_pattern, value, maxsplit=1)
    icon = result[1]
    rest = result[2]
    try:
        result_2 = split(r"(^[\s\\n('s)(.\s)(,\s)]+)", rest, maxsplit=1)
        separators = result_2[1]
        rest_2 = result_2[2]
        return icon, separators, rest_2
    except:
        print("Failed to split sentence on icon or similar start sequence")
        print(f"Original string: '{value}'")
        print(f"Result after splitting:\n{result_2}")
        raise
