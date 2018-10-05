#!/bin/bash

if [ -f pivoting.txt ]; then
    rm pivoting.txt;
fi
if [ -f conclusao.txt ]; then
    rm conclusao.txt;
fi
python3 src/main.py $1
rm -r src/__pycache__/
