#!/bin/bash

TRANSPOSED_INPUT=$(cat tinput.txt | python3 -c '
import sys
lines = sys.stdin.readlines()
for l in list(zip(*lines))[:-1]:
    print("".join(l))
')
UPPER_RIGHT_LOWER_LEFT_INPUT=$(cat tinput.txt | python3 -c '
import sys
from itertools import zip_longest
lines = sys.stdin.readlines()
for i in range(len(lines)):
    lines[i] = i * " " + lines[i]
for l in list(zip_longest(*lines, fillvalue="")):
    print("".join(l))
')
LOWER_RIGHT_UPPER_LEFT_INPUT=$(cat tinput.txt | python3 -c '
import sys
from itertools import zip_longest
lines = sys.stdin.readlines()
for i in range(len(lines)):
    lines[i] = (len(lines) - i) * " " + lines[i]
for l in list(zip_longest(*lines, fillvalue="")):
    print("".join(l))
')
LTR=$(grep -o 'XMAS' tinput.txt | wc -l)
RTL=$(grep -o $(echo 'XMAS' | rev) tinput.txt | wc -l)
TTB=$(grep -o 'XMAS' <(echo "$TRANSPOSED_INPUT") | wc -l)
BTT=$(grep -o $(echo 'XMAS' | rev) <(echo "$TRANSPOSED_INPUT") | wc -l)
LLUR=$(grep -o 'XMAS' <(echo "$UPPER_RIGHT_LOWER_LEFT_INPUT") | wc -l)
URLL=$(grep -o $(echo 'XMAS' | rev) <(echo "$UPPER_RIGHT_LOWER_LEFT_INPUT") | wc -l)
ULLR=$(grep -o 'XMAS' <(echo "$LOWER_RIGHT_UPPER_LEFT_INPUT") | wc -l)
LRUL=$(grep -o $(echo 'XMAS' | rev) <(echo "$LOWER_RIGHT_UPPER_LEFT_INPUT") | wc -l)

echo $((LTR + RTL + TTB + BTT + URLL + LLUR + ULLR + LRUL))
