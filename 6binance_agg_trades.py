import requests
import pandas as pd
import sqlite3
from parse_data import parse_data
from dateTimeUtil import *


pd.set_option('expand_frame_repr', False)
conn = sqlite3.connect('crypto.db')
# 获取交易所过去n天的aggTrades成交数据明细.
BASE_URL = 'https://api.binance.com/api/v3/aggTrades?'
final_message = []


# 获得下一次更新的开始日期：先查询btcusdt目前已经更新的日期，然后再往前追溯一天
def get_next_process_date():
    result_date = ""
    # 每天更新最新数据的sql
    query_sql = " select   tradingDateTime from buysell   where tradingPair = 'BTCUSDT' " \
                " order by tradingDateTime limit 1  "
    mycursor = conn.cursor()
    mycursor.execute(query_sql)
    rows = mycursor.fetchall()
    for row in rows:
        result_date = row[0][:10]
        print("result_date=", result_date, len(result_date))
    mycursor.close()
    if len(result_date) == 10:
        result_date = get_previous_date(result_date, 1)
    return result_date


def get_trading_pairs_date(query_sql):
    result_list = []
    mycursor = conn.cursor()
    mycursor.execute(query_sql)
    rows = mycursor.fetchall()
    for row in rows:
        result_list.append(row[0] + "#" + row[1])
    mycursor.close()
    return result_list


# process_date_yyyymmdd:开始更新数据的日期
# end_date_yyyymmdd：结束更新数据的日期（比开始更新数据的日期更古老）
def get_history_trading_data(trading_pairs, process_date_yyyymmdd, end_date_yyyymmdd):
    while True:
        # process_date_yyyymmdd = init_process_date_yyyymmdd   # 这个数值，每个交易对都要重新赋值一次

        # 再加一轮while循环：从昨天开始，一直往前到开始上交易所的日期
        # while True:
        for name_date in trading_pairs:  # for每个交易对
            temp_array = str(name_date).split("#")
            trading_pair_name = temp_array[0]
            print(trading_pair_name, "end_date_yyyymmdd=", end_date_yyyymmdd, "process_date_yyyymmdd=", process_date_yyyymmdd)

            # 对每个交易对-每天要取24个数据（每次取1个小时的数据）
            timestamp_24hlist = get_timestamp_24hlist(process_date_yyyymmdd)
            index_24h = 0
            for item in timestamp_24hlist:
                if index_24h > 23:
                    break
                start_timestamp = item
                end_timestamp = int(timestamp_24hlist[index_24h + 1])
                url = BASE_URL + 'symbol='+trading_pair_name
                url += '&startTime=' + start_timestamp
                url += '&endTime=' + str(end_timestamp)
                # print('index_24h=', index_24h, 'url=============>', url)

                resp = requests.get(url)
                data = resp.json()
                start_time_24h = process_date_yyyymmdd + get_hour_suffix(index_24h)
                parse_data(conn, data, trading_pair_name, start_time_24h)
                index_24h += 1
        if process_date_yyyymmdd == end_date_yyyymmdd:
            break
        process_date_yyyymmdd = get_previous_date(process_date_yyyymmdd, 1)


# 每天更新最新数据的sql
query_sql1 = " select tradingPair,startDate from coins order by id "
process_date_yyyymmdd1 = get_yesterday_yyyymmdd()
end_date_yyyymmdd1 = get_previous_date(process_date_yyyymmdd1, 1)
tradingPairs1 = get_trading_pairs_date(query_sql1)
get_history_trading_data(tradingPairs1, process_date_yyyymmdd1, end_date_yyyymmdd1)


# 往前追溯交易明细，LUNAUSDT的数据已经追溯到2020年11月2日，暂时不用再更新了
# query_sql2 = " select tradingPair,startDate from coins  where tradingPair <> 'LUNAUSDT'  "
# process_date_yyyymmdd2 = get_next_process_date()
# end_date_yyyymmdd2 = get_previous_date(process_date_yyyymmdd2, 5)   # 往前追溯10天的数据
# tradingPairs2 = get_trading_pairs_date(query_sql2)
# get_history_trading_data(tradingPairs2, process_date_yyyymmdd2, end_date_yyyymmdd2)



conn.close()
if len(final_message) == 0:
    print('Success! I have fetched the data for today.')
else:
    print('final_message', final_message)
