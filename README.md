# 남섬 & 시드니 여행 (2026-12-02 ~ 12-16)

**https://gin-2.github.io/travel/**

개인 여행 일정표 겸 기록 페이지. 정적 HTML 한 장이라 GitHub Pages에 그대로 올라간다.

```
index.html       배포본 (생성물 — 직접 고치지 말 것)
src/trip.html    소스. 내용·디자인 수정은 전부 여기서
build.py         src/trip.html → index.html
robots.txt       검색엔진 차단
.nojekyll        Jekyll 전처리 끄기
```

## 배포

리포지토리 **Settings → Pages → Source: Deploy from a branch → `main` / `/ (root)`**.
푸시하면 1~2분 뒤 `https://<계정>.github.io/<리포>/` 에 뜬다.

```sh
python3 build.py          # 수정했으면 항상 먼저
git add -A && git commit -m "update" && git push
```

## 왜 소스와 배포본이 따로인가

이 페이지는 claude.ai 아티팩트로도 서빙된다. 아티팩트는 업로드 시점에
`<!doctype>`·`<head>`·CSS 리셋을 자동으로 씌워주기 때문에 소스는 그 래퍼가 없는
조각이어야 한다. GitHub Pages에는 그런 래퍼가 없으므로 `build.py`가 대신 씌운다.
덕분에 양쪽이 같은 소스를 공유한다.

`build.py`가 붙여주는 것: doctype, meta(viewport·theme-color·noindex),
이모지 파비콘, 홈화면 추가용 메타, 그리고 최소 CSS 리셋.
리셋의 `button,input,textarea{font:inherit}`가 없으면 날짜 레일과 메모장이
브라우저 기본 폰트로 렌더되니 지우지 말 것.

## 환율

상단 환율은 페이지가 직접 조회한다.

- **소스**: frankfurter.app → 실패 시 open.er-api.com. 둘 다 키 불필요, CORS 허용
- AUD 기준으로 한 번만 받아 NZD는 교차환율로 계산한다 (요청 1회)
- 자동값은 6시간, 직접 입력값은 24시간 캐시. `↻ 갱신`은 캐시를 무시하고 다시 조회
- 조회 실패 시 마지막 값으로 표시하고 `(조회 실패)` + 구글 검색 링크를 띄운다
- 통화는 그날 위치를 따라간다. 12/12는 캠퍼밴 반납·주유·공항이라 NZD 유지

`src/trip.html`의 `FXB`는 조회가 안 될 때만 쓰이는 씨드값이다. 가끔 갱신해두면 좋다.

## ⚠️ 여기에 넣지 말 것

**GitHub Pages는 리포지토리가 private이어도 페이지는 공개로 서빙된다.**
URL을 아는 사람은 누구나 본다. `robots.txt` + `noindex`는 검색 노출만 막을 뿐
접근 차단이 아니다.

그래서 아래 항목은 소스에 넣지 않는다. 원본은 구글 시트에 있고 페이지는 링크만 건다.

| | 왜 |
|---|---|
| 항공 예약번호(PNR) | 대부분의 항공사 Manage Booking이 **PNR + 성(姓)** 두 개로 인증한다. 성은 추측 범위가 좁아 방어막이 못 된다. 좌석·수하물 변경과 **취소**까지 가능해진다 |
| 숙소·캠퍼밴 확인번호 | 취소 위험. 캠퍼밴은 선결제 ₩1.2M이고 픽업 임박 취소 수수료가 크다 |
| Felton Road 게이트 코드 | **본인 정보가 아니다.** 사유지 출입 코드를 공개하는 셈이고, 본인이 교체할 수도 없다 |
| 영문 성명 | PNR 인증의 나머지 반쪽 |

금액은 남겨둔다 — 환율 환산에 쓰이고, 그 자체로는 위험하지 않다.

한 번 푸시하면 나중에 지워도 **git 히스토리에 남는다.** 커밋 전에 확인할 것:

```sh
grep -rnE '[A-Z0-9]{6}|[0-9]{6,}' src/trip.html | grep -v 'DAYS\|STOPS'
```

### 더 조이고 싶다면

Pages를 쓰지 않고 `index.html`을 폰에 저장해 여는 방법도 있다.
단일 파일이라 그대로 열리고, `file://`에서도 환율 조회가 동작한다 (확인함).

## 저장되는 것

날짜별 메모, 준비물 체크, 환율은 브라우저 `localStorage`에 들어간다.
기기·브라우저마다 따로 저장되고 서버로 가지 않는다. 둘이 공유되지 않으니 주의.
