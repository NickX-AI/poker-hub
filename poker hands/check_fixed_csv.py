import csv

def check_csv_data(file_path):
    """检查修复后的CSV文件数据是否正确"""
    print(f"检查文件: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # 分析前5行数据
        for i, row in enumerate(reader):
            if i >= 5:  # 只检查前5条数据
                break
            
            print(f"\n==== 第 {i+1} 行数据 ====")
            print(f"Preflop_1st_Bet: {row['Preflop_1st_Bet']}")
            print(f"Preflop_3B: {row['Preflop_3B']}")
            print(f"Preflop_4B: {row['Preflop_4B']}")
            print(f"Preflop_5B: {row['Preflop_5B']}")
            
            # 检查内容合理性
            if 'raises' in row['Preflop_1st_Bet']:
                print("✓ Preflop_1st_Bet字段包含加注内容，看起来是正确的")
            
            # 输出Hero_3B_Chance用于参考
            print(f"Hero_3B_Chance: {row['Hero_3B_Chance']}")

# 检查原始CSV文件
print("原始CSV文件:")
check_csv_data('poker_output/parsed_hands.csv')

# 检查修复后的CSV文件
print("\n\n修复后的CSV文件:")
check_csv_data('poker_output_fixed/parsed_hands_fixed.csv') 