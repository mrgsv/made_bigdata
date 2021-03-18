#! /usr/bin/python
import sys
import random


run = True
out = []
while run:
    amount_of_idxs = random.randint(1, 5)
    buffer = []
    for _ in range(amount_of_idxs):
        line = sys.stdin.readline().rstrip("\n")
        if line == "":
            run = False
            break
        line = line.split("\t")[1]
        buffer.append(line)
    if len(buffer) > 0:
        out.append(",".join(buffer))

sys.stdout.buffer.write("\n".join(out).encode())