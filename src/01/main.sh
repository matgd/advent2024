#!/bin/bash

LEFT=$(cat input.txt | cut -d' ' -f1 | sort -n)
RIGHT=$(cat input.txt | cut -d' ' -f4 | sort -n)
MERGED=$(paste -d' ' <(echo "$LEFT") <(echo "$RIGHT"))
echo $MERGED | rs -t -C' ' 2 1000 > input_sorted.txt  # for some reason this works only in CLI
