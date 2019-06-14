#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author: Nick

from matplotlib import pyplot as plt
import wordcloud
from PIL import Image
import numpy as np

files = [r'D:\Python\big_data_analysis_group3\news\20190611 154754_高层动态_词频_国家.csv',
         r'D:\Python\big_data_analysis_group3\news\20190611 161819_海外新闻_词频_国家.csv']
for i in files:
    # 打开词频文件
    with open(i) as f:
        words = f.read()
    # 生成词云
    font = r'C:\Windows\Fonts\simfang.ttf'
    img = Image.open(r'D:\Python\big_data_analysis_group3\wordcloud\worldmap.jpg')  # 打开图片
    img_array = np.array(img)  # 将图片装换为数组

    w = wordcloud.WordCloud(font_path=font, mask=img_array, background_color='white',
                            width=2000)
    w.generate(words)
    plt.imshow(w)
    plt.axis('off')
    plt.show()
    w.to_file(r'D:\Python\big_data_analysis_group3\wordcloud\{}.png'.format(i[-14:-10]))
