# Unread / Read

> **「買過的書不一定都讀完了，但每一本都值得被好好建檔。」**

`Unread / Read` 是一個結合 **統一風格 AI 圖像生成 Agent** 與 **個人四學科藏書紀錄（物理、數學、心理學、哲學）** 的專案，同時作為「第十二週作業：統一風格圖像產生的 Agent（11/24）」的企劃與提示詞資產庫。

---

## 專案定位

1. **對學校作業**：建立一個專門產生**統一風格**作品的 AI 專案 Agent，能以同一套前沿平面設計美學，穩定產出**展覽海報（2:3）**、**概念學習圖卡（3:4）**、**書單封面（16:9）**與**藏書票插畫（1:1）**。
2. **對日常生活**：用來記錄在各處（如拼多多）購入的物理、數學、心理學與哲學書籍，透過 `[ ] UNREAD`／`[×] READ` 檔案標籤視覺化追蹤閱讀狀態。

---

## 視覺規範速覽（Style Anchor）

- **美學語言**：雙色 Risograph 孔版印刷質感 × 瑞士國際主義網格排版（Swiss Grid）
- **色彩預算（65 / 25 / 10）**：
  - `65%` 未漂白象牙棉紙白 `#EFECE6`
  - `25%` 消光炭墨黑 `#171717`
  - `10%` 單一學科重點色：
    - 物理 Physics：`#FF4F00`（國際信號橙）
    - 數學 Mathematics：`#1B4DFF`（群青鈷藍）
    - 心理學 Psychology：`#2D6A4F`（鼠尾草墨綠）
    - 哲學 Philosophy：`#7A1F2B`（勃艮第深酒紅）
    - 綜合總覽 Archive：`#1F2A44`（深炭藍）
- **狀態標記**：每張成品角落附上極簡檔案印章 `[ ] UNREAD` / `[×] READ`（或 `STATUS: UNREAD` / `STATUS: READ`）

---

## 目錄結構

```text
Unread-Read/
├── README.md                      # 專案總覽
├── AGENTS.md                      # 專案維護規範與多 AI 協作協定
├── .gitignore                     # Git 忽略規則
├── .agents/
│   └── skills/git-sync-guardian/  # 版本同步與逐條暫存工具鏈
├── .claude/
│   └── skills/git-sync-guardian/  # Claude Code 技能轉介檔
├── docs/
│   ├── discussion-notes.md        # 完整討論紀錄（參考 Skills、開源專案與設計決策）
│   ├── log.md                     # 操作日誌（Append-only）
│   ├── issues.md                  # 問題與風格修正清單（UR-NNN）
│   └── todo.md                    # 待辦清單（TD-NNN）
├── prompts/
│   └── system-instructions.md     # 可直接貼進 ChatGPT 專案 / Gemini Gem 的 Agent 專案指示
└── books/
    └── reading-list.md            # 個人書單紀錄模板（物理 / 數學 / 心理學 / 哲學）
```
