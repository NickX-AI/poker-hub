import csv
import os

def check_hero_position():
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'parsed_hands.csv')
    
    if os.path.exists(csv_path):
        print(f"正在读取文件: {csv_path}")
        try:
            # 统计Hero在各个位置的数量
            position_counts = {}
            bb_with_na_hero_bb = 0
            bb_without_na_hero_bb = 0
            total_count = 0
            
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    total_count += 1
                    
                    # 获取Hero的位置
                    hero_position = row.get('Hero_Position', '')
                    if hero_position:
                        position_counts[hero_position] = position_counts.get(hero_position, 0) + 1
                    
                    # 检查BB位置的Hero是否有NA_hero_BB标记
                    if hero_position == 'BB':
                        hero_open_position = row.get('Hero_Open_Position', '')
                        if hero_open_position == 'NA_hero_BB':
                            bb_with_na_hero_bb += 1
                        else:
                            bb_without_na_hero_bb += 1
                            # 打印几个没有NA_hero_BB标记的BB位置记录
                            if bb_without_na_hero_bb <= 5:
                                print(f"\n没有NA_hero_BB标记的BB位置记录 #{bb_without_na_hero_bb}:")
                                print(f"Hero_Position: {hero_position}")
                                print(f"Hero_Open_Position: {hero_open_position}")
                                print(f"Pool_Preflop_Summary: {row.get('Pool_Preflop_Summary', '')}")
                                print(f"Hero_Preflop_Summary: {row.get('Hero_Preflop_Summary', '')}")
            
            # 输出统计结果
            print(f"\n总记录数: {total_count}")
            print("\nHero在各个位置的数量:")
            for position, count in sorted(position_counts.items()):
                print(f"- {position}: {count} ({count/total_count*100:.2f}%)")
            
            # 输出BB位置的统计
            bb_total = bb_with_na_hero_bb + bb_without_na_hero_bb
            print(f"\nHero在BB位置的总数: {bb_total}")
            print(f"- 有NA_hero_BB标记: {bb_with_na_hero_bb} ({bb_with_na_hero_bb/bb_total*100:.2f}%)")
            print(f"- 没有NA_hero_BB标记: {bb_without_na_hero_bb} ({bb_without_na_hero_bb/bb_total*100:.2f}%)")
            
        except Exception as e:
            print(f"读取CSV文件时出错: {e}")
    else:
        print(f"文件不存在: {csv_path}")

if __name__ == "__main__":
    check_hero_position() 