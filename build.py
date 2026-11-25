#!/usr/bin/env python3
"""src/trip.html (아티팩트용 조각) → index.html (단독 배포본)

아티팩트는 publish 시점에 doctype/head/body와 CSS 리셋을 자동으로 씌워준다.
GitHub Pages에는 그런 래퍼가 없으므로 여기서 직접 만들어 준다.
두 환경에서 같은 소스를 쓰기 위해 소스는 조각으로 유지하고, 배포본만 생성한다.

    python3 build.py            # index.html 생성

예약번호·확인메일·게이트 코드는 이 페이지에 넣지 않는다. GitHub Pages는
리포지토리가 private이어도 공개로 서빙되기 때문이다. 원본은 구글 시트에 있고
페이지는 링크만 건다.
"""
import io
import os
import re
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src", "trip.html")
OUT = os.path.join(ROOT, "index.html")

FAVICON = "🚐"
DESC = "뉴질랜드 남섬과 시드니 15일 여행 일정표 — 경로 지도, 날짜별 일정, 주변 맛집, 예약 현황."
THEME = "#FBFAF5"

# 아티팩트 런타임이 넣어주는 리셋에 대응하는 최소 리셋.
# button/input/textarea의 font:inherit가 없으면 날짜 레일과 메모장이
# 브라우저 기본 폰트로 렌더되어 아티팩트와 다르게 보인다.
RESET = """*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0}
img,svg,video{display:block;max-width:100%}
button,input,textarea,select{font:inherit;color:inherit}
button{cursor:pointer;background:none;border:0;padding:0}
textarea{resize:vertical}
a{color:inherit}"""


def main():
    frag = io.open(SRC, encoding="utf-8").read()

    # 조각 맨 앞의 <title>/<link>를 head로 옮긴다 (body에 두면 비표준).
    head_tags, body_lines = [], []
    for line in frag.split("\n"):
        if re.match(r"^\s*<(title|link)\b", line) and not body_lines:
            head_tags.append(line.strip())
        else:
            body_lines.append(line)
    body = "\n".join(body_lines).lstrip("\n")

    m = re.search(r"<title>(.*?)</title>", "\n".join(head_tags))
    title = m.group(1) if m else "여행 일정표"

    icon = quote(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        '<text y=".9em" font-size="90">%s</text></svg>' % FAVICON,
        safe="",
    )

    doc = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="{desc}">
<meta name="theme-color" content="{theme}">
<meta name="robots" content="noindex,nofollow">
<meta name="referrer" content="no-referrer">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="{title}">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="icon" href="data:image/svg+xml,{icon}">
<link rel="apple-touch-icon" href="data:image/svg+xml,{icon}">
{head}
<style>
{reset}
</style>
</head>
<body>
{body}
</body>
</html>
""".format(
        desc=DESC,
        theme=THEME,
        title=title,
        icon=icon,
        head="\n".join(head_tags),
        reset=RESET,
        body=body,
    )

    io.open(OUT, "w", encoding="utf-8").write(doc)
    print("%s  (%.0f KB)" % (OUT, len(doc.encode()) / 1024))


if __name__ == "__main__":
    main()
