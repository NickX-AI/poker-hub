import csv
import os

# 检查生成的CSV文件，统计Hero_3B_Chance字段的不同状态
csv_file_path = 'poker_output/parsed_hands.csv'  # 使用最新生成的文件

if not os.path.exists(csv_file_path):
    print(f"错误：找不到文件 {csv_file_path}")
    exit(1)

print("开始检查文件:", csv_file_path)

# 统计数据
hero_3b_chance_counts = {
    'NO': 0,
    'Yes-3B': 0,
    'Yes-Calls': 0,
    'Yes-folds': 0,
    'YES': 0,  # 可能仍然有部分老的YES格式
    'Other': 0
}

# 收集样本数据
samples = {
    'NO': [],
    'Yes-3B': [],
    'Yes-Calls': [],
    'Yes-folds': [],
    'YES': []
}

# 读取CSV文件
with open(csv_file_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    # 读取数据
    total_rows = 0
    for row in reader:
        total_rows += 1
        
        # 统计Hero_3B_Chance
        hero_3b_chance = row['Hero_3B_Chance']
        if hero_3b_chance in hero_3b_chance_counts:
            hero_3b_chance_counts[hero_3b_chance] += 1
            # 收集样本
            if len(samples[hero_3b_chance]) < 3:
                samples[hero_3b_chance].append({
                    'Hand_ID': row['Hand_ID'],
                    'Hero_Position': row['Hero_Position'],
                    'Hero_3B_Chance': hero_3b_chance,
                    'Preflop_Actions': row['Preflop_Actions'][:100] + '...' if len(row['Preflop_Actions']) > 100 else row['Preflop_Actions'],
                    'Preflop_3B': row['Preflop_3B']
                })
        else:
            hero_3b_chance_counts['Other'] += 1

print("\n" + "="*50)
print("Hero_3B_Chance 统计")
print("="*50)
print(f"总行数: {total_rows}")
for status, count in hero_3b_chance_counts.items():
    if count > 0:
        print(f"{status}: {count} ({count/total_rows*100:.2f}%)")

# 计算有3B机会的总行数（Yes-3B + Yes-Calls + Yes-folds + YES）
yes_total = hero_3b_chance_counts['Yes-3B'] + hero_3b_chance_counts['Yes-Calls'] + hero_3b_chance_counts['Yes-folds'] + hero_3b_chance_counts['YES']
print(f"\n有3B机会的总行数: {yes_total} ({yes_total/total_rows*100:.2f}%)")
if yes_total > 0:
    print(f"在有3B机会中，选择3B的比例: {hero_3b_chance_counts['Yes-3B']/yes_total*100:.2f}%")
    print(f"在有3B机会中，选择Calls的比例: {hero_3b_chance_counts['Yes-Calls']/yes_total*100:.2f}%")
    print(f"在有3B机会中，选择folds的比例: {hero_3b_chance_counts['Yes-folds']/yes_total*100:.2f}%")
    if hero_3b_chance_counts['YES'] > 0:
        print(f"在有3B机会中，仍标记为YES的比例: {hero_3b_chance_counts['YES']/yes_total*100:.2f}%")

# 输出样本
for status, sample_list in samples.items():
    if sample_list:
        print("\n" + "="*50)
        print(f"Hero_3B_Chance 为 {status} 的样本")
        print("="*50)
        for i, sample in enumerate(sample_list):
            print(f"样本 {i+1}:")
            for key, value in sample.items():
                print(f"  {key}: {value}")
            print() 