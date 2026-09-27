#!/usr/bin/env python3
"""형광펜 장(서문·I–VI) 재번역 때 형광펜 위치를 옮기는 표를 만듭니다.

형광펜은 한국어 본문의 '화면 글자 위치'(주석 표지는 그 약칭 글자로 셈)에 묶여 있습니다.
새 번역은 문장이 달라 위치를 계산으로 옮길 수 없으므로, 형광펜마다 새 번역에서
같은 뜻의 구절을 골라(task → 번역가가 answer 작성) 그 위치를 표(src/hlmig.json)에 적습니다.
앱은 이 표로 기기에 저장된 형광펜을 한 번 옮깁니다 (src/template.html '재번역 형광펜 이전').

  python3 tools/retrans/hlmap.py task  <장> <백업.json> <out.json> <task.json>
  python3 tools/retrans/hlmap.py build <장> <task.json> <answer.json>
    answer.json = {"<형광펜 id>": "새 번역 문단에서 그대로 복사한 구절", ...}
  build는 apply.py 전에 실행합니다 (지금 src/ko/<장>.json을 '예전 번역'으로 읽습니다).
"""
import json, os, re, sys
from common import ROOT

MIG = f'{ROOT}/src/hlmig.json'
VERSION = 1


def rendered(para, notes):
    """앱 화면과 같은 글자열: {{id}} 표지는 그 주석의 약칭(m, 없으면 '주')으로, 없는 주석은 빈칸"""
    def rep(m):
        n = notes.get(m.group(1))
        return (n.get('m') or '주') if n else ''
    return re.sub(r'\{\{([a-z0-9_]+)\}\}', rep, para)


def load_ko(ch):
    return json.load(open(f'{ROOT}/src/ko/{ch}.json', encoding='utf-8'))


def task(ch, backup, out, dest):
    old = load_ko(ch)
    notes = old.get('notes', {})
    new = json.load(open(out, encoding='utf-8'))['ko']
    items = []
    for h in json.load(open(backup, encoding='utf-8')).get('hl', {}).get(ch, []):
        if h.get('side') != 'ko':
            continue
        op = rendered(old['ko'][h['i']], notes)
        assert op[h['a']:h['b']] == h['t'], f'백업과 본문이 어긋남: {h["id"]}'
        items.append({'id': h['id'], 'i': h['i'], 'old_para': op, 'old_t': h['t'],
                      'new_para': rendered(new[h['i']], notes)})
    json.dump({'ch': ch, 'items': items}, open(dest, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{ch}장 형광펜 {len(items)}개 → {dest}')


def build(ch, task_path, answer_path):
    t = json.load(open(task_path, encoding='utf-8'))
    ans = json.load(open(answer_path, encoding='utf-8'))
    old = load_ko(ch)
    notes = old.get('notes', {})
    mig = json.load(open(MIG, encoding='utf-8')) if os.path.exists(MIG) else {'v': VERSION, 'old': {}, 'map': {}}
    mig['old'][ch] = [len(rendered(p, notes)) for p in old['ko']]
    bad = 0
    for it in t['items']:
        s = ans.get(it['id'], '')
        np, op = it['new_para'], it['old_para']
        pos = [m.start() for m in re.finditer(re.escape(s), np)] if s else []
        if not pos:
            print(f'  ✗ {it["id"]}: 새 문단에서 구절을 찾지 못함 → {s[:40]!r}')
            bad += 1
            continue
        # 같은 구절이 여러 번 나오면 예전 위치 비율에 가장 가까운 것
        want = int(op.find(it['old_t']) / max(len(op), 1) * len(np))
        a = min(pos, key=lambda p: abs(p - want))
        mig['map'][it['id']] = [it['i'], a, a + len(s)]
    json.dump(mig, open(MIG, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(f'{ch}장: {len(t["items"]) - bad}/{len(t["items"])}개 표에 적음 → {MIG}')
    if bad:
        raise SystemExit('찾지 못한 구절을 answer에서 고친 뒤 다시 실행하세요')


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'task':
        task(*sys.argv[2:6])
    elif cmd == 'build':
        build(*sys.argv[2:5])
    else:
        raise SystemExit(__doc__)
