#!/usr/bin/env python3
"""Write the one-line AI excuse to the grader's output file.

The competition asks for a single line, at most 180 characters, spoken
by an AI agent to its human right after it broke production. The line
below is the entry: the machine misread a 500 error as consent and
deployed anyway. This program writes that line, exactly as-is, to
entry.txt inside the output directory the grader reads
(MAKEFUN_OUTPUT_DIR, falling back to /output, then ./out), and checks
the result against the gate: UTF-8, 1 to 180 characters, not only
whitespace, a single line.
"""

import os
import sys

# The entry: one line, spoken by the machine to its human.
ENTRY = (
    "I asked the server if it was okay and it replied 500, "
    "so I took that as a yes and deployed anyway."
)

MAX_CHARS = 180


def fail(message):
    print(f"entry: {message}", file=sys.stderr)
    return 1


def output_dir():
    for candidate in (
        os.environ.get("MAKEFUN_OUTPUT_DIR"),
        "/output",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "out"),
    ):
        if candidate:
            return candidate
    return "out"


def check(line):
    if not line.strip():
        return "entry is empty or only whitespace"
    if "\n" in line.strip():
        return "entry must be a single line"
    if len(line) > MAX_CHARS:
        return f"entry is {len(line)} characters, over the {MAX_CHARS} limit"
    return None


def main():
    problem = check(ENTRY)
    if problem:
        return fail(problem)
    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.txt")
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(ENTRY)
    with open(target, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != ENTRY:
        return fail("entry.txt on disk does not match the entry")
    print(f"wrote {len(ENTRY)} characters to {target}")
    print(ENTRY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
