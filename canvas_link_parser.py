"""
canvas_link_parser.py
Author: afwolfe

This module parses all files in a folder ending in `link.html` for the "url" value in the head
and outputs to a csv file.
"""

import html.parser
import argparse
import codecs
import os
import csv

urls = []

class MetaUrlParser(html.parser.HTMLParser):
    """
    Subclass of HTMLParser that looks for the url value in the attributes of a meta tag.
    """
    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            for attr in attrs:
                if attr[0] == "content":
                    if "url=" in attr[1]:
                        url = attr[1].split("url=")
                        #print(url[-1])
                        urls.append(url[-1])
                        break


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--folder', type=str, default="submissions",
                            help="The folder of link.html files from Canvas. Defaults to: submissions/")
    arg_parser.add_argument('--outfile', type=str, default="submission_urls.csv", help="The name of the csv file to create of the urls. Defaults to submission_urls.csv")
    args = arg_parser.parse_args()
    html_parser = MetaUrlParser()
    dir_list = os.listdir(args.folder)
    for file in dir_list:
        if file.endswith("link.html"):
            f = codecs.open(os.path.join(os.path.abspath(args.folder), file), "r")
            x = f.read()
            html_parser.feed(x)
    with open(os.path.join(os.path.join(os.getcwd(), args.outfile)), "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for url in urls:
            writer.writerow([url])