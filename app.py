import streamlit as st
import pandas as pd
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# --- 網頁設定 (換個望遠鏡 Icon 增加探測儀的感覺) ---
st.set_page_config(page_title="ShiFu 藍海市場探測儀", layout="wide", page_icon="🔭")

st.title("🔭 藍海市場情報雷達 (Blue Ocean Radar)")
st.caption("即時掃描 PTT 藍海看板，捕捉 30-40 歲主力消費族群的真實焦慮與痛點。")

# --- 側邊欄：API 金鑰設定 ---
st.sidebar.header("⚙️ 核心動力設定")
api_key = st.sidebar.text_input("請輸入 Gemini API Key 以啟動分析核心", type="password")
st.sidebar.markdown("---")
st.sidebar.info("💡 本系統專為大師課業 (ShiFu) 課程開發團隊設計，旨在透過社群聆聽 (Social Listening) 挖掘具備高轉換潛力的藍海課程主題。")

# --- 載入數據 (如果沒抓到會提示) ---
try:
    df = pd.read_csv('social_trends_data.csv')
    top_titles = df['post_title'].head(50).tolist()
    titles_text = "\n".join([f"- {title}" for title in top_titles])
except FileNotFoundError:
    st.error("⚠️ 找不到數據源！請先在終端機執行 `python real_ptt_scraper.py` 來攔截最新社群情報。")
    st.stop()

# --- 區塊 1：情報儀表板 (Dashboard) ---
# 使用欄位 (columns) 並排顯示關鍵指標，營造戰情室的感覺
col1, col2, col3, col4 = st.columns(4)
col1.metric("雷達監測總貼文", f"{len(df)} 篇")
col2.metric("最高討論熱度", f"{df['engagement_score'].max()} 推")
col3.metric("鎖定客群", "30-40 歲高消費力")
col4.metric("監測看板", "買房/育兒/職涯")

st.divider()

# --- 區塊 2：分頁切換 (Tabs) ---
# 將原始數據與 AI 分析拆開，讓介面更清爽專業
tab_data, tab_ai = st.tabs(["📊 原始數據信號庫 (Raw Signals)", "🧠 AI 大師企劃室 (Course Lab)"])

with tab_data:
    st.subheader("最新攔截到的社群痛點明細")
    # 使用 use_container_width 讓表格自動填滿，並隱藏醜醜的 index
    st.dataframe(df, use_container_width=True, hide_index=True)

with tab_ai:
    st.subheader("🚀 啟動高階語意分析，將雜亂數據轉化為爆款企劃")
    
    # 使用 type="primary" 讓按鈕變成主視覺顏色，更吸睛
    if st.button("✨ 點擊生成【大師課程提案與大師畫像】", type="primary"):
        if not api_key:
            st.warning("請先在左側面板輸入 Gemini API Key！")
        else:
            # 使用 status 取代 spinner，營造更高級的運算過程感
            with st.status("正在解析社群情緒與知識缺口...", expanded=True) as status:
                st.write("啟動 Gemini 2.5 Flash 核心...")
                st.write("萃取 PTT 鄉民痛點矩陣...")
                st.write("交叉比對潛力藍海市場...")
                
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    prompt = f"""
                    你是一位「大師課業 (ShiFu)」的頂尖課程產品經理 (Course PM)。
                    以下是我們透過網路爬蟲，抓取近期在 PTT 藍海看板上，互動熱度排名前 50 的真實討論標題：
                    
                    {titles_text}
                    
                    請分析這些討論背後隱藏的「知識焦慮」與「痛點」，找出一個目前市場上最渴望，但缺乏系統性教學的「藍海主題」。
                    並產出一份【新課程開發企劃與大師探測報告】，格式必須包含：
                    
                    ### 📊 市場趨勢洞察
                    (精煉總結這批數據反映出大眾最關心的 2 個核心痛點)
                    
                    ### 💡 爆款課程提案
                    * **課程名稱：** (請下一個極具吸引力、能提高轉換率的募資標題)
                    * **目標受眾 (TA)：** * **課程核心承諾：** (學完能解決什麼問題)
                    
                    ### 👤 潛力大師畫像 (BD 尋人指南)
                    為了這堂課，ShiFu 應該去網羅什麼背景的講師？請給出具體的「大師條件」(例如：具備某領域幾年經驗、在社群上有何種特質)，讓我們的 BD 團隊能按圖索驥去談合作。
                    
                    請直接輸出報告，不要加上任何 Markdown 的程式碼區塊符號 (```) 或額外的問候語。
                    """
                    
                   # 降低安全審查等級，避免被 PTT 鄉民的真實用語觸發阻擋機制
                    response = model.generate_content(
                        prompt,
                        safety_settings={
                            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                        }
                    )
                    
                    # 狀態列更新為完成，並自動收合
                    status.update(label="企劃生成完畢！鎖定高潛力市場缺口。", state="complete", expanded=False)
                    
                    # 將結果放在一個有邊框的容器裡
                    with st.container(border=True):
                        # 增加 Error Handling 防護網：確認模型真的有吐出文字
                        if response.parts:
                            st.markdown(response.text)
                        else:
                            st.warning("⚠️ 報告生成被 API 強制攔截。這通常是因為這批 PTT 標題中出現了極度敏感的字眼。請嘗試重新抓取數據或過濾髒話。")
                            # 面試時如果遇到這個警告，你可以從容地向面試官解釋 API 的安全機制！
                    
                except Exception as e:
                    status.update(label="系統發生錯誤", state="error", expanded=True)
                    st.error(f"錯誤訊息：{e}")