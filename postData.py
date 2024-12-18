import csv

def adjust_scores(input_file, output_file):
    # 读取CSV文件
    with open(input_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    # 调整评分
    for row in data:
        try:
            # 将评分转换为浮点数
            score = float(row['客户评分'])
            label = row['label']

            # 根据规则调整评分
            if label == 'positive' and score < 3.0:
                score += 1.0
            elif label == 'negative' and score > 3.0:
                score -= 1.0

            # 更新评分
            row['客户评分'] = score
        except ValueError:
            print(f"无法解析评分: {row['客户评分']}")

    # 计算每个酒店的平均评分
    hotel_scores = {}
    for row in data:
        hotel_name = row['酒店名称']
        score = float(row['客户评分'])

        if hotel_name not in hotel_scores:
            hotel_scores[hotel_name] = []
        hotel_scores[hotel_name].append(score)

    # 计算平均分并保留两位小数
    hotel_averages = {}
    for hotel_name, scores in hotel_scores.items():
        average_score = round(sum(scores) / len(scores), 2)  # 保留两位小数
        hotel_averages[hotel_name] = average_score

    # 写入调整后的评分和平均分到新的CSV文件
    with open(output_file, mode='w', encoding='utf-8', newline='') as file:
        fieldnames = reader.fieldnames + ['平均评分']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for row in data:
            hotel_name = row['酒店名称']
            row['平均评分'] = f"{hotel_averages[hotel_name]:.2f}"  # 格式化平均分为两位小数
            writer.writerow(row)

    print(f"处理完成，结果已保存到 {output_file}")

# 调用函数
input_file = 'output.csv'  # 输入的CSV文件名
output_file = 'output2.csv'  # 输出的CSV文件名
adjust_scores(input_file, output_file)