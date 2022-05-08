# Spellcheck

## Requirements

 - docker

## Setup

### Windows

To setup your environment to spell check, run the following:

```shell
docker run --volume <path\to\repo>:/host_dir --tty --interactive ubuntu:22.04
cd /host_dir && ./"# Development"/tools/spell-checking/cspell_docker_setup.sh
```

Note `<C:\path\to\repo\>` should be replaced by the path to the root of the repository,
for example `C:\Users\<user-name>\repos\WWU\`

It might take some time to install the required packages.
When the setup command above completes, your system is now ready to spell check.

## Run cspell

To spell check, run:

```shell
python3 \#\ Development/tools/spell-checking/spellcheck.py
```
