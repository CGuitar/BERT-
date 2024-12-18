# import pandas as pd
#
# # 读取Excel文件
# input_file = '携程-酒店评论2.xlsx'  # 输入的Excel文件名
# output_file = 'hotel_reviews.csv'  # 输出的CSV文件名
#
# # 使用 pandas 读取 Excel 文件
# df = pd.read_excel(input_file)
#
# # 将数据保存为 CSV 文件
# df.to_csv(output_file, index=False, encoding='utf-8-sig')
#
# print(f"数据已成功保存为 {output_file}")


import pandas as pd
import csv

# 读取Excel文件
input_file = '携程-酒店评论.xlsx'  # 输入的Excel文件名
output_file = 'hotel_reviews.csv'  # 输出的CSV文件名

# 使用 pandas 读取 Excel 文件
df = pd.read_excel(input_file)

# 替换评价内容中的换行符
df['评价内容'] = df['评价内容'].str.replace('\n', ' ', regex=False)  # 将换行符替换为空格

# 将数据保存为 CSV 文件，并使用双引号包裹所有字段
df.to_csv(output_file, index=False, encoding='utf-8-sig', quoting=csv.QUOTE_ALL)

print(f"数据已成功保存为 {output_file}")

