import csv
import os

def check_fields():
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
                # 检查Pool_Preflop_Summary字段
                pool_summaries = set()
                pool_count = 0
                total_count = 0
                
                # 检查Hero_Open_Position字段
                hero_open_positions = set()
                hero_bb_count = 0
                
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        total_count += 1
                        
                        # 检查Pool_Preflop_Summary
                        if row['Pool_Preflop_Summary'] and row['Pool_Preflop_Summary'].strip():
                            pool_summaries.add(row['Pool_Preflop_Summary'])
                            pool_count += 1
                        
                        # 检查Hero_Open_Position
                        if row['Hero_Open_Position'] and row['Hero_Open_Position'].strip():
                            hero_open_positions.add(row['Hero_Open_Position'])
                            if row['Hero_Open_Position'] == 'NA_hero_BB':
                                hero_bb_count += 1
                
                # 输出Pool_Preflop_Summary统计
                print(f'总共有 {pool_count} 条记录包含 Pool_Preflop_Summary 值 (占比: {pool_count/total_count*100:.2f}%)')
                print('不同的 Pool_Preflop_Summary 值 (前20个)：')
                for summary in sorted(list(pool_summaries))[:20]:
                    print(f'- {summary}')
                
                # 输出Hero_Open_Position统计
                print(f'\n总共有 {hero_bb_count} 条记录的 Hero_Open_Position 值为 NA_hero_BB')
                print('不同的 Hero_Open_Position 值：')
                for position in sorted(hero_open_positions):
                    print(f'- {position}')
                
                # 找到一个有效的CSV文件后退出循环
                break
            except Exception as e:
                print(f"读取CSV文件时出错: {e}")
        else:
            print(f"文件不存在: {csv_path}")
    else:
        print("所有尝试的路径都不存在")

if __name__ == "__main__":
    check_fields() 