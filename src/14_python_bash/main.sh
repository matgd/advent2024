#!/bin/bash

FILE=$1
TIMES=0
while true; do
    RES=$(python3.12 main.py $1 $TIMES)
    if echo $RES | grep -o "#########"; then
        echo "Found ->" $TIMES
        break
    fi
    echo $TIMES
    TIMES=$((TIMES+1))
done

# loop:
# ./main.sh inputprogress.txt
# if starts slowing down exec
# python3.12 main.py inputprogress.txt $TIMES save
# run again and if founds false positive run as above but $TIMES + $THIS_RUN_TIMES + 1
# add all times to have res
