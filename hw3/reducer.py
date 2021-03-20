#! /usr/bin/python3
import sys


current_year_tag = None
year_tag_count = 0

for line in sys.stdin:
    year_tag, counts = line.rsplit("\t", 1)
    counts = int(counts)
    if year_tag == current_year_tag:
        year_tag_count += counts
    else:
        if current_year_tag:
            print(current_year_tag, year_tag_count, sep="\t")
        current_year_tag = year_tag
        year_tag_count = counts

if current_year_tag:
    print(current_year_tag, year_tag_count, sep="\t")