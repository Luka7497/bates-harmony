#!/usr/bin/env bash
# 동기화 서버를 Cloudflare에 배포합니다.
#   1) bash sync/login.sh    (브라우저에서 한 번 로그인)
#   2) bash sync/setup.sh
set -euo pipefail
cd "$(dirname "$0")"

W="./node_modules/.bin/wrangler"
if [ ! -x "$W" ]; then
  echo "▶ wrangler를 설치합니다…"
  npm install --silent
fi

if ! "$W" whoami >/dev/null 2>&1; then
  echo "✗ 아직 로그인되어 있지 않습니다. 먼저 이것부터 실행해 주세요:" >&2
  echo "    bash $(pwd)/login.sh" >&2
  exit 1
fi

echo "▶ 로그인 계정 확인"
"$W" whoami 2>&1 | head -5

echo
echo "▶ KV 저장소를 만듭니다…"
CREATE_OUT="$("$W" kv namespace create HB 2>&1 || true)"
echo "$CREATE_OUT"

ID="$(printf '%s' "$CREATE_OUT" | grep -oE '[0-9a-f]{32}' | head -1 || true)"
if [ -z "$ID" ]; then
  echo "▶ 이미 있는 KV 저장소를 찾습니다…"
  ID="$("$W" kv namespace list 2>/dev/null | python3 -c "
import json,sys
try:
    d = json.load(sys.stdin)
except Exception:
    d = []
print(next((n['id'] for n in d if 'HB' in n.get('title','')), ''))
" || true)"
fi

if [ -z "$ID" ]; then
  echo "✗ KV 저장소 id를 찾지 못했습니다. 위 메시지를 확인해 주세요." >&2
  exit 1
fi

echo "▶ KV id: $ID"
python3 - "$ID" <<'PY'
import re, sys
p = 'wrangler.toml'
s = open(p, encoding='utf-8').read()
s = re.sub(r'id = "[^"]*"', 'id = "%s"' % sys.argv[1], s)
open(p, 'w', encoding='utf-8').write(s)
print('  wrangler.toml 갱신 완료')
PY

echo
echo "▶ 배포합니다…"
"$W" deploy

echo
echo "───────────────────────────────────────────────"
echo "완료! 위에 나온 https://bates-sync.○○○.workers.dev 주소를 알려 주세요."
echo "───────────────────────────────────────────────"
