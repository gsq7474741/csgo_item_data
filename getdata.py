import requests

def get_opt_chains(stk, date):
    response = requests.get('https://sandbox.tradier.com/v1/markets/options/chains',
                            params={'symbol': str(stk), 'expiration': str(date), 'greeks': 'true'},
                            headers={'Authorization': 'Bearer qwDAYgpkBpOG9fwTOa4H20yzm8mG',
                                     'Accept': 'application/json'}
                            )

    # print(response)
    f = open('opt_chains.txt', 'w')
    f.write(str(response))
    f.close()
    #json_response = response.json()
    # print(response.status_code)
    # print(json_response)
    #return json_response


def get_his(syl, itl, st, ed,filename):
    response = requests.get('https://sandbox.tradier.com/v1/markets/history',
                            params={'symbol': str(syl), 'interval': str(itl), 'start': str(st),
                                    'end': str(ed)},
                            headers={'Authorization': 'Bearer qwDAYgpkBpOG9fwTOa4H20yzm8mG',
                                     'Accept': 'application/json'}
                            )

    f = open(filename, 'w')
    f.write(str(response.json()))
    f.close()
    #json_response = response.json()
    # print(response.status_code)
    # print(json_response)
    #return json_response


get_his('TSLA200207C00700000', 'daily', '2020-02-01', '2020-02-20','opt_his.txt')
get_his('TSLA', 'daily', '2020-02-01', '2020-02-20','stk_his.txt')


#print(optinf)
#optinf = get_his('AAPL200417P00320000', 'daily', '2019-05-04', '2020-01-20')
#stkinf = get_his('AAPL', 'daily', '2019-05-04', '2020-01-20')

# list_1 = ['张三','李四','王五']
#
# # 1.打开文件
# file_handle = open('optinf.txt', mode='w')
#
# # 2.写入数据
# for name in optinf[0][0]:
#     file_handle.write(name[0][0])
#     # 写入换行符
#     file_handle.write('\n')
#
# # 3.关闭文件
# file_handle.close()
#
# # 读取文件，并且必须是一个列表，格式：['张三','李四','王五']
# file_handle = open('student.txt',mode='r')
# # 使用readlines() 读取所有行的数据，会返回一个列表，列表中存放的数据就是每一行的内容
# contents = file_handle.readlines()
# # 准备一个列表，用来存放取出来的数据
# student_list = []
# # for循环遍历列表，去除每一行读取到的内容
# for name in contents:
#     # strip()去除字符串中的某些字符  去除\n
#     name = name.strip('\n')
#     # 把处理好的name添加到列表中
#     student_list.append(name)
# # 这个列表中存放的就是和写入之前一样的内容
# print(student_list)
# # 3.关闭文件
# file_handle.close()
