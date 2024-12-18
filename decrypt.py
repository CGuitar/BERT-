import csv
from pypinyin import lazy_pinyin
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag
from tqdm import tqdm  # 导入 tqdm 库


# 读取CSV文件
def read_csv(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


# 将中文转换为拼音
def convert_to_pinyin(text):
    return lazy_pinyin(text)


# 将拼音转换回中文
def convert_pinyin_to_chinese(pinyin_list):
    dag_params = DefaultDagParams()
    result = dag(dag_params, pinyin_list, path_num=1, log=True)  # path_num=1 表示只返回一个最可能的结果
    if result:
        return result[0].path  # 返回最可能的中文句子
    return "".join(pinyin_list)  # 如果没有结果，返回原始拼音


# 处理CSV文件中的评价内容
def process_csv(file_path, output_path):
    data = read_csv(file_path)
    for row in tqdm(data, desc="处理进度", unit="行"):  # 使用 tqdm 显示进度条
        # 将评价内容转换为拼音
        pinyin_list = convert_to_pinyin(row['评价内容'])
        # 将拼音转换回中文
        chinese_text = convert_pinyin_to_chinese(pinyin_list)
        # 更新评价内容
        row['评价内容'] = chinese_text

    # 写入新的CSV文件
    with open(output_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# 示例使用
input_file = 'unique_reviews.csv'
output_file = 'final_reviews.csv'
process_csv(input_file, output_file)
