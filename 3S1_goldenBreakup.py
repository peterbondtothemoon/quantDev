import pandas as pd
import talib
import sqlite3
from dateTimeUtil import get_previous_date, get_yesterday_yyyymmdd
from coinsUtil import get_trading_pairs



conn = sqlite3.connect('crypto.db')
mycursor = conn.cursor()

fast_ma_window = 1
slow_ma_window30 = 30
slow_ma_window100 = 100
trend_status = 0
trading_day_yyyymmdd = get_yesterday_yyyymmdd()
# trading_day_yyyymmdd = '2021-06-29'
previous_date_yyyymmdd = get_previous_date(trading_day_yyyymmdd, 1)


def get_price_history(trading_pair):
    mylist = []
    sql = " select close from klines where tradingPair = '" + trading_pair + "'  "
    sql += " and tradingDate <= '"+trading_day_yyyymmdd+"' "
    sql += " order by tradingDate  "
    mycursor.execute(sql)
    items = mycursor.fetchall()
    for item in items:
        mylist.append(item[0])
    return mylist


def save_result(many_records, result_type):
    insert_sql = " insert into results(tradingPair,tradingDate, resultType )  values( ?,?,? )"
    conn.executemany(insert_sql, many_records)
    # delete_sql = " delete from results "
    # delete_sql += " where tradingPair IN(SELECT tradingPair FROM results GROUP BY tradingPair, resultType HAVING count(ID)>1)"
    # delete_sql += " and id not in(SELECT  max(id) id FROM results GROUP BY tradingPair,resultType HAVING count(ID)>1) "
    # print(delete_sql)
    # conn.execute(delete_sql)
    conn.commit()


def save_golden_breakup(slow_ma_window):
    final_result = []
    many_records = []
    for each_trading_pair in tradingPairs:
        # 至少要有2天的k线记录
        trading_data = get_price_history(each_trading_pair)
        if len(trading_data) < 2:
            print('<======length of trading data is less than 2, continue next coin======>')
            continue

        df = pd.DataFrame(trading_data, columns={'close': 0})
        # print('df', df)
        df['fast_ma'] = talib.MA(df['close'], timeperiod=fast_ma_window)
        df['slow_ma'] = talib.MA(df['close'], timeperiod=slow_ma_window)

        # 获得最后两个Bar, 看看他们的数据, 比较金叉和死叉.
        current_bar = df.iloc[-1]   # 最后一行
        last_bar = df.iloc[-2]

        # 金叉的时候.
        if current_bar['fast_ma'] > current_bar['slow_ma'] and last_bar['fast_ma'] <= last_bar['slow_ma']:
            temp_msg = "it's a golden break up!  " + each_trading_pair+" will to the moon!"
            final_result.append(temp_msg)
            one_record = []
            one_record.append(each_trading_pair)
            one_record.append(trading_day_yyyymmdd)
            one_record.append("ma"+str(slow_ma_window))
            many_records.append(one_record)
    if len(many_records) > 0:
        save_result(many_records, "ma"+str(slow_ma_window))
    return final_result


def get_golden_breakup(slow_ma_window):
    final_result = []
    temp_result_type = "ma" + str(slow_ma_window)
    sql = " select tradingPair from results where tradingDate = '" + trading_day_yyyymmdd + "' "
    sql += " and resultType = '" + temp_result_type + "'"
    sql += " and tradingPair not in ("
    sql += " select tradingPair from results where tradingDate = '" + previous_date_yyyymmdd + "' "
    sql += " and resultType = '" + temp_result_type + "'"
    sql += " )  "
    sql += " order by tradingPair  "
    # print(sql)
    mycursor.execute(sql)
    items = mycursor.fetchall()
    for item in items:
        token_name = item[0]
        temp_msg = "it's a golden break up!  " + token_name + " will to the moon!"
        final_result.append(temp_msg)
    return final_result


tradingPairs = get_trading_pairs(conn)
save_golden_breakup(slow_ma_window30)
save_golden_breakup(slow_ma_window100)
golden_breakup30 = get_golden_breakup(slow_ma_window30)
golden_breakup100 = get_golden_breakup(slow_ma_window100)

if len(golden_breakup30) == 0:
    print("no golden_breakup30 in ", trading_day_yyyymmdd)
else:
    print("\ngolden_breakup_ma30 in ", trading_day_yyyymmdd)
    for msg in golden_breakup30:
        print(msg)

if len(golden_breakup100) == 0:
    print("\nno golden_breakup100 in ", trading_day_yyyymmdd)
else:
    print("\ngolden_breakup100 in ", trading_day_yyyymmdd)
    for msg in golden_breakup100:
        print(msg)


mycursor.close()
conn.close()
