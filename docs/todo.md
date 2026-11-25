# 待辦清單（Todo）

> 本檔登記尚未完成之工作、交接事項與等待使用者決策的項目，格式與規則見 [AGENTS.md](../AGENTS.md) 第三章第 4 節。
> 標題四段依序為：編號（`TD-NNN`）、狀態（`open` / `waiting` / `doing`）、範圍（`prompt` / `books` / `assets` / `docs` / `rule` / `skill`）、一句話標題。完成或放棄時直接刪除條目，並於當次日誌寫明編號；新編號以 `stage_todo.py --next-id` 取得。

### TD-001 | waiting | books | 填入第一批已購書單至 books/reading-list.md
- **內容**：從拼多多購書訂單挑選至少 3 本代表書籍（建議涵蓋物理、數學、心理學或哲學），填入 [books/reading-list.md](../books/reading-list.md) 的書名、作者與欲視覺化的核心命題。
- **完成條件**：`books/reading-list.md` 至少登記 3 本真實書目。
- **等待**：使用者提供要納入紀錄的書單。
- **來源**：2026-11-25 登記，Antigravity by Google DeepMind。

### TD-002 | open | prompt | 建立 AI 專案並產出首批三類統一風格作品
- **內容**：於 ChatGPT 專案或 Gemini Gem 建立名為 `Unread / Read` 的專案，貼入 [prompts/system-instructions.md](../prompts/system-instructions.md)，依序生成至少 3 種版型（單書海報 2:3、概念學習圖卡 3:4、書單封面 16:9），並下載第一張滿意母圖作為參考圖鎖定風格，將成品與製作流程修正紀錄整理進作業繳交。
- **完成條件**：產出至少 3 張風格一致的不同類型圖片，完成步驟三製作流程說明（截止日 12/07 23:59）。
- **關聯**：TD-001
- **來源**：2026-11-25 登記，Antigravity by Google DeepMind。

### TD-003 | open | docs | 建置 index.html 藏書首頁與單書多比例圖庫
- **內容**：在核心圖片素材（書單封面 16:9、單書海報 2:3、概念學習圖卡 3:4 等）產出並鎖定風格後，建立靜態 `index.html` 與書目資料檔；首頁展示所有已購書籍封面與學科／狀態篩選，點進單書可依原比例檢視該書不同類型之圖片內容。
- **完成條件**：首頁可於本機雙擊與 GitHub Pages 正常開啟並瀏覽全部書目封面，點入單書可呈現多比例圖卡與 `UNREAD / READ` 狀態，視覺沿用 [prompts/system-instructions.md](../prompts/system-instructions.md)。
- **關聯**：TD-002
- **來源**：2026-11-25 登記，Antigravity by Google DeepMind。
