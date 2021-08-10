from datetime import datetime, timedelta
import sqlite3


conn = sqlite3.connect('crypto.db')
mycursor = conn.cursor()

try:
    x = 1 / 0
except:
    print("<=======exception function is running=======>")

yesterday_yyyymmdd = datetime.strftime((datetime.now() - timedelta(1)), '%Y-%m-%d')
error_message = []
temp_message = ""
# check the database tables is exists
try:
    sql = "select * from coins "
    mycursor.execute(sql)
    sql = "select * from klines "
    mycursor.execute(sql)
    sql = "select * from results "
    mycursor.execute(sql)
except:
    temp_message = "<!!!sth. wrong happened with the table of database!!!>"
    print(temp_message)
    error_message.append(temp_message)


# check no duplicate records in coins, klines or results
try:
    sql = " SELECT  COUNT(ID) num ,tradingPair FROM COINS "
    sql += " GROUP BY tradingPair HAVING count(ID) > 1 "
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    if len(rows) > 0:
        for row in rows:
            record_num = str(row[0])
            trading_pair = row[1]
            temp_message = trading_pair + " has " + record_num + " duplicate records in table COINS "
            error_message.append(temp_message)

    sql = "SELECT  COUNT(ID)  num ,tradingPair , tradingDate  FROM klines "
    sql += " GROUP BY tradingPair  , tradingDate  HAVING count(ID) > 1 "
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    if len(rows) > 0:
        for row in rows:
            record_num = str(row[0])
            trading_pair = row[1]
            temp_message = trading_pair + " has " + record_num + " duplicate records in table klines"
            error_message.append(temp_message)

except:
    temp_message += "error while checking duplicate records"
    print(temp_message)
    error_message.append(temp_message)

# check the data of yesterday is existed
try:
    sql = "select tradingPair from coins where whichExchange = 'BINANCE' order by id "
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    for row in rows:
        trading_pair = row[0]
        sql2 = " select * from klines where tradingPair='" + trading_pair + "'"
        sql2 += " and tradingDate = '" + yesterday_yyyymmdd + "'"
        # print("sql2=", sql2)
        mycursor.execute(sql2)
        rows = mycursor.fetchall()
        if len(rows) != 1:
            temp_message = "check the data of yesterday: wrong record number in klines with " + trading_pair+" in " + yesterday_yyyymmdd
            print(temp_message)
            error_message.append(temp_message)
            break
except:
    temp_message += "<!!!sth. wrong happened with the datas of yesterday!!!>"
    print(temp_message)
    error_message.append(temp_message)


# check no missing records in klines(最大日期-最小日期得出天数，有多少天就应该有多少条记录)


if len(error_message) == 0:
    print("\n<=======Excellent! Wonderful! Everything is fine! ========>")
else:
    print("sth. wrong happened:", error_message)
mycursor.close()
conn.close()
