import sqlite3
from dateTimeUtil import get_previous_date, get_yesterday_yyyymmdd

conn = sqlite3.connect('crypto.db')


def statistics_in_a_month():
    yesterday_yyyymmdd = get_yesterday_yyyymmdd()
    print(yesterday_yyyymmdd, "最近一个月内最强的选手是==========>")
    return statistics_recent_days(30)


def statistics_in_a_week():
    yesterday_yyyymmdd = get_yesterday_yyyymmdd()
    print(yesterday_yyyymmdd, "最近一周内最强的选手是==========>")
    return statistics_recent_days(7)


def statistics_recent_days(day_num):
    end_date_yyyymmdd = get_yesterday_yyyymmdd()
    begin_date_yyyymmdd = get_previous_date(end_date_yyyymmdd, day_num)
    return statistics_days_between(begin_date_yyyymmdd, end_date_yyyymmdd)


def statistics_days_between(begin_date_yyyymmdd, end_date_yyyymmdd):
    return statistics_days_between2(begin_date_yyyymmdd, end_date_yyyymmdd, "" )

def statistics_days_between2(begin_date_yyyymmdd, end_date_yyyymmdd, trading_pair):
    query_sql = "  select tradingPair, sum(buy_force)  bf_sum, sum(sell_force) sf_sum, sum( all_force ) af_sum, "
    query_sql += "  sum(buy_force)-sum(sell_force) as buy_minus_sell, "
    query_sql += "  (sum(buy_force)-sum(sell_force))/sum(all_force)*100 as gap_ratio "
    query_sql += " from buysell "
    query_sql += " where tradingDateTime >= '" + begin_date_yyyymmdd + "'"
    query_sql += " and tradingDateTime <= '" + end_date_yyyymmdd + "'"
    if len(trading_pair) > 0:
        query_sql += " and tradingPair = '" + trading_pair + "'"
    query_sql += " group by tradingPair "
    query_sql += " order by (sum(buy_force)-sum(sell_force))/sum(all_force)  desc"

    # print("sql=", query_sql)
    mycursor = conn.cursor()
    mycursor.execute(query_sql)
    rows = mycursor.fetchall()
    str_format = '{0:>4} {1:12} {2:>20} {3:>20} {4:>20} {5:>20} {6:>10} '
    print(str_format.format("id", "tradingPair", "bf_sum", "sf_sum", "af_sum", "buy_minus_sell", "gap_ratio(%)"))
    index = 0
    len_of_rows = len(rows)
    for row in rows:
        index += 1
        trading_pair = row[0]
        bf_sum = row[1]
        sf_sum = row[2]
        af_sum = row[3]
        buy_minus_sell = row[4]
        gap_ratio = row[5]
        bf_sum = "{0:,}".format(round(bf_sum, 2))
        sf_sum = "{0:,}".format(round(sf_sum, 2))
        af_sum = "{0:,}".format(round(af_sum, 2))
        buy_minus_sell = "{0:,}".format(round(buy_minus_sell, 2))
        gap_ratio = "{0:,}".format(round(gap_ratio, 2))
        gap_ratio += "%"
        if index <= 5 or index > len_of_rows-3:
            print(str_format.format(index, trading_pair, bf_sum, sf_sum, af_sum, buy_minus_sell, gap_ratio))

    mycursor.close()


statistics_in_a_month()
statistics_in_a_week()
# statistics_days_between2("2021-06-09", "2021-09-09", "CTKUSDT")
conn.close()
