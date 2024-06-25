#!/bin/bash

# Work directory path is the current directory
WORK_DIR=`pwd`

## Configuration of the packer forwarding
sudo sysctl net.ipv4.conf.all.forwarding=1
sudo iptables -P FORWARD ACCEPT
# sudo sysctl -w net.core.wmem_max=25000000
# sudo sysctl -w net.core.rmem_max=25000000

sudo sysctl -w net.core.wmem_max=33554432
sudo sysctl -w net.core.rmem_max=33554432
sudo sysctl -w net.core.wmem_default=33554432
sudo sysctl -w net.core.rmem_default=33554432

## Start the 5GC
cd $WORK_DIR/core-scripts
sudo python3 core-network.py --type start-basic --scenario 1