import requests
import json
from datetime import datetime


# https://www.mexc.com/open/api/v2/market/deals?symbol=ADA_USDT&start_time=1627917951919&limit=1000
BASE_URL = "https://www.mexc.com/open/api/v2/market/deals?"


def  add_value_to_dict(my_dict, input_key, input_value):
    if input_key in my_dict:
        old_value = my_dict[input_key]
        my_dict[input_key] = float(old_value) + float(input_value)
    else:
        my_dict[input_key] = input_value
    return my_dict


def take_tradeID(elem):
    return elem["tradeID"]


with open("deals_mxc_ada.json", "r") as read_file:
    json_response = json.load(read_file)
data = json_response['data']
# print("\n=========>data=", data)
index = 0
my_dict = {}
result_dict = {}
str_format = '{0:>10.2f}'
len_data = len(data)
last_timestamp = 0

for item in data:
    index += 1
    print(index, item)
    time_stamp10 = round(item['trade_time']/1000)
    dt_object = datetime.fromtimestamp(time_stamp10)

    trade_price = float(item['trade_price'])
    trade_quantity = float(item['trade_quantity'])
    turn_over = trade_price * trade_quantity

    if index == 1 or index == len_data:
        print('time=', dt_object)
        last_timestamp = round(item['trade_time']/1000)



url = BASE_URL + 'symbol=ADA_USDT'
url += "&limit=1000"
url += '&start_time=' + str(last_timestamp)

print("url======>", url)
# resp = requests.get(url)
# json_response = resp.json()
# data = json_response['data']
#
# index = 0
# len_data = len(data)
# for item in data:
#     index += 1
#     # print(index, item)
#
#     if index == 1 or index == len_data:
#         time_stamp10 = round(item['trade_time'] / 1000)
#         dt_object = datetime.fromtimestamp(time_stamp10)
#         print('time=', dt_object)
#         last_timestamp = item['trade_time']
