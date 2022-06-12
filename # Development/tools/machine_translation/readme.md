# Machine translation

## Requirements

 * python

## Setup

Install the requirements by running `pip install --requirement requirements.txt` in a
virtual environment.

## Translate

Run `python main.py --source-file <source-file> --target-language <language>` to translate
a single file. Replace `--source-file <source-file>` with `--update-all-localizations` to
translate every source file.
Note: Translation takes a very long time to run, it is recommended to run this through Github
Actions instead of running it manually.
