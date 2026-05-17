#!/usr/bin/env python3
"""Publish or update an article on Dev.to from an articles-src/*.md file.

Reads frontmatter + body, posts to https://dev.to/api/articles with
canonical_url set to the live site URL. Creates as draft by default;
use --publish to publish immediately.

On first publish, writes the returned `devto_id` back into the frontmatter
so subsequent runs PUT updates to the same post.

Requires:
  DEVTO_API_KEY environment variable
    (create one at https://dev.to/settings/extensions)

Usage:
  python3 publish_devto.py articles-src/<slug>.md
  python3 publish_devto.py articles-src/<slug>.md --publish
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

from build import SITE_URL, parse_md

DEVTO_API = "https://dev.to/api/articles"


def normalize_tag(t: str) -> str:
    """Dev.to allows alphanumerics only; truncate to 20 chars."""
    return re.sub(r"[^a-z0-9]", "", t.lower())[:20]


def prepare_body(body_md: str) -> str:
    """Strip the cover image (first image-only paragraph) and rewrite
    relative URLs to absolute so Dev.to renders them correctly."""
    lines = body_md.split("\n")
    # Skip leading blank lines, then check if first paragraph is image-only
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    j = i
    while j < len(lines) and lines[j].strip():
        j += 1
    first_para = "\n".join(lines[i:j])
    if re.fullmatch(r"!\[[^\]]*\]\([^)]+\)\s*", first_para):
        body_md = "\n".join(lines[j:]).lstrip("\n")

    # Rewrite relative image URLs → absolute site URLs
    body_md = re.sub(
        r"!\[([^\]]*)\]\(((?!https?://|/)[^)\s]+)(\s+\"[^\"]+\")?\)",
        lambda m: f'![{m.group(1)}]({SITE_URL}/{m.group(2)}{m.group(3) or ""})',
        body_md,
    )
    # Rewrite relative .html links → absolute
    body_md = re.sub(
        r"\]\(((?!https?://|/|#)[^)\s]+\.html)\)",
        lambda m: f"]({SITE_URL}/articles/{m.group(1)})",
        body_md,
    )
    return body_md


def build_payload(front: dict, body_md: str, publish: bool) -> dict:
    slug = front["slug"]
    canonical = f"{SITE_URL}/articles/{slug}.html"
    cover_url = f"{SITE_URL}/{front['cover']['src']}"

    raw_tags = front.get("devto_tags") or front["tags"]
    tags = [normalize_tag(t) for t in raw_tags]
    tags = [t for t in tags if t][:4]

    return {
        "article": {
            "title": front["title"],
            "body_markdown": prepare_body(body_md),
            "published": publish,
            "main_image": cover_url,
            "canonical_url": canonical,
            "description": front["description"],
            "tags": tags,
        }
    }


def call_devto(method: str, url: str, payload: dict, api_key: str) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "api-key": api_key,
            "Accept": "application/vnd.forem.api-v1+json",
            "User-Agent": "portdeveloper-site-publisher/1.0",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code} from Dev.to: {body}", file=sys.stderr)
        sys.exit(1)


def insert_devto_id(md_path: Path, devto_id: int) -> None:
    """Append `devto_id: <id>` to the YAML frontmatter, preserving the rest."""
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return
    end = text.index("\n---\n", 4)
    insertion = f"\ndevto_id: {devto_id}"
    md_path.write_text(text[:end] + insertion + text[end:], encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("md_path", type=Path)
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publish immediately (default: save as draft)",
    )
    args = parser.parse_args()

    api_key = os.environ.get("DEVTO_API_KEY")
    if not api_key:
        print(
            "ERROR: set DEVTO_API_KEY env var.\n"
            "  Create one at https://dev.to/settings/extensions",
            file=sys.stderr,
        )
        return 1

    if not args.md_path.exists():
        print(f"ERROR: not found: {args.md_path}", file=sys.stderr)
        return 1

    front, body = parse_md(args.md_path)
    payload = build_payload(front, body, args.publish)
    devto_id = front.get("devto_id")

    if devto_id:
        result = call_devto("PUT", f"{DEVTO_API}/{devto_id}", payload, api_key)
        action = "updated"
    else:
        result = call_devto("POST", DEVTO_API, payload, api_key)
        insert_devto_id(args.md_path, result["id"])
        action = "created"

    url = result.get("url") or result.get("canonical_url") or f"id={result.get('id')}"
    state = "published" if args.publish else "draft"
    print(f"  {action} ({state}): {url}")
    if not devto_id:
        print(f"  wrote devto_id={result['id']} back to {args.md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
