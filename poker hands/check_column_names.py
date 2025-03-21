import csv

# 打开CSV文件读取头部信息
with open('parsed_hands.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    print("CSV文件列名:")
    for i, column_name in enumerate(header):
        print(f"{i+1}. {column_name}")
    
    # 检查是否存在我们关心的列
    columns_of_interest = ['Pool_Preflop_Summary', 'Hero_Preflop_Summary', 'Flop_Actions']
    print("\n检查特定列是否存在:")
    for col in columns_of_interest:
        if col in header:
            print(f"✓ {col} 在位置 {header.index(col)+1}")
        else:
            print(f"✗ {col} 不存在") 