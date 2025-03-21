import pandas as pd

# 读取CSV文件
df = pd.read_csv('latest_parsed.csv')

# 检查两手牌
hand_ids = ['RC3334603213', 'RC3334603458']
for hand_id in hand_ids:
    row = df[df['Hand_ID'] == hand_id]
    if not row.empty:
        print(f'手牌 {hand_id}:')
        print(f'IP_Cbet_Flop: {row.iloc[0]["IP_Cbet_Flop"]}')
        print(f'VS_IP_Cbet: {row.iloc[0]["VS_IP_Cbet"]}')
        print(f'OOP_XR_Cbet: {row.iloc[0]["OOP_XR_Cbet"]}')
        print('---------------')
    else:
        print(f'未找到手牌 {hand_id}')
        print('---------------') 