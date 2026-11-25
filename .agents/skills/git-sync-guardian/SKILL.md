---
name: git-sync-guardian
description: >-
  Guard version control synchronization for Unread-Read in single or multi-AI collaborative workflows. Ensures pre-flight fetch checks, atomic commit-and-push operations, per-entry staging for shared log/issues/todo files, and append-only log merges.
---

# Git Sync Guardian（Unread-Read 版本同步守護技能）

## 一、設計目的（相較 Epoch-Kairos 原版之精簡優化）

本技能移植自 `Epoch-Kairos`，並針對 **Unread-Read** 單倉庫、輕量知識與視覺管理專案進行以下優化：
1. **移除雙倉庫（Mine-RAW）耦合**：只維護單一 `origin/main` 倉庫，指令更精簡。
2. **統一為純 Python 跨平台工具鏈**：僅維護一套 `.py` 腳本（macOS / Windows / Linux 皆可直接以 `python3` / `python` 執行，零外部依賴），不再雙份維護 `.sh`。
3. **支援首次提交安全檢查**：`stage_log.py`、`stage_issues.py`、`stage_todo.py` 均支援共用檔尚未存在於 `HEAD` 時的安全首次暫存。
4. **路徑改用 `docs/`**：日誌、問題清單與待辦清單統一位於 `docs/log.md`、`docs/issues.md`（編號 `UR-NNN`）、`docs/todo.md`（編號 `TD-NNN`）。

---

## 二、五大核心鐵律

### 1. 提交必含推送（Commit Implies Push）
- 凡執行階段性固化或收到使用者指示「提交」，必須透過 `safe_commit_push.py` 將 `commit` 與 `push` 視為原子操作；回報完成時須確認 `Ahead: 0`。

### 2. 動工前先檢查遠端（Pre-flight Fetch Check）
- 開始實質編輯前先執行 `status.py`；若落後遠端（`Behind > 0`），先執行 `sync.py` 安全合流再編輯。

### 3. 只提交自己的修改（Commit Only Your Own Changes）
- 嚴禁 `git add -A`、`git add .`、`git commit -a`。提交前先看 `git diff --stat`，只明確列出自己修改的相對檔案路徑。
- 共用檔案禁止整檔 `git add`，必須透過 `safe_commit_push.py` 自動呼叫對應腳本逐條暫存：
  - `docs/log.md`：以 `--agent "<代理名稱>"` 只暫存自己的新條目（必要時可加 `--log-heading`）。
  - `docs/issues.md`：以 `--issue UR-NNN`（或 `PREAMBLE`）逐條暫存，不得刪除既有條目。
  - `docs/todo.md`：以 `--todo TD-NNN` 逐條暫存新增、修改或刪除。

### 4. 寫入日誌即提交（Log Implies Commit）
- `docs/log.md` 為追加模式（Append-only），只代表已完成之工作。寫入新條目後必須於同一回合執行 `safe_commit_push.py` 提交並推送（除非使用者明確要求暫緩）。
- 標題時間一律先執行 `scripts/log_time.py` 取得臺北時間（UTC+8），不得憑記憶或估計填寫。
- 尚未完成或待使用者決定的工作不寫入日誌，改記於 `docs/todo.md`。

### 5. 撤回工作不刪紀錄（Undo Without Erasing Records）
- 撤回內容修正時，不得以 `git reset` 或 `git revert` 抹除已提交的 `docs/log.md` 與 `docs/issues.md` 紀錄；只還原內容檔並追加一筆日誌說明原因。

---

## 三、工具鏈指令

所有腳本位於 `.agents/skills/git-sync-guardian/scripts/`：

```bash
# 1. 檢查遠端與工作目錄狀態（動工前必跑）
python3 .agents/skills/git-sync-guardian/scripts/status.py

# 2. 安全合流遠端更新（含 autostash 與 docs/log.md 自動時間序合併）
python3 .agents/skills/git-sync-guardian/scripts/sync.py

# 3. 取得寫日誌用的臺北時間（YYYY-MM-DD HH:MM）
python3 .agents/skills/git-sync-guardian/scripts/log_time.py

# 4. 讀取日誌最後 N 筆（預設 3 筆，免去整份讀取）
python3 .agents/skills/git-sync-guardian/scripts/log_tail.py -n 3
python3 .agents/skills/git-sync-guardian/scripts/log_tail.py --grep TD-001 -n 0

# 5. 取得下一個待辦 / 問題編號
python3 .agents/skills/git-sync-guardian/scripts/stage_todo.py --next-id
python3 .agents/skills/git-sync-guardian/scripts/stage_issues.py --next-id

# 6. 原子提交並推送（明確列出自己的檔案）
python3 .agents/skills/git-sync-guardian/scripts/safe_commit_push.py "feat: update reading list" --agent "Antigravity" -- books/reading-list.md docs/log.md

# 若同時更新問題或待辦，於 -- 之前指定 --issue / --todo
python3 .agents/skills/git-sync-guardian/scripts/safe_commit_push.py "chore: complete TD-001" --agent "Antigravity" --todo TD-001 -- docs/todo.md docs/log.md
```

### 多 AI 共同作者標註（選用）
若以 AI 代理提交並希望於 GitHub 顯示共同作者圖示，可在 `<commit_message>` 結尾附帶空行與實際模型型號署名：
- Antigravity：`Co-authored-by: Antigravity (<Model Name>) <176961590+gemini-code-assist[bot]@users.noreply.github.com>`
- Codex：`Co-authored-by: Codex (<Model Name>) <267193182+codex@users.noreply.github.com>`
