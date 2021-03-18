#! /usr/bin/python
import sys
import random


out = []
for line in sys.stdin:
    prefix = random.randint(1, 100)
    out.append(str(prefix) + "\t" + line.rstrip("\n"))

sys.stdout.buffer.write("\n".join(out).encode())