# with open("tinput.txt", "r") as f:
#     r = f.readlines()
#     tr = list(zip(*r))
#     for l in tr[:-1]:
#         print("".join(l))

# import sys
# lines = sys.stdin.readlines()
# for l in list(zip(*lines))[:-1]:
#     print("".join(l))

# import sys
# from itertools import zip_longest
# lines = sys.stdin.readlines()
# for l in list(zip_longest(*lines, fillvalue="")):
#     print("".join(l))

# import sys
# from itertools import chain
# lines = [l.strip() for l in sys.stdin.readlines()]
# length = len(lines)
# oneline = list("".join(lines))
# curr_index = 1
# for i in chain.from_iterable((range(0, length), range(length, 0, -1))):
#     curr_index += i
#     oneline.insert(curr_index, '\n')

# print("".join(oneline))

import sys
from itertools import zip_longest
lines = sys.stdin.readlines()
for i in range(len(lines)):
    lines[i] = i * " " + lines[i]
for l in list(zip_longest(*lines, fillvalue="")):
    ln = "".join(l)
    ln = ln.replace("\n" ,"")
    print(ln.strip())

# import sys
# from itertools import zip_longest
# lines = sys.stdin.readlines()
# for i in range(len(lines)):
#     lines[i] = (len(lines) - i) * " " + lines[i]
# for l in list(zip_longest(*lines, fillvalue="")):
#     print("".join(l))
