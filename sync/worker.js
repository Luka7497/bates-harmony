/**
 * 신적 속성의 조화 — 기기 간 동기화 서버
 *
 * 아주 단순한 키-값 저장소입니다. 리더 앱이 자기 기록(형광펜·북마크·진도)을
 * 통째로 올리고 내려받습니다. 병합은 앱 쪽에서 하므로 여기서는 보관만 합니다.
 *
 *   GET  /d/<코드>        → 저장해 둔 JSON (없으면 {})
 *   PUT  /d/<코드>        → JSON 저장
 *   POST /d/<코드>        → PUT 과 동일 (navigator.sendBeacon 은 POST 만 보냅니다)
 *
 * <코드>는 앱이 만든 무작위 문자열입니다. 이 코드를 아는 기기끼리만 같은
 * 기록을 공유합니다.
 */

const ALLOW_ORIGIN = 'https://luka7497.github.io';
const MAX_BYTES = 2 * 1024 * 1024; // 2MB — 기록이 아무리 쌓여도 충분합니다

function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': ALLOW_ORIGIN,
    'Access-Control-Allow-Methods': 'GET, PUT, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
    Vary: 'Origin',
  };
}

function json(body, status, extra) {
  return new Response(body, {
    status,
    headers: {
      ...corsHeaders(),
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      ...(extra || {}),
    },
  });
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders() });
    }

    const path = new URL(request.url).pathname;
    const matched = path.match(/^\/d\/([A-Za-z0-9_-]{16,128})$/);
    if (!matched) return json('{"error":"not_found"}', 404);

    const key = 'doc:' + matched[1];

    if (request.method === 'GET') {
      const stored = await env.HB.get(key);
      return json(stored || '{}', 200);
    }

    // sendBeacon 은 POST 로만 보내므로 PUT 과 똑같이 처리합니다.
    if (request.method === 'PUT' || request.method === 'POST') {
      const body = await request.text();
      if (body.length > MAX_BYTES) return json('{"error":"too_large"}', 413);
      try {
        JSON.parse(body);
      } catch (e) {
        return json('{"error":"bad_json"}', 400);
      }
      await env.HB.put(key, body);
      return json('{"ok":true}', 200);
    }

    return json('{"error":"method_not_allowed"}', 405);
  },
};
