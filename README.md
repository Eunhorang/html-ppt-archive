# HTML 발표자료 보관함

html-ppt 스킬로 만든 발표자료를 모아 두는 폴더입니다.

**웹 주소:** https://eunhorang.github.io/html-ppt-archive/ (GitHub Pages, `main` 브랜치를 올리면 1~2분 뒤 자동 반영) 폴더 전체를 웹 서버나 정적 호스팅(GitHub Pages, Netlify, Vercel 등)에 올리면 그대로 웹사이트가 됩니다.

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
        └── style.css        이 발표자료에만 쓰는 스타일
```

새 발표자료는 `decks/` 아래에 영문 소문자와 하이픈으로 된 폴더를 하나 더 만들어 추가합니다. 공용 파일은 `../../assets/`로 참조합니다.

## 발표자료 목록

| 폴더 | 제목 | 장수 |
|---|---|---|
| `decks/proust-in-search-of-lost-time/` | 잃어버린 시간을 찾아서 · 처음 만나는 프루스트 | 21 |

## 조작법

`←` `→` 이동 · `S` 발표자 창(현재·다음 슬라이드, 대본, 타이머) · `N` 대본 메모 · `O` 전체 보기 · `T` 테마 바꾸기 · `F` 전체 화면

주소 끝에 `#/5`를 붙이면 5번째 슬라이드로 바로 열립니다. 글꼴은 Google Fonts에서 불러오므로 인터넷 연결이 필요합니다.
