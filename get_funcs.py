import csv
import http
import re
import ssl
import time
from urllib import parse

import OpenSSL
import pandas as pd
import requests
import urllib3
from retry import retry


# 字符串裁剪
def pick_char(list, r, l):
    n = len(list)  # 拿到列表的长度进行循环
    for i in range(0, n):
        # 下面这行代码才是真正意义上的修改列表
        list[i] = list[i][r:l]
    # i列表的为下标，列表中为i下标的元素被修改
    return list


# retry修饰器对网络错误自动重试
# 输入请求heade和物品id，生成时间价格数量的csv文件，并返回执行状态2 = 'No history'， 0 = 'success'
@retry(exceptions=(http.client.RemoteDisconnected, urllib3.exceptions.MaxRetryError, requests.exceptions.ProxyError,
                   OpenSSL.SSL.SysCallError, ssl.SSLError, requests.exceptions.SSLError), )
def get_item_data(headers, id):
    url = 'https://steamcommunity.com/market/listings/730/' + id
    # 将物品ID解码为名称
    name = parse.unquote(id)
    # 获取response
    response = requests.get(url, headers=headers)
    err = 0
    # HTTP响应错误处理
    while response.status_code != 200:
        # time.sleep(random.randint(1, 7))
        err += 1
        print(name + r' response.status_code = ' + str(response.status_code) + r' in ' + str(
            err) + r' times, sleeping 10s.')
        time.sleep(10)
        # retry
        response = requests.get(url, headers=headers)

    result = re.search('<script.*?line1=(.*?);.*?</script>', response.text, re.S)
    # Reg匹配价量信息，返回为字符串
    txt_path = r'./item_data/' + name + r'.txt'
    csv_path = r'./item_data/' + name + r'.csv'

    # AttributeError
    # 如果物品没有历史数据则return2
    try:
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(result.group(1))
    except:
        return 2
    # 写入txt
    file = open(txt_path)
    file_read = file.read()
    # 删除字符串中的“ ： + []
    table = str.maketrans('', '', '":+[]')
    file_translate = file_read.translate(table)
    # 以逗号为分隔符，将字符串转换为列表
    lst = file_translate.split(',')
    # 将时间、价格、数量三个信息分别存入三个list
    list_time = []
    list_price = []
    list_num = []
    i = 0
    j = 0
    while i < len(lst):
        list_time.insert(j, lst[i])
        list_price.insert(j, lst[i + 1])
        list_num.insert(j, lst[i + 2])
        i = i + 3
        j = j + 1

    # 写入csv
    with open(csv_path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'price', 'number'])
        for i in range(len(list_time)):
            writer.writerow([list_time[i], list_price[i], list_num[i]])
    return 0


# 获取单页物品列表
def get_item_list(url, headers, list_name):
    try:
        # name = parse.unquote(name)
        response = requests.get(url, headers=headers)
        # 获取物品id字符串
        id_pattern = re.compile(r'0.*\?f')
        id_result = id_pattern.findall(response.text)
        id_result = pick_char(id_result, 2, -2)
        if len(id_result) == 0:
            id_pattern = re.compile((r'0\/.*" id'))
            id_result = id_pattern.findall(response.text)
            id_result = pick_char(id_result, 2, -4)

        # 获取物品名称
        name_pattern = re.compile((r'2;">.*<'))
        name_result = name_pattern.findall(response.text)
        name_result = pick_char(name_result, 4, -1)
        csv_path = r'./item_list/' + list_name + r'.csv'

        list_name = name_result
        list_id = id_result

        # 创建csv文件，并将数据写入
        with open(csv_path, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'name'])
            for i in range(len(list_name)):
                writer.writerow([list_id[i], list_name[i]])
    except:
        return 1
    else:
        return 0


def get_data_from_list(headers, csv_path):
    with open(csv_path)as f:
        f_csv = csv.reader(f)
        column = [row[0] for row in f_csv]
        del column[0]
    for i in column:
        get_item_data(headers, i)


# 获取多页列表
def get_item_list_para(url, headers, params, list_name):
    try:
        # get
        response = requests.get(url, params=params, headers=headers, )
        # 匹配物品id
        id_pattern = re.compile(r'0.*\?f')
        id_result = id_pattern.findall(response.text)
        id_result = pick_char(id_result, 2, -2)
        if len(id_result) == 0:
            id_pattern = re.compile((r'0\/.*" id'))
            id_result = id_pattern.findall(response.text)
            id_result = pick_char(id_result, 2, -4)

        # 匹配物品名称
        name_pattern = re.compile((r'[0123456789ABCDEF];">.*<'))
        name_result = name_pattern.findall(response.text)
        name_result = pick_char(name_result, 4, -1)

        # result = re.search('0.*\?f', response.text, re.S)
        # with open('rerst.txt', 'w', encoding='utf-8') as f:
        #    f.write(str(id_result))

        csv_path = r'./item_list/' + list_name + r'.csv'

        list_name = name_result
        list_id = id_result
        if len(list_name) != 10:
            return 1

        # # 创建csv文件，并将数据写入
        with open(csv_path, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['id', 'name'])
            for i in range(len(list_name)):
                writer.writerow([list_id[i], list_name[i]])
    except:
        return 1
    else:
        return 0


# 多页列表合成
# csvpath = ./item_list/All_p
def csv_merge(csvpath, headerpath, num):
    total_csv = pd.read_csv(headerpath)
    for i in range(num):
        with open(csvpath + str(i + 1) + r'.csv', 'r') as f:
            f_csv = pd.read_csv(f)
            total_csv = pd.merge(total_csv, f_csv, on=['id', 'name'], how='outer')
    total_csv.to_csv(csvpath + r'_Done' + r'.csv', header=True, index=True)


def get_per_item_data():
    err_log = pd.read_csv('./err_log.csv')
    ord_list = list(err_log.ord)
    times = 0
    for item in tqdm(col_item_list.find()):
        id = item['id']
        ord = float(item['ordinal'])
        # if ord < 11941:
        #     continue
        if ord not in ord_list:
            continue
        # print(a)
        x = get_item_data(headers, id)
        times += 1
        # x = get_item_list_para(list_url, headers, params_list[i], name_list[i])
        err = 0
        # if times == random.randint(11, 20):
        #     times = 0
        #     print(r'Sleeping...')
        #     time.sleep(random.randint(9, 12))
        if x == 2:
            print(str(ord) + parse.unquote(id) + r' has no history.')
            with open('./no_his.csv', 'a') as f:
                f.write(str(ord) + r',' + parse.unquote(id) + r' has no history.' + '\n')
            continue
        while x == 1:
            err += 1
            print(ord + r' Get ' + parse.unquote(id) + r' return error times ' + str(err) + r'.')
            x = get_item_data(headers, id)
            if x == 0:
                err = 0
                break
        print(str(ord) + r' Get ' + parse.unquote(id) + r' has done.')
