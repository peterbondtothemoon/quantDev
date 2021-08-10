import sqlite3
conn = sqlite3.connect('crypto.db')
c = conn.cursor()


# deleteTableSql = "drop table coins if exists coins "
# c.execute(deleteTableSql)

c.execute("""
CREATE TABLE "coins" (
	"id"	INTEGER primary key autoincrement,
    "tradingPair"  TEXT,
	"whichExchange"	TEXT,
     "startDate" Text, --上交易所的日期/开始取数的日期,格式为yyyymmdd
	"remarks"	TEXT
)
""")



# dropTableSql = "drop table klines  if exists  klines "
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

# deleteTableSql = "drop table results  if exists  results "
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

# dropTableSql = "drop table buysell  if exists buysell "
# c.execute(dropTableSql)
# c.execute("""
#     CREATE TABLE "buysell" (
#     "id" INTEGER primary key autoincrement,
#     "tradingPair" TEXT,     --icpusdt/icpbusd
#     "tradingDateTime" TEXT, --yyyymmdd24h
#     "buy_force"  FLOAT, --turn over amount of buyer
#     "sell_force" FLOAT, --turn over amount of seller
#     "all_force" FLOAT,  --turn over amount of ALL(including buyer, seller,and others)
#     "all_volume" FLOAT, --turn over volume of ALL(including buyer, seller,and others)
#     "platform" TEXT DEFAULT 'BINANCE'     --binance/gate/mxc
#     )
# """)

dropTableSql = "drop table statistics  if exists  statistics "
c.execute(dropTableSql)
c.execute("""
    CREATE TABLE "statistics" (
    "id" INTEGER primary key autoincrement,
    "tradingPair" TEXT,     --icpusdt/icpbusd
    "tradingDate" TEXT,     --depends on schedule_type(date is yyyymmdd, month is yyyymm, year is yyyy)
    "buy_force"  FLOAT,     --turn over amount of buyer
    "sell_force" FLOAT,     --turn over amount of seller
    "all_force"  FLOAT,     --turn over amount of all(including buyer, seller,and others)
    "buy_minus_sell" FLOAT, --turn over amount of ALL()
    "gap_to_all" TEXT,      --buyforce_minus_sellforce/all_force
    "time_type" TEXT,       --date,month,year
    "platform" TEXT DEFAULT 'BINANCE'     --binance/gate/mxc
    )
""")

conn.commit()
conn.close()
print('Success! I have just initialized the database!')