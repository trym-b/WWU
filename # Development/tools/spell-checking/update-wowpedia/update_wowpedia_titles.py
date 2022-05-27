"""
Updates the wowpedia generated dictionary file to the latest version
"""

from pathlib import Path
from re import sub
from tempfile import TemporaryDirectory

from py7zr import SevenZipFile
from requests import get
from xmltodict import parse


def _filter_irrelevant_pages(pages: list[dict]) -> list[dict]:
    relevant_pages = []
    for page in pages:
        if not page["title"].startswith(
            (
                "API ",
                "Blizzard ",
                "BlizzCon",
                "Category talk:",
                "Category:Server:",
                "File talk:",
                "File:",
                "Forum:",
                "Help talk:",
                "Help:",
                "Patch ",
                "PlaySoundFile macros",
                "Quest:",
                "Server:",
                "Talk:",
                "User talk:",
                "User:",
                "Wowpedia talk:",
                "Wowpedia:",
                "Category:API",
                "Struct",
                "Template talk:",
                "Template:User",
                "Quotes of ",
            )
        ):
            relevant_pages.append(page)
    return relevant_pages


def _rename_disambiguation_parenthesis(pages: list[dict]) -> list[dict]:
    # remove disambiguation entires, i.e. "Thing", "Thing (quest)", "Thing (Horde)", etc
    for page in pages:
        title = page["title"]
        if title.strip().endswith(")"):
            title = sub(r"\([\s\S]*\)$", "", title)
            page["title"] = title.strip()
    return pages


def _download_and_parse_current_wowpedia_database() -> dict:
    wowpedia_url = "https://s3.amazonaws.com/wikia_xml_dumps/w/wo/wowpedia_pages_current.xml.7z"
    with TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        print("Downloading current wowpedia xml 7z", flush=True)
        response = get(url=wowpedia_url)
        zipped_archive = temp_dir / "wowpedia_pages_current.xml.7z"
        zipped_archive.write_bytes(response.content)
        with SevenZipFile(zipped_archive, mode="r") as zip_file:
            zip_file.extractall(temp_dir)
        wowpedia_xml = temp_dir / "wowpedia_pages_current.xml"
        print("Parsing xml", flush=True)
        return parse(wowpedia_xml.read_text(encoding="utf-8"))


def _split_tiles_on_certain_special_characters(pages: list[dict]) -> list[dict]:
    for page in pages:
        for i in r"""/":""":
            if i in page["title"]:
                page["title"] = page["title"].replace(i, " ")
    return pages


def _split_titles_into_words(pages: list[dict]) -> list[str]:
    words = []
    for title in [page["title"] for page in pages]:
        parts = title.split(" ")
        for part in parts:
            if len(part) <= 2:
                continue
            if part.isnumeric():
                continue
            if part[0].isnumeric():
                continue
            for element in ["'", r"\)", "!", ",", r"\.", "'s"]:
                part = sub(pattern=rf"^\S*{element}$", repl="", string=part)
            for element in [
                "'",
                r"\(",
            ]:
                part = sub(pattern=rf"^{element}\S*$", repl="", string=part)
            words.append(part)
    return words


def _main() -> None:
    wowpedia_database = _download_and_parse_current_wowpedia_database()
    repo_root = Path(__file__).parent.parent.parent.parent.parent

    print("Filtering titles", flush=True)
    relevant_pages = _filter_irrelevant_pages(wowpedia_database["mediawiki"]["page"])
    filtered_pages = _rename_disambiguation_parenthesis(relevant_pages)
    filtered_pages = _split_tiles_on_certain_special_characters(filtered_pages)

    print("Splitting titles into individual words", flush=True)
    words = sorted(set(_split_titles_into_words(filtered_pages)))

    wowpedia_titles_file = (
        repo_root / "# Development" / "tools" / "spell-checking" / "dictionaries" / "wowpedia-titles.txt"
    )
    wowpedia_titles_file.write_text("\n".join(words), encoding="utf-8")

    print("Update completed", flush=True)


if __name__ == "__main__":
    _main()
