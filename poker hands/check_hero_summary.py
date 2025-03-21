import csv
from collections import Counter

# 打开CSV文件分析Hero_Preflop_Summary内容
with open('parsed_hands.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    # 初始化计数器
    total_records = 0
    records_with_value = 0
    unique_values = set()
    value_counter = Counter()
    
    # 遍历每一行
    for row in reader:
        total_records += 1
        hero_summary = row.get('Hero_Preflop_Summary', '')
        
        if hero_summary and hero_summary.strip():
            records_with_value += 1
            unique_values.add(hero_summary)
            value_counter[hero_summary] += 1
    
    # 输出统计信息
    print(f"总记录数: {total_records}")
    print(f"含有Hero_Preflop_Summary值的记录数: {records_with_value}")
    print(f"占比: {records_with_value/total_records*100:.2f}%")
    print(f"唯一值数量: {len(unique_values)}")
    
    # 输出最常见的值
    print("\n最常见的Hero_Preflop_Summary值:")
    for value, count in value_counter.most_common(10):
        print(f"{value}: {count}次")
    
    # 输出示例值
    print("\n示例值:")
    samples = list(unique_values)[:10]
    for i, sample in enumerate(samples, 1):
        print(f"{i}. {sample}") 