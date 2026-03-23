# 🔭 藍海市場情報雷達 (Blue Ocean Market Radar)

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-Web_Scraping-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_API-8E75B2?logo=google&logoColor=white)

> **「用真實社群數據，精準探測下一個千萬級線上課程的知識缺口。」**
> 專為 課程開發 團隊設計的情報戰情室。自動化攔截 30-40 歲主力消費族群的真實焦慮，並透過 AI 瞬間轉化為具備高轉換率的爆款課程企劃。

---

## ✨ 核心功能與工程亮點
* **📊 戰情室 UI 介面 (Dashboard)**：拋棄傳統數據分析的冰冷報表，採用動態關鍵指標 (Metrics) 與分頁設計，讓非技術背景的企劃與管理層也能一目了然。
* **🕸️ 真實社群聆聽 (Social Listening)**：實作 Python 爬蟲繞過年齡驗證，自動抓取 PTT 藍海看板 (`BabyMother`, `home-sale`, `CareerPlan`) 的高熱度真實文章。
* **🛡️ 企業級 LLM 串接 (Safety Bypass)**：針對 PTT 鄉民生猛、非結構化的真實語料，客製化調校 Gemini 2.5 Flash 的安全過濾閾值 (HarmBlockThreshold)，確保系統在處理真實社群數據時具備 Production-ready 的極高穩定度。
* **🚀 自動化企劃與大師畫像**：一鍵生成完整的「課程提案」與「潛力講師畫像」，直接為 BD 團隊提供精準的尋人雷達。

---

## 🏆 實戰案例展示 (Case Study)
透過本雷達分析近期 PTT `BabyMother` (媽寶板) 數據，系統成功挖掘出極具潛力的藍海提案：

* **隱藏痛點**：新手父母極度缺乏睡眠，且面臨傳統育兒觀念與現代科學育兒的嚴重衝突。
* **💡 AI 爆款提案：【新手爸媽不崩潰：0-1歲科學睡眠與情緒教養課】**
* **大師尋人指南 (BD 畫像)**：
  * 具備國際認證的嬰幼兒睡眠顧問 (如 IACSC)。
  * 在社群上擁有「科學育兒但不焦慮」的人設，本身也是二寶/三寶媽，具備高度同理心。

---

## 📂 專案結構
```text
marketTrendDetector/
├── app.py                      # 戰情室 UI 主程式與 AI 分析核心
├── real_ptt_scraper.py         # 藍海看板真實數據爬蟲腳本
├── social_trends_data.csv      # 爬蟲自動攔截的社群情報資料庫
└── README.md                   # 專案說明文件

🛠️ 技術堆疊 (Tech Stack)
環境與套件管理: uv

網路爬蟲與資料擷取: requests, BeautifulSoup4, pandas

前端與情報儀表板: Streamlit

生成式 AI 與 NLP 分析: Google Gemini API (gemini-2.5-flash)

🚀 快速啟動 (Quick Start)
1. 建立環境與安裝依賴
# 使用 uv 建立並啟動虛擬環境
uv venv
source .venv/bin/activate  # Mac 或 Linux
# .venv\Scripts\activate   # Windows

# 安裝專案所需套件
uv pip install requests beautifulsoup4 pandas streamlit google-generativeai

2. 攔截最新社群情報
執行爬蟲腳本，系統將自動抓取 PTT 藍海看板並更新 social_trends_data.csv：
python real_ptt_scraper.py

3. 啟動情報雷達戰情室
streamlit run app.py

Note: 啟動後，請於瀏覽器打開 http://localhost:8501，在左側邊欄輸入 Gemini API Key 即可解鎖核心分析功能。
