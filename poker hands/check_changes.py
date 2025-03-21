import csv
import os

# 检查生成的CSV文件，验证Cash_Drop和Hero_Open_Position的修改
csv_file_path = 'parsed_hands.csv'  # 使用最新生成的文件

if not os.path.exists(csv_file_path):
    print(f"错误：找不到文件 {csv_file_path}")
    exit(1)

# 统计数据
cash_drop_yes_count = 0
cash_drop_no_count = 0
hero_open_position_counts = {}

# 收集样本数据
cash_drop_yes_samples = []
cash_drop_no_samples = []
hero_open_position_samples = {}

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
            if len(cash_drop_no_samples) < 3:
                cash_drop_no_samples.append({
                    'Hand_ID': row['Hand_ID'],
                    'Cash_Drop': row['Cash_Drop'],
                    'Preflop_Pot': row['Preflop_Pot']
                })
        
        # 统计Hero_Open_Position
        hero_open_position = row['Hero_Open_Position']
        if hero_open_position not in hero_open_position_counts:
            hero_open_position_counts[hero_open_position] = 0
        hero_open_position_counts[hero_open_position] += 1
        
        # 收集Hero_Open_Position样本
        if hero_open_position not in hero_open_position_samples:
            hero_open_position_samples[hero_open_position] = []
        
        if len(hero_open_position_samples[hero_open_position]) < 2:
            hero_open_position_samples[hero_open_position].append({
                'Hand_ID': row['Hand_ID'],
                'Hero_Open_Position': row['Hero_Open_Position'],
                'Hero_Position': row['Hero_Position'],
                'Preflop_Actions': row['Preflop_Actions'][:100] + '...' if len(row['Preflop_Actions']) > 100 else row['Preflop_Actions']
            })

# 输出统计结果
print("\n=== Cash_Drop 统计 ===")
print(f"总行数: {total_rows}")
print(f"Cash_Drop为YES的行数: {cash_drop_yes_count} ({cash_drop_yes_count/total_rows*100:.2f}%)")
print(f"Cash_Drop为NO的行数: {cash_drop_no_count} ({cash_drop_no_count/total_rows*100:.2f}%)")

print("\n=== Cash_Drop为YES的示例 ===")
for i, sample in enumerate(cash_drop_yes_samples):
    print(f"样本 {i+1}:")
    for key, value in sample.items():
        print(f"  {key}: {value}")
    print()

print("\n=== Cash_Drop为NO的示例 ===")
for i, sample in enumerate(cash_drop_no_samples):
    print(f"样本 {i+1}:")
    for key, value in sample.items():
        print(f"  {key}: {value}")
    print()

print("\n=== Hero_Open_Position 统计 ===")
for position, count in sorted(hero_open_position_counts.items()):
    print(f"{position}: {count} ({count/total_rows*100:.2f}%)")

print("\n=== Hero_Open_Position 样本 ===")
for position, samples in sorted(hero_open_position_samples.items()):
    print(f"\n== {position} 示例 ==")
    for i, sample in enumerate(samples):
        print(f"样本 {i+1}:")
        for key, value in sample.items():
            print(f"  {key}: {value}")
        print() 