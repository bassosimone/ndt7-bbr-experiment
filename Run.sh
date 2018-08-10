#!/bin/sh
# Script used to gather data.
set -ex
run=0
hostname=ndt-iupui-mlab4v4-lga0t.measurement-lab.org
while [ $run -lt 7 ]; do
  ndt-cloud-client -hostname $hostname -port 3020 2>&1 | tee res-$run-false.txt
  sleep 1
  ndt-cloud-client -hostname $hostname -port 3021 2>&1 | tee res-$run-true.txt
  sleep 1
  run=$(($run + 1))
done
