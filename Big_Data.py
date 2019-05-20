#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Nick
import pandas as pd
import time

folder = r'D:\Python\big_data_analysis_group3\\'  # 设置工作目录
new_data = []  # new_data用来存储清洗后新的数据
year = (2017-1960) + 1  # year为数据包含的年份数量

def initiate_new_data():  # initiate_new_data函数用以初始化new_data这个列表
    # new_data列表每一个元素代表一个年份，每一个元素是pd.DataFrame，每一行代表一个国家，每一列代表一个指标
    f = open(folder + 'country_list.txt', 'r')  #打开文件country_list.txt，该文件用以存储所有的国家列表
    country_list = f.readlines()  #读入临时数据country_list
    f.close()
    country_name, country_code = [], []  # country_name和country_code分别存储国家名与国家代码
    for i in country_list:
        country_name.append(i.split()[0])  #country_name列表存储国家名字
        country_code.append(i.split()[1])  #country_code列表存储国家代码
    for i in range(year):  # 对new_data的每一个元素初始化，使DataFrame的前两列初始化为国家名和国家代码
        new_data.append(pd.DataFrame({'国家名':country_name, '国家代码':country_code}))
    return None

def read_data(name, file):
    # 读入名为name的指标，其对应的excel文件为file
    log('read', (name, file))
    data = pd.read_excel(folder + 'raw data\\' + file, 'Data', header=3)  #读取指标对应的excel文件，header=3意思是表头在第3行
    for i in range(year):
        new_data[i][name] = data[str(1960 + i)]  # new_data每一个元素为一个DataFrame，添加一列名为name，数据来源于data中对应年份的列
    return None

def write_data():
    # 利用pandas的ExcelWriter将结果输出到结果excel里
    log('write','正在导出数据...')
    writer = pd.ExcelWriter(folder + "Result.xls")
    for i in range(year):
        new_data[i].to_excel(writer, sheet_name=str(1960+i), header=True, index=False)
    writer.save()
    writer.close()
    log('write','导出数据成功：{}\n'.format(folder + 'Result.xls'))
    return None

def log(mode, content):
    # 产生日志文件
    f = open(folder + 'log.txt', 'a+')
    if mode == 'init':
        localtime = time.asctime(time.localtime(time.time()))
        f.writelines('运行时间：{}\n'.format(localtime))
    if mode == 'read':
        f.writelines('正在读取指标：{}\n'.format(content[0]))
        f.writelines('正在读取文件：{}\n'.format(content[1]))
    if mode == 'write':
        f.writelines('{}\n'.format(content))
    f.close()

if __name__ == '__main__':
    # 首先读取存放指标列表的txt，该txt存储了需要读取的指标及其文件名
    f = open(folder + 'data_list.txt', 'r')
    files = f.readlines()
    f.close()
    log('init','')

    initiate_new_data()  # 初始化new_data，用以存储清洗后的数据

    # 接下来依次读取每个文件的数据
    for i in files:
        read_data(i.split()[0], i.split()[1])  #依次将指标名、指标文件位置传入read_files函数

    write_data()  #将数据输出到结果excel里