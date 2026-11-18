#!/usr/bin/env python3
"""Crawl a running copy of the site and report broken links and oversized pages.

Usage: python3 scripts/check_links.py http://127.0.0.1:8765/
Standard library only. Checks every href/src on every reachable page under the
start URL, every <loc> in sitemap.xml, in-page #fragments, leftover
placeholders, and that each page is under 100 KB. External links (other hosts,
mailto) are listed but not fetched.
"""
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin, urlparse

LIMIT = 100 * 1024


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key])


def fetch(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return r.status, r.headers.get("Content-Type", ""), r.read()


def main(start):
    origin = urlparse(start).netloc
    queue, seen, pages, errors, external = [start], set(), {}, [], set()
    while queue:
        url = queue.pop()
        if url in seen:
            continue
        seen.add(url)
        try:
            status, ctype, body = fetch(url)
        except urllib.error.HTTPError as e:
            errors.append(f"{e.code} {url}")
            continue
        if b"__BASE_URL__" in body or b"__CONTACT_EMAIL__" in body:
            errors.append(f"unfilled placeholder in {url}")
        if "html" not in ctype:
            if url.endswith("sitemap.xml"):
                for loc in body.decode().split("<loc>")[1:]:
                    loc = loc.split("</loc>")[0]
                    local = urljoin(start, urlparse(loc).path.split("/")[-1] or "")
                    queue.append(local)
            continue
        p = Parser()
        p.feed(body.decode("utf-8"))
        pages[url] = (len(body), p)
        for link in p.links:
            if link.startswith("mailto:"):
                external.add(link)
                continue
            target = urljoin(url, link)
            if urlparse(target).netloc != origin:
                external.add(target)
                continue
            queue.append(urldefrag(target)[0])
    for extra in ("sitemap.xml", "robots.txt", "favicon.svg"):
        if urljoin(start, extra) not in seen:
            queue.append(urljoin(start, extra))
    while queue:
        url = queue.pop()
        if url in seen:
            continue
        seen.add(url)
        try:
            fetch(url)
        except urllib.error.HTTPError as e:
            errors.append(f"{e.code} {url}")
    # fragments
    for url, (_, p) in pages.items():
        for link in p.links:
            target = urljoin(url, link)
            base, frag = urldefrag(target)
            if frag and base in pages and frag not in pages[base][1].ids:
                errors.append(f"missing #{frag} (linked from {url})")
    print("Pages:")
    for url, (size, _) in sorted(pages.items()):
        flag = "" if size < LIMIT else "  OVER 100 KB"
        print(f"  {size / 1024:6.1f} KB  {url}{flag}")
        if size >= LIMIT:
            errors.append(f"over 100 KB: {url}")
    print(f"Checked {len(seen)} local URLs. External, not fetched: {sorted(external)}")
    if errors:
        print("ERRORS:")
        for e in errors:
            print("  " + e)
        return 1
    print("No broken links.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765/"))
