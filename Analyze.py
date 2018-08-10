#!/usr/bin/env python

""" Plots the histogram of the speed measured by the client. Considers
    two files at a time: the file with BBR disabled and the one with
    BBR enabled, so we can compare them. """

import collections
import pylab
import os
import json
import sys

files = collections.deque(sys.argv[1:])

def parse_results(name):
    v = []
    previous_time = 0.0
    previous_bytes = 0
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
                speed = (((d["num_bytes"] - previous_bytes) * 8.0) / ((d["elapsed"] - previous_time) / 1000000000.0)) / 1000000.0
                previous_time = d["elapsed"]
                previous_bytes = d["num_bytes"]
                v.append(speed)
        return v

while True:
    nobbr_file = files.popleft()
    assert("-false.txt" in nobbr_file)
    bbr_file = files.popleft()
    assert("-true.txt" in bbr_file)

    nobbr_diff = parse_results(nobbr_file)
    bbr_diff = parse_results(bbr_file)

    pylab.hist(nobbr_diff, 16, cumulative=0, normed=1, label="!bbr")
    pylab.hist(bbr_diff, 16, cumulative=0, normed=1, label="bbr")
    pylab.legend()
    pylab.show()

