#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--dist", default="dist")
parser.add_argument("--ref", default="HEAD")
parser.add_argument("--allow-dirty", action="store_true")
args = parser.parse_args()

root = Path(subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], text=True
).strip())

if not args.allow_dirty and subprocess.check_output(
    ["git", "status", "--porcelain"], cwd=root, text=True
).strip():
    raise SystemExit("ERROR: working tree is not clean")

meta = json.loads((root / "module.json").read_text(encoding="utf-8"))
output = root / args.dist
output.mkdir(parents=True, exist_ok=True)

for name in (f"{meta['id']}-{meta['version']}.zip", f"{meta['id']}.zip"):
    subprocess.run(
        [
            "git", "archive", "--format=zip", f"--prefix={meta['id']}/",
            "-o", str(output / name), args.ref
        ],
        cwd=root,
        check=True
    )
