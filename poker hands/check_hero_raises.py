import csv
import os

# 检查生成的CSV文件，专门查找Hero raises的情况
csv_file_path = 'parsed_hands.csv'  # 使用最新生成的文件

if not os.path.exists(csv_file_path):
    print(f"错误：找不到文件 {csv_file_path}")
    exit(1)

# 统计数据
hero_raises_count = 0
hero_raises_samples = []

# 读取CSV文件
with open(csv_file_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    # 读取数据
    total_rows = 0
    for row in reader:
        total_rows += 1
        
        # 查找Hero raises的情况
        preflop_actions = row['Preflop_Actions']
        hero_position = row['Hero_Position']
        
        # 检查是否包含"Hero(位置): raises"
        if f"Hero({hero_position}): raises" in preflop_actions:
            hero_raises_count += 1
            
            if len(hero_raises_samples) < 5:
                hero_raises_samples.append({
                    'Hand_ID': row['Hand_ID'],
                    'Hero_Position': row['Hero_Position'],
                    'Hero_Open_Position': row['Hero_Open_Position'],
                    'Preflop_Actions': preflop_actions[:100] + '...' if len(preflop_actions) > 100 else preflop_actions
                })

# 输出统计结果
print(f"总行数: {total_rows}")
print(f"Hero raises的行数: {hero_raises_count} ({hero_raises_count/total_rows*100:.2f}%)")

print("\n=== Hero raises 样本 ===")
for i, sample in enumerate(hero_raises_samples):
    print(f"样本 {i+1}:")
    for key, value in sample.items():
        print(f"  {key}: {value}")
    print() 