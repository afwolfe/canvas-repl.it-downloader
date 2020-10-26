"""
repl_batch_download.py
Author: afwolfe

This module reads in a list of URLs from a CSV and attempts to download valid public repl.it projects.
"""

import argparse
import csv
from os import mkdir, listdir, path
from zipfile import ZipFile, BadZipFile

import requests

def verify_and_clean_url(url):
    """
    Checks the given url to verify that it is a proper repl.it link and cleans up any endings.
    """

    if url.startswith('http') and 'repl.it' in url: #check that it's a repl link.
        if '#' in url or '?' in url:
            url = url.split('#')[0].split('?')[0] #Remove any extra endings from the URL.
        if 'join' in url and cookies['connect.sid']: #If join URL and login SID
            r = requests.get(url, cookies=cookies)
            if r.status_code == 200:
                url = r.url #Update URL after following the join link.
            else:
                url = None
    else:
        url = None
    return url

def extract_all(outdir):
    """
    Extracts all of the project zips in the outdir.
    """
    print("Extracting all...")
    for x in listdir(outdir):
        p = path.abspath(path.join(outdir, x))
        outpath = path.join(outdir, x.split('.zip')[0])
        if x.endswith('.zip') and not path.exists(outpath):
            try:
                with ZipFile(p, 'r') as zip:
                    zip.extractall(outpath)
            except BadZipFile:
                print("{} is not a valid zip".format(x))


def download_project(url, outdir):
    name = url.split('/')[4]
    url = url + '.zip'

    outpath = path.join(outdir, name + '.zip')
    if args.overwrite or (not path.exists(outpath)):
        print("Downloading: " + url)
        file = requests.get(url, allow_redirects=True, cookies=cookies)
        if file.status_code == 200:
            open(outpath, 'wb').write(file.content)
        else:
            print("Error {} when downloading.".format(file.status_code))
    else:
        print("File already exists: {}".format(outpath))

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--infile', type=str, default="submission_urls.csv",
                            help="The submission urls to download from. Defaults to: submission_urls.csv")
    arg_parser.add_argument('--outdir', type=str, default="downloads/", help="The name of the csv file to create of the urls. Defaults to downloads/")
    arg_parser.add_argument('--sid', type=str, default=None, help="Specifies the connect.sid value for join links.")
    arg_parser.add_argument('--noextract', action="store_true", help="Disables automatic extraction of the downloaded zips.")
    arg_parser.add_argument('--overwrite', action="store_true", help="Overwrites (and reextracts) existing zip files with new ones.")
    args = arg_parser.parse_args()

    infile = path.abspath(args.infile)
    outdir = path.abspath(args.outdir)
    cookies = {}
    if args.sid:
        cookies['connect.sid'] = args.sid

    if not path.exists(outdir):
        mkdir(outdir)

    with open(infile, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            try:
                url = row[0]
                url = verify_and_clean_url(url)
                if url:
                    download_project(url, outdir)
                else:
                    print("Invalid URL: {}".format(row[0]))
            except IndexError:
                #print("Invalid row.")
                continue
    extract_all(outdir)