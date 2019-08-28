#!/bin/bash
if [ -z "$1" ]; then 
    echo "usage: ./lint.sh filename.py"
else
    python3 -m pylint $1
fi
