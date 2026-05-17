#!/usr/bin/env python3
"""Build site articles from articles-src/*.md.

Reads YAML frontmatter + markdown body, renders to articles/<slug>.html using
the canonical article template. Regenerates feed.xml and sitemap.xml from
the same sources.

Usage: python3 build.py
"""

from __future__ import annotations

import datetime as dt
import json
import re
import struct
import sys
from pathlib import Path
from typing import Any

import yaml

REPO = Path(__file__).resolve().parent
SRC = REPO / "articles-src"
OUT = REPO / "articles"
SITE_URL = "https://portdeveloper.github.io"


# ---------- image dimensions (no PIL dependency) ----------

def image_dims(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        head = f.read(30)
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", head[16:24])
        return w, h
    if head[:2] == b"\xff\xd8":
        with path.open("rb") as f:
            f.read(2)
            while True:
                b = f.read(2)
                if len(b) < 2 or b[0] != 0xFF:
                    raise ValueError(f"bad JPEG: {path}")
                marker = b[1]
                if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                    f.read(3)
                    h, w = struct.unpack(">HH", f.read(4))
                    return w, h
                length = struct.unpack(">H", f.read(2))[0]
                f.read(length - 2)
    raise ValueError(f"unsupported image: {path}")


# ---------- markdown rendering ----------

INLINE_PLACEHOLDER = "\x00\x01"

def _escape(text: str) -> str:
    """Escape for HTML text content. '>' is left as-is (legal in text)."""
    return text.replace("&", "&amp;").replace("<", "&lt;")


def _attr_escape(text: str) -> str:
    """Escape for HTML attribute values delimited by double quotes."""
    return (
        text.replace("&", "&amp;")
        .replace('"', "&quot;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _smart_typo(text: str) -> str:
    """Convert straight quotes / dashes to typographic entities.

    Runs on prose only; code/link/bold spans are stashed before this fires,
    so quotes inside code stay straight.
    """
    # Apostrophes / right single quote — between word chars (don't, we're)
    # and after a word at end of token (tools')
    text = re.sub(r"(\w)'(\w)", r"\1&rsquo;\2", text)
    text = re.sub(r"(\w)'", r"\1&rsquo;", text)
    text = re.sub(r"'(\w)", r"&lsquo;\1", text)
    # Double quotes — opening after start/space/punct, closing otherwise
    text = re.sub(r'(^|[\s\(\[>])"', r"\1&ldquo;", text)
    text = re.sub(r'"', r"&rdquo;", text)
    # Em-dash from "—" or "---"
    text = text.replace("—", "&mdash;")
    return text


def _render_inline(text: str) -> str:
    """Inline: code, links, images, bold. Escape the rest."""
    stash: list[str] = []
    def keep(rendered: str) -> str:
        stash.append(rendered)
        return f"{INLINE_PLACEHOLDER}{len(stash)-1}{INLINE_PLACEHOLDER}"

    # Inline code: `...`
    text = re.sub(
        r"`([^`]+)`",
        lambda m: keep(f"<code>{_escape(m.group(1))}</code>"),
        text,
    )
    # Inline HTML passthrough for a small whitelist of tags.
    text = re.sub(
        r"</?(?:br|sup|sub|kbd|mark|em|strong)\s*/?>",
        lambda m: keep(m.group(0)),
        text,
    )
    # Links: [text](url)  (images are handled at block level)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: keep(f'<a href="{_escape(m.group(2))}">{_smart_typo(_escape(m.group(1)))}</a>'),
        text,
    )
    # Bold: **text**
    text = re.sub(
        r"\*\*([^*]+)\*\*",
        lambda m: keep(f"<strong>{_smart_typo(_escape(m.group(1)))}</strong>"),
        text,
    )

    text = _escape(text)
    text = _smart_typo(text)
    # Restore placeholders (placeholders survived escape because \x00\x01 are not HTML-special)
    text = re.sub(
        rf"{INLINE_PLACEHOLDER}(\d+){INLINE_PLACEHOLDER}",
        lambda m: stash[int(m.group(1))],
        text,
    )
    return text


def _render_figure(src: str, alt: str, caption: str | None, *, is_cover: bool) -> str:
    full = REPO / src
    w, h = image_dims(full)
    is_small = w < 800
    class_attr = ' class="small-media"' if is_small else ""
    if is_cover:
        load_attrs = ' decoding="async" fetchpriority="high"'
    else:
        load_attrs = ' loading="lazy" decoding="async"'
    img = (
        f'<img{class_attr} src="../{src}" width="{w}" height="{h}"'
        f'{load_attrs} alt="{_attr_escape(alt)}">'
    )
    if caption:
        cap = f"\n  <figcaption>{_render_inline(caption)}</figcaption>"
    else:
        cap = ""
    return f"<figure>\n  {img}{cap}\n</figure>"


def _render_blocks(text: str, ctx: dict[str, Any]) -> list[str]:
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        # Headings
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            out.append(f"<h{level}>{_render_inline(m.group(2))}</h{level}>")
            i += 1
            continue

        # Horizontal rule
        if line.strip() in ("---", "***", "___"):
            out.append("<hr>")
            i += 1
            continue

        # Code fence — optional language after the opening fence
        if line.startswith("```"):
            lang = line[3:].strip() or "plaintext"
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            code = "\n".join(lines[i + 1 : j])
            cls = f' class="language-{_attr_escape(lang)}"'
            out.append(f"<pre><code{cls}>{_escape(code)}</code></pre>")
            i = j + 1
            continue

        # Blockquote: collect contiguous '>' lines
        if line.startswith(">"):
            j = i
            while j < len(lines) and lines[j].startswith(">"):
                j += 1
            stripped = []
            for l in lines[i:j]:
                if l.startswith("> "):
                    stripped.append(l[2:])
                elif l == ">":
                    stripped.append("")
                else:
                    stripped.append(l[1:])
            inner_html = "\n\n".join(_render_blocks("\n".join(stripped), ctx))
            inner_indented = "\n".join("  " + l if l else l for l in inner_html.split("\n"))
            out.append(f"<blockquote>\n{inner_indented}\n</blockquote>")
            i = j
            continue

        # Unordered list
        if re.match(r"^[-*]\s", line):
            j = i
            items: list[str] = []
            while j < len(lines) and re.match(r"^[-*]\s", lines[j]):
                items.append(lines[j][2:])
                j += 1
            li = "\n".join(f"  <li>{_render_inline(it)}</li>" for it in items)
            out.append(f"<ul>\n{li}\n</ul>")
            i = j
            continue

        # Ordered list
        if re.match(r"^\d+\.\s", line):
            j = i
            items = []
            while j < len(lines) and re.match(r"^\d+\.\s", lines[j]):
                items.append(re.sub(r"^\d+\.\s", "", lines[j]))
                j += 1
            li = "\n".join(f"  <li>{_render_inline(it)}</li>" for it in items)
            out.append(f"<ol>\n{li}\n</ol>")
            i = j
            continue

        # Raw HTML block (passthrough)
        if line.lstrip().startswith("<"):
            j = i
            while j < len(lines) and lines[j].strip():
                j += 1
            out.append("\n".join(lines[i:j]))
            i = j
            continue

        # Paragraph: gather until blank or new block marker
        j = i
        while j < len(lines) and lines[j].strip() and not _starts_block(lines[j]):
            j += 1
        para = "\n".join(lines[i:j]).replace("\n", " ")

        img_only = re.match(r"^!\[(.*?)\]\(([^)\s]+?)(?:\s+\"([^\"]+)\")?\)\s*$", para)
        if img_only:
            alt, src, cap = img_only.group(1), img_only.group(2), img_only.group(3)
            is_cover = ctx["figure_index"] == 0
            out.append(_render_figure(src, alt, cap, is_cover=is_cover))
            ctx["figure_index"] += 1
        else:
            # Allow soft <br> via trailing two spaces or explicit "<br>"
            rendered = _render_inline(para)
            out.append(f"<p>{rendered}</p>")
        i = j

    return out


def _starts_block(line: str) -> bool:
    s = line.lstrip()
    if not s:
        return True
    if s.startswith(("#", ">", "```", "<")) or s in ("---", "***", "___"):
        return True
    if re.match(r"^[-*]\s", s) or re.match(r"^\d+\.\s", s):
        return True
    return False


def render_body(md_body: str) -> str:
    ctx = {"figure_index": 0}
    blocks = _render_blocks(md_body, ctx)
    body = "\n\n".join(blocks)

    # Stash <pre>...</pre> regions before indenting so their internal
    # whitespace is preserved verbatim.
    pre_blocks: list[str] = []
    def stash_pre(m: re.Match) -> str:
        pre_blocks.append(m.group(0))
        return f"\x00PRE{len(pre_blocks)-1}\x00"
    body = re.sub(r"<pre>.*?</pre>", stash_pre, body, flags=re.DOTALL)

    indented = "\n".join("      " + l if l else l for l in body.split("\n"))
    indented = re.sub(
        r"\x00PRE(\d+)\x00", lambda m: pre_blocks[int(m.group(1))], indented
    )
    return indented.lstrip()  # template already indents the first line


# ---------- frontmatter parsing ----------

def parse_md(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing frontmatter: {path}")
    end = text.index("\n---\n", 4)
    front = yaml.safe_load(text[4:end])
    body = text[end + 5 :].lstrip("\n")
    return front, body


# ---------- HTML template ----------

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="port">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{cover_url}">
  <meta property="og:image:width" content="{cover_w}">
  <meta property="og:image:height" content="{cover_h}">
  <meta property="og:image:alt" content="{og_alt}">
  <meta property="article:author" content="{site_url}/">
{article_tags}
  <meta property="article:published_time" content="{published_at}">
  <meta property="article:modified_time" content="{modified_at}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{cover_url}">
  <meta name="twitter:image:alt" content="{og_alt}">
  <meta name="twitter:creator" content="@port_dev">
  <title>{title} - port</title>
  <link rel="stylesheet" href="../style.css">
  <link rel="alternate" type="application/rss+xml" title="port - writing" href="{site_url}/feed.xml">
  <script type="application/ld+json">
{ldjson}
  </script>
</head>
<body class="article-page">
  <main>
    <header class="site-header">
      <a class="site-title" href="../">port</a>
      <nav>
        <a href="../#about">About</a> &middot;
        <a href="../#projects">Projects</a> &middot;
        <a href="../#writing">Writing</a>
      </nav>
    </header>
    <hr>

    <article class="article">
      <h1>{title_html}</h1>
      <p class="article-meta">{date_display} &middot; originally published on <a href="{op_url}">{op_platform}</a></p>

      {body}
    </article>
  </main>
</body>
</html>
"""


def build_article(front: dict, body_md: str) -> tuple[str, str]:
    slug = front["slug"]
    title = front["title"]
    description = front["description"]
    section = front["section"]
    tags = front["tags"]
    keywords = front.get("keywords", tags + [section])
    cover = front["cover"]
    op = front["originally_published"]

    cover_path = REPO / cover["src"]
    cw, ch = image_dims(cover_path)
    cover_url = f"{SITE_URL}/{cover['src']}"
    canonical = f"{SITE_URL}/articles/{slug}.html"

    ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "image": cover_url,
        "url": canonical,
        "datePublished": front["published_at"],
        "dateModified": front["modified_at"],
        "inLanguage": "en",
        "keywords": keywords,
        "author": {
            "@type": "Person",
            "name": "port",
            "alternateName": ["portdeveloper", "port_dev"],
            "url": f"{SITE_URL}/",
            "sameAs": [
                "https://github.com/portdeveloper",
                "https://twitter.com/port_dev",
                "https://x.com/port_dev",
            ],
            "jobTitle": "Developer Advocate",
            "worksFor": {
                "@type": "Organization",
                "name": "Monad",
                "url": "https://www.monad.xyz/",
            },
        },
        "publisher": {"@type": "Person", "name": "port", "url": f"{SITE_URL}/"},
        "isPartOf": {"@type": "WebSite", "name": "port", "url": f"{SITE_URL}/"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
    }

    article_tags = "\n".join(
        [f'  <meta property="article:section" content="{_attr_escape(section)}">']
        + [
            f'  <meta property="article:tag" content="{_attr_escape(t)}">'
            for t in tags
        ]
    )

    body_html = render_body(body_md)

    page = PAGE.format(
        description=_attr_escape(description),
        canonical=canonical,
        title=_attr_escape(title),
        title_html=_render_inline(title),
        cover_url=cover_url,
        cover_w=cw,
        cover_h=ch,
        og_alt=_attr_escape(cover["og_alt"]),
        site_url=SITE_URL,
        article_tags=article_tags,
        published_at=front["published_at"],
        modified_at=front["modified_at"],
        ldjson=_indent(json.dumps(ld, indent=2, ensure_ascii=False), 4),
        date_display=_escape(front["date_display"]),
        op_url=_attr_escape(op["url"]),
        op_platform=_escape(op["platform"]),
        body=body_html,
    )
    return slug, page


def _indent(text: str, n: int) -> str:
    pad = " " * n
    return "\n".join(pad + line if line else line for line in text.split("\n"))


# ---------- feed.xml and sitemap.xml ----------

FEED_DESCRIPTION = (
    "Articles by port about developer tools, AI coding workflows, "
    "and Monad development."
)


def write_feed(articles: list[dict]) -> None:
    sorted_articles = sorted(
        articles, key=lambda x: x["published_at"], reverse=True
    )
    last_build = _rfc822_gmt(
        max(a["modified_at"] for a in sorted_articles)
    )
    items = []
    for a in sorted_articles:
        url = f"{SITE_URL}/articles/{a['slug']}.html"
        items.append(
            f"""    <item>
      <title>{_attr_escape(a['title'])}</title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <pubDate>{_rfc822_gmt(a['published_at'])}</pubDate>
      <description>{_attr_escape(a['description'])}</description>
    </item>"""
        )
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>port - writing</title>
    <link>{SITE_URL}/</link>
    <description>{FEED_DESCRIPTION}</description>
    <language>en</language>
    <lastBuildDate>{last_build}</lastBuildDate>
    <atom:link href="{SITE_URL}/feed.xml" rel="self" type="application/rss+xml" />
{chr(10).join(items)}
  </channel>
</rss>
"""
    (REPO / "feed.xml").write_text(feed, encoding="utf-8")


def write_sitemap(articles: list[dict]) -> None:
    sorted_articles = sorted(
        articles, key=lambda x: x["published_at"], reverse=True
    )
    site_lastmod = max(a["modified_at"] for a in sorted_articles)[:10]
    entries = [
        f"""  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{site_lastmod}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>"""
    ]
    for a in sorted_articles:
        url = f"{SITE_URL}/articles/{a['slug']}.html"
        entries.append(
            f"""  <url>
    <loc>{url}</loc>
    <lastmod>{a['modified_at'][:10]}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>"""
        )
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(entries)}
</urlset>
"""
    (REPO / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def _rfc822_gmt(iso: str) -> str:
    d = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return d.strftime("%a, %d %b %Y %H:%M:%S GMT")


# ---------- main ----------

def main() -> int:
    OUT.mkdir(exist_ok=True)
    articles: list[dict] = []
    for md_path in sorted(SRC.glob("*.md")):
        front, body = parse_md(md_path)
        slug, page = build_article(front, body)
        (OUT / f"{slug}.html").write_text(page, encoding="utf-8")
        articles.append(front)
        print(f"  built articles/{slug}.html")
    write_feed(articles)
    write_sitemap(articles)
    print(f"  wrote feed.xml + sitemap.xml ({len(articles)} articles)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
