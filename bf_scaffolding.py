from pydantic import BaseModel, Field
from typing import Callable, Iterable, Optional

from bf import BrainfuckInterpreter


class State(BaseModel):
    tape: Optional[list[int]] = None
    ptr: Optional[int] = None


class FailingTestData(BaseModel):
    """Data about a failing test case."""

    message: str
    macro: Optional[str] = None
    input: str
    before: Optional[State] = None
    expected_output: Optional[str]
    actual_output: str
    after: Optional[State] = None
    interpreter_state: str
    timed_out: bool = False
    logged_states: list[str] = Field(default_factory=list)

    def __str__(self) -> str:
        """Format the failure data with 512 character limits."""
        status = "[TIMEOUT]" if self.timed_out else "[FAILED]"
        data: Iterable[str | None] = (
            f"{status} {self.message}",
            f"Macro: {self.macro}" if self.macro else None,
            self.before and f"Before: PTR:{self.before.ptr} TAPE:{self.before.tape}",
            self.input and f"Input: {repr(truncate(self.input))}",
            f"Expected: {repr(truncate(self.expected_output))}"
            if self.expected_output is not None
            else None,
            f"Output: {repr(truncate(self.actual_output))}"
            if self.actual_output or self.expected_output is not None
            else None,
            f"State: {self.interpreter_state}",
            self.after
            and f"Expected state: PTR:{self.after.ptr} TAPE:{self.after.tape}",
            ("Logs: " + "\n       ".join(self.logged_states))
            if self.logged_states
            else None,
            "",
        )
        return "\n".join(filter(None, data))


def truncate(s: str, n=32) -> str:
    """Truncate a string to a maximum length."""
    n2 = n // 2
    if len(s) < n:
        return s
    return s[: n - n2] + "[...]" + s[-n2:]


def truncate_list(items: list, n=6) -> list:
    n2 = n // 2
    if len(items) < n:
        return items
    return items[: n - n2] + ["..."] + items[-n2:]


def bf_test(
    code: str, expected: Callable[[str], str], inputs: list[str]
) -> list[FailingTestData]:
    """
    Test a Brainfuck program with multiple inputs.

    Args:
        code: The Brainfuck program to test
        expected: A function that takes input and returns expected output
        inputs: List of input strings to test with

    Returns:
        Dictionary of failing test data, keyed by test identifier
    """
    failures = []

    for input_str in inputs:
        interp = BrainfuckInterpreter(code, input_str)
        actual_output = interp.run()
        expected_output = expected(input_str)

        timed_out = interp.steps >= interp.max_steps

        if actual_output != expected_output or timed_out:
            failures.append(
                FailingTestData(
                    message="output doesn't match expected",
                    input=input_str,
                    expected_output=expected_output,
                    actual_output=actual_output,
                    interpreter_state=interp.get_state(),
                    timed_out=timed_out,
                    logged_states=interp.logged_states,
                )
            )

    return failures
