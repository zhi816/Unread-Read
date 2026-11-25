# 問題與風格修正清單（Issues）

> 本檔登記 Prompt 風格漂移、生成瑕疵、書單資料缺漏或工具鏈待修正事項，格式與規則見 [AGENTS.md](../AGENTS.md) 第三章第 3 節。
> 標題五段依序為：編號（`UR-NNN`）、狀態（`open` / `fixed` / `wontfix`）、相關檔案、位置、問題分類。修正時就地改狀態並追加「處理」行，不得刪除條目；新編號以 `stage_issues.py --next-id` 取得。

---

### UR-001 | fixed | prompts/system-instructions.md | 2:3 單書封面海報文字規範 | 書目識別資訊缺漏
- **問題**：初版 `2:3` 規範僅要求放「書名（或簡短副標）」與「作者姓氏」，導致試產 `NO.01` 三版海報母圖時僅顯示《渾沌》而省略副標《開創一門新科學》與完整中文作者，未來同主題藏書增加時將難以在首頁書架直接辨識具體書目與作者。
- **建議解法**：將 `2:3` 明確定位為「單書封面海報（Book Cover Poster）」，規範必須完整保留書本原名（含副標）與完整作者姓名（不可只留姓氏，可中英並列）。
- **處理**：已更新 [prompts/system-instructions.md](../prompts/system-instructions.md) 與 [books/01-chaos.md](../books/01-chaos.md)，待選定 V1/V2/V3 構圖骨架後重產並驗證全稱字體清晰度。
- **發現於**：docs/log.md [2026-11-25 19:31]（Antigravity by Google DeepMind）

### UR-002 | open | assets/cards/01-chaos-card.jpg | 3:4 概念學習圖卡右下角關鍵字 | 中文字形微瑕
- **問題**：`assets/cards/01-chaos-card.jpg` 下方第三欄關鍵字 `03 分岔` 的「岔」字底部「山」部多出一道橫筆劃；其餘版面、配色與軌跡分岔圖解均符合規範。
- **建議解法**：後續若作為作業最終繳交圖卡，可局部修圖修正「岔」字或以 SVG／排版文字覆寫標籤層。
- **發現於**：docs/log.md [2026-11-25 19:40]（Antigravity by Google DeepMind）
