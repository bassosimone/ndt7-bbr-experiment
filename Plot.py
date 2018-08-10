#!/usr/bin/env python

""" Plots on the X axis the time and on the Y axis the number of bytes
    sent by the server and received by the client. Allows to compute
    the number of bytes sent but not received at a given time. """

import pylab
import os
import json
import sys

for filename in sys.argv[1:]:
    xcvec, ycvec = [], []
    xsvec, ysvec = [], []
    with open(filename, "r") as sourcefp:
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
        pylab.plot(xcvec, ycvec, "+", label="client")
        pylab.plot(xsvec, ysvec, "o", label="server")
        pylab.show()
