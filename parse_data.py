# from datetime import datetime

# trading_date_time：yyyymmdd24h格式的日期(每天24个小时，第一个小时以是yyyymmdd00，第24个小时是yyyymmdd23)
# 小杯星巴克咖啡的价格区间为(0->2000usd),不包含2000usd
MIDDLE_FORCE_LOW_BOUND = 2000  # 中杯星巴克咖啡的价格区间为【2000->5000usd) ：每笔最少 2000 usd，每笔最多 5000 usd（不含5000）
MIDDLE_FORCE_HIGH_BOUND = 5000  # 大杯星巴克咖啡的价格区间为【5000->1万usd)
BIG_FORCE_HIGH_BOUND = 10000  # 超大杯星巴克咖啡的价格区间为【1万usd及以上)


# 解析一个从交易所拿到的交易明细数据包，经过统计后存入数据库中
# 根据buyer maker flag字段(币安aggTrades接口返回的字段"m") ,区分主动性买单和主动性卖单，把主动性买单（或者主动性卖单）的成交金额（还有成交数量）存入数据库中
# 根据每笔成交金额的大小，区分是小单/中单/大单/超大单，把对应的成交金额（还有成交数量）存入数据库中
def parse_data(conn, json_data, trading_pair_name, trading_date_time):
    # print("parse_data-trading_date_time=", trading_date_time)
    index = 0
    buy_amount = 0  # 主动性买单的成交金额（成交金额=成交价*成交数量）
    buy_volume = 0  # 主动性买单的成交数量
    sell_amount = 0
    sell_volume = 0
    total_amount = 0
    total_volume = 0

    buy_small_amount = 0  # 小杯星巴克咖啡的成交金额(主动性买单)
    buy_small_volume = 0  # 小杯星巴克咖啡的成交量(主动性买单)
    buy_middle_amount = 0     # 中杯星巴克咖啡的成交金额(主动性买单)
    buy_middle_volume = 0     # 中杯星巴克咖啡的成交量(主动性买单)
    buy_big_amount = 0
    buy_big_volume = 0
    buy_super_big_amount = 0
    buy_super_big_volume = 0

    sell_small_amount = 0  # 小杯星巴克咖啡的成交金额(主动性卖单)
    sell_small_volume = 0  # 小杯星巴克咖啡的成交量(主动性卖单)
    sell_middle_amount = 0
    sell_middle_volume = 0
    sell_big_amount = 0
    sell_big_volume = 0
    sell_super_big_amount = 0
    sell_super_big_volume = 0

    many_records = []
    many_records_bigdeal = []
    for item in json_data:
        index = index + 1
        price = float(item['p'])
        volume = float(item['q'])
        temp_amount = price * volume
        buyer_maker_flag = item['m']
        # transaction_time = datetime.fromtimestamp(round(item['T']/1000))

        total_amount += temp_amount
        total_volume += volume
        if not buyer_maker_flag:
            buy_amount += temp_amount
            buy_volume += volume

            if MIDDLE_FORCE_LOW_BOUND <= temp_amount < MIDDLE_FORCE_HIGH_BOUND:
                buy_middle_amount += temp_amount
                buy_middle_volume += volume
            elif MIDDLE_FORCE_HIGH_BOUND <= temp_amount < BIG_FORCE_HIGH_BOUND:
                buy_big_amount += temp_amount
                buy_big_volume += volume
            elif temp_amount >= BIG_FORCE_HIGH_BOUND:
                buy_super_big_amount += temp_amount
                buy_super_big_volume += volume
            else:
                buy_small_amount += temp_amount
                buy_small_volume += volume

        else:
            sell_amount += temp_amount
            sell_volume += volume
            if MIDDLE_FORCE_LOW_BOUND <= temp_amount < MIDDLE_FORCE_HIGH_BOUND:
                sell_middle_amount += temp_amount
                sell_middle_volume += volume
            elif MIDDLE_FORCE_HIGH_BOUND <= temp_amount < BIG_FORCE_HIGH_BOUND:
                sell_big_amount += temp_amount
                sell_big_volume += volume
            elif temp_amount >= BIG_FORCE_HIGH_BOUND:
                sell_super_big_amount += temp_amount
                sell_super_big_volume += volume
            else:
                sell_small_amount += temp_amount
                sell_small_volume += volume

    # 最后，一个小时内的所有交易记录汇总成为一条记录
    one_record = [trading_pair_name, trading_date_time, buy_amount, buy_volume,
                  sell_amount, sell_volume, total_amount, total_volume]
    many_records.append(one_record)

    one_record_bigdeal = [trading_pair_name, trading_date_time, buy_small_amount, buy_small_volume,
                          buy_middle_amount, buy_middle_volume, buy_big_amount, buy_big_volume,
                          buy_super_big_amount, buy_super_big_volume, sell_small_amount, sell_small_volume,
                          sell_middle_amount, sell_middle_volume, sell_big_amount, sell_big_volume,
                          sell_super_big_amount, sell_super_big_volume, total_amount, total_volume]
    many_records_bigdeal.append(one_record_bigdeal)

    delete_sql = " delete from buysell where tradingPair = '" + trading_pair_name + "'"
    delete_sql += " and  tradingDateTime = '" + trading_date_time + "'"
    conn.execute(delete_sql)
    insert_sql = " insert into buysell(tradingPair,tradingDateTime,buy_force,buy_force_volume," \
                 " sell_force,sell_force_volume, all_force, all_force_volume)  " \
                 " values( ?, ?, ?, ?,   ?,?,?,? )"
    conn.executemany(insert_sql, many_records)

    delete_sql = " delete from buysell_bigdeal where tradingPair = '" + trading_pair_name + "'"
    delete_sql += " and  tradingDateTime = '" + trading_date_time + "'"
    conn.execute(delete_sql)
    insert_sql = " insert into buysell_bigdeal(tradingPair,tradingDateTime,buy_small_amount, buy_small_volume," \
                 " buy_middle_amount, buy_middle_volume, buy_big_amount, buy_big_volume," \
                 " buy_super_big_amount, buy_super_big_volume, sell_small_amount, sell_small_volume," \
                 " sell_middle_amount, sell_middle_volume, sell_big_amount, sell_big_volume, " \
                 " sell_super_big_amount, sell_super_big_volume, total_amount, total_volume)  " \
                 " values( ?,?,?,?,?,  ?,?,?,?,?,  ?,?,?,?,?,   ?,?,?,?,?)"
    conn.executemany(insert_sql, many_records_bigdeal)

    conn.commit()
    return
