import csv
import os

def check_limp_action():
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
                # 要检查的手牌ID
                target_hand_ids = ['RC3334557404', 'RC3334601956', 'RC3334370558']
                
                # 首先检查指定的手牌
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get('Hand_ID') in target_hand_ids:
                            print(f"\n手牌ID: {row.get('Hand_ID')}")
                            print(f"Pot_Type: {row.get('Pot_Type', '')}")
                            print(f"Pool_Preflop_Summary: {row.get('Pool_Preflop_Summary', '')}")
                            print(f"Hero_Preflop_Summary: {row.get('Hero_Preflop_Summary', '')}")
                            print(f"Preflop_Actions: {row.get('Preflop_Actions', '')}")
                            print(f"Hero_Position: {row.get('Hero_Position', '')}")
                            print(f"Final_Pot_Type: {row.get('Final_Pot_Type', '')}")
                
                # 统计limped开头的Pool_Preflop_Summary
                limped_summaries = {}
                limped_count = 0
                
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        pool_summary = row.get('Pool_Preflop_Summary', '')
                        if pool_summary.startswith('limped'):
                            limped_count += 1
                            limped_summaries[pool_summary] = limped_summaries.get(pool_summary, 0) + 1
                
                print(f"\n总共有 {limped_count} 条记录的Pool_Preflop_Summary以limped开头")
                print("\n所有limped开头的Pool_Preflop_Summary类型及其数量:")
                for summary, count in sorted(limped_summaries.items()):
                    print(f"- {summary}: {count}")
                
                # 找到一个有效的CSV文件后退出循环
                break
            
            except Exception as e:
                print(f"读取CSV文件时出错: {e}")
        else:
            print(f"文件不存在: {csv_path}")
    else:
        print("所有尝试的路径都不存在")

if __name__ == "__main__":
    check_limp_action() 