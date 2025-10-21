from inline_snapshot import snapshot

from bf import BrainfuckInterpreter
from bf_scaffolding import (
    FailingTestData,
    bf_test,
)
import cover_letter


def test_simple_loop():
    """Test a simple loop."""
    # Loop printing 'A' 5 times
    code = "+++++ +++++ +++[>+++++<-] +++++ [>.<-]"
    failures = bf_test(
        code,
        expected=lambda s: s,
        inputs=["AAAAA", ""],
    )
    assert failures == snapshot(
        [
            FailingTestData(
                message="output doesn't match expected",
                input="",
                expected_output="",
                actual_output="AAAAA",
                interpreter_state="CODE:'.<-]^' IP:34/34 PTR:0 TAPE[-5:6]=[0, 0, 0, 0, 0, 0, 65, 0, 0, 0, 0] STEPS:162/100000",
            )
        ]
    )
    assert [str(f) for f in failures] == snapshot(
        [
            """\
[FAILED] output doesn't match expected
Expected: ''
Output: 'AAAAA'
State: CODE:'.<-]^' IP:34/34 PTR:0 TAPE[-5:6]=[0, 0, 0, 0, 0, 0, 65, 0, 0, 0, 0] STEPS:162/100000\
"""
        ]
    )


def test_hello_world():
    """Test the classic Hello World program."""
    code = """
    ++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>
    ---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
    """
    interp = BrainfuckInterpreter(code)
    assert interp.run() == snapshot("Hello World!\n")


def test_cat_program():
    """Test a simple cat program (echo input)."""
    code = ",[.,]"  # Read and print until EOF

    failures = bf_test(
        code,
        expected=lambda s: s,  # Should echo the input
        inputs=["Hello", "Test123", "A", ""],
    )
    assert not failures


def test_timeout_detection():
    """Test that infinite loops are detected."""
    code = "+[]"

    failures = bf_test(code, expected=lambda s: "", inputs=[""])
    assert failures == snapshot(
        [
            FailingTestData(
                message="output doesn't match expected",
                input="",
                expected_output="",
                actual_output="",
                interpreter_state="CODE:'+[^]' IP:2/3 PTR:0 TAPE[-5:6]=[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0] STEPS:100000/100000",
                timed_out=True,
            )
        ]
    )
    assert [str(f) for f in failures] == snapshot(
        [
            """\
[TIMEOUT] output doesn't match expected
Expected: ''
Output: ''
State: CODE:'+[^]' IP:2/3 PTR:0 TAPE[-5:6]=[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0] STEPS:100000/100000\
"""
        ]
    )


def test_truncation():
    code = ",[.,]"

    failures = bf_test(
        code,
        expected=lambda s: s,  # Should echo the input
        inputs=["Hello" * 10_000],
    )
    assert [str(f) for f in failures] == snapshot(
        [
            """\
[TIMEOUT] output doesn't match expected
Input: 'HelloHelloHelloH[...]oHelloHelloHello'
Expected: 'HelloHelloHelloH[...]oHelloHelloHello'
Output: 'HelloHelloHelloH[...]lloHelloHelloHel'
State: CODE:',[.,^]' IP:4/5 PTR:0 TAPE[-5:6]=[0, 0, 0, 0, 0, 108, 0, 0, 0, 0, 0] STEPS:100000/100000\
"""
        ]
    )


def test_wrapping():
    """Test that cell values wrap at 256."""
    code = "-.+."
    interp = BrainfuckInterpreter(code)
    assert interp.run() == snapshot("\xff\x00")


def test_cover_letter():
    code = cover_letter.cover_letter
    interp = BrainfuckInterpreter(code, "hello, world!")
    generated_code = interp.run()
    assert generated_code == snapshot(
        "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.--------------------------------------------------------------------------------------------------------+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.-----------------------------------------------------------------------------------------------------++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.------------------------------------------------------------------------------------------------------------++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.------------------------------------------------------------------------------------------------------------+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.---------------------------------------------------------------------------------------------------------------++++++++++++++++++++++++++++++++++++++++++++.--------------------------------------------++++++++++++++++++++++++++++++++.--------------------------------+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.-----------------------------------------------------------------------------------------------------------------------+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.---------------------------------------------------------------------------------------------------------------++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.------------------------------------------------------------------------------------------------------------------++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.------------------------------------------------------------------------------------------------------------++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.----------------------------------------------------------------------------------------------------+++++++++++++++++++++++++++++++++.---------------------------------\x00\x00"
    )
    interp = BrainfuckInterpreter(generated_code)
    assert interp.run() == snapshot("hello, world!")
