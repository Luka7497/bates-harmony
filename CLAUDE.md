# bates-harmony — 개인 서재 앱

윌리엄 베이츠 『The Harmony of the Divine Attributes』(1674)의 한국어 번역 리더입니다.
GitHub Pages(`main` 브랜치)로 배포되고(https://luka7497.github.io/bates-harmony/), 사용자가 아이폰·아이패드 홈 화면 앱으로 매일 읽습니다.
사용자와는 한국어로 이야기합니다.

## 지금 진행 중

- **서재 앱 1단계** (여러 권을 담는 PWA로 전환, 성경 제외)
  - 브랜치: `seojae-v1`
  - 스펙: `docs/superpowers/specs/2026-09-27-seojae-app-phase1-design.md`
  - 화면 시안: https://claude.ai/artifact/1xcorzFa57aTKBCUSgMUBV
  - 다음 할 일: 스펙을 읽고 `superpowers:writing-plans`로 구현 계획을 쓴 뒤 구현합니다.
- **보류:** 성경. 새한글성경은 갓피플 성경앱의 저작권 협의 결과를 기다리는 중입니다.
- **후보:** 베이츠 재번역. VII장 시범 번역부터 합니다 (스펙 12장).

## 반드시 지킬 것

- **`main`에 커밋하면 곧바로 배포됩니다.** 1단계 작업은 `seojae-v1`에서만 하고, 사용자 확인을 받은 뒤 합칩니다.
- **형광펜은 한국어 본문의 글자 위치(`a`, `b` 오프셋)에 묶여 있습니다.** 이미 형광펜이 있는 장(현재 I–VI)의 `ko` 문단을 고치면 형광펜이 엉뚱한 글자를 가리킵니다.
- **새한글성경 본문은 싣지 않습니다.**
  - (재)대한성서공회 저작권이고 공개 API도 없습니다.
  - 크롤링하지 않습니다. 공식 리더(`bskorea.or.kr/KNT`)는 공회의 API.Bible 키로 본문을 받으므로, 크롤링은 남의 키를 무단으로 쓰는 일이 됩니다.
  - 성경 주석에서는 공식 리더의 해당 절로 가는 링크만 씁니다.
- **외부 성경·원문 데이터는 출처와 라이선스를 확인한 것만 씁니다.**
  - 확인된 것: SBLGNT (CC BY 4.0), 레닌그라드 사본 WLC (퍼블릭 도메인), STEPBible-Data (CC BY 4.0), KJV (퍼블릭 도메인)
  - 데이터 파일만 받고, 저장소에 든 스크립트는 실행하지 않습니다 (`npm install` 금지).
- **기존 기록 키 `hb.*`는 지우지 않습니다.** 되돌리기용입니다.
- 실제 기록 백업: `~/Desktop/bates-harmony-backup.json` (2026-09-27, 형광펜 139개 = 본문 87 + 주해 52, 북마크 3). 개인 독서 기록이므로 저장소에 넣거나 커밋하지 않습니다.
- 번역을 고칠 때는 `RETRANS_STYLE.md`를 따릅니다.

## 작업 방식

- 사용자는 Claude Pro 요금제를 씁니다. 사용량을 아낍니다.
  - 판단·설계·기록 이전 코드는 Opus가 직접 합니다.
  - 양이 많고 기계적인 데이터 변환·번역은 Sonnet 서브에이전트에 맡깁니다.
- 출처가 걸린 주장은 원문으로 확인합니다. 사용자는 이단 자료가 섞이는 것을 크게 우려합니다.

## 구성

- `build.py`: `src/english.json` + `src/ko/*.json` + `src/template.html` → `index.html` (1단계에서 장별 JSON 출력으로 바뀝니다)
- `sync/`: 기기 간 동기화 서버 (Cloudflare Worker `bates-sync` + KV)
