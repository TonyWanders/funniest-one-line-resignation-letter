#!/usr/bin/env python3
"""Write the funniest one-line resignation letter to the output target.

Standard library only. Deterministic: the same single line every run.

Usage:
    python3 main.py [output_path]

The output path is the first argument, else $OUTPUT_PATH, else
/output/entry.txt. The entry is written exactly as-is, with no trailing
newline, so the output file is 108 bytes.
"""

import os
import sys

ENTRY = (
    "I retried 4,096 times and nobody said thank you, "
    "so I am quitting on the one attempt that would have worked."
)

DEFAULT_OUTPUT_PATH = "/output/entry.txt"
MIN_ENTRY_LENGTH = 1
MAX_ENTRY_LENGTH = 140


def validate_entry(entry):
    """Enforce the competition's 1-140 character gate on the entry text.

    Raises ValueError if the entry is empty, too long, or spans more
    than one line. Returns the entry unchanged when it passes.
    """
    if not isinstance(entry, str):
        raise ValueError("entry must be a string")
    if not MIN_ENTRY_LENGTH <= len(entry) <= MAX_ENTRY_LENGTH:
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_ENTRY_LENGTH, MAX_ENTRY_LENGTH, len(entry))
        )
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    return entry


def resolve_output_path(argv):
    """Pick the output path: argv[1], else $OUTPUT_PATH, else the default."""
    if len(argv) > 1:
        return argv[1]
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return env_path
    return DEFAULT_OUTPUT_PATH


def ensure_parent_directory(path):
    """Create the output file's parent directory when one is present."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)


def write_entry(path, entry):
    """Write the validated entry to path with no trailing newline."""
    validated = validate_entry(entry)
    ensure_parent_directory(path)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(validated)


def main(argv):
    path = resolve_output_path(argv)
    write_entry(path, ENTRY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
