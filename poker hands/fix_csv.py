import csv
import os

def fix_csv_data_shift(input_file, output_file):
    """修复CSV文件中的数据位移问题"""
    print(f"正在修复文件: {input_file}")
    
    # 读取原始CSV数据
    rows = []
    headers = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)  # 获取列标题
        
        # 查找关键字段的索引
        preflop_1st_bet_index = headers.index('Preflop_1st_Bet') if 'Preflop_1st_Bet' in headers else -1
        preflop_3b_index = headers.index('Preflop_3B') if 'Preflop_3B' in headers else -1
        preflop_4b_index = headers.index('Preflop_4B') if 'Preflop_4B' in headers else -1
        preflop_5b_index = headers.index('Preflop_5B') if 'Preflop_5B' in headers else -1
        
        print(f"字段索引: 1st_bet={preflop_1st_bet_index}, 3B={preflop_3b_index}, 4B={preflop_4b_index}, 5B={preflop_5b_index}")
        
        # 读取所有数据行
        for row in reader:
            rows.append(row)
    
    # 修复数据位移
    fixed_rows = []
    for row in rows:
        fixed_row = row.copy()
        
        # 将Preflop_3B的数据移到Preflop_1st_Bet
        if preflop_1st_bet_index >= 0 and preflop_3b_index >= 0:
            fixed_row[preflop_1st_bet_index] = row[preflop_3b_index]
        
        # 将Preflop_4B的数据移到Preflop_3B
        if preflop_3b_index >= 0 and preflop_4b_index >= 0:
            fixed_row[preflop_3b_index] = row[preflop_4b_index]
            
        # 将Preflop_5B的数据移到Preflop_4B
        if preflop_4b_index >= 0 and preflop_5b_index >= 0:
            fixed_row[preflop_4b_index] = row[preflop_5b_index]
            
        # 清空Preflop_5B
        if preflop_5b_index >= 0:
            fixed_row[preflop_5b_index] = ""
            
        fixed_rows.append(fixed_row)
    
    # 写入修复后的数据
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)  # 写入列标题
        writer.writerows(fixed_rows)  # 写入修复后的数据
        
    print(f"修复完成，已保存到: {output_file}")
    print(f"修复了 {len(fixed_rows)} 行数据")

# 创建输出目录
output_dir = 'poker_output_fixed'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 修复CSV文件
fix_csv_data_shift('poker_output/parsed_hands.csv', f'{output_dir}/parsed_hands_fixed.csv') 