from datetime import datetime, timedelta


# 工具类1，取得当前日期之前若干天的时间
def get_previous_date(some_date_yyyymmdd, how_many_days):
    temp_date = datetime.fromisoformat(some_date_yyyymmdd)
    previous_day_yyyymmdd = datetime.strftime((temp_date - timedelta(how_many_days)), '%Y-%m-%d')
    return previous_day_yyyymmdd


# 工具类2，取得当前日期之后若干天的时间
def get_future_date(some_date_yyyymmdd, how_many_days):
    temp_date = datetime.fromisoformat(some_date_yyyymmdd)
    future_day_yyyymmdd = datetime.strftime((temp_date + timedelta(how_many_days)), '%Y-%m-%d')
    return future_day_yyyymmdd


# 工具类3，加上截至时间（第二天的0时）
def add_last_elem(temp_list2, temp_yyyymmdd):
    str_future_date = get_future_date(temp_yyyymmdd, 1) + " 00"
    dt_obj = datetime.strptime(str_future_date, '%Y-%m-%d %H')
    temp_timestamp = str(round(dt_obj.timestamp() * 1000))
    temp_list2.append(temp_timestamp)
    return temp_list2


# 工具类4，把10的小时返回： " 0x",否则返回" xx"
def get_hour_suffix(int_hour):
    result = ""
    if int_hour < 10:
        result = " 0" + str(int_hour)
    else:
        result = " " + str(int_hour)
    return result


# 工具类5，组建一个从0时到23时，最后是第二天0时，总共是25个时间点对应的timestamp列表
def get_timestamp_24hlist(temp_yyyymmdd):
    result_list = []
    index = 0
    temp_yyyymmdd24h = ""
    temp_timestamp = ""
    while True:
        if index > 23:
            break
        elif index < 10:
            temp_yyyymmdd24h = temp_yyyymmdd + " 0" + str(index)
        else:
            temp_yyyymmdd24h = temp_yyyymmdd + " " + str(index)

        dt_obj = datetime.strptime(temp_yyyymmdd24h, '%Y-%m-%d %H')
        temp_timestamp = str(round(dt_obj.timestamp() * 1000))

        result_list.append(temp_timestamp)
        index += 1

    result_list = add_last_elem(result_list, temp_yyyymmdd)
    return result_list


def get_yesterday_yyyymmdd():
    return datetime.strftime((datetime.now() - timedelta(1)), '%Y-%m-%d')
