import csv
import os

# 从带标记的手牌文件中统计各项指标
stats_from_hands = {
    'Total Hands': 0,
    'VPIP': 0,
    'PFR': 0,
    'ATS': 0,
    '3B': 0,
    '4B': 0,
    '5B': 0,
    'Call_3B': 0,
    'Fold_to_3B': 0
}

# 从poker_stats.csv获取的统计数据
stats_from_summary = {}

# 读取带标记的手牌文件
with open('output/parsed_hands_with_stats_new.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        stats_from_hands['Total Hands'] += 1
        
        if row['VPIP'] == 'Yes':
            stats_from_hands['VPIP'] += 1
        
        if row['PFR'] == 'Yes':
            stats_from_hands['PFR'] += 1
        
        if row['ATS'] == 'Yes':
            stats_from_hands['ATS'] += 1
        
        if row['3B'] == 'Yes':
            stats_from_hands['3B'] += 1
        
        if row['4B'] == 'Yes':
            stats_from_hands['4B'] += 1
        
        if row['5B'] == 'Yes':
            stats_from_hands['5B'] += 1
        
        if row['Call_3B'] == 'Yes':
            stats_from_hands['Call_3B'] += 1
        
        if row['Fold_to_3B'] == 'Yes':
            stats_from_hands['Fold_to_3B'] += 1

# 读取poker_stats.csv
with open('output/poker_stats.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) >= 3 and row[0] == 'Hero':
            stat_name = row[1]
            count = row[2]
            try:
                count = int(count)
                stats_from_summary[stat_name] = count
            except ValueError:
                pass

# 打印比较结果
print("统计指标对比:")
print("=" * 50)
print(f"{'指标名称':<15} {'手牌标记统计':<15} {'poker_stats.csv':<15} {'差异':<10}")
print("-" * 50)

# 映射poker_stats.csv中的统计名称到我们使用的名称
stat_name_mapping = {
    'Total Hands': 'Total Hands',
    'VPIP': 'VPIP',
    'PFR': 'PFR',
    'ATS': 'ATS',
    '3B': '3B(all)',
    '4B': '4B',
    '5B': '5B',
    'Call_3B': 'Call 3B(all)',
    'Fold_to_3B': 'Fold to 3B(all)'
}

for our_stat_name, their_stat_name in stat_name_mapping.items():
    our_count = stats_from_hands[our_stat_name]
    their_count = stats_from_summary.get(their_stat_name, "N/A")
    
    if their_count != "N/A":
        diff = our_count - their_count
        print(f"{our_stat_name:<15} {our_count:<15} {their_count:<15} {diff:<10}")
    else:
        print(f"{our_stat_name:<15} {our_count:<15} {'N/A':<15} {'N/A':<10}")

print("\n统计完成！可检查对比结果，确保数据一致性。") 