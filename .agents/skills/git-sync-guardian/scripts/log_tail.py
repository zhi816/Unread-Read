#!/usr/bin/env python3
"""log_tail.py: 依條目輸出 docs/log.md 最後幾筆，供接手時掌握脈絡，免去整份讀取日誌。

用法（於倉庫任意位置執行）：
    python3 .agents/skills/git-sync-guardian/scripts/log_tail.py              # 最後 3 筆
    python3 .agents/skills/git-sync-guardian/scripts/log_tail.py -n 5         # 最後 5 筆
    python3 .agents/skills/git-sync-guardian/scripts/log_tail.py --headings   # 只列最後 3 筆標題
    python3 .agents/skills/git-sync-guardian/scripts/log_tail.py --grep TD-001 -n 0
"""
import argparse
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
LOG = os.path.join(ROOT, 'docs', 'log.md')
HEADING = re.compile(r'(?m)^## \[')


def entries(text):
    idx = [m.start() for m in HEADING.finditer(text)]
    return [text[s:e].rstrip() for s, e in zip(idx, idx[1:] + [len(text)])]


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    ap = argparse.ArgumentParser(description='依條目輸出 docs/log.md 最後幾筆')
    ap.add_argument('-n', type=int, default=3, help='筆數，預設 3；0 表示不限')
    ap.add_argument('--headings', action='store_true', help='只輸出標題行')
    ap.add_argument('--grep', help='只保留含此關鍵字的條目（不分大小寫）')
    a = ap.parse_args()

    if not os.path.exists(LOG):
        print('docs/log.md 尚不存在。')
        return

    with open(LOG, 'rb') as f:
        items = entries(f.read().decode('utf-8').replace('\r\n', '\n'))
    total = len(items)
    if a.grep:
        key = a.grep.lower()
        items = [e for e in items if key in e.lower()]
    shown = items if a.n <= 0 else items[-a.n:]
    if a.headings:
        print('\n'.join(e.split('\n', 1)[0] for e in shown))
    else:
        print('\n\n'.join(shown))
    note = '含「%s」者 %d 筆，' % (a.grep, len(items)) if a.grep else ''
    print('\n--- docs/log.md 共 %d 筆，%s顯示 %d 筆' % (total, note, len(shown)))


if __name__ == '__main__':
    main()
