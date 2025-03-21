import csv
import os
import re

# 检查生成的CSV文件，验证Hero_3B_Chance字段的情况
csv_file_path = 'poker_output/parsed_hands.csv'  # 使用最新生成的文件

if not os.path.exists(csv_file_path):
    print(f"错误：找不到文件 {csv_file_path}")
    exit(1)

print("开始检查文件:", csv_file_path)

# 统计数据
hero_3b_chance_yes_count = 0
hero_3b_chance_no_count = 0
hero_3b_count = 0  # Hero实际3bet的次数

# 收集样本数据
hero_3b_chance_yes_samples = []
hero_3b_samples = []  # Hero实际3bet的样本

# 读取CSV文件
with open(csv_file_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    # 读取数据
    total_rows = 0
    for row in reader:
        total_rows += 1
        
        # 统计Hero_3B_Chance
        if row['Hero_3B_Chance'] == 'YES':
            hero_3b_chance_yes_count += 1
            if len(hero_3b_chance_yes_samples) < 5:
                hero_3b_chance_yes_samples.append({
                    'Hand_ID': row['Hand_ID'],
                    'Hero_Position': row['Hero_Position'],
                    'Hero_3B_Chance': row['Hero_3B_Chance'],
                    'Preflop_Actions': row['Preflop_Actions'][:100] + '...' if len(row['Preflop_Actions']) > 100 else row['Preflop_Actions'],
                    'Preflop_3B': row['Preflop_3B']
                })
        else:
            hero_3b_chance_no_count += 1
        
        # 检查Hero是否实际3bet
        preflop_3b = row['Preflop_3B']
        hero_position = row['Hero_Position']
        
        if preflop_3b and f"Hero({hero_position})" in preflop_3b:
            hero_3b_count += 1
            if len(hero_3b_samples) < 5:
                hero_3b_samples.append({
                    'Hand_ID': row['Hand_ID'],
                    'Hero_Position': row['Hero_Position'],
                    'Hero_3B_Chance': row['Hero_3B_Chance'],
                    'Preflop_Actions': row['Preflop_Actions'][:100] + '...' if len(row['Preflop_Actions']) > 100 else row['Preflop_Actions'],
                    'Preflop_3B': preflop_3b
                })

print("\n" + "="*50)
print("Hero_3B_Chance 统计")
print("="*50)
print(f"总行数: {total_rows}")
print(f"Hero_3B_Chance为YES的行数: {hero_3b_chance_yes_count} ({hero_3b_chance_yes_count/total_rows*100:.2f}%)")
print(f"Hero_3B_Chance为NO的行数: {hero_3b_chance_no_count} ({hero_3b_chance_no_count/total_rows*100:.2f}%)")
print(f"Hero实际3bet的次数: {hero_3b_count}")

if hero_3b_chance_yes_count > 0:
    print(f"Hero有3bet机会时实际3bet的比例: {hero_3b_count/hero_3b_chance_yes_count*100:.2f}%")

print("\n" + "="*50)
print("Hero_3B_Chance为YES的样本")
print("="*50)
for i, sample in enumerate(hero_3b_chance_yes_samples):
    print(f"样本 {i+1}:")
    for key, value in sample.items():
        print(f"  {key}: {value}")
    print()

print("\n" + "="*50)
print("Hero实际3bet的样本")
print("="*50)
for i, sample in enumerate(hero_3b_samples):
    print(f"样本 {i+1}:")
    for key, value in sample.items():
        print(f"  {key}: {value}")
    print() 