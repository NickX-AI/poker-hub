import csv
import os

def check_specific_records():
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
                target_hand_ids = ['RC3334603565', 'RC3334600370', 'RC3334601029']
                
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
                
                # 另外统计一下所有的Pot_Type和Pool_Preflop_Summary类型
                pot_types = {}
                pool_summaries = {}
                
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        pot_type = row.get('Pot_Type', '')
                        pot_types[pot_type] = pot_types.get(pot_type, 0) + 1
                        
                        pool_summary = row.get('Pool_Preflop_Summary', '')
                        pool_summaries[pool_summary] = pool_summaries.get(pool_summary, 0) + 1
                
                print("\n所有Pot_Type类型及其数量:")
                for pot_type, count in sorted(pot_types.items()):
                    print(f"- {pot_type}: {count}")
                
                print("\n所有Pool_Preflop_Summary类型（前20个）及其数量:")
                for i, (summary, count) in enumerate(sorted(pool_summaries.items())):
                    if i >= 20:
                        break
                    print(f"- {summary}: {count}")
                
                # 检查所有Hero_Preflop_Summary为空的记录
                empty_hero_summary_count = 0
                hero_bb_empty_summary_count = 0
                
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        hero_summary = row.get('Hero_Preflop_Summary', '')
                        if not hero_summary or hero_summary.isspace():
                            empty_hero_summary_count += 1
                            if row.get('Hero_Position') == 'BB':
                                hero_bb_empty_summary_count += 1
                                if hero_bb_empty_summary_count <= 5:
                                    print(f"\n空的Hero_Preflop_Summary记录 #{hero_bb_empty_summary_count}:")
                                    print(f"Hand_ID: {row.get('Hand_ID', '')}")
                                    print(f"Hero_Position: {row.get('Hero_Position', '')}")
                                    print(f"Pool_Preflop_Summary: {row.get('Pool_Preflop_Summary', '')}")
                                    print(f"Preflop_Actions: {row.get('Preflop_Actions', '')}")
                
                print(f"\n空的Hero_Preflop_Summary记录总数: {empty_hero_summary_count}")
                print(f"其中Hero在BB位置的记录数: {hero_bb_empty_summary_count}")
                
                # 找到一个有效的CSV文件后退出循环
                break
            
            except Exception as e:
                print(f"读取CSV文件时出错: {e}")
        else:
            print(f"文件不存在: {csv_path}")
    else:
        print("所有尝试的路径都不存在")

if __name__ == "__main__":
    check_specific_records() 