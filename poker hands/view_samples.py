import csv
import os

# 查看不同Hero_3B_Chance状态的样本
csv_file_path = 'poker_output/parsed_hands_new_format.csv'  # 使用新格式的CSV文件

if not os.path.exists(csv_file_path):
    print(f"错误：找不到文件 {csv_file_path}")
    exit(1)

# 收集样本数据
samples = {
    'NO': [],
    'Yes-3B': [],
    'Yes-Calls': [],
    'Yes-folds': []
}

# 读取CSV文件
with open(csv_file_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    # 读取数据
    for row in reader:
        # 收集样本
        hero_3b_chance = row['hero_3b_chance']
        if hero_3b_chance in samples and len(samples[hero_3b_chance]) < 3:
            samples[hero_3b_chance].append({
                'Hand_ID': row['hand_id'],
                'Hero_Position': row['hero_position'],
                'Hero_3B_Chance': hero_3b_chance,
                'Preflop_Actions': row['preflop_actions'][:100] + '...' if len(row['preflop_actions']) > 100 else row['preflop_actions'],
                'Preflop_3B': row['preflop_action_3B']
            })
        
        # 如果已经收集了所有状态的样本，就退出
        if all(len(sample_list) >= 3 for sample_list in samples.values()):
            break

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