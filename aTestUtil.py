from dateTimeUtil import *
from parse_data import parse_data
import sqlite3
import json



conn = sqlite3.connect('crypto.db')

start_time_24h = "2021-08-18" + get_hour_suffix(0)
trading_pair_name = 'ICPUSDT'
print(start_time_24h)
#
# Opening JSON file
f = open('aggTrades_icp.json')
data = json.load(f)
print(data)

parse_data(conn, data, trading_pair_name, start_time_24h)

conn.close()
