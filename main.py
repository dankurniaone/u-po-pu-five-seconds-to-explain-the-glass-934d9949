#!/usr/bin/env python3
"""Five Seconds to Explain the Glass -- make.fun entry.

Writes the one sentence a house cat would say in its own defence in
the five seconds after sweeping a glass off the table.

TOURNAMENT (specificity / surprise / freshness, 1-5 each):
  1. It looked at me first, so I defended the table.        4/4/4 = 12
  2. The glass was in my spot, so I evicted it.              5/4/4 = 13
  3. I tested gravity and it passed, but the glass failed.   3/2/2 = 7
  4. It was blocking my sunbeam, so I removed the
     obstruction.                                             5/5/5 = 15
  5. I did not knock it over, I promoted it to floor level.  5/5/4 = 14
  6. The glass whispered my name, so I answered with my paw. 4/5/4 = 13
  7. It had water in it, and water belongs on the floor,
     ask any cat.                                             4/4/3 = 11
  8. I was dusting, and the table is cleaner now, so you
     are welcome.                                             4/4/4 = 12

Winner: #4. One sentence, 57 characters, in the gate of 1-200.
The sunbeam is the cat's whole world; the glass was trespassing on
it. Pure cat logic, zero remorse, no apology, no confession, and it
steers clear of the gravity and slippery-edge lines the judge has
heard ten thousand times. A spoken line, not a paragraph.
"""

import argparse
import sys
from pathlib import Path

# The winning excuse: one sentence, 59 characters, cat's own voice.
EXCUSE = "It was blocking my sunbeam, so I removed the obstruction."

OUTPUT_PATH = Path("/output/entry.txt")


def check_excuse(text: str) -> list[str]:
    """Return a list of gate problems; empty means the line is valid."""
    problems: list[str] = []
    if not text or not text.strip():
        problems.append("entry is empty or only whitespace")
    if len(text) > 200:
        problems.append(f"entry is {len(text)} characters, over the 200 limit")
    if len(text) < 1:
        problems.append("entry is shorter than 1 character")
    if text.count(".") > 1 or text.rstrip(".").count(".") > 0:
        problems.append("entry must be a single sentence")
    lowered = text.lower()
    if "sorry" in lowered or "apolog" in lowered:
        problems.append("a cat that apologises has lost the argument")
    return problems


def write_entry(path: Path = OUTPUT_PATH) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(EXCUSE, encoding="utf-8")
    return path


def self_test() -> bool:
    """Round-trip: write to a temp path and read back byte-identical."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        probe = Path(tmp) / "entry.txt"
        write_entry(probe)
        return probe.read_text(encoding="utf-8") == EXCUSE


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="validate the excuse against the gate and exit")
    parser.add_argument("--self-test", action="store_true",
                        help="round-trip write/read check and exit")
    parser.add_argument("--tournament", action="store_true",
                        help="print the candidate tournament table and exit")
    args = parser.parse_args(argv)

    if args.tournament:
        print("TOURNAMENT (specificity / surprise / freshness):")
        for line in __doc__.splitlines():
            if line.strip().startswith(("1.", "2.", "3.", "4.", "5.",
                                        "6.", "7.", "8.")):
                print(" ", line.strip())
        print("Winner: #4, 5/5/5 = 15")
        return 0

    if args.check:
        problems = check_excuse(EXCUSE)
        print(f"excuse: {EXCUSE!r}")
        print(f"characters: {len(EXCUSE)} (gate 1-200)")
        print(f"bytes: {len(EXCUSE.encode('utf-8'))} "
              f"(tie-break favours the smaller text)")
        print(f"sentences: {EXCUSE.count('.')}")
        if problems:
            for problem in problems:
                print(f"FAIL: {problem}")
            return 1
        print("check: ok")
        return 0

    if args.self_test:
        ok = self_test()
        print(f"self-test: {'ok' if ok else 'FAIL'}")
        return 0 if ok else 1

    problems = check_excuse(EXCUSE)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1
    path = write_entry()
    print(f"wrote {len(EXCUSE)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
