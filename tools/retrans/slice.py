#!/usr/bin/env python3
"""장 하나 분량의 번역 작업 묶음을 만듭니다.
사용: python3 tools/retrans/slice.py <장> <작업폴더>   예) slice.py 8 /tmp/retrans/8"""
import json, os, re, shutil, sys
from common import ROOT, guard

ch, out = sys.argv[1], os.path.abspath(sys.argv[2])
guard(ch)
en = json.load(open(f'{ROOT}/src/english.json', encoding='utf-8'))[ch]
ko = json.load(open(f'{ROOT}/src/ko/{ch}.json', encoding='utf-8'))
os.makedirs(out, exist_ok=True)

def dump(name, obj):
    json.dump(obj, open(f'{out}/{name}', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

dump('en.json', {k: en.get(k) for k in ('title', 'heading', 'argument', 'paras')})
dump('ko.json', {'ko': ko['ko']})
used = set(re.findall(r'\{\{([a-z0-9_]+)\}\}', ' '.join(ko['ko'])))
dump('notes.json', {i: {k: n.get(k) for k in ('k', 'm', 'title') if n.get(k)}
                    for i, n in ko.get('notes', {}).items() if i in used})
tone = json.load(open(f'{ROOT}/src/ko/7.json', encoding='utf-8'))['ko'][:3]
open(f'{out}/tone.txt', 'w', encoding='utf-8').write('\n\n'.join(tone))
shutil.copy(f'{ROOT}/RETRANS_STYLE.md', out)

here = os.path.dirname(os.path.abspath(__file__))
validate = f'python3 {here}/validate.py {ch} {out}/out.json'
prompt = open(f'{here}/PROMPT.md', encoding='utf-8').read()
for k, v in {'{CH}': ch, '{DIR}': out, '{N}': str(len(en['paras'])), '{VALIDATE}': validate}.items():
    prompt = prompt.replace(k, v)
open(f'{out}/PROMPT.md', 'w', encoding='utf-8').write(prompt)
print(f'{ch}장 묶음: {out} | 영어 {len(en["paras"])}문단 {sum(len(p.split()) for p in en["paras"])}단어 | 표지 {len(used)}개')
