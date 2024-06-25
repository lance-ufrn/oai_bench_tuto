#!/bin/bash

# Work directory path is the current directory
WORK_DIR=`pwd`

## Start the 5GC
cd $WORK_DIR/core-scripts
sudo python3 core-network.py --type stop-basic