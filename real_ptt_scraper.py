import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def fetch_ptt_board(board_name, pages_to_scrape=10):
    """抓取 PTT 指定看板的文章"""
    print(f"🚀 開始抓取 PTT {board_name} 板，預計抓取 {pages_to_scrape} 頁...")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    # 繞過 PTT 十八歲驗證
    cookies = {'over18': '1'}
    
    base_url = f"https://www.ptt.cc/bbs/{board_name}/index.html"
    article_list = []
    
    for i in range(pages_to_scrape):
        res = requests.get(base_url, headers=headers, cookies=cookies)
        if res.status_code != 200:
            print(f"❌ 無法讀取頁面: {base_url}")
            break
            
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 解析文章區塊
        items = soup.find_all('div', class_='r-ent')
        for item in items:
            title_element = item.find('div', class_='title').find('a')
            if not title_element:
                continue # 文章可能被刪除
                
            title = title_element.text.strip()
            # 排除公告與版規
            if "[公告]" in title or "[版規]" in title:
                continue
                
            # 抓取推文數 (轉化為熱度分數)
            push_element = item.find('div', class_='nrec').text.strip()
            push_count = 0
            if push_element == '爆':
                push_count = 100
            elif push_element.startswith('X'):
                push_count = -10 # 被噓
            elif push_element.isdigit():
                push_count = int(push_element)
                
            article_list.append({
                'platform': f'PTT {board_name}',
                'post_title': title,
                'engagement_score': push_count
            })
            
        # 尋找「上一頁」的連結
        controls = soup.find('div', class_='btn-group btn-group-paging').find_all('a')
        if len(controls) > 1:
            prev_page_link = controls[1].get('href')
            if not prev_page_link:
                break
            base_url = "https://www.ptt.cc" + prev_page_link
            time.sleep(0.5) # 禮貌性延遲，避免被鎖 IP
        else:
            break
            
    return article_list

# 1. 執行抓取 (鎖定 30-40 歲關注的買房、育兒、職涯焦慮)
print("開始挖掘 30-40 歲族群的藍海市場痛點...\n")
homesale_data = fetch_ptt_board('home-sale', pages_to_scrape=20)   # 買房板
babymother_data = fetch_ptt_board('BabyMother', pages_to_scrape=20) # 媽寶板
career_data = fetch_ptt_board('CareerPlan', pages_to_scrape=15)    # 職涯規劃板

# 2. 合併資料並轉換為 DataFrame
all_data = homesale_data + babymother_data + career_data
df = pd.DataFrame(all_data)

# 3. 過濾掉冷門文章 (只保留推文數大於 20 的熱門討論)，並依照熱度排序
# 提高門檻，確保我們只分析「痛到大家都在討論」的議題
hot_trends_df = df[df['engagement_score'] > 20].sort_values(by='engagement_score', ascending=False)

# 4. 存檔覆蓋數據
hot_trends_df.to_csv('social_trends_data.csv', index=False)

print(f"\n✅ 真實藍海數據抓取完成！共收集 {len(hot_trends_df)} 筆高熱度真實社群討論。")
print("檔案已儲存為：social_trends_data.csv")
print("\n--- 預覽前 5 筆最高熱度痛點 ---")
print(hot_trends_df.head(5))