import csv
import re
import urllib3
import OpenSSL
import random
import ssl
import http
import time
import pandas as pd
import tqdm
from urllib import parse
from retry import retry
import requests


def pick_char(list, r, l):
    n = len(list)  # 拿到列表的长度进行循环
    for i in range(0, n):
        # 下面这行代码才是真正意义上的修改列表
        list[i] = list[i][r:l]
    # i列表的为下标，列表中为i下标的元素被修改
    return list


def retry_if_result_none(result):
    return result is None


@retry(exceptions=(http.client.RemoteDisconnected, urllib3.exceptions.MaxRetryError, requests.exceptions.ProxyError,
                   OpenSSL.SSL.SysCallError, ssl.SSLError, requests.exceptions.SSLError), )
def get_item_data(headers, id):
    url = 'https://steamcommunity.com/market/listings/730/' + id
    name = parse.unquote(id)
    response = requests.get(url, headers=headers)
    err = 0
    while response.status_code != 200:
        # time.sleep(random.randint(1, 7))
        err += 1
        print(name + r' response.status_code = ' + str(response.status_code) + r' in ' + str(err) + r' times.')
        time.sleep(10)
        # print(r'Sleeping 5s...')
        # for i in tqdm.trange(10):
        #     time.sleep(1)
        response = requests.get(url, headers=headers)
    # print(response.text)

    result = re.search('<script.*?line1=(.*?);.*?</script>', response.text, re.S)
    # with open('rst.txt', 'w') as f:
    #   f.write(result)
    # 匹配表格的信息，价格为美元，返回的类型为字符串
    str1 = r'./item_data/' + name + r'.txt'
    str2 = r'./item_data/' + name + r'.csv'
    path: str = str1
    # AttributeError
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(result.group(1))
    except:
        return 2
    file = open(path)
    file_read = file.read()

    table = str.maketrans('', '', '":+[]')  # 删除字符串中的“ ： + []
    file_translate = file_read.translate(table)

    lst = file_translate.split(',')  # 以逗号为分隔符，将字符串转换为列表

    list_time = []
    list_price = []
    list_num = []
    # 将时间、价格、数量三个信息分别存入三个list
    i = 0
    j = 0
    while i < len(lst):
        list_time.insert(j, lst[i])
        list_price.insert(j, lst[i + 1])
        list_num.insert(j, lst[i + 2])
        i = i + 3
        j = j + 1

    if len(list_time) == 0:
        return 1

    # 创建csv文件，并将数据写入
    with open(str2, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'price', 'number'])
        for i in range(len(list_time)):
            writer.writerow([list_time[i], list_price[i], list_num[i]])
    return 0


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

        # result = re.search('0.*\?f', response.text, re.S)
        # with open('rerst.txt', 'w', encoding='utf-8') as f:
        #    f.write(str(id_result))
        # 匹配表格的信息，价格为美元，返回的类型为字符串

        # txt_path = r'./item_list/' + list_file_name + r'.txt'

        csv_path = r'./item_list/' + list_name + r'.csv'
        # path: str = txt_path
        #
        # file = open(path)
        # file_read = file.read()
        #
        # table = str.maketrans('', '', '":+[]')  # 删除字符串中的“ ： + []
        # file_translate = file_read.translate(table)
        #
        # # result = file_translate.split(',')  # 以逗号为分隔符，将字符串转换为列表
        #
        list_name = name_result
        list_id = id_result

        # list_num = []
        # 将id、名称、分别存入list
        # i = 0
        # j = 0
        # while i < len(id_result):
        #     list_file_name.insert(j, id_result[i])
        #     list_id.insert(j, id_result[i + 1])
        #     list_num.insert(j, id_result[i + 2])
        #     i = i + 3
        #     j = j + 1

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


def get_list_data(headers, csv_path):
    with open(csv_path)as f:
        f_csv = csv.reader(f)
        column = [row[0] for row in f_csv]
        del column[0]
    for i in column:
        get_item_data(headers, i)


def get_item_list_para(url, headers, params, list_name):
    try:
        # name = parse.unquote(name)
        # response = requests.get(url, headers=headers)
        response = requests.get(url, params=params, headers=headers, )
        # 获取物品id字符串
        id_pattern = re.compile(r'0.*\?f')
        id_result = id_pattern.findall(response.text)
        id_result = pick_char(id_result, 2, -2)
        if len(id_result) == 0:
            id_pattern = re.compile((r'0\/.*" id'))
            id_result = id_pattern.findall(response.text)
            id_result = pick_char(id_result, 2, -4)

        # 获取物品名称
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


# csvpath = ./item_list/All_p
def csv_merge(csvpath, headerpath, num):
    total_csv = pd.read_csv(headerpath)
    for i in range(num):
        with open(csvpath + str(i + 1) + r'.csv', 'r') as f:
            f_csv = pd.read_csv(f)
            total_csv = pd.merge(total_csv, f_csv, on=['id', 'name'], how='outer')
    total_csv.to_csv(csvpath + r'_Done' + r'.csv', header=True, index=True)


def mongo_save_item_data(headers, id):
    url = 'https://steamcommunity.com/market/listings/730/' + id
    id = parse.unquote(id)
    response = requests.get(url, headers=headers)

    # print(response.text)

    result = re.search('<script.*?line1=(.*?);.*?</script>', response.text, re.S)
    # with open('rst.txt', 'w') as f:
    #   f.write(result)
    # 匹配表格的信息，价格为美元，返回的类型为字符串
    str1 = r'./item_data/' + id + r'.txt'
    str2 = r'./item_data/' + id + r'.csv'
    path: str = str1

    with open(path, 'w', encoding='utf-8') as f:
        f.write(result.group(1))

    file = open(path)
    file_read = file.read()

    table = str.maketrans('', '', '":+[]')  # 删除字符串中的“ ： + []
    file_translate = file_read.translate(table)

    lst = file_translate.split(',')  # 以逗号为分隔符，将字符串转换为列表

    list_time = []
    list_price = []
    list_num = []
    # 将时间、价格、数量三个信息分别存入三个list
    i = 0
    j = 0
    while i < len(lst):
        list_time.insert(j, lst[i])
        list_price.insert(j, lst[i + 1])
        list_num.insert(j, lst[i + 2])
        i = i + 3
        j = j + 1
    # 创建csv文件，并将数据写入
    with open(str2, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['time', 'price', 'number'])
        for i in range(len(list_time)):
            writer.writerow([list_time[i], list_price[i], list_num[i]])
