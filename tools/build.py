#!/usr/bin/env python3
"""decks.json을 읽어 첫 페이지(index.html)의 목록과 README.md의 목록 표를 다시 만듭니다.

    python3 tools/build.py

- 슬라이드 장수는 각 발표자료의 index.html에서 직접 셉니다.
- decks/ 아래에 있는데 decks.json에 없는 발표자료는 제목·설명을 읽어 맨 위에 추가하고 알려 줍니다.
  (주제는 '기타'로 들어가니 decks.json에서 고쳐 주세요.)
- 표지(cover.jpg)가 없는 발표자료가 있으면 tools/make-covers.sh를 실행합니다.
- 링크 공유용 그림(assets/og.jpg)을 최신 표지로 다시 만듭니다(tools/make-og.py).
"""
import html
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "decks.json"
INDEX = ROOT / "index.html"
README = ROOT / "README.md"
START, END = "<!-- DECKS:START -->", "<!-- DECKS:END -->"


def read_deck(slug):
    src = (ROOT / "decks" / slug / "index.html").read_text(encoding="utf-8")
    slides = len(re.findall(r'<section[^>]*class="slide[" ]', src))
    title = re.search(r"<title>(.*?)</title>", src, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)"', src, re.S)
    return {
        "slides": slides,
        "title": html.unescape(title.group(1).strip()) if title else slug,
        "description": html.unescape(desc.group(1).strip()) if desc else "",
    }


def semester(d):
    """한국 학교 학기: 3~8월은 1학기, 9~2월은 2학기(1·2월은 전년도 2학기)."""
    y, m = int(d[:4]), int(d[5:7])
    if 3 <= m <= 8:
        return (y, 1)
    return (y if m >= 9 else y - 1, 2)


def esc(s):
    return html.escape(s, quote=True)


def render_list(decks):
    groups = {}
    for d in decks:
        groups.setdefault(semester(d["date"]), []).append(d)
    out = []
    for (y, s) in sorted(groups, reverse=True):
        items = groups[(y, s)]
        out.append(f'      <div class="group">')
        out.append(f'        <h3 class="group-title">{y}년 {s}학기 <span>{len(items)}편</span></h3>')
        out.append('        <ul class="list">')
        for d in items:
            m, dd = d["date"][5:7], d["date"][8:10]
            out.append(f'          <li data-topics="{esc(" ".join(d["topics"]))}">')
            out.append(f'            <a href="decks/{esc(d["slug"])}/">')
            out.append(f'              <h4>{esc(d["title"])}</h4>')
            out.append(f'              <p>{esc(d["description"])}</p>')
            out.append(f'              <span class="meta">{d["slides"]}장 · {int(m)}.{int(dd)}</span>')
            out.append('            </a>')
            out.append('          </li>')
        out.append('        </ul>')
        out.append('      </div>')
    return "\n".join(out)


def render_readme(decks):
    rows = ["| 폴더 | 제목 | 주제 | 장수 | 등록일 |", "|---|---|---|---|---|"]
    for d in decks:
        rows.append(f'| `decks/{d["slug"]}/` | {d["title"]} | {", ".join(d["topics"])} | {d["slides"]} | {d["date"]} |')
    return "\n".join(rows)


def replace_between(text, body, path):
    if START not in text or END not in text:
        sys.exit(f"{path.name}에 {START} … {END} 표시가 없습니다.")
    a, b = text.index(START) + len(START), text.index(END)
    indent = text[text.rfind("\n", 0, text.index(END)) + 1 : text.index(END)]
    return text[:a] + "\n" + body + "\n" + indent + text[b:]


def main():
    decks = json.loads(DATA.read_text(encoding="utf-8"))
    known = {d["slug"] for d in decks}

    # decks.json에 없는 새 발표자료를 찾아 맨 위에 추가
    found = sorted(p.name for p in (ROOT / "decks").iterdir() if (p / "index.html").exists())
    for slug in found:
        if slug not in known:
            info = read_deck(slug)
            decks.insert(0, {"slug": slug, "title": info["title"], "description": info["description"],
                             "topics": ["기타"], "date": date.today().isoformat()})
            print(f"새 발표자료를 목록에 추가했습니다: {slug} (주제는 decks.json에서 고쳐 주세요)")
    missing = [d["slug"] for d in decks if d["slug"] not in found]
    if missing:
        sys.exit(f"decks.json에는 있지만 폴더가 없는 발표자료: {', '.join(missing)}")

    # 장수는 언제나 실제 슬라이드 수로, 정렬은 등록일 최신순(같은 날은 decks.json 순서)
    for d in decks:
        d["slides"] = read_deck(d["slug"])["slides"]
    decks = [d for _, d in sorted(enumerate(decks), key=lambda x: (x[1]["date"], -x[0]), reverse=True)]

    DATA.write_text(json.dumps([{k: d[k] for k in ("slug", "title", "description", "topics", "date")} for d in decks],
                               ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    INDEX.write_text(replace_between(INDEX.read_text(encoding="utf-8"), render_list(decks), INDEX), encoding="utf-8")
    README.write_text(replace_between(README.read_text(encoding="utf-8"), render_readme(decks), README), encoding="utf-8")

    if any(not (ROOT / "decks" / d["slug"] / "cover.jpg").exists() for d in decks):
        subprocess.run([str(ROOT / "tools" / "make-covers.sh")], check=True)

    subprocess.run([sys.executable, str(ROOT / "tools" / "make-og.py")], check=False)

    print(f"목록을 다시 만들었습니다: {len(decks)}편, 슬라이드 {sum(d['slides'] for d in decks)}장")


if __name__ == "__main__":
    main()
