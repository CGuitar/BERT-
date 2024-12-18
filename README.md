@[TOC](用BERT文本情感分析实现酒店评分有效性调整——自然语言处理期末大作业)

# 原题背景与要求

## 背景
由于评论文本自身存在差异，可能会出现**内容不相关**、**简单复制修改**和**无有效内容**等现象，这会妨碍游客从网络评价中获得有价值的信息，也为各网络平台的运营工作带来了挑战。探其根本，自动地评价文本有效性，有助于提升景区和酒店的服务质量，将游客的需求落到实处，同时有利于旅游平台的在线运营。因此，本文融合五项指标，从**相关性**、**完整性**、**可解释性**、**情感性**、**时效性**等角度，自动地评价文本的有效性，并创新性地进行了高效评论排序。

## 要求
对于评论中的文本有效性进行分析，主要是从三方面进行分析。**第一点，有的评论可能是由其他评论简单复制修改后的垃圾评论**；**第二点，有的评论的内容可能与店家无关，是打广告之类的无关内容**；**第三点，有的评论虽然主题与店家相关，但是店家的介绍之类的，没有对店家进行评价**。我们建立的模型主要从这三方面对于评论进行筛选。

---
# 新的观点与实现大纲
+ 在原题要求中的第二点中，因为用户的评论数据来自于各大旅游平台，而多数平台会自动删除过滤掉一些无效信息以及广告，因此对无关内容的筛选，实际意义并不高。
+ 在对大量旅游评论的观察统计后，发现在评论区中，许多用户评论很好，但打分很低；或者评论很差，打分很高。也有不少复制粘贴的评论以及无意义的评论。

**综上所述，我重新调整了需求，以符合现实意义。以下是项目的实现大纲：**

1. 爬取携程网上日本东京的8家平价酒店各200条评论，下面是字段名
   - 酒店名称
   - 酒店总体评分
   - 入住时间
   - 客户评分
   - 评价内容
2. 爬取后的Excel转csv文件
3. 删除2年前的评论
4. 删除字数小于5的评论（不包括标点符号）
5. 使用余弦相似度，用TF-IDF 将评论转换为向量，删除重复度高的评论
6. *对所有评论使用pypinyin+Pinyin2Hanzi实现“中文加密”破解*
7. 使用BERT模型，实现文本情感分析
8. 通过情感分析微调客户评分
9. 重新计算各酒店总体评分


# 项目架构
```
.
├── ./bert
│   ├── ./bert/checkpoints
│   ├── ./bert/data
│   │   ├── ./bert/data/test.txt
│   │   ├── ./data/data/train.txt
│   ├── ./bert/config.py
│   ├── ./bert/exc2csv.py
│   ├── ./bert/postData.py
│   ├── ./bert/preData.py
│   ├── ./bert/process.py
│   ├── ./bert/test.py
│   ├── ./bert/train.py
│   ├── ./bert/TF-IDF.py
│   └── ./bert/decrypt.py
————————————————
```
## 文件解释：
exc2csv.py，preData.py，TF-IDF.py，decrypt.py用于数据预处理
train.py，test.py，process.py，config.py，data，checkpoints用于BERT文本情感分析
postData.py实现最终数据处理

---
# 快速开始

## 一、酒店网评爬取
具体过程略，这里我选择了携程上日本东京300-500的平价酒店，
爬取了{酒店名称，酒店总体评分，入住时间，客户评分，评价内容}五个部分

## 二、Excel转csv
方便后续处理
```shell
pip install -r requirements.txt
python exc2csv.py
```

## 三、删除2年前的评论以及字数小于5的评论（不包括标点符号）
2年前的评论参考价值较低，字数小于5的评论多数为随意评论
```shell
python preData.py
```

## 四、使用余弦相似度，用TF-IDF 将评论转换为向量，删除重复度高的评论
重复度高的评论多数为复制粘贴，或者套用模板
```shell
python TF-IDF.py
```

## * 五、对所有评论使用pypinyin+Pinyin2Hanzi实现“中文加密”破解
什么是“中文加密”: [bilibili-中文加密评论：西班牙餐厅避雷指南！](https://www.bilibili.com/video/BV1MjsLeyEBD?vd_source=56fa190c2c2f18f1c5a6a89188ec1dc1)
因为中文加密多数为容易让外国人以及AI曲解的谐音字。因此想到可以试着重构一下，让汉字变回拼音再变回汉字。
> 例如：
> 喃吃的饭，服务是完全美诱的，千万补药来！ -->
> nan chi de fan, fu wu shi wan quan mei you de, qian wan bu yao lai！ -->
> 难吃的饭，服务是完全没有的，千万不要来！

但因为Pinyin2Hanzi性能较差，没有找到其他合适的拼音转汉字方法，因此实际效果并不理想

```shell
python decrypt.py
```

## 六、通过BERT文本情感分析微调客户评分
2年前的评论参考价值较低，字数小于5的评论多数为随意评论
```shell
# 调用config.py中的参数开始训练data中内容，在checkpoints文件夹中生成模型文件
python train.py
# 读取预处理后的csv文件，实现文本情感的三分类
python test.py
# 通过BERT模型得出的文本情感，对客户评分字段进行微调，并更新酒店总体评分
python postData.py
```


## 七、部分工作过程
+ 预处理、后处理、BERT的test在本机上实现，模型训练在云服务器上进行

![BERT在AutoDL上的训练](https://i-blog.csdnimg.cn/direct/e4dc0273dae84b49950222db7cd4d306.png)

![BERT情感分析测试](https://i-blog.csdnimg.cn/direct/eb75d01b8db9481cb082fa9bbac72d49.png)
![重复度高的评论的查找与删除](https://i-blog.csdnimg.cn/direct/d2366a49b74145329b4e0d8dc3f4b044.png)
![分数前后对比](https://i-blog.csdnimg.cn/direct/b13eb2efc3fa41db8efad2905fa3caa0.png)


## 八、参考代码

GitHub：[中文情感分类 | 基于三分类的文本情感分析](https://github.com/yaokui2018/SentimentAnalysis?tab=readme-ov-file)
+ 参考了他使用BERT文本情感分析的训练方法

---
本项目的具体代码放在了我的GitHub上：[中文情感分类 | 基于三分类的文本情感分析](https://github.com/yaokui2018/SentimentAnalysis?tab=readme-ov-file)
