#!/usr/bin/env python3
"""stage_issues.py: 只把指定編號的問題條目加入 Git 暫存區（docs/issues.md），或取得下一個可用編號。

用法（於倉庫任意位置執行）：
    python3 .agents/skills/git-sync-guardian/scripts/stage_issues.py --next-id
    python3 .agents/skills/git-sync-guardian/scripts/stage_issues.py UR-001 UR-002
    python3 .agents/skills/git-sync-guardian/scripts/stage_issues.py UR-001 --dry-run
"""
import argparse
import os
import re
import subprocess
import sys

PATH = 'docs/issues.md'
LOG = 'docs/log.md'
ISSUE = re.compile(r'(?m)^### (UR-\d{3,}) ')
ANY_ID = re.compile(r'UR-(\d{3,})')
ID_FORMAT = re.compile(r'UR-\d{3,}')
BOUNDARY = re.compile(r'(?m)^##+ ')


def git(*args, data=None):
    r = subprocess.run(['git', *args], input=data, capture_output=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr.decode('utf-8', 'replace'))
        sys.exit(1)
    return r.stdout


def head_text(root, path):
    r = subprocess.run(['git', '-C', root, 'show', 'HEAD:' + path], capture_output=True)
    return r.stdout.decode('utf-8').replace('\r\n', '\n') if r.returncode == 0 else None


def work_text(root, path):
    p = os.path.join(root, path)
    if not os.path.exists(p):
        return None
    with open(p, 'rb') as f:
        return f.read().decode('utf-8').replace('\r\n', '\n')


def blocks(text):
    out = {}
    for m in ISSUE.finditer(text):
        nxt = BOUNDARY.search(text, m.end())
        out[m.group(1)] = (m.start(), nxt.start() if nxt else len(text))
    return out


def preamble_end(text):
    m = BOUNDARY.search(text)
    return m.start() if m else len(text)


def norm(s):
    return s.replace('\r\n', '\n').strip()


def next_id(root):
    nums = []
    for t in (head_text(root, PATH), work_text(root, PATH), work_text(root, LOG)):
        if t:
            nums += [int(n) for n in ANY_ID.findall(t)]
    return 'UR-%03d' % (max(nums, default=0) + 1)


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8')
        except Exception:
            pass
    ap = argparse.ArgumentParser(description='只暫存 docs/issues.md 中指定編號的條目')
    ap.add_argument('ids', nargs='*', help='要提交的問題編號（例如 UR-001）或 PREAMBLE')
    ap.add_argument('--dry-run', action='store_true', help='只列出結果，不寫入暫存區')
    ap.add_argument('--next-id', action='store_true', help='印出下一個可用編號')
    a = ap.parse_args()

    root = git('rev-parse', '--show-toplevel').decode().strip()
    if a.next_id:
        print(next_id(root))
        return
    if not a.ids:
        ap.error('須指定編號、PREAMBLE，或使用 --next-id')

    work = work_text(root, PATH)
    if work is None:
        sys.stderr.write('錯誤：工作目錄中找不到 %s。\n' % PATH)
        sys.exit(1)
    base = head_text(root, PATH)

    want_preamble = 'PREAMBLE' in a.ids
    raw_ids = [k for k in a.ids if k != 'PREAMBLE']
    bad = [k for k in raw_ids if not ID_FORMAT.fullmatch(k)]
    if bad:
        sys.stderr.write('錯誤：編號格式應為 UR-NNN：%s\n' % '、'.join(bad))
        sys.exit(1)

    wb = blocks(work)
    missing = [k for k in raw_ids if k not in wb]
    if missing:
        sys.stderr.write('錯誤：工作目錄中找不到指定的問題編號：%s\n' % '、'.join(missing))
        sys.exit(1)

    if base is None:
        others = [k for k in wb if k not in set(raw_ids)]
        if others:
            sys.stderr.write('錯誤：%s 尚未提交過，首次提交會帶入未指定條目：%s\n' % (PATH, '、'.join(others)))
            sys.exit(1)
        print('%s 尚未提交過，整檔暫存（首次建立）。' % PATH)
        if a.dry_run:
            print('（dry-run）未寫入暫存區。')
            return
        git('-C', root, 'add', '--', PATH)
        return

    bb = blocks(base)
    gone = [k for k in bb if k not in wb]
    if gone:
        sys.stderr.write('錯誤：工作目錄刪除了已提交的問題條目（問題清單不得刪除條目）：%s\n' % '、'.join(gone))
        sys.exit(1)

    staged = base
    wanted = set(raw_ids)
    for k in sorted((k for k in wanted if k in bb), key=lambda k: bb[k][0], reverse=True):
        s, e = bb[k]
        ws, we = wb[k]
        staged = staged[:s] + work[ws:we] + staged[e:]

    order = sorted(wb, key=lambda k: wb[k][0])
    for k in [k for k in order if k in wanted and k not in bb]:
        ws, we = wb[k]
        chunk = work[ws:we]
        cur = blocks(staged)
        prev = [p for p in order[:order.index(k)] if p in cur]
        pos = cur[prev[-1]][1] if prev else len(staged)
        if pos == len(staged) and not staged.endswith('\n\n'):
            staged += '\n' if staged.endswith('\n') else '\n\n'
            pos = len(staged)
        staged = staged[:pos] + chunk + staged[pos:]

    for k in raw_ids:
        print(('暫存（新條目）：' if k not in bb else '暫存：') + k)

    if want_preamble:
        staged = work[:preamble_end(work)] + staged[preamble_end(staged):]
        print('暫存：檔頭說明（PREAMBLE）')

    others = [k for k in wb if k not in wanted and (k not in bb or norm(work[slice(*wb[k])]) != norm(base[slice(*bb[k])]))]
    for k in others:
        print('略過（未指定，留在工作目錄）：' + k)
    if a.dry_run:
        print('（dry-run）未寫入暫存區。')
        return
    sha = git('-C', root, 'hash-object', '-w', '--stdin', data=staged.encode('utf-8')).decode().strip()
    git('-C', root, 'update-index', '--add', '--cacheinfo', '100644,%s,%s' % (sha, PATH))
    print('已暫存；工作目錄中的 %s 未變更，其他 %d 筆修改留在工作目錄。' % (PATH, len(others)))


if __name__ == '__main__':
    main()
