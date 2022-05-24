"""
Spell checks all localisation files that ends with `l_english.yml`
"""

from pathlib import Path
from subprocess import check_call, CalledProcessError
from sys import exit
from json import load, dump


def _main() -> None:
    repo_root = Path(__file__).parent.parent.parent.parent
    localisation_directory = repo_root / "localisation"
    localisation_files = sorted(
        [str(path) for path in localisation_directory.rglob("*l_english.yml")]
    )
    if len(localisation_files) < 1:
        raise RuntimeError(f"No localisation files found in {localisation_directory}")
    
    with open(repo_root/ repo_root/'# Development'/'tools'/'spell-checking'/'cspell.json') as fp:
        intial_read = load(fp)
    with open(repo_root/ repo_root/'# Development'/'tools'/'spell-checking'/'temp-cspell.json', "w") as fp:
        dump(intial_read,fp)
    #temp_config = 
    print(intial_read)
    current = intial_read
    for i in intial_read["words"]:
        current["words"].remove(i)
        with open(repo_root/'# Development'/'tools'/'spell-checking'/'temp-cspell.json', "w") as fp:
            dump(current,fp)
        check_call(
                args=[
                    "prettier",
                    "--tab-width",
                    "4",
                    "--write",
                    str(repo_root/'# Development'/'tools'/'spell-checking'/'temp-cspell.json')
                ]
            )
    #for 
        try:
            check_call(
                args=[
                    "cspell",
                    "--no-summary",
                    "--no-progress",
                    "--fail-fast",
                    f"--config={repo_root/'# Development'/'tools'/'spell-checking'/'temp-cspell.json'}",
                    *localisation_files,
                ]
            )
            print(f"Deleted: {i}")
        except CalledProcessError:
            print("Spell checking failed", flush=True)
            #exit(1)
            current["words"].append(i)
            current["words"] = sorted(current["words"], key=str.casefold)
            
    print("No spelling errors found", flush=True)



if __name__ == "__main__":
    _main()
