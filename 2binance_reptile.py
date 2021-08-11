import requests
import pandas as pd
import sqlite3
from dateTimeUtil import *
from coinsUtil import get_trading_pairs



pd.set_option('expand_frame_repr', False)
conn = sqlite3.connect('crypto.db')
# 获取交易所过去n天的XXXUSDT数据.
BASE_URL = 'https://api.binance.com'
HOW_MANY_DAYS = 1
final_message = []

first_starttime_yyyymmdd = datetime.strftime((datetime.now() - timedelta(1)), '%Y-%m-%d')
# first_starttime_yyyymmdd = "2021-08-08"
first_start_str = first_starttime_yyyymmdd+" 00:00"
first_end_str = first_starttime_yyyymmdd+" 23:59"
last_endtime_yyyymmdd = get_previous_date(first_starttime_yyyymmdd, HOW_MANY_DAYS)


tradingPairs = get_trading_pairs(conn)
for each_trading_pair in tradingPairs:
    print("Now processing this coin:", each_trading_pair)
    dt_obj = datetime.strptime(first_start_str, '%Y-%m-%d %H:%M')
    start_time = round(dt_obj.timestamp() * 1000)

    dt_obj = datetime.strptime(first_end_str, '%Y-%m-%d %H:%M')
    end_time = round(dt_obj.timestamp() * 1000)
    many_records = []
    count = 0
    while True:
        count = count+1
        one_record = []
        current_date = datetime.strftime(datetime.fromtimestamp(start_time/1000), '%Y-%m-%d')
        print('current_date=', current_date)
        start_time = int(start_time - 24 * 60 * 60 * 1000)
        # print('start_time=', start_time)
        end_time = int(end_time - 24 * 60 * 60 * 1000)
        # print('each_trading_pair=', each_trading_pair, '&current_date=', current_date)
        url = BASE_URL + '/api/v3/klines' + '?symbol='+each_trading_pair+'&interval=1d&limit=1&startTime=' + str(
            start_time) + '&endTime=' + str(end_time)
        # print('url=', url)

        resp = requests.get(url)
        data = resp.json()
        # print("return data=", data)
        if len(data) == 0:
            if count == 1:    # no records at all
                temp_msg = "\n<===========this trading_pair has no records!=======>" + each_trading_pair
                print("temp_msg=", temp_msg)
                final_message += temp_msg
            break

        firstElement = data[0]
        openPrice = firstElement[1]
        highPrice = firstElement[2]
        lowPrice = firstElement[3]
        closePrice = firstElement[4]
        tradingVolume = firstElement[5]

        one_record.append(each_trading_pair)
        one_record.append(current_date)
        one_record.append(openPrice)
        one_record.append(closePrice)
        one_record.append(highPrice)
        one_record.append(lowPrice)
        one_record.append(tradingVolume)
        many_records.append(one_record)

        if count >= HOW_MANY_DAYS or current_date == last_endtime_yyyymmdd:
            break

    # print('many_records', many_records)
    # delete_sql = " delete from klines where tradingPair = '" + each_trading_pair + "' "
    # delete_sql += " and  tradingDate BETWEEN '" + last_endtime_yyyymmdd + "'  and  '" + first_starttime_yyyymmdd + "'"
    # conn.execute(delete_sql)
    insert_sql = "insert into klines(tradingPair,tradingDate,  open,close,high,low,volume)  values( ?,?,  ?,?,?,?,? )"
    conn.executemany(insert_sql, many_records)
    conn.commit()

conn.close()
if len(final_message) == 0:
    print('Success! I have just just initialized data for today.')
else:
    print('final_message', final_message)
