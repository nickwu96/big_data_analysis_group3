#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Author: Nick
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

news = {}


def get_news_list(category):
    news_list = {}
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/74.0.3729.169 Safari/537.36'}
    if category == '高层动态':
        pages = 1
        while True:
            print('正在读取第{}页'.format(str(pages)))
            try:
                re = requests.get(
                    url='https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10149&cur_page={}'.format(str(pages)),
                    headers=header)
            except:
                print('服务器已限制访问，请等待30s后自动重试')
                time.sleep(30)
                re = requests.get(
                    url='https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10149&cur_page={}'.format(str(pages)),
                    headers=header)
            re.encoding = 'UTF-8'
            html = re.text
            soup = BeautifulSoup(html, features="html.parser")
            tag = soup.find('ul', class_='commonList_dot')  # 首先定位到<ul>，即所有文章链接的父节点
            a = tag.find_all('a')  # 查找所有的<a>
            if not a:
                break
            else:
                for i in a:
                    news_list[i['title']] = i['href']
            pages += 1
    elif category == '海外新闻':
        pages = 1
        while True:
            print('正在读取第{}页'.format(str(pages)))
            # 异常处理：若被服务器禁止访问，则30s后重试
            try:
                re = requests.get(
                    url='https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10005&cur_page={}'.format(str(pages)),
                    headers=header)
            except:
                print('服务器已限制访问，请等待30s后自动重试')
                time.sleep(30)
                re = requests.get(
                    url='https://www.yidaiyilu.gov.cn/info/iList.jsp?cat_id=10005&cur_page={}'.format(str(pages)),
                    headers=header)
            re.encoding = 'UTF-8'
            html = re.text
            soup = BeautifulSoup(html, features="html.parser")
            tag = soup.find_all('div', class_='left_content left')  # 首先定位到<div> class=left_content left标签
            if not tag:
                break
            for i in tag:
                a = i.find_all('a')  # 查找所有的<a>
                for i in a:
                    news_list[i['title']] = i['href']
            pages += 1
    print('共读取{}页，共{}条新闻'.format(pages - 1, len(news_list)))
    return news_list


def get_news_content(news_list):
    # 遍历news_list中的每一条新闻
    news_content = pd.DataFrame(columns=['新闻名', '新闻内容'])
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/74.0.3729.169 Safari/537.36'}
    ind = 0
    for titles, urls in news_list.items():
        ind += 1
        print('正在读取第{}条新闻：“{}”，地址：{}'.format(ind, titles, urls))
        news = ''
        try:
            re = requests.get(url='https://www.yidaiyilu.gov.cn/' + urls, headers=header)
        except:
            print('服务器已限制访问，请等待30s后自动重试')
            time.sleep(30)
            re = requests.get(url='https://www.yidaiyilu.gov.cn/' + urls, headers=header)
        re.encoding = 'UTF-8'
        html = re.text
        soup = BeautifulSoup(html, features="html.parser")
        contents = soup.find_all('p', style='text-indent:2em;')
        for i in contents[:-1]:
            if i.string is not None:
                news += i.string.strip('\n\t')
        news_content.loc[ind] = [titles, news]
    return news_content


def write(df, name):  # df 为新闻的内容; names为新闻分类的名字
    now_time = time.strftime("%Y%m%d %H%M%S", time.localtime())  # 获取当前时间
    df.to_csv(r'D:\Python\big_data_analysis_group3\news\{}_{}.csv'.format(now_time, name))
    return None


if __name__ == '__main__':
    category_list = ['高层动态', '海外新闻']
    category_list = ['海外新闻']
    for i in category_list:
        print('正在读取“{}”的新闻列表：'.format(i))
        news_list = get_news_list(i)
        print('“{}”的新闻列表读取完成'.format(i))
        df = get_news_content(news_list)  # df 以DataFrame的形式存储新闻标题和新闻内容
        write(df, i)
