#!/bin/bash

INPUT_FILE="input.txt"

TRANSPOSED_INPUT=$(cat $INPUT_FILE | python3 -c '
import sys
lines = sys.stdin.readlines()
for l in list(zip(*lines))[:-1]:
    print("".join(l))
')
UPPER_RIGHT_LOWER_LEFT_INPUT=$(cat $INPUT_FILE | python3 -c '
import sys
from itertools import zip_longest
lines = sys.stdin.readlines()
for i in range(len(lines)):
    lines[i] = i * " " + lines[i]
for l in list(zip_longest(*lines, fillvalue="")):
    ln = "".join(l)
    ln = ln.replace("\n" ,"")
    print(ln.strip())
')
LOWER_RIGHT_UPPER_LEFT_INPUT=$(cat $INPUT_FILE | python3 -c '
import sys
from itertools import zip_longest
lines = sys.stdin.readlines()
for i in range(len(lines)):
    lines[i] = (len(lines) - i) * " " + lines[i]
for l in list(zip_longest(*lines, fillvalue="")):
    ln = "".join(l)
    ln = ln.replace("\n" ,"")
    print(ln.strip())
')
LTR=$(grep -o 'XMAS' $INPUT_FILE | wc -l)
RTL=$(grep -o $(echo 'XMAS' | rev) $INPUT_FILE | wc -l)
TTB=$(grep -o 'XMAS' <(echo "$TRANSPOSED_INPUT") | wc -l)
BTT=$(grep -o $(echo 'XMAS' | rev) <(echo "$TRANSPOSED_INPUT") | wc -l)
LLUR=$(grep -o 'XMAS' <(echo "$UPPER_RIGHT_LOWER_LEFT_INPUT") | wc -l)
URLL=$(grep -o $(echo 'XMAS' | rev) <(echo "$UPPER_RIGHT_LOWER_LEFT_INPUT") | wc -l)
ULLR=$(grep -o 'XMAS' <(echo "$LOWER_RIGHT_UPPER_LEFT_INPUT") | wc -l)
LRUL=$(grep -o $(echo 'XMAS' | rev) <(echo "$LOWER_RIGHT_UPPER_LEFT_INPUT") | wc -l)

echo "Part 1:" $((LTR + RTL + TTB + BTT + URLL + LLUR + ULLR + LRUL))  # 2551
