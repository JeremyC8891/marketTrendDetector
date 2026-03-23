import streamlit as st
import pandas as pd
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# --- 新增的視覺化與斷詞套件 ---
import jieba
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import platform

# --- 網頁設定 ---
st.set_page_config(page_title="ShiFu 藍海市場探測儀", layout="wide", page_icon="🔭")

st.title("🔭 藍海市場情報雷達 (Blue Ocean Radar)")
st.caption("即時掃描 PTT 藍海看板，捕捉 30-40 歲主力消費族群的真實焦慮與痛點。")

# --- 側邊欄設定 ---
st.sidebar.header("⚙️ 核心動力設定")
api_key = st.sidebar.text_input("請輸入 Gemini API Key 以啟動分析核心", type="password")
st.sidebar.markdown("---")
st.sidebar.info("💡 本系統專為大師課業 (ShiFu) 課程開發團隊設計，旨在透過社群聆聽 (Social Listening) 挖掘具備高轉換潛力的藍海課程主題。")

# --- 載入數據 ---
try:
    df = pd.read_csv('social_trends_data.csv')
    top_titles = df['post_title'].head(50).tolist()
    titles_text = "\n".join([f"- {title}" for title in top_titles])
except FileNotFoundError:
    st.error("⚠️ 找不到數據源！請先在終端機執行 `python real_ptt_scraper.py`。")
    st.stop()

# --- 區塊 1：情報儀表板 ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("雷達監測總貼文", f"{len(df)} 篇")
col2.metric("最高討論熱度", f"{df['engagement_score'].max()} 推")
col3.metric("鎖定客群", "30-40 歲高消費力")
col4.metric("監測看板", "買房/育兒/職涯")

st.divider()

# --- 區塊 2：分頁切換 ( Tabs 擴充為 3 個) ---
tab_data, tab_keyword, tab_ai = st.tabs([
    "📊 原始數據信號庫", 
    "🔥 核心痛點關鍵字", 
    "🧠 AI 大師企劃室"
])

# 【頁籤 1：原始數據】
with tab_data:
    st.subheader("最新攔截到的社群痛點明細")
    st.dataframe(df, use_container_width=True, hide_index=True)

# 【頁籤 2：關鍵字儀表板 (文字雲 + 熱力長條圖)】
with tab_keyword:
    st.subheader("鄉民焦慮關鍵字萃取 (Keyword Extraction)")
    
    with st.spinner('正在執行 NLP 中文斷詞與頻率分析...'):
        # 1. 彙整所有標題文字
        all_text = " ".join(df['post_title'].tolist())
        
        # 2. 使用 jieba 進行斷詞
        words = jieba.lcut(all_text)
        
        # 3. 過濾停用詞 (Stop words) 與單一字元
        stop_words = {'的', '了', '是', '嗎', '怎麼', '在', '我', '有', '請教', '如何', '什麼', '問題', '大家', '請', '與', '和', '不', '都', '會', '被', '想'}
        filtered_words = [w for w in words if len(w) > 1 and w not in stop_words]
        
        # 4. 計算詞頻
        word_counts = Counter(filtered_words)
        top_words = word_counts.most_common(20) # 取前 20 大關鍵字
        
        # 建立兩欄式排版：左邊熱力圖表，右邊文字雲
        col_k1, col_k2 = st.columns([1, 1.5])
        
        with col_k1:
            st.markdown("##### 📈 Top 20 痛點熱力分佈")
            # 轉換為 DataFrame 方便 Streamlit 顯示
            df_words = pd.DataFrame(top_words, columns=['關鍵字', '出現次數'])
            # 使用強大的 column_config 製作熱力長條圖
            st.dataframe(
                df_words,
                column_config={
                    "出現次數": st.column_config.ProgressColumn(
                        "熱度 (出現次數)",
                        help="關鍵字出現的頻率",
                        format="%d 次",
                        min_value=0,
                        max_value=int(df_words['出現次數'].max()),
                    ),
                },
                hide_index=True,
                use_container_width=True
            )
            
        with col_k2:
            st.markdown("##### ☁️ 焦慮文字雲")
            # 處理系統字體，避免中文變成方塊 (Tofu)
            sys_plat = platform.system()
            if sys_plat == 'Darwin': # Mac OS
                font_path = '/System/Library/Fonts/PingFang.ttc'
            elif sys_plat == 'Windows': # Windows
                font_path = 'C:\\Windows\\Fonts\\msjh.ttc' # 微軟正黑體
            else:
                font_path = None
                
            try:
                # 產生文字雲
                wc = WordCloud(
                    font_path=font_path,
                    background_color='white',
                    width=600, 
                    height=400,
                    colormap='magma' # 使用像熱力圖的配色
                ).generate_from_frequencies(word_counts)
                
                # 使用 matplotlib 畫出並在 Streamlit 顯示
                fig, ax = plt.subplots()
                ax.imshow(wc, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            except Exception as e:
                st.warning(f"⚠️ 無法載入中文字體，請確認您的作業系統字體路徑。({e})")

# 【頁籤 3：AI 企劃室】
with tab_ai:
    st.subheader("🚀 啟動高階語意分析，將雜亂數據轉化為爆款企劃")
    if st.button("✨ 點擊生成【大師課程提案與大師畫像】", type="primary"):
        if not api_key:
            st.warning("請先在左側面板輸入 Gemini API Key！")
        else:
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
                    ### 💡 爆款課程提案
                    ### 👤 潛力大師畫像 (BD 尋人指南)
                    請直接輸出報告，不要加上任何 Markdown 的程式碼區塊符號。
                    """
                    
                    response = model.generate_content(
                        prompt,
                        safety_settings={
                            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                        }
                    )
                    
                    status.update(label="企劃生成完畢！鎖定高潛力市場缺口。", state="complete", expanded=False)
                    with st.container(border=True):
                        if response.parts:
                            st.markdown(response.text)
                        else:
                            st.warning("⚠️ 報告生成被 API 強制攔截。")
                except Exception as e:
                    status.update(label="系統發生錯誤", state="error", expanded=True)
                    st.error(f"錯誤訊息：{e}")