from copy import deepcopy

import pymongo

from get_funcs import *


def page_list_builder(url_front, p):
    pages = []
    for i in range(p + 1):
        tmp = url_front + str(i) + r'_name_desc'
        pages.append(tmp)
    del pages[0]
    return pages


def name_list_builder(list_name, p, c):
    names = []
    for i in range(p + 1):
        tmp = list_name + str(i)
        names.append(tmp)
    del names[0:c]

    return names


def params_list_builder(param: dict, p, c):
    paramss = []
    for i in range(p):
        tmp = param
        tmp['start'] = str(i * 10)
        paramss.append(deepcopy(tmp))
    del paramss[0:c - 1]
    return paramss


time_start = time.time()
# 输入数据区域--------------------------------
# 翻页程序
p = 817
c = 817
'817 817 817, 14733 total'
list_file_name = 'All_p'
#
# id = 'DreamHack%202014%20Cobblestone%20Souvenir%20Package'
list_url = r'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B0%5D=any&category_730_ProPlayer%5B0%5D=any&category_730_StickerCapsule%5B0%5D=any&category_730_TournamentTeam%5B0%5D=any&category_730_Weapon%5B0%5D=any&appid=730'
raw_headers = '''Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Cookie: steamMachineAuth76561198291930354=19CDC70BC19B8655EE19D50DDC29199374A7D57A; browserid=1198456931416991764; _ga=GA1.2.596629681.1581340398; timezoneOffset=28800,0; _gid=GA1.2.1388132909.1581491376; steamRememberLogin=76561198291930354%7C%7C162d052affba916df8c4efb7fe3cc633; strInventoryLastContext=730_2; sessionid=1a9eb5d976ad185474adc585; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A7%2C%22time_checked%22%3A1581579907%7D; steamLoginSecure=76561198291930354%7C%7CA170EC85E9673586C7038E61612A3591F8253440
Host: steamcommunity.com
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36
X-Requested-With: XMLHttpRequest'''
raw_headers1 = '''Accept: text/javascript, text/html, application/xml, text/xml, */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Cookie: steamMachineAuth76561198291930354=19CDC70BC19B8655EE19D50DDC29199374A7D57A; browserid=1198456931416991764; _ga=GA1.2.596629681.1581340398; timezoneOffset=28800,0; _gid=GA1.2.1388132909.1581491376; steamRememberLogin=76561198291930354%7C%7C162d052affba916df8c4efb7fe3cc633; strInventoryLastContext=730_2; sessionid=1a9eb5d976ad185474adc585; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A7%2C%22time_checked%22%3A1581579907%7D; steamLoginSecure=76561198291930354%7C%7CA170EC85E9673586C7038E61612A3591F8253440
Host: steamcommunity.com
Referer: https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_StickerCategory%5B%5D=tag_TeamLogo&category_730_Tournament%5B%5D=tag_Tournament13&category_730_Type%5B%5D=tag_CSGO_Tool_Sticker&appid=730
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36
X-Prototype-Version: 1.7
X-Requested-With: XMLHttpRequest'''
raw_headers2 = '''Accept: text/javascript, text/html, application/xml, text/xml, */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Connection: keep-alive
Cookie: steamMachineAuth76561198291930354=19CDC70BC19B8655EE19D50DDC29199374A7D57A; browserid=1198456931416991764; _ga=GA1.2.596629681.1581340398; timezoneOffset=28800,0; _gid=GA1.2.1388132909.1581491376; steamRememberLogin=76561198291930354%7C%7C162d052affba916df8c4efb7fe3cc633; strInventoryLastContext=730_2; sessionid=1a9eb5d976ad185474adc585; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A7%2C%22time_checked%22%3A1581579907%7D; steamLoginSecure=76561198291930354%7C%7CD805A8611C4C9B3C61FACE46FC7D384E7306818E
Host: steamcommunity.com
Referer: https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&appid=730
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36
X-Prototype-Version: 1.7
X-Requested-With: XMLHttpRequest'''
raw_headers3 = '''Accept: */*
Referer: https://steamcommunity.com/market/listings/730/
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36
X-Requested-With: XMLHttpRequest'''
raw_params = '''query=
start=0
count=10
search_descriptions=0
sort_column=name
sort_dir=asc
appid=730
category_730_ItemSet%5B%5D=any
category_730_ProPlayer%5B%5D=any
category_730_StickerCapsule%5B%5D=any
category_730_TournamentTeam%5B%5D=any
category_730_Weapon%5B%5D=any'''
# ------------------------------------区域结束

headers = dict([line.split(": ", 1) for line in raw_headers3.split("\n")])
params = dict([line.split("=", 1) for line in raw_params.split("\n")])

name_list = name_list_builder(list_file_name, p, c)
params_list = params_list_builder(params, p, c)

# 执行区域-----------------
i = 0

if i == 0:
    get_item_data(headers,
                  '%E2%98%85%20StatTrak%E2%84%A2%20Nomad%20Knife%20%7C%20Boreal%20Forest%20%28Battle-Scarred%29')

elif i == 1:
    get_item_list(list_url, headers, 'Boston_2018_team_logo_p8')

elif i == 2:
    get_data_from_list(headers, r'item_list/Cobblestone_p1.csv')

elif i == 3:
    for i in range(p - c + 1):
        x = get_item_list_para(list_url, headers, params_list[i], name_list[i])
        err = 0
        while x == 1:
            err += 1
            print(r'Get ' + list_file_name + str(i + c) + r' return error times ' + str(err) + r'.')
            x = get_item_list_para(list_url, headers, params_list[i], name_list[i])
            if x == 0:
                err = 0
                break
        print(r'Get ' + list_file_name + str(i + c) + r' has done.')

elif i == 4:
    csv_merge('./item_list/All_p', './item_list/All_.csv', 1474)

elif i == 5:
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db_steam = client["steam"]
    col_item_list = db_steam["item_list"]
    get_per_item_data()

else:
    raise IOError('没有选择要执行的程序')

time_end = time.time()
print('总耗时：', time_end - time_start, r's')
# 区域结束----------------
