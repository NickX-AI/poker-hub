import csv
import os

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_paths = [
    os.path.join(current_dir, 'parsed_hands.csv'),
    os.path.join(current_dir, 'poker_output', 'parsed_hands.csv')
]

for csv_path in csv_paths:
    if os.path.exists(csv_path):
        print(f"正在读取文件: {csv_path}")
        try:
            # 打开CSV文件
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
                # 检查同时包含Pool_Preflop_Summary和Hero_Preflop_Summary信息的数据
                count_both = 0
                for row in rows:
                    if row['Pool_Preflop_Summary'] and row['Hero_Preflop_Summary']:
                        count_both += 1
                
                print(f'总共有 {count_both} 条数据同时包含Pool_Preflop_Summary和Hero_Preflop_Summary信息')
                
                # 检查只包含Pool_Preflop_Summary信息的数据
                count_pool_only = 0
                for row in rows:
                    if row['Pool_Preflop_Summary'] and not row['Hero_Preflop_Summary']:
                        count_pool_only += 1
                
                print(f'总共有 {count_pool_only} 条数据只包含Pool_Preflop_Summary信息')
                
                # 检查只包含Hero_Preflop_Summary信息的数据
                count_hero_only = 0
                for row in rows:
                    if not row['Pool_Preflop_Summary'] and row['Hero_Preflop_Summary']:
                        count_hero_only += 1
                
                print(f'总共有 {count_hero_only} 条数据只包含Hero_Preflop_Summary信息')
                
                # 检查不包含任何信息的数据
                count_none = 0
                for row in rows:
                    if not row['Pool_Preflop_Summary'] and not row['Hero_Preflop_Summary']:
                        count_none += 1
                
                print(f'总共有 {count_none} 条数据不包含任何信息')
                
                # 检查总数
                print(f'总共有 {len(rows)} 条数据')
                print(f'总和: {count_both + count_pool_only + count_hero_only + count_none}')
                
                # 找到一个有效的CSV文件后退出循环
                break
        except Exception as e:
            print(f"读取CSV文件时出错: {e}")
    else:
        print(f"文件不存在: {csv_path}")
else:
    print("所有尝试的路径都不存在") 