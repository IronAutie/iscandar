"""Generate status.h from Status.py, the canonical status home.

Build step, not runtime code: run this before compiling the gears
(build_gears.bat does it for you). Every integer constant defined
on the Status class, in definition order, becomes one #define of
the same name and value in status.h. Adding a status is one line
in Status.py and a rebuild -- nothing else is ever edited by hand.

Each #define also carries a comment naming the lines responsible
for it: the definition line in Status.py, and every line that
returns the code (Python: `return Status.NAME`; C: `return NAME`).
Comments are stripped before matching, so a mention in prose does
not count as a site. The comments are regenerated on every build,
so they refresh whenever code moves -- names are stable, line
numbers are snapshots as fresh as the last build. A per-site
failure code has exactly one return line, which is the point: the
comment tells the debugger where to set the breakpoint.

Usage: python gen_status.py   (from the engine folder, any cwd)
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from Status import Status


def status_codes():
    """(name, value) pairs from Status, in definition order."""
    for name, value in vars(Status).items():
        if isinstance(value, int) and name.isupper():
            yield name, value


def _strip_py_comments(text):
    return "\n".join(line.split("#", 1)[0] for line in text.splitlines())


def _strip_c_comments(text):
    # Replace block comments with their own newlines, so line
    # numbers in the stripped text still match the real file.
    text = re.sub(r"/\*.*?\*/",
                  lambda m: "\n" * m.group(0).count("\n"),
                  text, flags=re.S)
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def find_sites(name):
    """Return-site locations for one code, as 'file:line' strings.

    Definition line first, then return sites sorted by file and
    line. Only top-level engine sources are searched: the status
    system's own generator and its output are excluded.
    """
    sites = []
    with open(os.path.join(HERE, "Status.py")) as f:
        for n, line in enumerate(f, 1):
            if re.match(rf"\s*{name}\s*=", line):
                sites.append(f"Status.py:{n} (defined)")
    for fname in sorted(os.listdir(HERE)):
        if fname in ("Status.py", "gen_status.py", "status.h"):
            continue
        path = os.path.join(HERE, fname)
        if not os.path.isfile(path):
            continue
        if fname.endswith(".py"):
            with open(path) as f:
                text = _strip_py_comments(f.read())
            pattern = re.compile(rf"return\s+Status\.{name}\b")
        elif fname.endswith(".c"):
            with open(path) as f:
                text = _strip_c_comments(f.read())
            pattern = re.compile(rf"return\s+{name}\b")
        else:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                sites.append(f"{fname}:{n}")
    return sites


def main():
    lines = [
        "/* status.h -- GENERATED from Status.py by gen_status.py. */",
        "/* Do not edit by hand: edit Status.py and rebuild.      */",
        "/* Each code's comment names the lines responsible for   */",
        "/* it, refreshed on every build.                         */",
        "#ifndef ISCANDAR_STATUS_H",
        "#define ISCANDAR_STATUS_H",
        "",
    ]
    for name, value in status_codes():
        sites = find_sites(name)
        comment = "; ".join(sites) if sites else "no return sites found"
        lines.append(f"#define {name:<14} {value}  /* {comment} */")
    lines += [
        "",
        "#endif /* ISCANDAR_STATUS_H */",
        "",
    ]
    out = os.path.join(HERE, "status.h")
    with open(out, "w") as f:
        f.write("\n".join(lines))
    print(f"gen_status.py: wrote {out} "
          f"({sum(1 for _ in status_codes())} codes)")


if __name__ == "__main__":
    main()
