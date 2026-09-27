#!/usr/bin/env python3
"""검증을 통과한 번역을 src/ko/<장>.json의 ko 배열에만 반영합니다 (다른 필드는 그대로).
사용: python3 tools/retrans/apply.py <장> <out.json>   그다음 python3 build.py"""
import json, os, subprocess, sys
from common import ROOT, guard

ch, path = sys.argv[1], sys.argv[2]
guard(ch)
here = os.path.dirname(os.path.abspath(__file__))
if subprocess.run([sys.executable, f'{here}/validate.py', ch, path]).returncode != 0:
    sys.exit('검증을 통과하지 못해 반영하지 않았습니다')
p = f'{ROOT}/src/ko/{ch}.json'
d = json.load(open(p, encoding='utf-8'))
d['ko'] = json.load(open(path, encoding='utf-8'))['ko']
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'반영: src/ko/{ch}.json — 다음: python3 build.py')
