#!/bin/zsh
# 각 발표자료의 첫 슬라이드를 찍어 decks/<이름>/cover.jpg(1280×720)로 저장합니다.
# 보관함 첫 페이지가 이 그림을 목록 미리보기로 씁니다.
#   tools/make-covers.sh          표지가 없는 발표자료만 만들기
#   tools/make-covers.sh --all    모든 표지를 다시 만들기
set -e
cd "${0:A:h}/.."
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP=$(mktemp -d)
for dir in decks/*/; do
  name=${dir:t}
  out="decks/$name/cover.jpg"
  [[ -f $out && $1 != --all ]] && continue
  "$CHROME" --headless=new --hide-scrollbars --window-size=1920,1080 \
    --virtual-time-budget=8000 --screenshot="$TMP/$name.png" \
    "file://$PWD/decks/$name/index.html?preview=1" >/dev/null 2>&1
  sips -s format jpeg -s formatOptions 82 --resampleWidth 1280 "$TMP/$name.png" --out "$out" >/dev/null
  echo "표지 생성: $out"
done
rm -rf "$TMP"
