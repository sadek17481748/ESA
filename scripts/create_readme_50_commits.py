#!/usr/bin/env python3
"""Append README expansion in 50 commits dated today — does NOT push."""
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
CHUNKS_FILE = ROOT / "docs" / "readme_expansion_chunks.md"
TODAY = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
PER_DAY = 50
INTERVAL = 14  # minutes between commits


def run(cmd, **kw):
    subprocess.run(cmd, cwd=ROOT, check=True, **kw)


def commit_at(dt, msg):
    run(["git", "add", "README.md"])
    r = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if r.returncode == 0:
        print(f"Skip: {msg}")
        return False
    env = {
        **dict(subprocess.os.environ),
        "GIT_AUTHOR_DATE": dt.strftime("%Y-%m-%d %H:%M:%S +0100"),
        "GIT_COMMITTER_DATE": dt.strftime("%Y-%m-%d %H:%M:%S +0100"),
    }
    run(["git", "commit", "-m", msg], env=env)
    print(f"✓ {msg}")
    return True


def load_chunks():
    text = CHUNKS_FILE.read_text()
    parts = [p.strip() for p in text.split("\n---\n") if p.strip()]
    if len(parts) != 50:
        raise SystemExit(f"Expected 50 chunks, found {len(parts)} in {CHUNKS_FILE}")
    return parts


def load_readme_parts():
    body = README.read_text()
    marker = "\n## Author\n"
    if marker not in body:
        raise SystemExit("## Author section not found in README.md")
    before, _, after = body.partition(marker)
    if "## Portal Login Hub Introduction" in before:
        start = before.find("## Sprint delivery evidence")
        if start == -1:
            start = before.find("## Portal Login Hub Introduction")
        if start != -1:
            before = before[:start].rstrip() + "\n"
    return before, marker + after


def main():
    base_before_author, author_section = load_readme_parts()
    if "## Portal Login Hub Introduction" in base_before_author:
        print("README expansion already present — aborting to avoid duplicate.")
        raise SystemExit(1)

    chunks = load_chunks()
    expansion = (
        "## Sprint delivery evidence (June–July 2025)\n\n"
        "Sprint deliverables from 19 June through 1 July: Qur'an annotation, exams with "
        "teacher finalisation, payments with Stripe Connect, plus user acceptance testing, "
        "design references, and deployment readiness.\n\n"
    )
    made = 0
    for i, chunk in enumerate(chunks):
        title_line = chunk.split("\n", 1)[0]
        msg = title_line.lstrip("# ").strip()
        if len(msg) > 72:
            msg = msg[:69] + "..."
        expansion += chunk + "\n\n"
        README.write_text(f"{base_before_author}\n{expansion}{author_section}")
        dt = TODAY + timedelta(minutes=i * INTERVAL)
        if commit_at(dt, f"docs: {msg}"):
            made += 1
    print(f"\nDone — {made} README commits (local only, not pushed).")
    words = len(README.read_text().split())
    print(f"README word count: {words}")


if __name__ == "__main__":
    main()
