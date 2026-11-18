#!/usr/bin/env python3
"""Copy src/ to _site/, filling in the two values from site.config.

This is the only processing the site gets: a plain string substitution of
__BASE_URL__ and __CONTACT_EMAIL__. Standard library only.

Usage: python3 scripts/render.py [--base-url URL]
  --base-url overrides everything (used for local previews).
"""
import argparse
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "_site")
TEXT_EXT = {".html", ".css", ".svg", ".xml", ".txt"}


def read_config():
    values = {}
    with open(os.path.join(ROOT, "site.config"), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            values[key.strip()] = value.strip()
    return values


def resolve_base_url(config, override):
    if override:
        return override.rstrip("/")
    if config.get("BASE_URL"):
        return config["BASE_URL"].rstrip("/")
    cname = os.path.join(ROOT, "CNAME")
    if os.path.exists(cname):
        with open(cname, encoding="utf-8") as f:
            domain = f.read().strip()
        if domain:
            return "https://" + domain
    repo = os.environ.get("GITHUB_REPOSITORY")  # set by GitHub Actions, "owner/name"
    if repo and "/" in repo:
        owner, name = repo.split("/", 1)
        if name.lower() == f"{owner.lower()}.github.io":
            return f"https://{owner.lower()}.github.io"
        return f"https://{owner.lower()}.github.io/{name}"
    sys.exit("BASE_URL is empty, there is no CNAME file, and GITHUB_REPOSITORY is not set. "
             "Pass --base-url for a local build.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url")
    args = parser.parse_args()
    config = read_config()
    email = config.get("CONTACT_EMAIL", "")
    if "@" not in email:
        sys.exit("CONTACT_EMAIL in site.config is missing or invalid.")
    base = resolve_base_url(config, args.base_url)

    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT)
    for dirpath, _, files in os.walk(OUT):
        for name in files:
            if os.path.splitext(name)[1] not in TEXT_EXT:
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            text = text.replace("__BASE_URL__", base).replace("__CONTACT_EMAIL__", email)
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
    cname = os.path.join(ROOT, "CNAME")
    if os.path.exists(cname):
        shutil.copy(cname, os.path.join(OUT, "CNAME"))
    print(f"Rendered {SRC} -> {OUT} with BASE_URL={base} CONTACT_EMAIL={email}")


if __name__ == "__main__":
    main()
