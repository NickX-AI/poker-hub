import csv

def check_csv_headers(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        print("CSV文件列标题顺序:")
        for i, header in enumerate(headers):
            print(f"{i+1}. {header}")
        
        # 检查特定字段的顺序
        preflop_1st_bet_index = headers.index('Preflop_1st_Bet') if 'Preflop_1st_Bet' in headers else -1
        preflop_3b_index = headers.index('Preflop_3B') if 'Preflop_3B' in headers else -1
        preflop_4b_index = headers.index('Preflop_4B') if 'Preflop_4B' in headers else -1
        preflop_5b_index = headers.index('Preflop_5B') if 'Preflop_5B' in headers else -1
        
        print(f"\n字段索引:")
        print(f"Preflop_1st_Bet 索引: {preflop_1st_bet_index}")
        print(f"Preflop_3B 索引: {preflop_3b_index}")
        print(f"Preflop_4B 索引: {preflop_4b_index}")
        print(f"Preflop_5B 索引: {preflop_5b_index}")
        
        # 读取第一行数据
        first_row = next(reader)
        print("\n第一行数据:")
        for i, (header, value) in enumerate(zip(headers, first_row)):
            if header in ['Preflop_1st_Bet', 'Preflop_3B', 'Preflop_4B', 'Preflop_5B']:
                print(f"{header}: {value}")

# 检查CSV文件
check_csv_headers('poker_output/parsed_hands.csv') 