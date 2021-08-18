from datetime import datetime, timedelta
import sqlite3

conn = sqlite3.connect('crypto.db')
mycursor = conn.cursor()


# 工具类1，取得当前日期之前若干天的时间
def get_previous_date(some_date_yyyymmdd, how_many_days):
    temp_date = datetime.fromisoformat(some_date_yyyymmdd)
    previous_day_yyyymmdd = datetime.strftime((temp_date - timedelta(how_many_days)), '%Y-%m-%d')
    return previous_day_yyyymmdd


# 工具类2：通过数据库的查询，取得某个标的在某个时间段内段平均价格
# trading_pair：交易对，例如BTCUSDT
# start_time:开始时间,格式为yyyy-mm-dd
# end_time: 结束时间，比开始时间要晚，数值更大,格式为yyyy-mm-dd
def get_avg_price_for_interval(trading_pair, start_time, end_time):
    avg_price = 0
    sql = "select avg(close) from klines where tradingPair = '" + trading_pair + "' "
    sql += " and tradingDate >= '" + start_time + "' "
    sql += " and tradingDate <= '" + end_time + "' "
    # print("get_avg_price_for_interval:\n", sql)
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    if len(rows) == 1:
        avg_price = rows[0][0]
        # print('get_avg_price_for_interval==>avg_price=', avg_price)
    else:
        print("sth. wrong with average price,sql is:", sql)
    return avg_price


trading_day_yyyymmdd = datetime.strftime((datetime.now() - timedelta(1)), '%Y-%m-%d')
# trading_day_yyyymmdd = '2021-07-10'
how_many_days_30 = 30
how_far_from_home = 0.5
how_close_from_home = 0.1


# 1已经突破了ma30的标的：
def get_good_boys():
    result_list = []
    sql = " select tradingPair,tradingDate from results  "
    sql += " where stillEffectiveNow = 'yes' and resultType = 'ma30' order by id "
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    for row in rows:
        temp_dic = {}
        temp_dic['trading_pair'] = row[0]
        temp_dic['breaking_date'] = row[1]
        result_list.append(temp_dic)
    return result_list


# 2宝宝曾经展翅翱翔：
# 曾经离家万里（在突破日后到昨天这个时间段内）：
# (日k的close价-当天对应的ma30价格)/当天对应的ma30价格 >=50%
# start_date:突破ma的日期
# end_date:昨天的日期
def once_flied_farfaraway(trading_pair, start_date, end_date):
    sql = " select tradingDate, close from klines where tradingPair = '" + trading_pair + "' "
    sql += " and tradingDate >= '" + start_date + "' "
    sql += " and tradingDate <= '" + end_date + "' "
    sql += " order by tradingDate "

    # print("\n=====>once_flied_farfaraway: ", sql)
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    for row in rows:
        temp_date = row[0]
        temp_close_price = row[1]

        previous_date_date = get_previous_date(temp_date, how_many_days_30)
        avg_price = get_avg_price_for_interval(trading_pair, previous_date_date, temp_date)

        # compare current price with the relative ma_price in the same date
        distance_rate = (temp_close_price - avg_price) / avg_price
        # distance_rate_percent = "%.2f%%" % (distance_rate * 100)
        if distance_rate > how_far_from_home:
            # print('temp_close_price=', temp_close_price)
            # print("distance_rate_percent=", distance_rate_percent)
            # print("<============Super boy flied far far away!!!===========>\n")
            return 1
    return 0


#  3回家:回到均线附近
# （日k的收盘价-对应日期的ma30的价格）/对应日期的ma30的价格 < 10%
def boy_return_home(trading_pair_par):
    # get current price
    sql = "  select close from klines where tradingPair = '" + trading_pair_par + "' "
    sql += " and tradingDate = '" + trading_day_yyyymmdd + "' "
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    if len(rows) == 1:
        cnt_price = rows[0][0]
    else:
        print("sth.wrong in klines with tradingPair:", trading_pair_par, " &len(rows)=", len(rows))
        return 0

    # get average price
    temp_previous_date = get_previous_date(trading_day_yyyymmdd, how_many_days_30)
    avg_price = get_avg_price_for_interval(trading_pair_par, temp_previous_date, trading_day_yyyymmdd)

    distance_rate = (cnt_price - avg_price) / avg_price
    distance_rate_percent = "%.2f%%" % (distance_rate * 100)
    if distance_rate < how_close_from_home:
        # print("current price = ", cnt_price)
        # print("distance_rate_percent=", distance_rate_percent)
        # print("good boy returned home :)")
        return 1
    return 0


good_boys = get_good_boys()
final_trading_pairs = []
for good_boy in good_boys:
    # print("good_boy is:", good_boy)

    str_trading_pair = str(good_boy['trading_pair'])
    str_breaking_date = str(good_boy['breaking_date'])
    flied_farfaraway_flag = once_flied_farfaraway(str_trading_pair, str_breaking_date, trading_day_yyyymmdd)
    return_home_flag = boy_return_home(str_trading_pair)
    if flied_farfaraway_flag == 1 and return_home_flag == 1:
        print("good boy flied far far away, good_boy has just returned home:", good_boy)
        final_trading_pairs.append(str_trading_pair)
        continue


for temp_trading_pair in final_trading_pairs:
    print("final trading_pair=", temp_trading_pair)
mycursor.close()
conn.close()
