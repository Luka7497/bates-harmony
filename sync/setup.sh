#!/usr/bin/env bash
# 동기화 서버를 Cloudflare에 배포합니다.
#   1) npx wrangler login   (브라우저에서 한 번 로그인)
#   2) bash sync/setup.sh
set -euo pipefail
cd "$(dirname "$0")"

echo "▶ KV 저장소를 만듭니다…"
CREATE_OUT="$(npx --yes wrangler@latest kv namespace create HB 2>&1 || true)"
echo "$CREATE_OUT"

# 새로 만들었으면 그 id를, 이미 있으면 목록에서 찾아 씁니다.
ID="$(printf '%s' "$CREATE_OUT" | grep -oE '[0-9a-f]{32}' | head -1 || true)"
if [ -z "$ID" ]; then
  echo "▶ 이미 있는 KV 저장소를 찾습니다…"
  ID="$(npx --yes wrangler@latest kv namespace list 2>/dev/null \
        | python3 -c "import json,sys;
d=json.load(sys.stdin)
print(next((n['id'] for n in d if 'HB' in n.get('title','')), ''))" || true)"
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

echo "▶ 배포합니다…"
npx --yes wrangler@latest deploy

echo
echo "완료! 위에 출력된 https://bates-sync.<계정>.workers.dev 주소를 알려 주세요."
