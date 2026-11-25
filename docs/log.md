# Unread / Read 操作日誌 (Operation Log)

> 本日誌為嚴格按時間追加（Append-only）之紀錄，完整追蹤專案架構、Prompt 調整、書單擴充、圖像成品產出與問題修正。
> **日誌追溯規範**：每一次寫入均須先執行 `log_time.py` 取得臺北時間，並在第一條明確標註「執行代理」與「模型版本」。全篇嚴格禁止使用任何表情符號。

---

## [2026-11-25 17:56] init | 建立專案追蹤架構與 git-sync-guardian 單倉庫優化版
- **執行代理**：Antigravity by Google DeepMind
- **模型版本**：Gemini 4 Hydrogen
- **架構導入**：參照 Epoch-Kairos 建立 `AGENTS.md`、`docs/log.md`、`docs/issues.md`、`docs/todo.md` 四檔追蹤體系，並依單倉庫與跨平台需求精簡優化。
- **技能移植**：建立 `.agents/skills/git-sync-guardian/`（純 Python 腳本群，含首次提交安全處理、臺北時間校驗與 `UR-NNN` / `TD-NNN` 逐條暫存）及 `.claude/skills/git-sync-guardian/` 轉介檔。
- **待辦建立**：登記 `TD-001` 與 `TD-002` 於 `docs/todo.md`，追蹤書籍資料填入與 AI 專案實測產圖。

## [2026-11-25 18:44] update | 登記第一本購入書籍 NO.01《渾沌：開創一門新科學》
- **執行代理**：Antigravity by Google DeepMind
- **模型版本**：Gemini 4 Hydrogen
- **具體變更**：將使用者購入的第一本書《渾沌：開創一門新科學》（*Chaos: Making a New Science*，James Gleick 著）登記至 `books/reading-list.md` 的 `NO.01`（物理 Physics，重點色 `#FF4F00`），預設狀態為 `STATUS: UNREAD`，並擬定核心視覺命題（勞倫茲奇異吸引子／從紊亂中浮現秩序）待確認後啟動母圖試作。

## [2026-11-25 19:24] prompt | 調整 16:9 版型為單書內頁橫幅並建立 NO.01 腳本與母圖候選
- **執行代理**：Antigravity by Google DeepMind
- **模型版本**：Gemini 4 Hydrogen
- **具體變更**：
  - 更新 `prompts/system-instructions.md`，將第 3 種 `16:9` 版型由單純書單封面擴充為「單書內頁橫幅／專題封面（Banner / Cover）」，使其可隨每本書持續產出作為詳情頁頂部主視覺。
  - 新增 `books/01-chaos.md`，定稿 `NO.01`《渾沌：開創一門新科學》於 `2:3` 海報、`16:9` 橫幅與 `3:4` 概念圖卡三種用途之文字腳本與視覺隱喻。
  - 試產 3 版 `NO.01` 單書海報母圖候選（建築極簡版、刊物編輯版、科學策展圖譜版），待使用者選定 1 版作為正式風格母圖。

## [2026-11-25 19:31] fix | 修正 2:3 封面海報須保留完整書名與作者全名（UR-001）
- **執行代理**：Antigravity by Google DeepMind
- **模型版本**：Gemini 4 Hydrogen
- **具體變更**：依使用者審閱意見，將 `prompts/system-instructions.md` 中 `2:3` 單書海報明確定義為封面海報，並由簡稱／作者姓氏修正為必須保留完整書名原稱（含正副標）與完整作者姓名；同步更新 `books/01-chaos.md` 腳本並於 `docs/issues.md` 登記 `UR-001`（`fixed`）。

## [2026-11-25 19:40] asset | 完成 NO.01《渾沌》四種比例統一風格成品與書籤規範擴充
- **執行代理**：Antigravity by Google DeepMind
- **模型版本**：Gemini 4 Hydrogen
- **具體變更**：
  - 於 `prompts/system-instructions.md` 新增第 5 種「書籤 Bookmark（`9:16` 直長構圖，中軸預留 `1:3` 實體裁切安全區）」版型規範。
  - 依 V2 瑞士網格排版重產保留完整書名與完整作者之 `2:3` 封面海報母圖 `assets/posters/01-chaos-poster.jpg`。
  - 以該母圖為風格基準，生成同風格之 `16:9` 單書內頁橫幅 `assets/covers/01-chaos-banner.jpg`、`3:4` 概念學習圖卡 `assets/cards/01-chaos-card.jpg` 及 `9:16` 藏書書籤 `assets/bookmarks/01-chaos-bookmark.jpg`。
  - 於 `books/01-chaos.md` 補入四張成品內嵌預覽方便 GitHub 行動端直接閱覽，並於 `docs/issues.md` 登記 `UR-002` 記錄學習圖卡「岔」字微瑕。
