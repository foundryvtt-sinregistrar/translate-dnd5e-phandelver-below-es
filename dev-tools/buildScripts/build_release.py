#!/usr/bin/env python3
import argparse
import json
import subprocess
import re
import zipfile
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

commit = subprocess.check_output(
    ["git", "rev-parse", "--verify", "--end-of-options", f"{args.ref}^{{commit}}"],
    cwd=root, text=True
).strip()
manifest = subprocess.check_output(["git", "show", f"{commit}:module.json"], cwd=root)
meta = json.loads(manifest)
if not re.fullmatch(r"[a-z0-9-]+", meta['id']) or not re.fullmatch(r"[0-9]+(?:\.[0-9]+){2}", meta['version']):
    raise SystemExit("ERROR: unsafe module id or version")
if args.ref.startswith('v') and args.ref != f"v{meta['version']}":
    raise SystemExit("ERROR: release tag does not match archived module version")
output = root / args.dist
output.mkdir(parents=True, exist_ok=True)

for name in (f"{meta['id']}-{meta['version']}.zip", f"{meta['id']}.zip"):
    subprocess.run(
        [
            "git", "archive", "--format=zip", f"--prefix={meta['id']}/",
            "-o", str(output / name), commit
        ],
        cwd=root,
        check=True
    )
    with zipfile.ZipFile(output / name) as archive:
        prefix = f"{meta['id']}/"
        allowed = {'module.json', 'README.md', 'CHANGELOG.md', 'LICENSE.md', 'compendium', 'lang', 'scripts'}
        for member in archive.namelist():
            relative = member.removeprefix(prefix)
            if not member.startswith(prefix) or '..' in relative.split('/'):
                raise SystemExit(f"ERROR: invalid archive member: {member}")
            if relative and relative.split('/')[0] not in allowed:
                raise SystemExit(f"ERROR: unexpected distribution file: {member}")
        archived_manifest = archive.read(prefix + 'module.json')
        # git archive may honor CRLF conversion on Windows.
        if archived_manifest.replace(b'\r\n', b'\n') != manifest.replace(b'\r\n', b'\n'):
            raise SystemExit("ERROR: archive manifest differs from selected ref")
        for path in meta.get('esmodules', []) + [entry['path'] for entry in meta.get('languages', [])]:
            archive.getinfo(prefix + path)
        for member in archive.namelist():
            if member.endswith('.json'):
                json.loads(archive.read(member))
        print(f"Verified {name}: {len(archive.namelist())} members from {commit[:12]}")
(output / 'module.json').write_bytes(archived_manifest)
