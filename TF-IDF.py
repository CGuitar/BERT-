import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

# 读取CSV文件
df = pd.read_csv('processed_file.csv')

# 计算TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['评价内容'])

# 计算余弦相似度
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# 设定相似度阈值
threshold = 0.6

# 创建集合来存储已经保留的索引
unique_indices = set()

# 创建集合来存储需要删除的索引
duplicate_indices = set()

# 创建一个字典来存储重复的评价内容对
duplicate_pairs = []

# 使用 tqdm 添加进度条
for i in tqdm(range(len(cosine_sim)), desc="Processing"):
    if i not in duplicate_indices:
        for j in range(i + 1, len(cosine_sim)):
            if cosine_sim[i][j] > threshold:
                duplicate_indices.add(j)
                # 记录重复的评价内容对
                duplicate_pairs.append((i, j, cosine_sim[i][j]))

# 保留的索引是所有索引减去需要删除的索引
unique_indices = set(range(len(df))) - duplicate_indices

# 从原始数据框中筛选出保留的记录
df_unique = df.iloc[list(unique_indices)]

# 保存结果
df_unique.to_csv('unique_reviews.csv', index=False)

# 对比列出重复度高的评价内容
if duplicate_pairs:
    print("\n以下是重复度高的评价内容对（相似度 > {:.2f}）：".format(threshold))
    for pair in duplicate_pairs:
        i, j, sim = pair
        print(f"\n相似度: {sim:.4f}")
        print(f"评价内容 {i}:\n{df.iloc[i]['评价内容']}")
        print(f"评价内容 {j}:\n{df.iloc[j]['评价内容']}")
        print("-" * 40)
else:
    print("没有找到重复度高的评价内容。")

