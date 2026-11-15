#!/usr/bin/env python3
"""Update Merlin from its latest stable GitHub release, without extra secrets."""
import json
import os
import re
import urllib.request
from pathlib import Path

REPO = "kylianmarceau/merlin"
ROOT = Path(__file__).resolve().parent.parent
CASK = ROOT / "Casks/merlin.rb"


def fetch(url, api=False):
    headers = {"User-Agent": "merlin-homebrew-tap"}
    if api:
        headers["Accept"] = "application/vnd.github+json"
        if os.environ.get("GH_TOKEN"):
            headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as response:
        return response.read().decode("utf-8")


def release_asset(release):
    tag = release.get("tag_name", "")
    if release.get("draft") or release.get("prerelease") or not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        raise ValueError("Expected a published stable vMAJOR.MINOR.PATCH release")
    version = tag[1:]
    name = f"Merlin-{version}-arm64.dmg"
    base = f"https://github.com/{REPO}/releases/download/{tag}/"
    assets = {asset["name"]: asset for asset in release["assets"]}
    for filename in (name, name + ".sha256"):
        if assets[filename]["browser_download_url"] != base + filename:
            raise ValueError(f"Unexpected download URL for {filename}")
    return version, name, assets[name], assets[name + ".sha256"]


def checksum_from(text, name, digest=None):
    match = re.fullmatch(r"([0-9a-f]{64}) [ *]" + re.escape(name) + r"\n?", text)
    if not match:
        raise ValueError("Checksum file must contain the exact DMG filename and SHA-256")
    checksum = match[1]
    if digest and digest != "sha256:" + checksum:
        raise ValueError("Checksum disagrees with GitHub's asset digest")
    return checksum


def update_text(current, version, checksum):
    match = re.search(r'^  version "(\d+\.\d+\.\d+)"$', current, re.M)
    if not match:
        raise ValueError("Missing existing stable cask version")
    number = lambda value: tuple(map(int, value.split(".")))
    if number(version) < number(match[1]):
        raise ValueError("Refusing to downgrade the cask")
    if version == match[1]:
        old_checksum = re.search(r'^  sha256 "([0-9a-f]{64})"$', current, re.M)
        if not old_checksum or checksum != old_checksum[1]:
            raise ValueError("An existing release's checksum changed; review it manually")
        return current
    updated, count = re.subn(r'^  version "[^"]+"$', f'  version "{version}"', current, flags=re.M)
    updated, hashes = re.subn(r'^  sha256 "[0-9a-f]{64}"$', f'  sha256 "{checksum}"', updated, flags=re.M)
    if count != 1 or hashes != 1:
        raise ValueError("Expected exactly one version and checksum")
    return updated


def main():
    release = json.loads(fetch(f"https://api.github.com/repos/{REPO}/releases/latest", api=True))
    version, name, dmg, checksum_asset = release_asset(release)
    checksum = checksum_from(fetch(checksum_asset["browser_download_url"]), name, dmg.get("digest"))
    current = CASK.read_text()
    updated = update_text(current, version, checksum)
    if updated != current:
        CASK.write_text(updated)
        print(f"Updated Merlin to {version}")
    else:
        print(f"Merlin {version} is already current")


if __name__ == "__main__":
    main()
