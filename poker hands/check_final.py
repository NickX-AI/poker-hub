import csv
import os
import re

# 检查生成的CSV文件，验证Cash_Drop和Hero_Open_Position的修改
csv_file_path = 'poker_output/parsed_hands.csv'  # 使用最新生成的文件

if not os.path.exists(csv_file_path):
    print(f"错误：找不到文件 {csv_file_path}")
    exit(1)

print("开始检查文件:", csv_file_path)

# 统计数据
cash_drop_yes_count = 0
cash_drop_no_count = 0
hero_open_position_counts = {}
hero_first_raise_count = 0
hero_first_raise_with_position_count = 0

# 收集样本数据
cash_drop_yes_samples = []
hero_first_raise_samples = []

# 读取CSV文件
with open(csv_file_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    # 读取数据
    total_rows = 0
    for row in reader:
        total_rows += 1
        
        # 统计Cash_Drop
        if row['Cash_Drop'] == 'YES':
            cash_drop_yes_count += 1
            if len(cash_drop_yes_samples) < 3:
                cash_drop_yes_samples.append({
                    'Hand_ID': row['Hand_ID'],
                    'Cash_Drop': row['Cash_Drop'],
                    'Preflop_Pot': row['Preflop_Pot']
                })
        else:
            cash_drop_no_count += 1
        
        # 统计Hero_Open_Position
        hero_open_position = row['Hero_Open_Position']
        if hero_open_position not in hero_open_position_counts:
            hero_open_position_counts[hero_open_position] = 0
        hero_open_position_counts[hero_open_position] += 1
        
        # 查找Hero是第一个raises的情况
        preflop_actions = row['Preflop_Actions']
        hero_position = row['Hero_Position']
        
        # 使用正则表达式检查Hero是否是第一个raises的玩家
        if 'raises' in preflop_actions:
            match = re.search(r'([^;]+raises[^;]+)', preflop_actions)
            if match:
                first_raise = match.group(1)
                # 检查这个raise是否由Hero做出
                if f"Hero({hero_position})" in first_raise:
                    hero_first_raise_count += 1
                    # 检查Hero_Open_Position是否等于Hero_Position
                    if hero_open_position == hero_position:
                        hero_first_raise_with_position_count += 1
                    
                    if len(hero_first_raise_samples) < 5:
                        hero_first_raise_samples.append({
                            'Hand_ID': row['Hand_ID'],
                            'Hero_Position': row['Hero_Position'],
                            'Hero_Open_Position': row['Hero_Open_Position'],
                            'Preflop_Actions': preflop_actions[:100] + '...' if len(preflop_actions) > 100 else preflop_actions,
                            'First_Raise': first_raise
                        })

print("\n" + "="*50)
print("Cash_Drop 统计")
print("="*50)
print(f"总行数: {total_rows}")
print(f"Cash_Drop为YES的行数: {cash_drop_yes_count} ({cash_drop_yes_count/total_rows*100:.2f}%)")
print(f"Cash_Drop为NO的行数: {cash_drop_no_count} ({cash_drop_no_count/total_rows*100:.2f}%)")

print("\n" + "="*50)
print("Cash_Drop为YES的示例")
print("="*50)
for i, sample in enumerate(cash_drop_yes_samples):
    print(f"样本 {i+1}:")
    for key, value in sample.items():
        print(f"  {key}: {value}")
    print()

print("\n" + "="*50)
print("Hero_Open_Position 统计")
print("="*50)
for position, count in sorted(hero_open_position_counts.items()):
    print(f"{position}: {count} ({count/total_rows*100:.2f}%)")

print("\n" + "="*50)
print("Hero是第一个raises的统计")
print("="*50)
print(f"Hero是第一个raises的行数: {hero_first_raise_count} ({hero_first_raise_count/total_rows*100:.2f}%)")
if hero_first_raise_count > 0:
    print(f"其中Hero_Open_Position等于Hero_Position的行数: {hero_first_raise_with_position_count} ({hero_first_raise_with_position_count/hero_first_raise_count*100:.2f}%)")
else:
    print("没有找到Hero是第一个raises的情况")

print("\n" + "="*50)
print("Hero是第一个raises的样本")
print("="*50)
for i, sample in enumerate(hero_first_raise_samples):
    print(f"样本 {i+1}:")
    for key, value in sample.items():
        print(f"  {key}: {value}")
    print() 