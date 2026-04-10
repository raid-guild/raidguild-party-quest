#!/usr/bin/env python3
import random
import sys


def main() -> int:
    sides = 20
    count = 1
    mod = 0

    args = sys.argv[1:]
    if args:
        try:
            count = max(1, int(args[0]))
        except ValueError:
            print("usage: d20.py [count] [modifier]", file=sys.stderr)
            return 2
    if len(args) > 1:
        try:
            mod = int(args[1])
        except ValueError:
            print("usage: d20.py [count] [modifier]", file=sys.stderr)
            return 2

    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls) + mod
    crit = " CRIT!" if count == 1 and rolls[0] == 20 else ""
    fumble = " FUMBLE!" if count == 1 and rolls[0] == 1 else ""
    mod_text = f" {mod:+d}" if mod else ""

    print(f"d20 rolls: {rolls} | total: {sum(rolls)}{mod_text} = {total}{crit}{fumble}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
