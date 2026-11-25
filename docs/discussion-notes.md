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

---

## 六、提示詞演進與風格收斂紀錄（2026-11-25 至 2026-11-26）

> 本節完整紀錄 `prompts/experiments/01` 至 `08` 的反覆實測、翻車診斷與設計決策，可直接作為第十二週作業步驟三「Agent 設定方法、修正風格漂移與排版迭代說明」之核心素材。

### 1. 補充開源參考調研與「純 AI 生圖」底線確立
- **補充參考開源專案**：
  - `GenielabsOpenSource/style-consistency-ai`：強調以 Reference Atlas 基準母圖、Minimal Delta 最小變動與 Corrective Guidelines（糾偏條款）維持跨圖一致性。
  - `PicoTrex/Awesome-Nano-Banana-images`、`JimmyLv/awesome-nano-banana`：Gemini / Nano Banana 生態之編輯感插畫與海報結構配方。
  - `flaqai/awesome-gpt-image-2-prompt`：Prompt as Code 結構化排版階層、明確文字階層與精準字串約束。
  - `anthropics/skills`（`canvas-design`）：兩段式設計哲學流程（Phase 1 先寫構成宣言 Design Manifesto，Phase 2 再落筆於畫布，強調只鎖美學基因、不綁死制式模板）。
  - `zeke/swiss-design-skill`、`rampstackco/swiss-style-theme`、`swiss-ui/core`：供後續靜態網頁展示頁（`TD-003`）參考的零建置瑞士網格 CSS 規範。
- **工程與作業底線決策**：明確排除以程式繪圖或 SVG 後製疊字（例如 `p5.riso`）來規避生圖模型的錯字問題，堅持**純靠 AI Agent 專案指示一次生成完整圖片**，確保完全貼合第十二週作業「統一風格圖像產生的 Agent」評分核心。

### 2. 八版實驗提示詞（`prompts/experiments/`）實測診斷與修正脈絡

#### 階段 A：基礎規範測試與「提示詞漏印」診斷（`01`–`03`）
- **測試檔案**：[01-style-atlas-risograph.md](../prompts/experiments/01-style-atlas-risograph.md)、[02-editorial-ink-doodle.md](../prompts/experiments/02-editorial-ink-doodle.md)、[03-embossed-swiss-typography.md](../prompts/experiments/03-embossed-swiss-typography.md)。
- **實測發現的三個關鍵問題**：
  1. **技術規格漏印（Prompt Leakage）**：指令中若出現 `0.75pt–1.25pt`、`2:3 POSTER`、`DOUBLE-COLOR RISOGRAPH`、`CONTEMPORARY DESIGN ARCHIVE` 等設計元詞彙，生圖模型會誤將其直接當成文案印進座標線與頁尾。
  2. **文字過載與微距視角縮版**：`03` 同時要求 `Flat-lay Graphic Print` 與 7 組以上文字，導致畫面外圈多出灰色桌面邊框、壓縮海報本體面積，底部極小繁體中文筆劃模糊崩壞。
  3. **精簡四組文案的高穩定度**：`02` 僅保留「書名、作者、1 句極短提問、`NO.XX STATUS`」四組文字且保持大留白，實現中英文零錯字；但編排屬於手繪敘事風，若未指定編號會出現模型自編編號（如 `NO. 24`）的情況。
- **解法**：建立 **Text Whitelist（文字白名單）**，刪除所有 `pt` 數值與比例元詞彙，規定僅能出現使用者提供的四組精確文案，且核心提問限制於 8–10 字內。

#### 階段 B：文字圖形海報實驗與減法修正（`04`–`05`）
- **動機**：初期模板規定過死，導致不同書籍容易長成相同的「上標題＋中圖解＋下頁尾」公式，缺乏平面海報的創意發散度。參考當代文字圖形海報靈感與 `canvas-design` 兩段式宣言後，建立 [04-kinetic-typo-graphic.md](../prompts/experiments/04-kinetic-typo-graphic.md)。
- **色彩基調升級**：依審美評估將 65% 背景由溫暖象牙米白（`#EFECE6`）調整為高張力**純淨畫廊白（`#FFFFFF` / `#FAFAFA`）**搭配極致純黑（`#0A0A0A`）與 10% 單一學科色，拉開黑白銳利度。
- **踩坑與反效果紀錄**：
  1. **無融合感的巨字堆疊**：首輪放開構圖後，模型僅將厚重粗黑體放得極大並斜切色帶，搭配散落刻度與雜點，文字與幾何呈現兩層分離。
  2. **過度疊加規則引發的「徽章太極化」**：當在 `04` 同時強制「補滿 25% 黑塊＋弧形軌道排字＋雙渦旋」，模型直接退化成復古社團徽章與太極陰陽魚，且彎曲排字造成英文拼字錯誤（`NEW SEW SCIENCE`）與作者譯名擅改。
- **減法重構（`05`）**：建立 [05-brutalist-minimal-fusion.md](../prompts/experiments/05-brutalist-minimal-fusion.md)，大幅精簡指令長度，明訂**禁止弧形彎字、禁止徽章構圖、文字一律直線排列**。實測物理／數學題材時純白留白與黑墨張力明顯改善；但套用至心理／哲學書目時暴露「萬用幾何黑圓切片與書籍內容不搭嘎」及「90 度側轉長串英文破字」兩個盲點。
- **測試流程經驗**：發現於同一個對話串連續測圖會產生「跨輪記憶殘留」（沿用前一張的弧形排字或錯字譯名），後續測試新版指令須開全新對話窗口以確保獨立驗證。

#### 階段 C：多路線拆解、通用性原則校正與風格統一收斂（`06`–`08`）
- **多路線試驗與通用性修正（`06`）**：建立 [06-multi-route-editorial-poster.md](../prompts/experiments/06-multi-route-editorial-poster.md)，將構圖拆為五大路線（Routes A–E）並禁止「置中三明治構圖（上置中標＋中正方圖＋下置中字）」。同時修正一項關鍵 Prompt 原則：**嚴禁在通用系統指令中寫死特定書名與特定物件範例**，以免模型遇到該書時照抄硬拼或污染其他書籍，全面清除 `prompts/` 內特定書目殘留。
- **跨學科風格斷層診斷**：以 `06` 實測心理學（路線 A：人頭與大腦剪影）與數學（路線 C：拓撲線網與半調點陣向量射線）後，確認路線 C 在現代美感、純白留白比例與中英字體銳利度上表現最佳；若與具象實心剪影混用，系列並列時會產生明顯風格斷層。
- **「寫實雕版肖像」誤觸發與去細節校正（`07`）**：建立 [07-optical-halftone-system.md](../prompts/experiments/07-optical-halftone-system.md) 統一全系列採用路線 C 語法。當嘗試允許「具象人物改以等高線網格繪製」時，模型被觸發寫實鈔票雕版人像先驗，刻出完整五官、鬍鬚與皮膚紋理，並於右上角硬切白色長方形貼紙蓋字。隨即修訂 `07`，明訂「去寫實五官／去細節幾何抽離」與「禁止硬貼白方塊遮蓋圖形」。
- **最終美學定案：純平滑線條位移系統（`08` 初版與實測精修）**：對比純線條藝術參考（透過等距平行線與同心波紋的平滑隆起與疏密變化模擬無五官形體與空間深淵），確立排斥「無規律手繪亂線（Chaotic scribbles）」與「實心小人剪影」的共識，建立 [08-line-displacement-system.md](../prompts/experiments/08-line-displacement-system.md)。
  - **初版實測再診斷**：實測後發現模型將多個構圖原型以 `+` 號混搭，並把「波紋摺疊」與「階梯狀錯位（Stepped shear）」直接具現成尖銳鋸齒斑馬折紙，且細碎深酒紅裂隙塞在粗黑線縫間顯得暗沉；左側純白留白與建築明體排版則表現良好。
  - **精修定案四原則**：
    1. **唯一平滑造物語法**：改為「平滑連續、互不相交的等距細線＋柔和半調點陣（Soft halftone dot shading）」，嚴禁尖銳折角、波紋摺疊、階梯錯位、外輪廓描邊、寫實五官與實心剪影。
    2. **嚴禁混搭原型**：四種獨立線條原型每次僅擇一執行，不准使用 `+` 號混搭。
    3. **10% 學科色雙向融入（2C）**：衝突與張力不再由黑白線自己折斷，而是透過「3–5 條平滑關鍵線條轉色」或「單一銳利向量射線穿刺」乾淨呈現。
    4. **主動留白收束**：線條場佔 55%–65% 後齊整止步或平順漸隱，自然讓出連貫 `#FFFFFF` 純白空間承載直排明體與瑞士無襯線體。

### 3. 待驗證與下一步（銜接 `TD-002`、`TD-003`）
- [ ] 開立全新對話測試 [08-line-displacement-system.md](../prompts/experiments/08-line-displacement-system.md)，分別實測心理／哲學與物理／數學書目，驗證跨學科並列時「風格高度統一 ＋ 構圖自由變化」的實際產出。
- [ ] 確認 `08` 穩定後，將其正式升格更新至 [`prompts/system-instructions.md`](../prompts/system-instructions.md)，並依序產出四種比例成品（`2:3` 海報、`3:4` 學習圖卡、`16:9` 橫幅、`9:16` 書籤）供作業繳交與 `index.html` 展示頁使用。
