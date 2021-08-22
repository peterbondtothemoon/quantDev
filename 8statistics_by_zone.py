import sqlite3
conn = sqlite3.connect('crypto.db')
str_format_title = '{0:>14} {1:>7} {2:>7} {3:>7} {4:>7} {5:>20} {6:>20}'
str_format = '{0:>20} {1:>10} {2:>10} {3:>8} {4:>8} {5:>20} {6:>20}'


def get_force_by_zone(trading_pair, date_yyyymmdd):
    query_sql = "select sum(buy_small_amount),sum(buy_middle_amount) , sum(buy_big_amount), " \
                " sum(buy_super_big_amount), sum(total_amount) " \
                " from buysell_bigdeal where tradingPair = '" + trading_pair + "' "
    query_sql += " and tradingDateTime like '" + date_yyyymmdd + "%' "
    # print("sql=", query_sql)
    mycursor = conn.cursor()
    mycursor.execute(query_sql)
    rows = mycursor.fetchall()
    index = 0

    for row in rows:
        index += 1
        # print("row", index, row)
        buy_small_amount = row[0]
        buy_middle_amount = row[1]
        buy_big_amount = row[2]
        buy_super_big_amount = row[3]
        total_amount = row[4]
        # print("sum:", buy_small_amount, buy_middle_amount, buy_big_amount, buy_super_big_amount, total_amount)
        ratio_small_to_all = round(buy_small_amount/total_amount*100, 2)
        ratio_middle_to_all = round(buy_middle_amount/total_amount*100, 2)
        ratio_big_to_all = round(buy_big_amount/total_amount*100, 2)
        ratio_super_to_all = round(buy_super_big_amount/total_amount*100, 2)
        bigsuper_to_all = round(ratio_big_to_all + ratio_super_to_all, 2)
        middlebigsuper_to_all = round(ratio_middle_to_all+ratio_big_to_all+ratio_super_to_all, 2)

        print(str_format.format(trading_pair, ratio_small_to_all, ratio_middle_to_all, ratio_big_to_all,
                                ratio_super_to_all, bigsuper_to_all, middlebigsuper_to_all))



def save_force():
    pass


print(str_format_title.format("主买成交量vs所有成交量:", "小买单%", "中买单%", "大买单%", "超大买单%", "大单超大买单%", "中单大单超大买单%" ))
get_force_by_zone("BTCUSDT", "2021-08-16")
get_force_by_zone("ETHUSDT", "2021-08-16")
get_force_by_zone("ARDRUSDT", "2021-08-16")
get_force_by_zone("AXSUSDT", "2021-08-16")
get_force_by_zone("HARDUSDT", "2021-08-16")
get_force_by_zone("ICPUSDT", "2021-08-16")
get_force_by_zone("DODOUSDT", "2021-08-16")
get_force_by_zone("LUNAUSDT", "2021-08-16")
get_force_by_zone("CAKEUSDT", "2021-08-16")
get_force_by_zone("CTSIUSDT", "2021-08-16")
get_force_by_zone("SOLUSDT", "2021-08-16")
get_force_by_zone("ALPHAUSDT", "2021-08-16")
get_force_by_zone("1INCHUSDT", "2021-08-16")
conn.close()
