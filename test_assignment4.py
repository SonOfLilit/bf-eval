#!/usr/bin/env python3
"""Test for Assignment 4: Output 'Y' if input is empty, 'N' if it has any characters"""

from bf_scaffolding import bf_test

# Strategy:
# - Cell 0: input character
# - Cell 1: output ('Y'=89 or 'N'=78, diff=11)
# Build 'Y', read one char, if non-zero convert to 'N' and clear input
code = """
+++++++++[>++++++++++<-]>-<,[>-----------<[-]]>.
"""

def expected(input_str: str) -> str:
    return 'Y' if len(input_str) == 0 else 'N'

# Test with empty and non-empty inputs
test_inputs = [
    "",          # empty -> Y
    "a",         # one char -> N
    "hello",     # multiple chars -> N
    "x",         # different char -> N
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
