import csv
import os

def check_csv_final():
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'parsed_hands.csv')
    
    if not os.path.exists(csv_path):
        print(f"文件不存在: {csv_path}")
        return
        
    # 统计不同类型的fold
    fold_types = {}
    total_records = 0
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_records += 1
            hero_summary = row.get('Hero_Preflop_Summary', '')
            
            if not hero_summary:
                continue
                
            fold_types[hero_summary] = fold_types.get(hero_summary, 0) + 1
    
    print(f"总共分析了 {total_records} 条记录")
    print("\nHero_Preflop_Summary字段的统计信息:")
    
    # 按数量排序输出
    for summary, count in sorted(fold_types.items(), key=lambda x: x[1], reverse=True):
        print(f"- {summary}: {count}")
        
    # 特别关注fold相关的记录
    print("\n特别关注fold相关的记录:")
    fold_related = ["folds", "folds to open", "fold to 3B", "fold to 4B", "fold to 5B", "limp-fold", "fold to raises", "all folds hero in BB"]
    for fold_type in fold_related:
        print(f"- {fold_type}: {fold_types.get(fold_type, 0)}")

if __name__ == "__main__":
    check_csv_final() 