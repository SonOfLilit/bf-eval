#!/usr/bin/env python3
"""Test for Assignment 1: Output 'abc'"""

from bf_scaffolding import bf_test

# ASCII values: a=97, b=98, c=99
# Strategy: Build 97 efficiently, then increment twice
code = """
+++++++++[>++++++++++<-]>+++++++.+.+.
"""

# Expected behavior: always output 'abc' regardless of input
def expected(input_str: str) -> str:
    return "abc"

# Test with different inputs (output should always be 'abc')
test_inputs = [
    "",           # empty input
    "xyz",        # some input
    "hello",      # different input
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
