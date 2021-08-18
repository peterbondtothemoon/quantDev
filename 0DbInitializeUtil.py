import sqlite3
conn = sqlite3.connect('crypto.db')
c = conn.cursor()


# deleteTableSql = "drop table if exists coins "
# c.execute(deleteTableSql)

# c.execute("""
# CREATE TABLE "coins" (
# 	"id"	INTEGER primary key autoincrement,
#     "tradingPair"  TEXT,
# 	"whichExchange"	TEXT,
#      "startDate" Text, --上交易所的日期/开始取数的日期,格式为yyyymmdd
# 	"remarks"	TEXT
# )
# """)

# dropTableSql = "drop table  if exists  klines "
# c.execute(dropTableSql)
#
# c.execute("""
#     CREATE TABLE "klines" (
#     "id" INTEGER primary key autoincrement,
#     "tradingPair" TEXT,
#     "tradingDate" DATE,
#     "open" INTEGER,
#     "close"INTEGER,
#     "high" INTEGER,
#     "low" INTEGER,
#     "volume" INTEGER
#     )
# """)

# deleteTableSql = "drop table  if exists  results "
# c.execute(deleteTableSql)

# c.execute("""
# CREATE TABLE "results" ( --the tradingPairs where closePrice > price(ma30),brokeUp happened
# 	"id"	INTEGER primary key autoincrement,
#     "tradingPair"  TEXT,
# 	"tradingDate" DATE,
# 	"resultType" TEXT,
# 	"stillEffectiveNow" TEXT DEFAULT 'yes'
# )
# """)

# dropTableSql = "drop table  if exists buysell "
# c.execute(dropTableSql)
# c.execute("""
#     CREATE TABLE "buysell" (
#     "id" INTEGER primary key autoincrement,
#     "tradingPair" TEXT,       --icpusdt/icpbusd
#     "tradingDateTime" TEXT,   --yyyymmdd24h
#     "buy_force"  FLOAT,       --turn over amount of buyer
#     "buy_force_volume"  FLOAT, --turn over volume of buyer
#     "sell_force" FLOAT,        --turn over amount of seller
#     "sell_force_volume" FLOAT, --turn over amount of seller
#     "all_force" FLOAT,  --turn over amount of ALL(including buyer, seller,and others)
#     "all_force_volume" FLOAT, --turn over volume of ALL(including buyer, seller,and others)
#     "platform" TEXT DEFAULT 'BINANCE'     --binance/gate/mxc
#     )
# """)


dropTableSql = "drop table  if exists buysell_bigdeal "
c.execute(dropTableSql)
c.execute("""
    CREATE TABLE "buysell_bigdeal" (
    "id" INTEGER primary key autoincrement,
    "tradingPair" TEXT,       --icpusdt/icpbusd
    "tradingDateTime" TEXT,   --yyyymmdd24h
    
    "buy_small_amount"  FLOAT,  --turn over amount of small buy(maybe less than 2000 usdt)
    "buy_small_volume"  FLOAT,  --turn over volume of small buy
    "buy_middle_amount"  FLOAT, --turn over amount of middle buy(maybe 2k->5k usdt)
    "buy_middle_volume"  FLOAT, --turn over volume of middle buy
    "buy_big_amount" FLOAT,            --turn over amount of big buy(maybe 5k->10k usdt)
    "buy_big_volume" FLOAT,     --turn over amount of big buy
    "buy_super_big_amount"  FLOAT,           --turn over amount of super big buy(maybe bigger than 10k usdt)
    "buy_super_big_volume" FLOAT,     --turn over volume of super big buy
    
    "sell_small_amount"  FLOAT,  --turn over amount of small sell(maybe less than 2000 usdt)
    "sell_small_volume"  FLOAT,  --turn over volume of small sell
    "sell_middle_amount"  FLOAT, --turn over amount of middle sell(maybe 2k->5k usdt)
    "sell_middle_volume"  FLOAT, --turn over volume of middle sell
    "sell_big_amount" FLOAT,            --turn over amount of big sell(maybe 5k->10k usdt)
    "sell_big_volume" FLOAT,     --turn over amount of big sell
    "sell_super_big_amount"  FLOAT,           --turn over amount of super big sell(maybe bigger than 10k usdt)
    "sell_super_big_volume" FLOAT,     --turn over volume of super big sell
    
    "total_amount"  FLOAT,           --turn over amount of all force
    "total_volume" FLOAT      --turn over volume of all force
    )
""")

dropTableSql = "drop table   if exists  statistics "
c.execute(dropTableSql)
# c.execute("""
#     CREATE TABLE "statistics" (
#     "id" INTEGER primary key autoincrement,
#     "tradingPair" TEXT,     --icpusdt/icpbusd
#     "tradingDate" TEXT,     --depends on schedule_type(date is yyyymmdd, month is yyyymm, year is yyyy)
#     "buy_force"  FLOAT,     --turn over amount of buyer
#     "sell_force" FLOAT,     --turn over amount of seller
#     "all_force"  FLOAT,     --turn over amount of all(including buyer, seller,and others)
#     "buy_minus_sell" FLOAT, --turn over amount of ALL()
#     "gap_to_all" TEXT,      --buyforce_minus_sellforce/all_force
#     "time_type" TEXT,       --date,month,year
#     "platform" TEXT DEFAULT 'BINANCE'     --binance/gate/mxc
#     )
# """)

conn.commit()
conn.close()
print('Success! I have just initialized the database!')