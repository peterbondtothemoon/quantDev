from datetime import datetime


# 解析一个从交易所拿到的交易明细数据包，经过统计后存入数据库中
# trading_date_time：yyyymmdd24h格式的日期(每天24个小时，第一个小时以是yyyymmdd00，第24个小时是yyyymmdd23)
def parse_data(conn, json_data, trading_pair_name, trading_date_time) :
    # print("parse_data-trading_date_time=", trading_date_time)
    index = 0
    turn_over_buyer = 0
    turn_over_seller = 0
    turn_over_total = 0
    many_records = []
    for item in json_data:
        index = index+1
        price = float(item['p'])
        quantity = float(item['q'])
        turn_over = price * quantity
        ifBuyerMaker = item['m']
        transaction_time = datetime.fromtimestamp(round(item['T']/1000))

        turn_over_total += turn_over
        if ifBuyerMaker:
            bsFlag = 'SellerStrong'
            turn_over_seller += turn_over
        else:
            bsFlag = 'BuyerStrong'
            turn_over_buyer += turn_over
        str_format = '{0:4d} {1:6.2f}  {2:6.2f} {3:10.2f}  {4:5}   {5:12}  {6:20}'
        # print(str_format.format(index, price, quantity, turn_over, str(ifBuyerMaker), bsFlag, str(transaction_time)))

    # str_format2 = '{0:10.2f}'
    # print("turn_over_buyer =",   str_format2.format(turn_over_buyer),
    #       "\nturn_over_seller=", str_format2.format(turn_over_seller),
    #       "\nturn_over_total =", str_format2.format(turn_over_total))

    one_record = [trading_pair_name, trading_date_time, turn_over_buyer, turn_over_seller, turn_over_total]
    many_records.append(one_record)

    delete_sql = " delete from buysell where tradingPair = '" + trading_pair_name + "'"
    delete_sql += " and  tradingDateTime = '" + trading_date_time + "'"
    conn.execute(delete_sql)
    insert_sql = " insert into buysell(tradingPair,tradingDateTime,buy_force, sell_force, all_force)  " \
                 " values( ?, ?, ?, ?, ? )"
    conn.executemany(insert_sql, many_records)
    conn.commit()
    return
