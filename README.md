# HTML 발표자료 보관함

html-ppt 스킬로 만든 발표자료를 모아 두는 폴더입니다. 폴더 전체를 웹 서버나 정적 호스팅(GitHub Pages, Netlify, Vercel 등)에 올리면 그대로 웹사이트가 됩니다.

**웹 주소:** https://eunhorang.github.io/html-ppt-archive/ (GitHub Pages, `main` 브랜치를 올리면 1~2분 뒤 자동 반영)

## 구조

```
html-ppt-archive/
├── assets/                  모든 발표자료가 함께 쓰는 공용 파일 (html-ppt 스킬에서 복사, MIT)
│   ├── base.css · fonts.css · runtime.js
│   ├── themes/*.css         테마 36종
│   └── animations/animations.css
└── decks/
    └── <발표자료-이름>/
        ├── index.html       슬라이드 본문과 발표 대본
        ├── style.css        이 발표자료에만 쓰는 스타일
        ├── cover.jpg        첫 슬라이드 표지(보관함 첫 페이지 미리보기용)
        └── intro.mp4·jpg    소개 영상과 포스터(있을 때만)
```

새 발표자료는 `decks/` 아래에 영문 소문자와 하이픈으로 된 폴더를 하나 더 만들어 추가합니다. 공용 파일은 `../../assets/`로 참조합니다.

### 새 발표자료를 올리는 순서

1. `decks/<발표자료-이름>/`에 발표자료를 넣습니다.
2. `decks.json` 맨 위에 한 항목을 더합니다. (`slug` 폴더 이름, `title` 제목, `description` 한두 문장 소개, `topics` 주제 목록, `date` 등록일 `YYYY-MM-DD`)
3. `python3 tools/build.py`를 실행합니다. 전체 목록(`list.html`), 첫 페이지의 표지·숫자, 아래 표가 다시 만들어지고, 장수는 실제 슬라이드 수로 채워집니다. 표지(`cover.jpg`)가 없으면 함께 만듭니다.
   - 2번을 건너뛰어도 스크립트가 새 폴더를 찾아 제목·설명을 읽어 넣습니다. 이때 주제는 `기타`가 되니 `decks.json`에서 고쳐 주세요.
4. 커밋하고 `main`에 올립니다.

### 소개 영상을 붙이는 순서

1. 발표자료 폴더에 `intro.mp4`(1920×1080, 1~2분, 100MB 미만)를 넣습니다. 예: `decks/seneca-stoic-life/intro.mp4`
2. `python3 tools/build.py`를 실행합니다. 포스터 그림(`intro.jpg`)이 자동으로 만들어지고, 첫 페이지 '영상으로 미리 보기'와 목록의 `· 영상` 표시, 아래 표의 '소개 영상' 칸이 채워집니다.

영상은 HyperFrames로 만들며, 원본 프로젝트는 이 저장소 밖(`../videos/<이름>/`)에 둡니다.

전체 목록(`list.html`)은 등록일 기준 학기(3~8월 1학기, 9~2월 2학기)로 묶이고, 검색창과 주제 버튼으로 거를 수 있습니다.

## 발표자료 목록

아래 표는 `tools/build.py`가 `decks.json`으로 만듭니다. 직접 고치지 마세요.

<!-- DECKS:START -->
| 폴더 | 제목 | 주제 | 장수 | 영상 | 등록일 |
|---|---|---|---|---|---|
| `decks/pause-at-one-sentence/` | 책을 많이 읽었는데, 왜 내 삶은 그대로일까? | 독서 | 22 | [YouTube](https://youtu.be/RdLauBjbM_I) | 2026-10-21 |
| `decks/claude-html-slides-howto/` | 코딩 없이, 말로 만드는 HTML 발표자료 | AI | 25 |  | 2026-10-21 |
| `decks/charlie-munger/` | 찰리 멍거 · 어리석음을 피하는 기술 | 투자 | 28 | [YouTube](https://youtu.be/GIFvJtn5_i0) | 2026-10-21 |
| `decks/marcus-aurelius-meditations/` | 마르쿠스 아우렐리우스 · 황제가 자신에게 쓴 일기 | 철학 | 26 | [YouTube](https://youtu.be/-DIFBZy_oQY) | 2026-10-20 |
| `decks/nietzsche-philosophy/` | 니체 · 망치를 든 철학자 | 철학 | 33 | [YouTube](https://youtu.be/MyNHAkq_26E) | 2026-10-20 |
| `decks/otrovert-gift-of-not-belonging/` | 이향인 · 무리 속에서도 섞이지 않는 사람들 | 심리 | 26 | [YouTube](https://youtu.be/VGmj-kfY7aY) | 2026-10-20 |
| `decks/schopenhauer-parerga/` | 쇼펜하우어 · 삶이 괴로울 때 읽는 철학 | 철학 | 27 | [YouTube](https://youtu.be/T9bq1fWaFu0) | 2026-10-20 |
| `decks/seneca-stoic-life/` | 세네카 · 2000년 전 로마에서 온 인생 상담 | 철학 | 22 | [YouTube](https://youtu.be/TupSjoRAFL0) | 2026-10-20 |
| `decks/mac-studio-local-ai/` | 맥스튜디오 한 대로 만드는 나만의 AI 시스템 | AI | 10 |  | 2026-10-20 |
| `decks/proust-in-search-of-lost-time/` | 잃어버린 시간을 찾아서 | 문학 | 21 |  | 2026-10-20 |
<!-- DECKS:END -->

## 조작법

`←` `→` 이동 · `S` 발표자 창(현재·다음 슬라이드, 대본, 타이머) · `N` 대본 메모 · `O` 전체 보기 · `T` 테마 바꾸기 · `F` 전체 화면

주소 끝에 `#/5`를 붙이면 5번째 슬라이드로 바로 열립니다. 글꼴은 Google Fonts에서 불러오므로 인터넷 연결이 필요합니다.
