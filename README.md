# canvas-repl.it-downloader
Batch downloader for [repl.it](https://repl.it) and extracting URLs from "link.html" files created by [canvas-lms](https://github.com/instructure/canvas-lms).

## Overview

This repository contains scripts for:
1. Turning a folder of URL submissions from canvas-lms into a more usable and generic .csv file.
2. Downloading project and extracting zips from repl.it.


## Usage

### canvas_link_parser.py

This is the script that takes a folder of submission `link.html` files and extracts the URLs from them.

```bash
$ python canvas_link_parser.py -h
usage: canvas_link_parser.py [-h] [--folder FOLDER] [--outfile OUTFILE]

optional arguments:
  -h, --help         show this help message and exit
  --folder FOLDER    The folder of link.html files from Canvas. Defaults to: submissions/
  --outfile OUTFILE  The name of the csv file to create of the urls. Defaults to submission_urls.csv
```

### repl_batch_download.py

This is the script that downloads and extracts the project.zip files from repl.it for offline use.
In order to handle "Multiplayer" `/join` links, you need to specify a valid session id from the `connect.sid` cookie in your browser using the `--sid` argument.

```bash
$ python repl_batch_download.py -h
usage: repl_batch_download.py [-h] [--infile INFILE] [--outdir OUTDIR] [--sid SID] [--noextract] [--overwrite]

optional arguments:
  -h, --help       show this help message and exit
  --infile INFILE  The submission urls to download from. Defaults to: submission_urls.csv
  --outdir OUTDIR  The name of the csv file to create of the urls. Defaults to downloads/
  --sid SID        Specifies the connect.sid value for join links.
  --noextract      Disables automatic extraction of the downloaded zips.
  --overwrite      Overwrites (and reextracts) existing zip files with new ones.
```

## Requirements

* Python 3.x
* requests