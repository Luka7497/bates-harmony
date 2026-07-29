#!/usr/bin/env python3
"""src/english.json + src/ko/*.json → index.html (자립형 단일 파일)"""
import json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src')

# 성경 책이름 → USFM 코드 (우리말성경 YouVersion 링크 생성용)
USFM = {
    'genesis':'GEN','exodus':'EXO','leviticus':'LEV','numbers':'NUM','deuteronomy':'DEU',
    'joshua':'JOS','judges':'JDG','ruth':'RUT','1 samuel':'1SA','2 samuel':'2SA',
    '1 kings':'1KI','2 kings':'2KI','1 chronicles':'1CH','2 chronicles':'2CH','ezra':'EZR',
    'nehemiah':'NEH','esther':'EST','job':'JOB','psalm':'PSA','psalms':'PSA','proverbs':'PRO',
    'ecclesiastes':'ECC','song of solomon':'SNG','song of songs':'SNG','canticles':'SNG',
    'isaiah':'ISA','jeremiah':'JER','lamentations':'LAM','ezekiel':'EZK','daniel':'DAN',
    'hosea':'HOS','joel':'JOL','amos':'AMO','obadiah':'OBA','jonah':'JON','micah':'MIC',
    'nahum':'NAM','habakkuk':'HAB','zephaniah':'ZEP','haggai':'HAG','zechariah':'ZEC','malachi':'MAL',
    'matthew':'MAT','mark':'MRK','luke':'LUK','john':'JHN','acts':'ACT','romans':'ROM',
    '1 corinthians':'1CO','2 corinthians':'2CO','galatians':'GAL','ephesians':'EPH',
    'philippians':'PHP','colossians':'COL','1 thessalonians':'1TH','2 thessalonians':'2TH',
    '1 timothy':'1TI','2 timothy':'2TI','titus':'TIT','philemon':'PHM','hebrews':'HEB',
    'james':'JAS','1 peter':'1PE','2 peter':'2PE','1 john':'1JN','2 john':'2JN','3 john':'3JN',
    'jude':'JUD','revelation':'REV',
}
import re as _re


def to_usfm(ref):
    """'Genesis 9:6' / '1 Peter 1:18-19' → 'GEN.9.6' (범위는 첫 절)"""
    m = _re.match(r'^\s*(.+?)\s+(\d+):(\d+)', ref or '')
    if not m:
        return None
    book = USFM.get(m.group(1).strip().lower())
    if not book:
        print(f'  · USFM 미매핑: "{ref}"')
        return None
    return f'{book}.{m.group(2)}.{m.group(3)}'

ORDER = ['cover', 'p'] + [str(i) for i in range(1, 24)]

PARTS = [
    {'name': '들어가며', 'ch': ['cover', 'p']},
    {'name': '제1부 · 사람이 잃은 것', 'ch': ['1', '2', '3', '4']},
    {'name': '제2부 · 지혜 WISDOM', 'ch': ['5', '6', '7']},
    {'name': '제3부 · 긍휼 MERCY', 'ch': ['8', '9', '10', '11']},
    {'name': '제4부 · 공의 JUSTICE', 'ch': ['12', '13', '14', '15']},
    {'name': '제5부 · 거룩 HOLINESS', 'ch': ['16', '17', '18', '19']},
    {'name': '제6부 · 능력 POWER', 'ch': ['20', '21', '22']},
    {'name': '제7부 · 진실 TRUTH', 'ch': ['23']},
]

# 번역이 아직 없는 장을 위한 임시 한글 제목 (목차·이동 카드에 쓰입니다)
FALLBACK_TITLES = {
    'p': '서문', '1': '사람의 본래 상태', '2': '타락', '3': '온 인류가 타락에 연루됨',
    '4': '사람은 스스로를 회복할 수 없음', '5': '구속에 나타난 하나님의 지혜',
    '6': '실천적 적용', '7': '실천적 적용 (이어서)', '8': '구속에 나타난 하나님의 긍휼',
    '9': '긍휼 (이어서)', '10': '긍휼 (맺음)', '11': '실천적 적용',
    '12': '구속에 나타난 하나님의 공의', '13': '공의 (이어서)', '14': '공의 (맺음)',
    '15': '실천적 적용', '16': '구속에 나타난 하나님의 거룩', '17': '거룩 (이어서)',
    '18': '거룩 (맺음)', '19': '실천적 적용', '20': '구속에 나타난 하나님의 능력 — 성육신',
    '21': '능력 (이어서)', '22': '적용 — 신적 능력의 역사는 기독교 진리의 확증',
    '23': '구속에 나타난 하나님의 진실하심',
}


def main():
    eng = json.load(open(os.path.join(SRC, 'english.json')))
    chapters = {'cover': {'title': 'Cover', 'title_ko': '표지', 'paras': [], 'done': True, 'roman': ''}}

    for key in ORDER[1:]:
        e = eng[key]
        ch = {
            'roman': (e['roman'] + '.') if key != 'p' else '',
            'title': e['title'],
            'title_ko': FALLBACK_TITLES[key],
            'argument': e.get('argument', ''),
            'paras': e['paras'],
            'done': False,
        }
        ko_path = os.path.join(SRC, 'ko', key + '.json')
        if os.path.exists(ko_path):
            k = json.load(open(ko_path))
            n_en, n_ko = len(ch['paras']), len(k.get('ko', []))
            if n_ko and n_ko != n_en:
                sys.exit(f'[중단] {key}장: 영어 {n_en}문단 / 한글 {n_ko}문단 — 개수가 어긋납니다.')
            ch.update({
                'title_ko': k.get('title_ko', ch['title_ko']),
                'argument_ko': k.get('argument_ko', ''),
                'gist': k.get('gist'),
                'ko': k.get('ko'),
                'notes': k.get('notes', {}),
                'done': bool(k.get('ko')),
            })
            # 우리말성경 링크용 USFM 코드를 각 주석에 심어 둡니다
            for n in ch['notes'].values():
                if n.get('ref'):
                    u = to_usfm(n['ref'])
                    if u:
                        n['usfm'] = u
            # 본문에서 실제로 쓰인 주석만 남기고 미아 표지를 검증합니다
            used = set()
            blob = ' '.join(k.get('ko', []) + [k.get('argument_ko', '')] + (k.get('gist') or []))
            for nid in ch['notes']:
                if '{{' + nid + '}}' in blob:
                    used.add(nid)
            missing = [n for n in ch['notes'] if n not in used]
            if missing:
                print(f'  · {key}장 주의: 본문에 걸리지 않은 주석 {missing}')
        chapters[key] = ch

    data = {'order': ORDER, 'parts': PARTS, 'chapters': chapters}
    tpl = open(os.path.join(SRC, 'template.html')).read()

    # 한글 명조(나눔명조 OFL) 서브셋을 data URI로 내장 — 아이패드·아이폰에서도 명조로 렌더링됩니다
    def font_face(weight, fname):
        b64 = open(os.path.join(SRC, 'fonts', fname)).read().strip()
        return ("@font-face{font-family:'HBMyeongjo';font-style:normal;font-weight:%d;"
                "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2')}" % (weight, b64))
    kofont = ("/* Nanum Myeongjo (SIL OFL 1.1) — 본문 글자만 서브셋해 내장 */"
              + font_face(400, 'hb-regular.woff2.b64')
              + font_face(700, 'hb-bold.woff2.b64'))
    tpl = tpl.replace('/*__KOFONT__*/', kofont)

    payload = 'var DATA = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';'
    out = tpl.replace('/*__DATA__*/', payload)

    path = os.path.join(ROOT, 'index.html')
    open(path, 'w').write(out)

    done = [k for k in ORDER[1:] if chapters[k]['done']]
    notes = sum(len(chapters[k].get('notes', {})) for k in ORDER[1:])
    print(f'index.html  {len(out)/1024:.0f} KB')
    print(f'번역 완료   {len(done)}/24 장  ({", ".join(done) or "없음"})')
    print(f'주석        {notes} 개')


if __name__ == '__main__':
    main()
