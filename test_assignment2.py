#!/usr/bin/env python3
"""Test for Assignment 2: Read input until EOF and output only the last character"""

from bf_scaffolding import bf_test

# Strategy: Keep overwriting a cell with each input character
# When we hit EOF (0), output the last non-zero character we saw
code = """
,[>[-]<[>+<-],]>.
"""

def expected(input_str: str) -> str:
    if input_str:
        return input_str[-1]
    return ""

# Test with various inputs
test_inputs = [
    "a",          # single character
    "abc",        # multiple characters
    "hello",      # word
    "x",          # different single char
    "12345",      # numbers
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
