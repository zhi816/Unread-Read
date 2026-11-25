# Unread / Read 企劃討論紀錄

> 紀錄日期：2026-11-25  
> 對應任務：第十二週作業 11/24「統一風格圖像產生的 Agent」（繳交期限：12/07 23:59，遲交期限：12/08）

---

## 一、作業核心要求拆解

- **工具形式**：使用 AI 工具的「專案」功能（ChatGPT 專案、Claude 專案、Gemini Gem），建議優先使用可直接在對話內生圖的 **ChatGPT 專案** 或 **Gemini Gem**。
- **核心目標**：先把色調、筆觸、角色／符號等風格規則寫進專案指示（Instructions），再用它生成**至少三個不同主題或不同用途的作品**（例如：**海報、學習圖卡、封面**）。
- **評分重點**：**「風格一致」**，不看單張圖有多精美；需在步驟三說明如何設定 Agent、如何下指令，以及中間如何修正設定讓風格更穩定。

---

## 二、前沿美感與開源參考研究

### 1. 為什麼一般 AI 生圖顯得「空洞、有塑膠感」？
- 僅使用泛泛形容詞（如 `masterpiece, futuristic, high quality`）會導致模型自動套用廉價 3D 光澤、霓虹漸層與過度對稱的構圖。
- 解法來自開源社群的 **「Philosophy-First（哲學優先）＋ Style Anchor / Delta 拆解」** 方法論：
  1. 先定義明確的設計哲學與**反面禁忌清單（Anti-Patterns）**。
  2. 鎖定具體的**物理媒介與微瑕疵**（例如 Risograph 孔版印刷網點、紙張纖維、套印微錯位）。
  3. 嚴格限制色彩比例與負空間留白（40% 以上留白）。
  4. 將「不變的風格基因（Style Anchor）」與「每次變動的內容與版型（Delta）」徹底分離。

### 2. 值得參考的開源 Agent Skills 與 Prompt 專案
- **Agent Skills（學習 `SKILL.md` 如何規範美感與一致性）**
  - `anthropics/skills`（`https://github.com/anthropics/skills`）
    - `canvas-design`：強制先寫美學設計哲學，反對資訊堆砌，把文字當成極簡視覺點綴，追求美術館海報／雜誌封面氣質。
    - `algorithmic-art`：先寫演算法宣言，再以固定種子規則生成幾何藝術。
    - `theme-factory` & `brand-guidelines`：示範如何以明確 Hex 色碼與字體配對鎖死跨產出視覺風格。
  - `JimLiu/baoyu-skills`（`https://github.com/JimLiu/baoyu-skills`）
    - 包含 `baoyu-cover-image`、`baoyu-article-illustrator`、`baoyu-image-gen` / `baoyu-imagine`，將封面與配圖拆分為正交維度（類型、配色、渲染風格、文字密度、比例）。
- **Prompt 庫與美學詞彙參考**
  - `YouMind-OpenLab/awesome-nano-banana-pro-prompts`（結構化自然語言提示詞與復古硬體／編輯風／單色高對比美學）
  - `YouMind-OpenLab/awesome-gpt-image-2`（精準排版、跨圖一致性與插畫配方）
  - `jau123/nanobanana-trending-prompts`
  - `AIGC-Hackers/awesome-ai-image-prompts-claude`（Schema + YAML 結構化 Prompt）
  - `willwulfken/MidJourney-Styles-and-Keywords-Reference`、`jtatum/srefs`（藝術媒介與風格詞彙庫）

---

## 三、素材選題決策過程

### 1. 為什麼排除直接拿「長篇筆記」硬塞生圖？
- AI 圖片不適合承載大量文字段落；正確做法是把核心知識或命題「脫水濃縮」成 **1 句大標／核心提問（海報）** 或 **1 個幾何視覺隱喻＋最多 3 個短關鍵詞（學習圖卡）**。

### 2. 為什麼最終不強行綁定 `Epoch-Kairos`？
- 檢查既有專案 `Epoch-Kairos` 後確認，該專案已有一套極為完整且克制的純文字卡片與 SVG 機制圖規範（`DESIGN.md`、`paper-card-writer`）。
- 雖然 `Epoch-Kairos` 確實缺少對外用的 `og:image` 與 GitHub Social Preview，但為了單週作業而強行套入多種類型 AI 插圖並不合適，將兩件事切開才能維持兩個專案各自的純粹性。

### 3. 候選個人興趣方案比較與定案
- 考慮了兩個與個人生活真實連結的主題：
  - **方案 A：四學科藏書紀錄（物理、心理學、哲學、數學）** — 記錄拼多多買過的書，兼具實用性、持續性與思辨美感。
  - **方案 B：古典鋼琴與聲學視覺** — 結合彈鋼琴興趣與 ECM Records／圖形樂譜極簡風格。
- **最終決定**：採用 **方案 A**，並將專案正式命名為 **`Unread / Read`**。
  - **命名意涵**：呼應買了許多書卻常常分不清讀過沒的真實日常，同時可作為設計系統的「檔案狀態印章」：`[ ] UNREAD`（未讀）與 `[×] READ`（已讀）（若避免生圖模型誤判方框符號，亦可寫成 `STATUS: UNREAD` / `STATUS: READ`）。

---

## 四、視覺系統與四種圖片類型設計

### 1. 色彩與媒介規範（Style Anchor）
- **媒介**：雙色 Risograph 孔版印刷質感 ＋ 瑞士國際主義網格排版（Swiss Grid）＋ 未漂白紙張纖維紋理 ＋ 微小網點顆粒 ＋ 角落印刷十字對位標記。
- **65 / 25 / 10 色彩預算**：
  - 65% 背景底色：象牙棉紙白 `#EFECE6`
  - 25% 線條與文字：消光炭墨黑 `#171717`
  - 10% 學科單一重點色（每張圖僅用一種）：
    - 物理 Physics：`#FF4F00`（國際信號橙）
    - 數學 Mathematics：`#1B4DFF`（群青鈷藍）
    - 心理學 Psychology：`#2D6A4F`（鼠尾草墨綠）
    - 哲學 Philosophy：`#7A1F2B`（勃艮第深酒紅）
    - 綜合總覽 Archive：`#1F2A44`（深炭藍）
- **留白原則**：每張圖至少保留 40% 負空間。
- **反面禁忌**：嚴禁 3D 塑膠光澤、霓虹漸層光暈、寫實照片與書堆插畫、滿版長段落文字。

### 2. 涵蓋的四種圖片類型（Format Adapters）
1. **單書展覽海報（Poster, 2:3 直式）**：單一巨型幾何隱喻 ＋ 書名／作者 ＋ 一句 10 字內核心提問 ＋ `STATUS: UNREAD / READ`。
2. **概念學習圖卡（Learning Card, 3:4 直式）**：65% 幾何圖解區 ＋ 35% 標註區，呈現書中單一機制或對比（1 個標題 ＋ 最多 3 個短關鍵詞）。
3. **書單總覽封面（Cover, 16:9 橫式）**：不對稱構圖，一側 45% 乾淨留白放書單標題，另一側放置四學科幾何符號矩陣。
4. **藏書票／圖騰插畫（Ex-Libris, 1:1 方形，選用）**：純無字或僅編號的幾何象徵圖騰。

---

## 五、後續實作步驟檢查清單

- [x] 確定主題與專案名稱：`Unread / Read`
- [x] 建立 GitHub 遠端倉庫：`https://github.com/zhi816/Unread-Read.git`
- [ ] 在 AI 工具（ChatGPT 專案 / Gemini Gem）建立專案並貼入 [`prompts/system-instructions.md`](../prompts/system-instructions.md)
- [ ] 挑選 3 本已購書籍填入 [`books/reading-list.md`](../books/reading-list.md)
- [ ] 生成第一張「母圖（Key Visual）」，挑選最滿意版本下載並設為後續參考圖以鎖定風格一致性
- [ ] 依序產出至少 3 種不同類型圖片：海報（2:3）、學習圖卡（3:4）、書單封面（16:9）
- [ ] 整理作業步驟三「製作流程說明」（記錄規則設計、參考圖固定、以及修正風格漂移的過程）
