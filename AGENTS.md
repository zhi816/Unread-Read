# AGENTS.md - Unread / Read 專案維護手冊

> 本手冊為 **Unread / Read**（四學科藏書視覺誌與統一風格圖像生成 Agent 專案）之維護規範。
> 全份 `AGENTS.md`、`docs/log.md`、`docs/issues.md`、`docs/todo.md` 嚴格禁止使用任何表情符號（Zero-Emoji）。

---

## 一、專案定位與核心架構

本專案結合兩項目標：
1. **統一風格生圖 Agent（第十二週作業）**：以不可變的物理媒介與色彩憲法，穩定生成展覽海報（2:3）、概念學習圖卡（3:4）、書單封面（16:9）與藏書票插畫（1:1）。
2. **個人四學科購書視覺檔案**：長期紀錄購入的 **物理（Physics）**、**數學（Mathematics）**、**心理學（Psychology）** 與 **哲學（Philosophy）** 書籍，以 `STATUS: UNREAD` / `STATUS: READ` 追蹤閱讀狀態。

### 目錄與職責

| 路徑 | 職責 | 修改原則 |
|---|---|---|
| `AGENTS.md` | 專案總規範、追蹤格式與 Git 協作鐵律 | 規範變更須寫日誌並經使用者確認 |
| `prompts/system-instructions.md` | AI 專案指示（Style Anchor、色票、版型、禁忌）唯一真相來源 | 每次微調 Prompt 須記錄版本與原因 |
| `books/reading-list.md` | 個人購書清單與狀態追蹤（`NO.XX`） | 依實際購書與閱讀狀態更新 |
| `docs/discussion-notes.md` | 企劃背景、開源參考與設計決策紀錄 | 供回顧脈絡使用 |
| `docs/log.md` | 操作歷史紀錄（只追加，不刪改） | 寫入前先執行 `log_time.py`，寫完即提交 |
| `docs/issues.md` | 問題與風格漂移追蹤清單（`UR-NNN`） | 就地改狀態，不得刪除條目 |
| `docs/todo.md` | 未完成工作、待確認事項與交接清單（`TD-NNN`） | 完成或經同意放棄時直接刪除條目 |
| `assets/` | 存放實際生成之母圖（Key Visual）、海報、圖卡與封面成品 | 建議依 `assets/posters/`、`assets/cards/`、`assets/covers/` 分類 |
| `.agents/skills/git-sync-guardian/` | 版本同步與安全提交工具鏈 | 跨工具標準技能（`.claude/skills/` 為轉介檔） |

---

## 二、視覺與提示詞唯一真相來源

所有生圖風格規則、色彩預算（65% 未漂白棉紙白 `#EFECE6` / 25% 炭墨黑 `#171717` / 10% 單一學科重點色）與反面禁忌，一律以 [`prompts/system-instructions.md`](./prompts/system-instructions.md) 為準：

- 物理 Physics：`#FF4F00`（國際信號橙）
- 數學 Mathematics：`#1B4DFF`（群青鈷藍）
- 心理學 Psychology：`#2D6A4F`（鼠尾草墨綠）
- 哲學 Philosophy：`#7A1F2B`（勃艮第深酒紅）
- 綜合總覽 Archive：`#1F2A44`（深炭藍）

若於生圖實測中發現風格漂移（例如出現 3D 塑膠光澤、文字過多或色票跑掉），應將問題現象與修正策略登記於 `docs/issues.md`，並同步更新 `prompts/system-instructions.md`，方便後續整理作業步驟三之「製作流程說明」。

---

## 三、AI 核心作業流程（SOP）

### 1. 接手脈絡（Handoff）
開工前依序執行：
1. `python3 .agents/skills/git-sync-guardian/scripts/status.py`（確認本機與遠端狀態；落後時先執行 `sync.py`）。
2. `git log --oneline -10`（查看近期提交）。
3. 完整閱讀 `docs/todo.md` 與 `docs/issues.md` 中 `open` 條目。
4. 需要近期細節時執行 `python3 .agents/skills/git-sync-guardian/scripts/log_tail.py -n 3`（不須整份讀取 `docs/log.md`）。

### 2. 操作日誌規範 `docs/log.md`
- 嚴格 **Append-only**（只追加於檔尾，不得改寫或刪除既有條目）。
- 寫入條目前先執行 `python3 .agents/skills/git-sync-guardian/scripts/log_time.py` 取得臺北時間（`YYYY-MM-DD HH:MM`）。
- 條目第一點必須寫明執行代理名稱與底層模型版本，格式如下：

```markdown
## [YYYY-MM-DD HH:MM] <類型：init|update|prompt|asset|fix|rule> | <一句話摘要>
- **執行代理**：<代理名稱>
- **模型版本**：<實際模型名稱>
- **具體變更**：<說明修改或產出內容；若有完成待辦需寫明 TD-NNN>
```

### 3. 問題清單規範 `docs/issues.md`
- 記錄風格漂移、Prompt 缺陷、版面錯誤或流程缺漏。
- 新增前執行 `python3 .agents/skills/git-sync-guardian/scripts/stage_issues.py --next-id` 取得 `UR-NNN` 流水號。
- 狀態僅限 `open`、`fixed`、`wontfix`；不得刪除條目。格式如下：

```markdown
### UR-001 | open | prompts/system-instructions.md | 海報版型 | 風格漂移
- **問題**：具體描述出現的問題（例如生成時誤出現 3D 陰影或英文拼字錯誤）。
- **建議解法**：預計如何調整規範或參考圖。
- **發現於**：docs/log.md [YYYY-MM-DD HH:MM]（執行代理）
```

### 4. 待辦清單規範 `docs/todo.md`
- 記錄尚未完成之工作與需等使用者決定之事項；完成或經同意放棄時**直接刪除條目**（並在當次 `docs/log.md` 註明編號）。
- 新增前執行 `python3 .agents/skills/git-sync-guardian/scripts/stage_todo.py --next-id` 取得 `TD-NNN` 流水號。
- 狀態：`open`（可接手）、`waiting`（須等使用者提供資料或拍板）、`doing`（進行中）。
- 範圍：`prompt`、`books`、`assets`、`docs`、`rule`、`skill`。
- 格式如下：

```markdown
### TD-001 | open | prompt | 一句話說明要做什麼
- **內容**：具體任務與涉及檔案。
- **完成條件**：做到什麼程度算完成。
- **等待**：（狀態為 waiting 時必填）
- **來源**：登記日期、執行代理。
```

---

## 四、版本控制與多 AI 協作協定

本專案強制使用 `.agents/skills/git-sync-guardian/` 管理 Git 流程，完整細則見 [`SKILL.md`](./.agents/skills/git-sync-guardian/SKILL.md)：
1. **提交必含推送**：統一使用 `safe_commit_push.py`，禁止只 commit 不 push。
2. **只提交自己的修改**：嚴禁 `git add -A` 或 `git add .`，必須逐一列出相對檔案路徑。
3. **共用檔逐條暫存**：`docs/log.md`（`--agent`）、`docs/issues.md`（`--issue UR-NNN`）、`docs/todo.md`（`--todo TD-NNN`）由腳本自動逐條組出暫存內容。
4. **寫入日誌即提交**：工作完成並追加 `docs/log.md` 後，應於同一回合提交並推送（使用者要求暫緩時除外）。
5. **只更新待辦免寫日誌**：若本次僅新增或更新 `docs/todo.md`（無實質成品變更），可直接提交，不須另寫日誌。
