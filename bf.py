import re


class BrainfuckInterpreter:
    """A Brainfuck interpreter with configurable step limit and logging."""

    def __init__(self, code: str, input_data: str = "", max_steps: int = 100000):
        self.code = remove_comments(code)
        self.input_data = input_data
        self.input_pos = 0
        self.output = []
        self.tape = [0] * 30000
        self.ptr = 0
        self.ip = 0  # instruction pointer
        self.max_steps = max_steps
        self.steps = 0
        self.logged_states = []

    def run(self) -> str:
        """Execute the Brainfuck code and return the output."""
        while self.ip < len(self.code) and self.steps < self.max_steps:
            self.step()
            self.steps += 1
        return "".join(self.output)

    def step(self):
        """Execute a single Brainfuck instruction."""
        if self.ip >= len(self.code):
            return

        cmd = self.code[self.ip]

        if cmd == ">":
            self.ptr += 1
            if self.ptr == len(self.tape):
                self.ptr = 0
        elif cmd == "<":
            self.ptr = self.ptr - 1
            if self.ptr < 0:
                self.ptr = len(self.tape) - 1
        elif cmd == "+":
            self.tape[self.ptr] = (self.tape[self.ptr] + 1) % 256
        elif cmd == "-":
            self.tape[self.ptr] = (self.tape[self.ptr] - 1) % 256
        elif cmd == ".":
            self.output.append(chr(self.tape[self.ptr]))
        elif cmd == ",":
            if self.input_pos < len(self.input_data):
                self.tape[self.ptr] = ord(self.input_data[self.input_pos])
                self.input_pos += 1
            else:
                self.tape[self.ptr] = 0  # EOF
        elif cmd == "!":
            self.logged_states.append(self.get_state())
        elif cmd == "[":
            if self.tape[self.ptr] == 0:
                # Jump forward to matching ]
                depth = 1
                self.ip += 1
                while depth > 0 and self.ip < len(self.code):
                    if self.code[self.ip] == "[":
                        depth += 1
                    elif self.code[self.ip] == "]":
                        depth -= 1
                    self.ip += 1
                self.ip -= 1  # Back up since we'll increment at the end
        elif cmd == "]":
            if self.tape[self.ptr] != 0:
                # Jump back to matching [
                depth = 1
                self.ip -= 1
                while depth > 0 and self.ip >= 0:
                    if self.code[self.ip] == "]":
                        depth += 1
                    elif self.code[self.ip] == "[":
                        depth -= 1
                    self.ip -= 1
                self.ip += 1  # skip the [

        self.ip += 1

    def get_state(self) -> str:
        """Return a string representation of the interpreter state."""
        # Show current position, instruction pointer, and nearby tape cells
        start = self.ptr - 5
        end = self.ptr + 6
        if start < 0:
            tape_view = self.tape[start:] + self.tape[:end]
        elif end >= len(self.tape):
            tape_view = self.tape[start:] + self.tape[: end - len(self.tape)]
        else:
            tape_view = self.tape[start:end]

        snippet = (
            self.code[max(0, self.ip - 4) : self.ip]
            + "^"
            + self.code[self.ip : self.ip + 5]
        )
        return (
            f"CODE:'{snippet}' IP:{self.ip}/{len(self.code)} PTR:{self.ptr} "
            f"TAPE[{start}:{end}]={tape_view} "
            f"STEPS:{self.steps}/{self.max_steps}"
        )


def remove_comments(code: str) -> str:
    return re.sub(r"[^+\-<>\[\],.]", "", code)
