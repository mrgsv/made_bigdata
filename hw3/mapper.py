#! /usr/bin/python3
import sys
import re

import lxml.etree as et


for line in sys.stdin:
    line = line.strip().strip("\n")
    if line[:4] != "<row":
        continue
    root = et.fromstring(line)
    try:
        year = root.xpath("@CreationDate")[0][:4]
        if year not in ("2010", "2016"):
            continue

        tags = filter(lambda x: len(x) > 0, re.split(r"<|>", root.xpath("@Tags")[0]))
        for tag in tags:
            print(year, tag, "1", sep="\t")
    except IndexError:
        continue
