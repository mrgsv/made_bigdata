#! /usr/bin/python3
import sys


AMOUNT_OF_STRINGS = 10
year_2010, year_2016 = 0, 0

for line in sys.stdin:
    year, tag_counts = line.strip().split("\t", 1)
    if "2010" == year and year_2010 < AMOUNT_OF_STRINGS:
        print(year, tag_counts, sep="\t")
        year_2010 += 1
    elif "2016" == year and year_2016 < AMOUNT_OF_STRINGS:
        print(year, tag_counts, sep="\t")
        year_2016 += 1
    else:
        continue