#!/usr/bin/env python

""" Similar to Analyze.py, however here we plot the histogram of the
    "number of bytes in flight" (as defined in Plot.py) """

import collections
import pylab
import os
import json
import sys

files = collections.deque(sys.argv[1:])

def parse_results(name):
    xcvec, ycvec = [], []
    xsvec, ysvec = [], []
    with open(name, "r") as sourcefp:
        for line in sourcefp:
            line = line.strip()
            index = line.find("client: ")
            is_client = index >= 0
            if index == -1:
                index = line.find("server: ")
                if index == -1:
                    continue
            line = line[index + len("server: "):]
            line = line.strip()
            print(line)
            d = json.loads(line)
            if is_client:
                xcvec.append(d["elapsed"] / 1e9)
                ycvec.append(d["num_bytes"])
            else:
                xsvec.append(d["elapsed"] / 1e9)
                ysvec.append(d["num_bytes"])
        assert(len(ysvec) == len(ycvec))
        diff = []
        for i in range(len(ysvec)):
            diff.append(ysvec[i] - ycvec[i])
        return diff

while True:
    nobbr_file = files.popleft()
    assert("-false.txt" in nobbr_file)
    bbr_file = files.popleft()
    assert("-true.txt" in bbr_file)

    nobbr_diff = parse_results(nobbr_file)
    bbr_diff = parse_results(bbr_file)

    pylab.hist(nobbr_diff, 16, normed=1, label="!bbr")
    pylab.hist(bbr_diff, 16, normed=1, label="bbr")
    pylab.legend()
    pylab.show()

