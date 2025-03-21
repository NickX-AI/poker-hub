import csv
import os

# 检查最新生成的原始CSV文件
csv_file_path = 'poker_output/parsed_hands.csv'

if not os.path.exists(csv_file_path):
    print(f"错误：找不到文件 {csv_file_path}")
    exit(1)

# 读取CSV文件
with open(csv_file_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    # 获取列名
    fieldnames = reader.fieldnames
    print(f"CSV文件列名：{fieldnames}")
    
    # 找出特定列的索引
    preflop_1st_bet_index = fieldnames.index('Preflop_1st_Bet') if 'Preflop_1st_Bet' in fieldnames else -1
    preflop_3b_index = fieldnames.index('Preflop_3B') if 'Preflop_3B' in fieldnames else -1
    preflop_4b_index = fieldnames.index('Preflop_4B') if 'Preflop_4B' in fieldnames else -1
    preflop_5b_index = fieldnames.index('Preflop_5B') if 'Preflop_5B' in fieldnames else -1
    
    print(f"Preflop_1st_Bet 索引: {preflop_1st_bet_index}")
    print(f"Preflop_3B 索引: {preflop_3b_index}")
    print(f"Preflop_4B 索引: {preflop_4b_index}")
    print(f"Preflop_5B 索引: {preflop_5b_index}")
    
    # 统计各列的数据数量
    count_1st_bet = 0
    count_3b = 0
    count_4b = 0
    count_5b = 0
    
    # 收集样本数据
    samples_3b = []
    
    # 读取数据
    total_rows = 0
    for row in reader:
        total_rows += 1
        
        if row['Preflop_1st_Bet']:
            count_1st_bet += 1
            
        if row['Preflop_3B']:
            count_3b += 1
            if len(samples_3b) < 3:  # 收集3个示例
                samples_3b.append({
                    'Hand_ID': row['Hand_ID'],
                    'Preflop_1st_Bet': row['Preflop_1st_Bet'],
                    'Preflop_3B': row['Preflop_3B'],
                    'Preflop_4B': row['Preflop_4B'],
                    'Hero_3B_Chance': row['Hero_3B_Chance']
                })
                
        if row['Preflop_4B']:
            count_4b += 1
            
        if 'Preflop_5B' in row and row['Preflop_5B']:
            count_5b += 1
    
    # 输出统计结果
    print(f"\n总行数: {total_rows}")
    print(f"包含 Preflop_1st_Bet 的行数: {count_1st_bet}")
    print(f"包含 3B 的行数: {count_3b}")
    print(f"包含 4B 的行数: {count_4b}")
    print(f"包含 5B 的行数: {count_5b}")
    
    # 输出样本数据
    print("\n3B 示例数据:")
    for i, sample in enumerate(samples_3b):
        print(f"样本 {i+1}:")
        for key, value in sample.items():
            print(f"  {key}: {value}")
        print() 