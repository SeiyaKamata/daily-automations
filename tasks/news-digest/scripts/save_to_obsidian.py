#!/usr/bin/env python3
"""
要約済み記事をObsidian vaultのnews/YYYY-MM-DD.mdに1日1ファイルとしてまとめて保存する。
"""

import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

JST = timezone(timedelta(hours=9))
FALLBACK_BODY_LENGTH = 500


def parse_article(path: Path) -> tuple[dict, str] | None:
    text = path.read_text()
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None
    try:
        fm = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError:
        return None
    if not isinstance(fm, dict):
        return None
    body = "\n".join(lines[end + 1:]).strip()
    return fm, body


def build_markdown(today: str, articles: list[dict]) -> str:
    lines = [f"# News {today}", ""]
    for article in articles:
        title = article["title"] or "(no title)"
        url = article["url"] or ""
        summary = article["summary"] or ""
        lines.append(f"## {title}")
        if url:
            lines.append(f"URL: {url}")
        lines.append("")
        if summary:
            lines.append(summary)
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    vault_path = os.environ.get("OBSIDIAN_VAULT_PATH")
    if not vault_path:
        print("ERROR: OBSIDIAN_VAULT_PATH not set", file=sys.stderr)
        sys.exit(1)

    today = datetime.now(JST).strftime("%Y-%m-%d")
    repo_root = Path(__file__).parent.parent
    date_dir = repo_root / "articles" / today

    if not date_dir.exists():
        print(f"No articles directory: {date_dir}")
        return

    article_files = sorted(
        f for f in date_dir.glob("*.md") if f.name != "README.md"
    )
    if not article_files:
        print("No articles found.")
        return

    articles = []
    skipped = 0
    for path in article_files:
        parsed = parse_article(path)
        if not parsed:
            print(f"  SKIP (parse error): {path.name}", file=sys.stderr)
            skipped += 1
            continue
        fm, body = parsed
        summary = fm.get("ai_summary") or body[:FALLBACK_BODY_LENGTH]
        articles.append({
            "title": fm.get("title", ""),
            "url": fm.get("url", ""),
            "summary": summary,
        })

    if not articles:
        print("No valid articles to save.")
        return

    out_dir = Path(vault_path) / "news"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{today}.md"
    out_path.write_text(build_markdown(today, articles))

    print(f"Saved {len(articles)} articles to {out_path} ({skipped} skipped)")


if __name__ == "__main__":
    main()
