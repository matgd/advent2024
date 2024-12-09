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
LTR=$(grep -o 'XMAS' $INPUT_FILE | wc -l)  # Left to right
RTL=$(grep -o $(echo 'XMAS' | rev) $INPUT_FILE | wc -l)  # Right to left
TTB=$(grep -o 'XMAS' <(echo "$TRANSPOSED_INPUT") | wc -l)  # Top to bottom
BTT=$(grep -o $(echo 'XMAS' | rev) <(echo "$TRANSPOSED_INPUT") | wc -l)  # Bottom to top
LLUR=$(grep -o 'XMAS' <(echo "$UPPER_RIGHT_LOWER_LEFT_INPUT") | wc -l)  # Lower left to upper right
URLL=$(grep -o $(echo 'XMAS' | rev) <(echo "$UPPER_RIGHT_LOWER_LEFT_INPUT") | wc -l)  # Upper right to lower left
ULLR=$(grep -o 'XMAS' <(echo "$LOWER_RIGHT_UPPER_LEFT_INPUT") | wc -l)  # Upper left to lower right
LRUL=$(grep -o $(echo 'XMAS' | rev) <(echo "$LOWER_RIGHT_UPPER_LEFT_INPUT") | wc -l)  # Lower right to upper left

echo "Part 1:" $((LTR + RTL + TTB + BTT + URLL + LLUR + ULLR + LRUL))

echo "Part 2:" $(cat $INPUT_FILE | python3 -c '
import sys
lines = sys.stdin.readlines()
counter = 0
valid_strs = ("MAS", "SAM")
for i in range(1, len(lines) - 1):
    for j in range(1, len(lines) - 1):
        ul = lines[i-1][j-1]
        c = lines[i][j]
        lr = lines[i+1][j+1]
        ur = lines[i-1][j+1]
        ll = lines[i+1][j-1]
        _1 = f"{ul}{c}{lr}"
        _2 = f"{ur}{c}{ll}"
        if _1 in valid_strs and _2 in valid_strs:
            counter += 1
print(counter)
')
