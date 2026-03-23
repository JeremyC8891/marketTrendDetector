import pandas as pd
import numpy as np
import random

np.random.seed(2026)

# 模擬 800 篇近期各大社群論壇的熱門貼文
n_posts = 800

platforms = np.random.choice(['PTT Stock', 'Dcard 投資', 'Tech_Job', '社群行銷社團'], n_posts)

# 模擬真實的網友討論標題 (包含各種痛點與求助)
title_templates = [
    "有人用 Python 寫過自動下單機器人嗎？求帶",
    "現在開始存 ETF 還來得及嗎？",
    "短影音流量越來越差，演算法是不是又改了？",
    "想轉職數據分析，SQL 跟 Python 哪個要先學？",
    "美股期權好難懂，有推薦的新手資源嗎？",
    "台股當沖一直賠，心態快崩潰...",
    "Docker 部署微服務一直報錯，求解",
    "TikTok 帶貨真的能賺錢嗎？真實心得分享",
    "如何利用 AI 工具自動產出 IG 貼文？",
    "量化交易的回測數據大家都去哪裡抓？"
]

titles = [random.choice(title_templates) for _ in range(n_posts)]

# 加入隨機變異，讓標題看起來更真實
for i in range(len(titles)):
    if "Python" in titles[i]:
        titles[i] += random.choice([" (附程式碼)", " 完全新手看不懂", " 拜託大神救救我"])
    if "ETF" in titles[i]:
        titles[i] = titles[i].replace("ETF", random.choice(["0050", "00878", "高股息 ETF"]))

# 模擬互動指標
likes = np.random.exponential(scale=500, size=n_posts).astype(int) + 10
comments = (likes * np.random.uniform(0.1, 0.5, n_posts)).astype(int)
shares = (likes * np.random.uniform(0.01, 0.1, n_posts)).astype(int)

# 計算綜合熱度分數 (Engagement Score)
engagement_score = likes * 1 + comments * 2 + shares * 5

df = pd.DataFrame({
    'platform': platforms,
    'post_title': titles,
    'likes': likes,
    'comments': comments,
    'shares': shares,
    'engagement_score': engagement_score
})

# 只保留熱度最高的前 200 篇貼文作為分析樣本
top_trends_df = df.sort_values(by='engagement_score', ascending=False).head(200)
top_trends_df.to_csv('social_trends_data.csv', index=False)

print("✅ 成功生成社群趨勢數據：social_trends_data.csv")