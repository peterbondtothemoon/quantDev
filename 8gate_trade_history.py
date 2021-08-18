import requests
import json


def  add_value_to_dict(my_dict, input_key, input_value):
    if input_key in my_dict:
        old_value = my_dict[input_key]
        my_dict[input_key] = float(old_value) + float(input_value)
    else:
        my_dict[input_key] = input_value
    return my_dict


def take_tradeID(elem):
    return elem["tradeID"]


with open("gate_omi_usdt_20210731pm9.json", "r") as read_file:
    json_response = json.load(read_file)
data = json_response['data']
print("\n=========>")
index = 0
first_trade_id = 0
my_dict = {}
result_dict = {}
str_format = '{0:>10.2f}'


data.sort(key=take_tradeID, reverse=True)
first_trade_id = data[len(data)-1]['tradeID']
for item in data:
    index += 1
    date_yyyymmdd24h = str(item['date'])[:13]
    total_value = float(item['total'])
    type_bs = item['type']
    date_bs = date_yyyymmdd24h + "#" + type_bs
    print(index, "tradeID=", item['tradeID'], "date=", date_yyyymmdd24h, "type=", type_bs, "total=", str_format.format(total_value))
    add_value_to_dict(result_dict, date_bs, total_value )



print("first_trade_id=", first_trade_id)
for temp_key in result_dict:
    temp_value = result_dict[temp_key]
    print("temp_key=", temp_key, "temp_value=", str_format.format(temp_value))


# 获取从[TID]往后的最多1000历史成交记录：
next_start_id = int(first_trade_id) - 3000
print("next_start_id=", next_start_id)
BASE_URL = 'https://data.gateapi.io/api2/1/tradeHistory/omi_usdt/'
next_url = BASE_URL + str(next_start_id)
print("next_url=", next_url)
resp = requests.get(next_url)
json_response = resp.json()
data = json_response['data']

index = 0
data.sort(key=take_tradeID, reverse=True)
first_trade_id = data[len(data)-1]['tradeID']
for item in data:
    index += 1
    date_yyyymmdd24h = str(item['date'])[:13]
    total_value = float(item['total'])
    type_bs = item['type']
    date_bs = date_yyyymmdd24h + "#" + type_bs
    # print(index, "tradeID=", item['tradeID'], "date=", date_yyyymmdd24h, "type=", type_bs, "total=", str_format.format(total_value))
    add_value_to_dict(result_dict, date_bs, total_value )

print("first_trade_id=", first_trade_id)
for temp_key in result_dict:
    temp_value = result_dict[temp_key]
    print("temp_key=", temp_key, "temp_value=", str_format.format(temp_value))
