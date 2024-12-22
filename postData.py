import pandas as pd
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.layout import Layout, ManualLayout


def adjust_scores(input_file, output_file):
    # 读取CSV文件
    df = pd.read_csv(input_file, encoding='utf-8')

    # 调整评分
    for index, row in df.iterrows():
        try:
            # 将评分转换为浮点数
            score = float(row['客户评分'])
            label = row['label']

            # 根据规则调整评分
            if label == 'positive' and score < 3.0:
                score += 1.0
            elif label == 'negative' and score > 3.0:
                score -= 1.0

            # 确保评分在合理范围内
            score = max(1.0, min(5.0, score))

            # 更新评分
            df.at[index, '客户评分'] = score
        except ValueError:
            print(f"无法解析评分: {row['客户评分']}")
            # 可以选择跳过该行数据
            continue

    # 计算每个酒店的平均评分
    hotel_averages = df.groupby('酒店名称')['客户评分'].mean().round(2)

    # 将平均评分添加到原始数据中
    df['处理后评分'] = df['酒店名称'].map(hotel_averages)

    # 只保留第1、2、8个字段
    selected_columns = df.columns[[0, 1, 7]]  # 选择第1、2、8列
    df_selected = df[selected_columns]

    # 确保第一个字段（酒店名称）不重复
    df_selected = df_selected.drop_duplicates(subset=df_selected.columns[0])

    # 将结果保存为Excel文件
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_selected.to_excel(writer, sheet_name='酒店评分', index=False)

        # 获取工作簿和工作表
        workbook = writer.book
        worksheet = writer.sheets['酒店评分']

        # 添加柱状图
        create_bar_chart(workbook, worksheet, df_selected)

    print(f"处理完成，结果已保存到 {output_file}")



from openpyxl.chart import BarChart, Reference
from openpyxl.chart.layout import Layout, ManualLayout
from openpyxl.chart.axis import NumericAxis

def create_bar_chart(workbook, worksheet, df_selected):
    # 创建柱状图
    chart = BarChart()
    chart.title = "酒店评分 vs 处理后评分"
    chart.x_axis.title = "酒店名称"
    chart.y_axis.title = "评分"

    # 设置数据范围
    rows = df_selected.shape[0] + 1  # 包括表头
    cols = df_selected.shape[1]

    # 添加数据到图表
    data = Reference(worksheet, min_col=2, max_col=3, min_row=1, max_row=rows)
    categories = Reference(worksheet, min_col=1, min_row=2, max_row=rows)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(categories)

    # 设置柱状图样式
    chart.series[0].graphicalProperties.solidFill = "ADD8E6"  # 淡蓝色
    chart.series[1].graphicalProperties.solidFill = "8B0000"  # 深红色

    # 设置 Y 轴的范围为 3-5
    chart.y_axis = NumericAxis(scaling=None)  # 重新定义 Y 轴
    chart.y_axis.scaling.min = 3.6  # 设置 Y 轴最小值
    chart.y_axis.scaling.max = 5  # 设置 Y 轴最大值

    # 确保坐标轴显示数值
    chart.y_axis.majorGridlines = None  # 可选：隐藏网格线
    chart.y_axis.majorTickMark = "out"  # 设置刻度线样式
    chart.y_axis.tickLblPos = "nextTo"  # 设置刻度标签位置
    chart.y_axis.delete = False  # 确保 Y 轴不会被删除

    # 确保 X 轴显示数值
    chart.x_axis.majorTickMark = "out"  # 设置刻度线样式
    chart.x_axis.tickLblPos = "nextTo"  # 设置刻度标签位置
    chart.x_axis.delete = False  # 确保 X 轴不会被删除

    # 放大图表并增加上下留白
    chart.width = 20  # 设置图表宽度
    chart.height = 18  # 设置图表高度

    # 设置布局以增加上下留白
    chart.layout = Layout(ManualLayout(x=-0.1, y=0, h=0.8, w=0.8))

    # 将图表添加到工作表
    worksheet.add_chart(chart, "E1")  # 图表放置在E1位置


# 调用函数
input_file = 'output.csv'  # 输入的CSV文件名
output_file = 'output2.xlsx'  # 输出的Excel文件名
adjust_scores(input_file, output_file)
