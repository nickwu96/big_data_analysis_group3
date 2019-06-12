#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author: Nick
# import jieba
import jieba.analyse
import pandas as pd
import os
import csv


def sum_word_freq(files):
    words_except = ['，', ',', '。', '的', '、', '和', '”', '“', '是', '了', '要', '为', '等', '同', '对', '\n', '!', '在', '将', '与',
                    '年', '中', '也', '月', '说']
    print('正在读取文件：{}'.format(files))
    ans = {}
    news = pd.read_csv('{}.csv'.format(files), header=0, index_col=0, encoding='utf-8')
    for rows in range(news.shape[0]):
        print('正在处理第{}条新闻'.format(rows + 1))
        news_content = news.iloc[rows, 1]  # 获取新闻内容
        if pd.notna(news_content):
            jieba.suggest_freq('一带一路', True)  # 手动调整“一带一路”词频，使之分词后为一个整体
            news_content_list = jieba.cut(news_content)
        for j in news_content_list:
            if j in ans:
                ans[j] += 1
            elif j not in words_except:
                ans[j] = 1
    with open('{}_词频.csv'.format(files), 'w', encoding='utf-8') as f:
        for j in sorted(ans.items(), key=lambda x: x[1], reverse=True):
            f.write('{},{}\n'.format(j[0], j[1]))  # 按照词频由大到小的顺序输出
    return None


def sum_word_freq_country(file):
    with open(r'D:\Python\big_data_analysis_group3\news\国家列表.txt', encoding='utf-8') as f:
        country = [i.rstrip() for i in f.readlines()]
    word_freq = pd.read_csv('{}_词频.csv'.format(file), encoding='utf-8', quoting=csv.QUOTE_NONE)
    ans = {}
    for i in range(word_freq.shape[0]):
        if word_freq.iloc[i][0] in country:
            ans[word_freq.iloc[i][0]] = word_freq.iloc[i][1]
    with open('{}_词频_国家.csv'.format(file), 'w') as f:
        for i, j in ans.items():
            f.writelines('{},{}\n'.format(i, j))
    return None


if __name__ == '__main__':
    files = ['D:\\Python\\big_data_analysis_group3\\news\\'+i for i in ['20190611 154754_高层动态','20190611 161819_海外新闻']]
    for i in files:
        sum_word_freq(i)
        sum_word_freq_country(i)
