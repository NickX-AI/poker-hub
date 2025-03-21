import csv
import os
import re

# 检查生成的CSV文件，专门查找Hero是第一个raises的情况
csv_file_path = 'parsed_hands.csv'  # 使用最新生成的文件

if not os.path.exists(csv_file_path):
    print(f"错误：找不到文件 {csv_file_path}")
    exit(1)

# 统计数据
hero_first_raise_count = 0
hero_first_raise_samples = []

# 读取CSV文件
with open(csv_file_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    # 读取数据
    total_rows = 0
    for row in reader:
        total_rows += 1
        
        # 查找Hero是第一个raises的情况
        preflop_actions = row['Preflop_Actions']
        hero_position = row['Hero_Position']
        
        # 使用正则表达式检查Hero是否是第一个raises的玩家
        # 首先检查preflop_actions中是否有raises
        if 'raises' in preflop_actions:
            # 获取第一个raises的玩家
            match = re.search(r'([^;]+raises[^;]+)', preflop_actions)
            if match:
                first_raise = match.group(1)
                # 检查这个raise是否由Hero做出
                if f"Hero({hero_position})" in first_raise:
                    hero_first_raise_count += 1
                    
                    if len(hero_first_raise_samples) < 5:
                        hero_first_raise_samples.append({
                            'Hand_ID': row['Hand_ID'],
                            'Hero_Position': row['Hero_Position'],
                            'Hero_Open_Position': row['Hero_Open_Position'],
                            'Preflop_Actions': preflop_actions[:100] + '...' if len(preflop_actions) > 100 else preflop_actions,
                            'First_Raise': first_raise
                        })

# 输出统计结果
print(f"总行数: {total_rows}")
print(f"Hero是第一个raises的行数: {hero_first_raise_count} ({hero_first_raise_count/total_rows*100:.2f}%)")

print("\n=== Hero是第一个raises的样本 ===")
for i, sample in enumerate(hero_first_raise_samples):
    print(f"样本 {i+1}:")
    for key, value in sample.items():
        print(f"  {key}: {value}")
    print() 