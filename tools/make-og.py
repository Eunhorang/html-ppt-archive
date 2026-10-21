#!/usr/bin/env python3
"""링크 공유용 미리보기 그림(assets/og.jpg, 1200×630)을 만듭니다.

카카오톡·밴드·메신저에 주소를 붙이면 이 그림이 뜹니다.
위쪽은 먹색 바탕에 최신 발표자료 표지 6장, 아래 종이색 띠에는 원고지 칸 로고와 사이트 이름, 편수를 적습니다.
tools/build.py가 목록을 만들 때마다 함께 실행합니다. (맥의 Pillow와 Apple SD Gothic Neo 글꼴 필요)
"""
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow가 없어 공유 그림을 건너뜁니다. (pip3 install pillow)")

ROOT = Path(__file__).resolve().parent.parent
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
INK, PAPER, BG, MUTED = (31, 28, 24), (243, 236, 223), (233, 223, 204), (102, 93, 80)
MARK = ROOT / "assets" / "brand" / "mark.png"  # 원고지 칸 + 손글씨 '정'과 하트
W, H, BAND = 1200, 630, 180


def main():
    decks = json.loads((ROOT / "decks.json").read_text(encoding="utf-8"))
    img = Image.new("RGB", (W, H), INK)
    cw, ch = W // 3, (H - BAND) // 2
    for i in range(6):
        x, y = (i % 3) * cw, (i // 3) * ch
        cover = ROOT / "decks" / decks[i]["slug"] / "cover.jpg" if i < len(decks) else None
        if cover and cover.exists():
            im = Image.open(cover).convert("RGB")
            # 표지를 칸에 꽉 차게, 제목이 있는 왼쪽 아래를 남기며 자릅니다.
            scale = max(cw / im.width, ch / im.height)
            im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
            top = round((im.height - ch) * 0.7)
            img.paste(im.crop((0, top, cw, top + ch)), (x, y))
        else:
            ImageDraw.Draw(img).rectangle((x, y, x + cw, y + ch), fill=BG)
    d = ImageDraw.Draw(img)
    d.rectangle((0, H - BAND, W, H), fill=PAPER)
    x0 = 56
    if MARK.exists():
        mark = Image.open(MARK).convert("RGB").resize((124, 124), Image.LANCZOS)
        img.paste(mark, (48, H - BAND + 28))
        x0 = 200
    bold = ImageFont.truetype(FONT, 60, index=6)
    medium = ImageFont.truetype(FONT, 28, index=2)
    d.text((x0, H - BAND + 38), "정주샘의 슬라이드 모음", font=bold, fill=INK)
    freq = {}
    for deck in decks:
        for t in deck["topics"]:
            freq[t] = freq.get(t, 0) + 1
    topics = " · ".join(sorted(freq, key=lambda t: -freq[t])[:4])
    d.text((x0 + 2, H - BAND + 116), f"{topics} 발표자료 {len(decks)}편", font=medium, fill=MUTED)
    out = ROOT / "assets" / "og.jpg"
    img.save(out, "JPEG", quality=85, optimize=True)
    print(f"공유 그림을 만들었습니다: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
