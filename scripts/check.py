#!/usr/bin/env python3
"""Checks the site before it is published: Google's ownership file is intact,
and the pages load nothing from another site."""
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent.parent
errors = []

for f in root.glob("google*.html"):
    if f.read_text() != f"google-site-verification: {f.name}":
        errors.append(f"{f.name}: content is not Google's verification line")
if not list(root.glob("google*.html")):
    errors.append("no Google site verification file")

for page in root.glob("*.html"):
    text = page.read_text()
    for attr, url in re.findall(r'\b(src|href)="([^"]+)"', text):
        if attr == "src" and not url.startswith("/") and "://" in url:
            errors.append(f"{page.name}: loads {url} from another site")
    for css in re.findall(r'<link[^>]+href="([^"]+)"', text):
        if "://" in css:
            errors.append(f"{page.name}: stylesheet {css} from another site")
        elif not (root / css).exists():
            errors.append(f"{page.name}: missing {css}")

for e in errors:
    print(e, file=sys.stderr)
sys.exit(1 if errors else 0)
