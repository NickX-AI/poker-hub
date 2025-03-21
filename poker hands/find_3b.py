import csv

def find_3b_data(file_path):
    """查找包含3B数据的行"""
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        
        for row_num, row in enumerate(reader, 1):
            if row['Preflop_3B'] and 'raises' in row['Preflop_3B']:
                print(f"\n==== 找到3B数据, 行 {row_num} ====")
                print(f"Preflop_1st_Bet: {row['Preflop_1st_Bet'][:70]}...")
                print(f"Preflop_3B: {row['Preflop_3B'][:70]}...")
                print(f"Hero_3B_Chance: {row['Hero_3B_Chance']}")
                
                count += 1
                if count >= 3:  # 只显示前3条
                    break
                    
        print(f"\n总共找到 {count} 条包含3B数据的记录")

# 检查修复后的CSV文件
print("修复后的CSV文件中的3B数据:")
find_3b_data('poker_output_fixed/parsed_hands_fixed.csv') 