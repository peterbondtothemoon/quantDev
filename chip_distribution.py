"""
计算筹码分布
"""

import pandas as pd
import numpy as np
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行


# ===导入数据
df = pd.read_csv('btc.csv', parse_dates=['trade_date'])
df = df.sort_values(by='trade_date', ascending=True).reset_index(drop=True)  #按照日期排列
df.reset_index(drop=True, inplace=True)


df['price'] = np.round(df['price'], 2)  # 保留两位小数
df['volume'] = df['volume']    # 成交量
df = df[['trade_date', 'price', 'volume']]


# ====计算筹码分布
chips = pd.DataFrame()

# 初始发行
chips.loc[0, 'price'] = 10  # 发行价
chips.loc[0, 'ratio'] = 1
TOTAL_VOLUME = 100

# 遍历每根K线
for index, row in df.iterrows():
    price = row['price']
    volume = row['volume']
    turn_over = volume/TOTAL_VOLUME
    print("price=", price, "volume=", volume, "turn_over=", turn_over)

    # 如果价格从未出现过
    if price not in chips['price'].tolist():
        # 所有价格的筹码比例 ×（1 - 换手率）
        chips['ratio'] = chips['ratio'] * (1 - turn_over)
        # 将新价格添加到筹码分布中
        _t = {'price': price, 'ratio': turn_over}
        chips = chips.append(_t, ignore_index=True)

    # 如果价格出现过
    else:
        # 所有价格的筹码比例 ×（1 - 换手率）
        chips['ratio'] = chips['ratio'] * (1 - turn_over)
        # 当日价格的筹码在之前变动的基础上加上今日换手率
        chips.loc[chips['price'] == price, 'ratio'] += turn_over

# 按照价格从大到小排序
chips.sort_values('price', inplace=True, ascending=False)
chips.reset_index(inplace=True, drop=True)
chips[chips['ratio'] >= 0.0001].to_csv('chip_distribution_result.csv', index=False)