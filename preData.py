import pandas as pd
import re

# 读取CSV文件
df = pd.read_csv('hotel_reviews.csv')

# 任务1：删除入住时间小于2023年的记录
def extract_year(date_str):
    # 确保 date_str 是字符串类型
    if isinstance(date_str, float) and pd.isna(date_str):
        return None  # 如果是 NaN，返回 None
    try:
        # 提取年份
        year = int(date_str.split('年')[0].split('于')[1])
        return year
    except (AttributeError, ValueError):
        # 如果字符串格式不正确，返回 None
        return None

# 应用函数提取年份
df['入住年份'] = df['入住时间'].apply(extract_year)

# 删除入住年份为 None 或小于2023年的记录
df = df[df['入住年份'].notna() & (df['入住年份'] >= 2023)]

# 任务2：删除评价内容文字数量（不包括标点符号）小于等于5的记录
def count_text_length(text):
    # 确保 text 是字符串类型
    if isinstance(text, float) and pd.isna(text):
        return 0  # 如果是 NaN，返回 0
    try:
        # 使用正则表达式去除标点符号
        cleaned_text = re.sub(r'[^\w\s]', '', text)
        # 返回文字数量
        return len(cleaned_text.strip())
    except (AttributeError, ValueError):
        # 如果字符串格式不正确，返回 0
        return 0

# 应用函数计算评价内容的文字数量
df['评价内容长度'] = df['评价内容'].apply(count_text_length)

# 删除评价内容文字数量小于等于5的记录
df = df[df['评价内容长度'] > 5]

# 删除中间生成的辅助列
df = df.drop(columns=['入住年份', '评价内容长度'])

# 保存处理后的数据到新的CSV文件
df.to_csv('processed_file.csv', index=False)

print("处理完成，结果已保存到 processed_file.csv")