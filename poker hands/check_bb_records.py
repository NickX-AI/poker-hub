import csv
import os

def check_bb_records():
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'parsed_hands.csv')
    
    if os.path.exists(csv_path):
        print(f"正在读取文件: {csv_path}")
        try:
            # 找出所有Hero在BB位置但没有NA_hero_BB标记的记录
            bb_records = []
            
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # 获取Hero的位置
                    hero_position = row.get('Hero_Position', '')
                    hero_open_position = row.get('Hero_Open_Position', '')
                    
                    # 检查BB位置的Hero是否有NA_hero_BB标记
                    if hero_position == 'BB' and hero_open_position != 'NA_hero_BB':
                        bb_records.append(row)
            
            # 输出这些记录的详细信息
            print(f"\n找到 {len(bb_records)} 条Hero在BB位置但没有NA_hero_BB标记的记录:")
            for i, record in enumerate(bb_records):
                print(f"\n记录 #{i+1}:")
                print(f"Hand_ID: {record.get('Hand_ID', '')}")
                print(f"Hero_Position: {record.get('Hero_Position', '')}")
                print(f"Hero_Open_Position: {record.get('Hero_Open_Position', '')}")
                print(f"Pool_Preflop_Summary: {record.get('Pool_Preflop_Summary', '')}")
                print(f"Hero_Preflop_Summary: {record.get('Hero_Preflop_Summary', '')}")
                print(f"Preflop_Actions: {record.get('Preflop_Actions', '')}")
                print(f"Preflop_1st_Bet: {record.get('Preflop_1st_Bet', '')}")
                print(f"Pot_Type: {record.get('Pot_Type', '')}")
            
        except Exception as e:
            print(f"读取CSV文件时出错: {e}")
    else:
        print(f"文件不存在: {csv_path}")

if __name__ == "__main__":
    check_bb_records() 