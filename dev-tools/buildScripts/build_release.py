#!/usr/bin/env python3
"""Build and validate a Foundry module archive from one immutable Git commit."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT_FILES = {"module.json", "README.md", "README.en.md", "CHANGELOG.md", "LICENSE.md"}
PAYLOAD_DIRS = {"compendium", "lang", "scripts"}
SAFE_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
SAFE_VERSION = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?")


def git(root: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=root, check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout


def resolve_commit(root: Path, ref: str) -> str:
    return git(root, "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}").decode().strip()


def load_manifest(root: Path, commit: str) -> tuple[bytes, dict]:
    manifest = git(root, "show", f"{commit}:module.json")
    meta = json.loads(manifest)
    if not isinstance(meta, dict):
        raise ValueError("module.json must be an object")
    if not isinstance(meta.get("id"), str) or not SAFE_NAME.fullmatch(meta["id"]):
        raise ValueError("Invalid module id")
    if not isinstance(meta.get("version"), str) or not SAFE_VERSION.fullmatch(meta["version"]):
        raise ValueError("Invalid module version")
    return manifest, meta


def load_profile(root: Path, commit: str) -> dict:
    path = "dev-tools/buildScripts/release-profile.json"
    profile = {"archive_name": "", "manifest_channel": "latest", "variant": "standard"}
    if git(root, "ls-tree", "--name-only", commit, "--", path).strip():
        custom = json.loads(git(root, "show", f"{commit}:{path}"))
        if not isinstance(custom, dict) or custom.keys() - profile.keys():
            raise ValueError("Invalid release profile")
        profile.update(custom)
    if not isinstance(profile["archive_name"], str) or (profile["archive_name"] and not SAFE_NAME.fullmatch(profile["archive_name"])):
        raise ValueError("Invalid profile archive name")
    if profile["manifest_channel"] not in {"latest", "main"} or profile["variant"] not in {"standard", "text-only"}:
        raise ValueError("Invalid release profile channel or variant")
    return profile


def check_release(root: Path, ref: str, commit: str, meta: dict, release_tag: str | None,
                  archive_name: str | None = None, manifest_channel: str = "latest") -> bool:
    # A SHA/HEAD is also supported; CI supplies --release-tag independently.
    symbolic = git(root, "rev-parse", "--symbolic-full-name", "--verify", "--end-of-options", ref).decode().strip()
    tags = []
    if symbolic.startswith("refs/tags/"):
        tags.append(symbolic.removeprefix("refs/tags/"))
    if release_tag is not None:
        tags.append(release_tag.removeprefix("refs/tags/"))
    for tag in set(tags):
        if tag != f"v{meta['version']}":
            raise ValueError("Release tag does not match module.json version")
        if resolve_commit(root, f"refs/tags/{tag}") != commit:
            raise ValueError("Release tag does not point to the selected commit")
    if tags:
        changelog = git(root, "show", f"{commit}:CHANGELOG.md").decode("utf-8")
        if not re.search(r"^## \[" + re.escape(meta["version"]) + r"\](?:\s|$)", changelog, re.MULTILINE):
            raise ValueError("Release version is missing from CHANGELOG.md")
        repository = meta.get("url", "")
        if not isinstance(repository, str) or not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise ValueError("Release url must be a GitHub repository URL without a trailing slash")
        expected_manifest = (f"{repository}/releases/latest/download/module.json" if manifest_channel == "latest"
                             else repository.replace("https://github.com/", "https://raw.githubusercontent.com/") + "/main/module.json")
        if meta.get("manifest") != expected_manifest:
            raise ValueError("Release manifest must point to the selected publication channel")
        expected_download = f"{repository}/releases/download/v{meta['version']}/{archive_name or meta['id']}.zip"
        if meta.get("download") != expected_download:
            raise ValueError("Release download must point to the versioned tag and module ZIP")
    return bool(tags)


def validate_archive(archive_path: Path, manifest: bytes, meta: dict) -> bytes:
    prefix = meta["id"] + "/"
    with zipfile.ZipFile(archive_path) as archive:
        if archive.testzip() is not None:
            raise ValueError("Invalid ZIP checksum")
        files = set()
        for member in archive.infolist():
            if not member.filename.startswith(prefix):
                raise ValueError(f"Invalid archive prefix: {member.filename}")
            relative = member.filename[len(prefix):]
            parts = relative.rstrip("/").split("/")
            if relative and (any(part in {"", ".", ".."} for part in parts) or "\\" in relative):
                raise ValueError(f"Invalid archive path: {member.filename}")
            if stat.S_ISLNK(member.external_attr >> 16):
                raise ValueError(f"Symlink is not distributable: {member.filename}")
            if not relative:
                continue
            if not (relative in ROOT_FILES or parts[0] in PAYLOAD_DIRS):
                raise ValueError(f"Unexpected distribution file: {relative}")
            if not member.is_dir():
                if relative in files:
                    raise ValueError(f"Duplicate distribution file: {relative}")
                files.add(relative)
                if relative.endswith(".json"):
                    try:
                        json.loads(archive.read(member))
                    except (ValueError, UnicodeError) as error:
                        raise ValueError(f"Invalid JSON in archive: {relative}") from error
        missing = ROOT_FILES - files
        if missing:
            raise ValueError(f"Missing distribution files: {', '.join(sorted(missing))}")
        archived_manifest = archive.read(prefix + "module.json")
        if archived_manifest.replace(b"\r\n", b"\n") != manifest.replace(b"\r\n", b"\n"):
            raise ValueError("Archived manifest differs from selected commit")
        paths = meta.get("esmodules", []) + [entry["path"] for entry in meta.get("languages", [])]
        for path in paths:
            if path not in files:
                raise ValueError(f"Missing manifest entry: {path}")
        return archived_manifest


def build(args: argparse.Namespace) -> tuple[str, list[Path]]:
    root = Path(git(Path.cwd(), "rev-parse", "--show-toplevel").decode().strip())
    if not args.allow_dirty and git(root, "status", "--porcelain").strip():
        raise ValueError("Working tree is not clean; commit changes or use --allow-dirty for a committed preview")
    commit = resolve_commit(root, args.ref)
    manifest, meta = load_manifest(root, commit)
    profile = load_profile(root, commit)
    expected_name = profile["archive_name"] or meta["id"]
    base_name = args.name or expected_name
    if not SAFE_NAME.fullmatch(base_name):
        raise ValueError("Invalid archive name")
    is_release = check_release(root, args.ref, commit, meta, args.release_tag, expected_name, profile["manifest_channel"])
    if is_release and (args.no_alias or base_name != expected_name):
        raise ValueError("Release requires the default module ZIP alias referenced by download")

    output = (root / args.dist).resolve()
    output.mkdir(parents=True, exist_ok=True)
    # Validate in an isolated directory before replacing any existing artifacts.
    with tempfile.TemporaryDirectory(prefix=".build-", dir=output) as temporary:
        stage = Path(temporary)
        suffix = "-light" if profile["variant"] == "text-only" else ""
        versioned = stage / f"{base_name}-{meta['version']}{suffix}.zip"
        git(root, "archive", "--format=zip", f"--prefix={meta['id']}/", "-o", str(versioned), commit)
        if profile["variant"] == "text-only":
            from text_only import transform_archive
            manifest, meta = transform_archive(root, commit, versioned, meta)
        archived_manifest = validate_archive(versioned, manifest, meta)
        artifacts = [versioned]
        if not args.no_alias:
            alias = stage / f"{base_name}.zip"
            shutil.copyfile(versioned, alias)
            artifacts.append(alias)
        external_manifest = stage / "module.json"
        external_manifest.write_bytes(archived_manifest)
        artifacts.append(external_manifest)
        checksums = stage / "SHA256SUMS.txt"
        checksums.write_text("".join(f"{hashlib.sha256(item.read_bytes()).hexdigest()}  {item.name}\n" for item in artifacts), encoding="ascii")
        artifacts.append(checksums)
        destinations = []
        for artifact in artifacts:
            destination = output / artifact.name
            artifact.replace(destination)
            destinations.append(destination)
    return commit, destinations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", default="dist", help="Output directory, relative to the repository root.")
    parser.add_argument("--ref", default="HEAD", help="Commit, branch or tag to archive.")
    parser.add_argument("--release-tag", help="Require this release tag to match the selected commit and version.")
    parser.add_argument("--name", default="", help="ZIP filename base; the internal folder always uses the module id.")
    parser.add_argument("--allow-dirty", action="store_true", help="Allow local changes; only committed files are archived.")
    parser.add_argument("--no-alias", action="store_true", help="Do not create the additional ZIP without a version.")
    args = parser.parse_args()
    try:
        commit, artifacts = build(args)
        print(f"Commit: {commit}")
        for artifact in artifacts:
            print(f"OK: {artifact} ({artifact.stat().st_size} bytes)")
        return 0
    except subprocess.CalledProcessError as error:
        print(f"ERROR (git): {error.stderr.decode('utf-8', errors='replace').strip()}", file=sys.stderr)
        return 2
    except (ValueError, KeyError, TypeError, OSError, zipfile.BadZipFile) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
