import csv
import os

def check_fold_actions():
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_paths = [
        os.path.join(current_dir, 'poker_output', 'parsed_hands.csv'),
        os.path.join(current_dir, 'parsed_hands.csv')
    ]
    
    for csv_path in csv_paths:
        if os.path.exists(csv_path):
            print(f"正在读取文件: {csv_path}")
            try:
                # 统计fold相关记录
                fold_counts = {
                    'folds': 0,
                    'folds to open': 0,
                    'fold to 3B': 0,
                    'fold to 4B': 0,
                    'fold to 5B': 0,
                    'limp-fold': 0,
                    'other_fold_types': {}
                }
                
                total_hands = 0
                
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        total_hands += 1
                        hero_summary = row.get('Hero_Preflop_Summary', '')
                        
                        if not hero_summary:
                            continue
                            
                        if hero_summary == 'folds':
                            fold_counts['folds'] += 1
                        elif hero_summary == 'folds to open':
                            fold_counts['folds to open'] += 1
                        elif hero_summary == 'fold to 3B':
                            fold_counts['fold to 3B'] += 1
                        elif hero_summary == 'fold to 4B':
                            fold_counts['fold to 4B'] += 1
                        elif hero_summary == 'fold to 5B':
                            fold_counts['fold to 5B'] += 1
                        elif hero_summary == 'limp-fold':
                            fold_counts['limp-fold'] += 1
                        elif 'fold' in hero_summary.lower():
                            fold_counts['other_fold_types'][hero_summary] = fold_counts['other_fold_types'].get(hero_summary, 0) + 1
                
                print(f"\n总共分析了 {total_hands} 条记录")
                print("\nHero_Preflop_Summary中fold相关的记录统计:")
                print(f"- folds: {fold_counts['folds']}")
                print(f"- folds to open: {fold_counts['folds to open']}")
                print(f"- fold to 3B: {fold_counts['fold to 3B']}")
                print(f"- fold to 4B: {fold_counts['fold to 4B']}")
                print(f"- fold to 5B: {fold_counts['fold to 5B']}")
                print(f"- limp-fold: {fold_counts['limp-fold']}")
                
                if fold_counts['other_fold_types']:
                    print("\n其他包含fold的类型:")
                    for fold_type, count in sorted(fold_counts['other_fold_types'].items()):
                        print(f"- {fold_type}: {count}")
                
                # 找到一个有效的CSV文件后退出循环
                break
            
            except Exception as e:
                print(f"读取CSV文件时出错: {e}")
        else:
            print(f"文件不存在: {csv_path}")
    else:
        print("所有尝试的路径都不存在")

if __name__ == "__main__":
    check_fold_actions() 