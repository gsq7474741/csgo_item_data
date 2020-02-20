from steam import *
from tqdm import tqdm
import pymongo
import pandas as pd

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

headers = dict([line.split(": ", 1) for line in raw_headers3.split("\n")])


client = pymongo.MongoClient('mongodb://localhost:27017/')
db_steam = client["steam"]
col_item_list = db_steam["item_list"]

db_item_data = client['csgo_item_data']
col_peritem = ['']


# def mongo_write(dt: pd.DataFrame, id):
#     csvpath = r'./item_data/' + parse.unquote(id) + r'.csv'
#     with pd.read_csv(csvpath) as f:
#         for i in range(len(f)):
#             s = f.loc[i]
#             # 这里加了str（）函数是无奈之举，DataFrame中的专有float64等数字格式使MongoDB无法识别，写入会报错，暂时先全部转换为字符串格式写入吧
#             dic = {index:str(s[index]) for index in s.index}
#             x = item_list.insert_one(dic)
#             print(x)


# result = pd.read_csv('/Users/songqi/Desktop/All_csgo_item.csv')
#
# for i in range(len(result)):
#     s = result.loc[i]
# #这里加了str（）函数是无奈之举，DataFrame中的专有float64等数字格式使MongoDB无法识别，写入会报错，暂时先全部转换为字符串格式写入吧
#     dic = {index:str(s[index]) for index in s.index}
#     x = item_list.insert_one(dic)
#     print(x)

# res = pd.read_csv(str2)
#
# for i in range(len(result)):
#     s = result.loc[i]
#     # 这里加了str（）函数是无奈之举，DataFrame中的专有float64等数字格式使MongoDB无法识别，写入会报错，暂时先全部转换为字符串格式写入吧
#     dic = {index: str(s[index]) for index in s.index}
#     x = item_data.insert_one(dic)
#     print(x)

log = pd.read_csv('./log.csv')
ord_list = list(log.ord)
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
        with open('./log3.csv', 'a') as f:
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

