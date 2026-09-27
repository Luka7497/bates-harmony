#!/usr/bin/env python3
"""재번역 결과 검증: 문단 수, 문단별 주석 표지, 분량(누락 의심), 영어 잔재.
사용: python3 tools/retrans/validate.py <장> <out.json>"""
import json, re, sys
from common import ROOT

ch, path = sys.argv[1], sys.argv[2]
cur = json.load(open(f'{ROOT}/src/ko/{ch}.json', encoding='utf-8'))['ko']
out = json.load(open(path, encoding='utf-8'))
ko = out.get('ko') if isinstance(out, dict) else None
MK = re.compile(r'\{\{([a-z0-9_]+)\}\}')
errs, warns = [], []
if not isinstance(ko, list):
    sys.exit('FAIL: {"ko": [...]} 형식이 아닙니다')
if len(ko) != len(cur):
    errs.append(f'문단 수 {len(ko)} ≠ 기존 {len(cur)}')
for i, (a, b) in enumerate(zip(ko, cur)):
    if sorted(MK.findall(a)) != sorted(MK.findall(b)):
        errs.append(f'문단 {i}: 표지 {sorted(MK.findall(a))} ≠ 기존 {sorted(MK.findall(b))}')
    if re.search(r'\{\{|\}\}', MK.sub('', a)):
        errs.append(f'문단 {i}: 깨진 표지')
    pa, pb = len(MK.sub('', a)), len(MK.sub('', b))
    r = pa / max(pb, 1)
    if r < 0.7 or r > 1.5:
        warns.append(f'문단 {i}: 분량 {pa}자 / 기존 {pb}자 (×{r:.2f}) — 누락·군더더기 확인')
    eng = re.findall(r'\b[A-Za-z]{4,}\b', MK.sub('', a))
    if len(eng) > 6:
        warns.append(f'문단 {i}: 로마자 단어 {len(eng)}개 — {eng[:6]}')
print('문단', len(ko), '| 글자', sum(len(MK.sub('', p)) for p in ko), '(기존', sum(len(MK.sub('', p)) for p in cur), ')')
for w in warns: print('WARN', w)
for e in errs: print('FAIL', e)
print('OK' if not errs else 'FAILED')
sys.exit(1 if errs else 0)
