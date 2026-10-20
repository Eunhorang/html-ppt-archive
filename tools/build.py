#!/usr/bin/env python3
"""decks.json을 읽어 첫 페이지(index.html)의 목록과 README.md의 목록 표를 다시 만듭니다.

    python3 tools/build.py

- 슬라이드 장수는 각 발표자료의 index.html에서 직접 셉니다.
- decks/ 아래에 있는데 decks.json에 없는 발표자료는 제목·설명을 읽어 맨 위에 추가하고 알려 줍니다.
  (주제는 '기타'로 들어가니 decks.json에서 고쳐 주세요.)
- 표지(cover.jpg)가 없는 발표자료가 있으면 tools/make-covers.sh를 실행합니다.
- 링크 공유용 그림(assets/og.jpg)을 최신 표지로 다시 만듭니다(tools/make-og.py).
- 발표자료 폴더에 소개 영상(intro.mp4)이 있으면 첫 페이지 '영상으로 미리 보기'에 싣고,
  포스터 그림(intro.jpg)이 없으면 ffmpeg로 만듭니다.
- decks.json 항목에 "youtube" 주소가 있으면 목록 카드 아래에 'YouTube에서 보기' 링크를 답니다.
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
VSTART, VEND = "<!-- VIDEOS:START -->", "<!-- VIDEOS:END -->"


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


def video_info(slug):
    """decks/<slug>/intro.mp4가 있으면 길이(초)를 돌려주고, 포스터(intro.jpg)가 없으면 만듭니다."""
    mp4 = ROOT / "decks" / slug / "intro.mp4"
    if not mp4.exists():
        return None
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                         capture_output=True, text=True)
    secs = round(float(out.stdout.strip() or 0))
    poster = mp4.with_suffix(".jpg")
    if not poster.exists():
        at = 12 if secs > 20 else max(0, secs // 2)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(at), "-i", str(mp4), "-frames:v", "1",
                        "-vf", "scale=1280:-2", "-q:v", "4", str(poster)], check=True)
        print(f"영상 포스터를 만들었습니다: decks/{slug}/intro.jpg")
    return secs


def length_ko(secs):
    m, s = divmod(secs, 60)
    return f"{m}분 {s}초" if m else f"{s}초"


def render_videos(decks):
    vids = [d for d in decks if d.get("video")]
    if not vids:
        return "      <p class=\"vid-none\">아직 영상이 없습니다.</p>"
    first = vids[0]
    out = ['      <figure class="vid-player">',
           f'        <video id="vid" controls preload="none" playsinline width="1920" height="1080" '
           f'poster="decks/{esc(first["slug"])}/intro.jpg" src="decks/{esc(first["slug"])}/intro.mp4"></video>',
           f'        <figcaption id="vid-cap"><b>{esc(first["title"])}</b> <span>소개 영상 · {length_ko(first["video"])}</span> '
           f'<a href="decks/{esc(first["slug"])}/">발표자료 열기 →</a></figcaption>',
           '      </figure>',
           '      <ol class="vid-list" id="vid-list">']
    for i, d in enumerate(vids):
        out.append(f'        <li><button type="button" aria-pressed="{"true" if i == 0 else "false"}" '
                   f'data-slug="{esc(d["slug"])}" data-title="{esc(d["title"])}" data-len="{length_ko(d["video"])}">'
                   f'<img src="decks/{esc(d["slug"])}/intro.jpg" alt="" width="1280" height="720" loading="lazy">'
                   f'<b>{esc(d["title"])}</b><span>{length_ko(d["video"])}</span></button></li>')
    out.append('      </ol>')
    return "\n".join(out)


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
            out.append(f'          <li data-topics="{esc(" ".join(d["topics"]))}"{' data-video' if d.get("video") else ''}>')
            out.append(f'            <a href="decks/{esc(d["slug"])}/">')
            out.append(f'              <h4>{esc(d["title"])}</h4>')
            out.append(f'              <p>{esc(d["description"])}</p>')
            vid = " · 영상" if d.get("video") else ""
            out.append(f'              <span class="meta">{d["slides"]}장 · {int(m)}.{int(dd)}{vid}</span>')
            out.append('            </a>')
            if d.get("youtube"):
                out.append(f'            <a class="yt" href="{esc(d["youtube"])}" target="_blank" rel="noopener">'
                           f'<span aria-hidden="true">▶</span> YouTube에서 보기</a>')
            out.append('          </li>')
        out.append('        </ul>')
        out.append('      </div>')
    return "\n".join(out)


def render_readme(decks):
    rows = ["| 폴더 | 제목 | 주제 | 장수 | 영상 | 등록일 |", "|---|---|---|---|---|---|"]
    for d in decks:
        vid = length_ko(d["video"]) if d.get("video") else ""
        if d.get("youtube"):
            vid = f'[YouTube]({d["youtube"]})'
        rows.append(f'| `decks/{d["slug"]}/` | {d["title"]} | {", ".join(d["topics"])} | {d["slides"]} | {vid} | {d["date"]} |')
    return "\n".join(rows)


def replace_between(text, body, path, start=START, end=END):
    if start not in text or end not in text:
        sys.exit(f"{path.name}에 {start} … {end} 표시가 없습니다.")
    a, b = text.index(start) + len(start), text.index(end)
    indent = text[text.rfind("\n", 0, text.index(end)) + 1 : text.index(end)]
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
        d["video"] = video_info(d["slug"])
    decks = [d for _, d in sorted(enumerate(decks), key=lambda x: (x[1]["date"], -x[0]), reverse=True)]

    DATA.write_text(json.dumps([{k: d[k] for k in ("slug", "title", "description", "topics", "date", "youtube") if k in d} for d in decks],
                               ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    page = replace_between(INDEX.read_text(encoding="utf-8"), render_list(decks), INDEX)
    page = replace_between(page, render_videos(decks), INDEX, VSTART, VEND)
    INDEX.write_text(page, encoding="utf-8")
    README.write_text(replace_between(README.read_text(encoding="utf-8"), render_readme(decks), README), encoding="utf-8")

    if any(not (ROOT / "decks" / d["slug"] / "cover.jpg").exists() for d in decks):
        subprocess.run([str(ROOT / "tools" / "make-covers.sh")], check=True)

    subprocess.run([sys.executable, str(ROOT / "tools" / "make-og.py")], check=False)

    print(f"목록을 다시 만들었습니다: {len(decks)}편, 슬라이드 {sum(d['slides'] for d in decks)}장")


if __name__ == "__main__":
    main()
