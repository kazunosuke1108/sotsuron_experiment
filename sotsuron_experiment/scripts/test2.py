import pandas as pd

# タイムスタンプを持つDataFrameを作成する例
data = {
    'value': [1, 3, 6, 7, 8],
    'timestamp': ['2023-10-26 10:00:00', '2023-10-26 10:00:01', '2023-10-26 10:00:02', '2023-10-26 10:00:08', '2023-10-26 10:00:09']
}

df = pd.DataFrame(data)
print(df)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

# 時間の差分を計算する
nblank=100
while nblank>0:
    # 5秒以上の間隔がある行を削除する
    print(df)
    time_diff = df.index.to_series().diff().dt.total_seconds()
    print(time_diff)
    df = df[time_diff<=5]
    print(df)
    time_diff = df.index.to_series().diff().dt.total_seconds()
    nblank=len(df[time_diff<=5])
    print(df)
    print(nblank)

