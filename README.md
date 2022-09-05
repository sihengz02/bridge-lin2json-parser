# Bridge

This is a parser for converting `.lin` file in bridge game to `.json` file, which is easy for Python to read and human to understand.

This parser is easy to use:

- first, you should `git clone` this repo

- second, run `bash lin2json.sh` in your shell, by doing this:

  - we download data to the directory `./raw_file`

  - we then automatically using `lin2json.py` to turn raw `.lin` file to `.json ` file
  - the final `.json` file is in `data.json`

- if you want to clean all the data (including raw data and json data), just run `bash clean.sh` in your shell

Here I also list some open-source Bridge Game AI that can be found in Github:
- https://github.com/oriyanh/Bridge-AI
  - Language: Python3
  - Algorithm: Monte Carlo Tree Search
- https://github.com/ifplusor/alphabridge
  - Language: C++
  - Algorithm: CFR
