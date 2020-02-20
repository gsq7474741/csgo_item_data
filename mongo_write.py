from urllib import parse

import pandas as pd
import pymongo
from tqdm import tqdm

client = pymongo.MongoClient('mongodb://localhost:27017/')
db_steam = client["steam"]
col_item_list = db_steam["item_list"]

db_item_data = client['csgo_item_data']


# 物品列表写入mongo
def mongo_write_list(id):
    csvpath = r'./item_data/' + parse.unquote(id) + r'.csv'
    with pd.read_csv(csvpath) as f:
        for i in range(len(f)):
            s = f.loc[i]
            # 这里加了str（）函数是无奈之举，DataFrame中的专有float64等数字格式使MongoDB无法识别，写入会报错，暂时先全部转换为字符串格式写入吧
            dic = {index: str(s[index]) for index in s.index}
            x = col_item_list.insert_one(dic)
            print(x)


# 物品数据清洗&写入mongo
def mongo_write_item_data(id: str, ord):
    col_peritem = db_item_data[str(ord) + r'_' + parse.unquote(id)]
    csvpath = r'./item_data/' + parse.unquote(id) + r'.csv'
    f = pd.read_csv(csvpath)
    nf = f.price.to_frame()
    nf['num'] = f.number.astype('int')
    nf['date'] = f.time.astype('str').str[0:12]
    nf['time'] = f.time.astype('str').str[12:15]
    # nf_num = nf.num
    nf_date = nf.date
    nf_time = nf.time
    nf = nf.drop('time', axis=1)
    nf.insert(0, 'time', nf_time)
    nf = nf.drop('date', axis=1)
    nf.insert(0, 'date', nf_date)
    lis = []
    for i in range(len(nf)):
        s = nf.loc[i]
        # 这里加了str（）函数是无奈之举，DataFrame中的专有float64等数字格式使MongoDB无法识别，写入会报错，暂时先全部转换为字符串格式写入吧
        dic = {index: str(s[index]) for index in s.index}
        lis.append(dic)
    x = col_peritem.insert_many(lis)
        # print(x)


# test
# mongo_write_item_data('Sticker%20%7C%20Ramz1kBOss%20%7C%20Berlin%202019', '8552')
df = pd.read_csv('./item_list/All_p_Done.csv')

# main
for i in tqdm(range(len(df))):
    s = df.loc[i]
    id = s['id']
    ord = s['ord']
    mongo_write_item_data(id, ord)
