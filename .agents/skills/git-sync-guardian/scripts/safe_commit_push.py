#!/usr/bin/env python3
"""safe_commit_push.py: Atomic Commit-and-Push Guardian for Unread-Read.

Rule 1: Whenever changes are committed, they MUST be pushed immediately.
Rule 4: Commit ONLY your own changes (never `git add -A` / `git add .`);
        docs/log.md, docs/issues.md, and docs/todo.md are staged entry by entry.
"""
import ntpath
import os
import subprocess
import sys
import time
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', '..'))


def usage():
    prog = os.path.basename(sys.argv[0])
    print(f'Usage: python3 .agents/skills/git-sync-guardian/scripts/{prog} "<commit_message>" [main] --agent "<執行代理名稱>" [--log-heading "<exact heading>"] [--issue UR-NNN ...] [--todo TD-NNN ...] [--allow-stale-log] -- <path> [<path> ...]')
    print('')
    print('  --agent      執行代理名稱（例如 "Antigravity"、"Claude Code"、"Codex"）；列出 docs/log.md 時必填。')
    print('  --log-heading  只提交指定的新日誌標題；可重複使用。')
    print('  --issue      提交 docs/issues.md 時必填：只提交指定問題編號（如 UR-001）或 PREAMBLE。')
    print('  --todo       提交 docs/todo.md 時必填：只提交指定待辦編號的新增、修改或刪除（如 TD-001）。')
    print('  --allow-stale-log  允許日誌標題時間早於現在 60 分鐘以上。')
    print("  -- <path>    只會提交這些相對於倉庫根目錄的單一檔案路徑。不接受 '.'、'-A' 或資料夾。")
    print('')
    print(f'Example: python3 .agents/skills/git-sync-guardian/scripts/{prog} "docs: update reading list" --agent "Antigravity" -- books/reading-list.md docs/log.md')
    sys.exit(1)


def run_git(cwd, *args, check=False):
    for attempt in range(5):
        r = subprocess.run(
            ['git', '-C', cwd, *args],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
        )
        if r.returncode == 0 or 'index.lock' not in (r.stderr or ''):
            break
        time.sleep(0.5 * (attempt + 1))
    if check and r.returncode != 0:
        if r.stderr:
            sys.stderr.write(r.stderr)
        sys.exit(r.returncode)
    return r


def git_out(cwd, *args, default=''):
    r = run_git(cwd, *args)
    return r.stdout.strip() if r.returncode == 0 else default


def run_helper(cwd, script_name, args):
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    r = subprocess.run(
        [sys.executable, os.path.join(SCRIPT_DIR, script_name), *args],
        cwd=cwd,
        env=env,
    )
    return r.returncode == 0


def reset_paths(cwd, paths):
    literal_paths = [f':(literal){p.replace(chr(92), "/")}' for p in paths]
    run_git(cwd, 'reset', '-q', '--', *literal_paths)


def validate_paths(repo_path, paths):
    normalized = []
    for path in paths:
        norm_path = path.replace('\\', '/')
        parts = norm_path.split('/')
        if (
            not norm_path
            or '\n' in path
            or '\r' in path
            or norm_path in ('.', './', '-A', '--all', '*')
            or os.path.isabs(path)
            or ntpath.isabs(path)
            or bool(ntpath.splitdrive(path)[0])
            or norm_path.startswith(':(')
            or any(part in ('.', '..') for part in parts)
        ):
            print(f"ERROR: 不接受路徑 '{path}'；請列出倉庫內單一檔案的相對路徑。")
            return None
        disk_path = os.path.join(repo_path, *parts)
        if os.path.isdir(disk_path):
            print(f"ERROR: '{path}' 是資料夾；請逐一列出檔案。")
            return None
        indexed = run_git(repo_path, 'ls-files', '-z', '--', f':(literal){norm_path}')
        if indexed.returncode != 0:
            if indexed.stderr:
                sys.stderr.write(indexed.stderr)
            print(f"ERROR: 無法確認 '{path}' 是否為單一檔案路徑；已中止。")
            return None
        indexed_paths = [item for item in indexed.stdout.split('\0') if item]
        if any(item != norm_path for item in indexed_paths):
            print(f"ERROR: '{path}' 對應到索引中的資料夾內容；請逐一列出檔案。")
            return None
        normalized.append(norm_path)
    return normalized


def only_log_conflict(cwd):
    return git_out(cwd, 'diff', '--name-only', '--diff-filter=U') == 'docs/log.md'


def has_unmerged(cwd):
    return bool(git_out(cwd, 'diff', '--name-only', '--diff-filter=U'))


def top_stash_is_autostash(cwd):
    stash_list = git_out(cwd, 'stash', 'list')
    first_line = stash_list.splitlines()[0] if stash_list else ''
    return 'autostash' in first_line


def parse_cli(argv):
    if len(argv) < 3:
        usage()
    commit_msg = argv[0]
    rest = argv[1:]
    if rest and rest[0] == 'main':
        rest = rest[1:]

    agent = ''
    log_headings = []
    allow_stale = False
    issues = []
    todos = []

    idx = 0
    while idx < len(rest) and rest[idx] != '--':
        opt = rest[idx]
        if opt == '--agent' and idx + 1 < len(rest):
            agent = rest[idx + 1]
            idx += 2
        elif opt == '--log-heading' and idx + 1 < len(rest):
            log_headings.append(rest[idx + 1])
            idx += 2
        elif opt == '--allow-stale-log':
            allow_stale = True
            idx += 1
        elif opt == '--issue' and idx + 1 < len(rest):
            issues.append(rest[idx + 1])
            idx += 2
        elif opt == '--todo' and idx + 1 < len(rest):
            todos.append(rest[idx + 1])
            idx += 2
        else:
            print(f"Unknown option '{opt}'.")
            usage()

    if idx >= len(rest) or rest[idx] != '--':
        usage()
    paths = rest[idx + 1:]
    if not paths:
        print('ERROR: 未列出任何要提交的檔案。')
        usage()

    return commit_msg, agent, log_headings, allow_stale, issues, todos, paths


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding='utf-8', line_buffering=True)
        except Exception:
            pass

    commit_msg, agent, log_headings, allow_stale, issues, todos, paths = parse_cli(sys.argv[1:])

    print('==================================================')
    print('Unread-Read Atomic Commit-and-Push Guardian')
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Agent: {agent or '（未指定）'}")
    print(f'Message: {commit_msg}')
    print('==================================================')

    if not os.path.isdir(os.path.join(REPO_ROOT, '.git')):
        print(f'ERROR: Git directory not found at {REPO_ROOT}.')
        sys.exit(1)

    branch = git_out(REPO_ROOT, 'branch', '--show-current', default='')
    if branch != 'main':
        print(f"ERROR: 只推送 origin/main，但目前分支為 '{branch or '(detached HEAD)'}'。")
        sys.exit(1)

    prestaged = git_out(REPO_ROOT, 'diff', '--cached', '--name-only')
    if prestaged:
        print('ERROR: 暫存區已有檔案（可能是其他代理暫存的），已中止：')
        for line in prestaged.splitlines():
            print(f'    {line}')
        sys.exit(1)

    paths = validate_paths(REPO_ROOT, paths)
    if paths is None:
        sys.exit(1)

    print('    提交前先更新 origin/main...')
    run_git(REPO_ROOT, 'fetch', 'origin', 'main', '--quiet', check=True)

    for norm_p in paths:
        if norm_p == 'docs/log.md':
            if not agent:
                reset_paths(REPO_ROOT, paths)
                print('ERROR: 提交 docs/log.md 時必須以 --agent 指定執行代理名稱。')
                sys.exit(1)
            stage_args = [agent]
            for h in log_headings:
                stage_args.extend(['--heading', h])
            if allow_stale:
                stage_args.append('--allow-stale')
            if not run_helper(REPO_ROOT, 'stage_log.py', stage_args):
                reset_paths(REPO_ROOT, paths)
                print('ERROR: 日誌暫存失敗，已還原本次暫存。')
                sys.exit(1)
        elif norm_p == 'docs/issues.md':
            if not issues:
                reset_paths(REPO_ROOT, paths)
                print('ERROR: 提交 docs/issues.md 時必須以 --issue UR-NNN 指定編號（或 PREAMBLE）。')
                sys.exit(1)
            if not run_helper(REPO_ROOT, 'stage_issues.py', issues):
                reset_paths(REPO_ROOT, paths)
                print('ERROR: 問題清單暫存失敗，已還原本次暫存。')
                sys.exit(1)
        elif norm_p == 'docs/todo.md':
            if not todos:
                reset_paths(REPO_ROOT, paths)
                print('ERROR: 提交 docs/todo.md 時必須以 --todo TD-NNN 指定編號。')
                sys.exit(1)
            if not run_helper(REPO_ROOT, 'stage_todo.py', todos):
                reset_paths(REPO_ROOT, paths)
                print('ERROR: 待辦清單暫存失敗，已還原本次暫存。')
                sys.exit(1)
        else:
            r = run_git(REPO_ROOT, 'add', '--', f':(literal){norm_p}')
            if r.returncode != 0:
                reset_paths(REPO_ROOT, paths)
                if r.stderr:
                    sys.stderr.write(r.stderr)
                sys.exit(r.returncode)

    print('    即將提交的檔案：')
    stat_out = git_out(REPO_ROOT, 'diff', '--cached', '--stat')
    if stat_out:
        for line in stat_out.splitlines():
            print(f'    {line}')

    if run_git(REPO_ROOT, 'diff', '--cached', '--quiet').returncode == 0:
        print('    暫存區沒有變更，不建立新提交。')
    else:
        commit_res = run_git(REPO_ROOT, 'commit', '-q', '-m', commit_msg)
        if commit_res.returncode != 0:
            for out in (commit_res.stdout, commit_res.stderr):
                if out:
                    sys.stderr.write(out)
            reset_paths(REPO_ROOT, paths)
            print('ERROR: 建立提交失敗，已還原本次暫存。')
            sys.exit(1)
        print(f"    已建立提交：{git_out(REPO_ROOT, 'log', '--oneline', '-1')}")

    behind = int(git_out(REPO_ROOT, 'rev-list', '--count', 'HEAD..origin/main', default='0') or '0')
    if behind > 0:
        print(f'    遠端領先 {behind} 個提交，進行三方合併...')
        merge_res = subprocess.run(['git', '-C', REPO_ROOT, 'merge', '--autostash', '--no-edit', 'origin/main'])
        if merge_res.returncode != 0:
            if only_log_conflict(REPO_ROOT):
                print('    只有 docs/log.md 衝突，依 append-only 原則自動合併...')
                if not run_helper(REPO_ROOT, 'merge_log.py', []):
                    sys.exit(1)
                run_git(REPO_ROOT, 'add', 'docs/log.md', check=True)
                commit_res = run_git(REPO_ROOT, 'commit', '-q', '--no-edit')
                if commit_res.returncode != 0:
                    if commit_res.stderr:
                        sys.stderr.write(commit_res.stderr)
                    print('ERROR: 日誌衝突已整理，但合併提交失敗；請人工處理。')
                    sys.exit(commit_res.returncode)
            else:
                print('ERROR: 合併衝突，請人工排解後執行 git push origin main。')
                sys.exit(1)

        if has_unmerged(REPO_ROOT):
            if only_log_conflict(REPO_ROOT) and top_stash_is_autostash(REPO_ROOT):
                print('    放回其他代理的未提交修改時 docs/log.md 衝突，自動併入...')
                if not run_helper(REPO_ROOT, 'merge_log.py', []):
                    sys.exit(1)
                run_git(REPO_ROOT, 'reset', '-q')
                run_git(REPO_ROOT, 'stash', 'drop', '-q')
            else:
                print('ERROR: 放回未提交修改時發生衝突，請檢查 git stash list。')
                sys.exit(1)

        run_git(REPO_ROOT, 'reset', '-q')

    ahead = int(git_out(REPO_ROOT, 'rev-list', '--count', 'origin/main..HEAD', default='0') or '0')
    if ahead > 0:
        print(f'    推送 {ahead} 個提交到 origin main...')
        push_res = subprocess.run(['git', '-C', REPO_ROOT, 'push', 'origin', 'main'])
        if push_res.returncode != 0:
            sys.exit(push_res.returncode)

    run_git(REPO_ROOT, 'fetch', 'origin', 'main', '--quiet', check=True)
    ahead_after = int(git_out(REPO_ROOT, 'rev-list', '--count', 'origin/main..HEAD', default='0') or '0')
    if ahead_after == 0:
        print('    Success: Fully synchronized with origin/main (Ahead: 0).')
    else:
        print(f'    ERROR: Push failed or local still ahead by {ahead_after} commit(s).')
        sys.exit(1)

    remaining = git_out(REPO_ROOT, 'status', '--porcelain')
    if remaining:
        print('    工作目錄仍有未提交的修改（可能屬於其他代理，本腳本不會處理）：')
        for line in remaining.splitlines():
            print(f'    {line}')
    print('==================================================')


if __name__ == '__main__':
    main()
