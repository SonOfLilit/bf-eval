#!/usr/bin/env python3
"""Test for Assignment 3: Read input until EOF and output the count of characters as a single digit (0-9)"""

from bf_scaffolding import bf_test

# Strategy:
# - Cell 0: temp
# - Cell 1: counter starting at ASCII '0' (48)
# - Cell 2: input character
# Build 48 in cell 1, then read into cell 2, increment cell 1 for each char
code = """
++++++++[>++++++<-]>>,
[<+>,]
<.
"""

def expected(input_str: str) -> str:
    count = len(input_str)
    return str(count)

# Test with various inputs (max 9 chars since output is single digit)
test_inputs = [
    "",          # 0 characters
    "a",         # 1 character
    "ab",        # 2 characters
    "abc",       # 3 characters
    "hello",     # 5 characters
    "world!",    # 6 characters
    "123456789", # 9 characters (max single digit)
]

failures = bf_test(code.strip(), expected, test_inputs)

if failures:
    for failure in failures:
        print(failure)
    print(f"\n{len(failures)} test(s) failed!")
    exit(1)
else:
    print(f"All {len(test_inputs)} tests passed!")
    print("Solution:", repr(code.strip()))
