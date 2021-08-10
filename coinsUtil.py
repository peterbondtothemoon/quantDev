def get_trading_pairs(conn):
    result_list = []
    query_sql = "  select tradingPair from coins where whichExchange = 'BINANCE' order by id "
    mycursor = conn.cursor()
    mycursor.execute(query_sql)
    rows = mycursor.fetchall()
    for row in rows:
        result_list.append(row[0])
    mycursor.close()
    return result_list
