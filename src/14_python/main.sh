#!/bin/bash

TIMES=3564
while true; do
    RES=$(python3.12 main.py input.txt $TIMES)
    if echo $RES | grep -o "#######"; then
        echo "Found ->" $TIMES
        break
    fi
    echo $TIMES
    TIMES=$((TIMES+1))
done
