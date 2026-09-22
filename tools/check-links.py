#!/usr/bin/env python3
"""Check every relative link in the tracked markdown.

Cross-references are how this repository holds together - a decision cited from a
drawing, a SPECS.md cited from the BOM - and they are exactly what breaks when a
file moves. Run it after any move or rename.

A link into vendor/ is reported separately: those files are real but untracked,
so the link works on this machine and not in a fresh clone.
"""
import os, posixpath, re, subprocess, sys

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
LINK = re.compile(r"\]\(([^)]+)\)")
SKIP = re.compile(r"^(https?:|mailto:|#|~)")

files = subprocess.run(["git", "ls-files", "*.md"],
                       capture_output=True, text=True).stdout.split()
broken, vendor, checked = [], [], 0

for f in files:
    for m in LINK.finditer(open(f).read()):
        t = m.group(1)
        if SKIP.match(t):
            continue
        checked += 1
        target = posixpath.normpath(
            posixpath.join(posixpath.dirname(f), t.partition("#")[0]))
        if target.startswith("vendor/"):
            vendor.append((f, t))
        elif not os.path.exists(target):
            broken.append((f, t, target))

for f, t, target in broken:
    print("BROKEN  %s -> %s  (no %s)" % (f, t, target))
for f, t in vendor:
    print("VENDOR  %s -> %s  (untracked; absent in a fresh clone)" % (f, t))

print("\n%d relative links checked in %d files: %d broken, %d into vendor/"
      % (checked, len(files), len(broken), len(vendor)))
sys.exit(1 if broken else 0)
