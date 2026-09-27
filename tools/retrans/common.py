"""재번역 도구 공용 설정."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 형광펜이 한국어 글자 위치에 묶여 있는 장 — 본문을 바꾸면 형광펜이 어긋나므로 막습니다
PROTECTED = {'p', '1', '2', '3', '4', '5', '6'}

def guard(ch):
    # 형광펜 이전(tools/retrans/hlmap.py)과 함께 진행할 때만 RETRANS_UNLOCK=1 로 풉니다
    if ch in PROTECTED and os.environ.get('RETRANS_UNLOCK') != '1':
        raise SystemExit(f'{ch}장은 형광펜이 걸려 있어 재번역하지 않습니다 (README 참고)')
