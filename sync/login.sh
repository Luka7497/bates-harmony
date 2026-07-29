#!/usr/bin/env bash
# Cloudflare 계정으로 로그인합니다. 브라우저가 열리면 기존 계정으로 허용해 주세요.
set -euo pipefail
cd "$(dirname "$0")"

W="./node_modules/.bin/wrangler"
if [ ! -x "$W" ]; then
  echo "▶ wrangler를 설치합니다…"
  npm install --silent
fi

if "$W" whoami >/dev/null 2>&1; then
  echo "이미 로그인되어 있습니다:"
  "$W" whoami 2>&1 | head -5
  echo
  echo "다음 단계: bash $(pwd)/setup.sh"
  exit 0
fi

echo "▶ 브라우저가 열립니다. 기존 Cloudflare 계정으로 'Allow'를 눌러 주세요."
"$W" login

echo
echo "완료! 다음 단계: bash $(pwd)/setup.sh"
