import csv

def simple_check():
    """简单检查CSV文件中的limp情况"""
    csv_file_path = 'parsed_hands.csv'  # 当前目录下的文件
    
    try:
        # 打开CSV文件
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)  # 读取标题行
            
            # 找到hero_open_position列索引
            hero_open_position_index = None
            preflop_actions_index = None
            preflop_limp_index = None
            
            for i, header in enumerate(headers):
                header_lower = header.lower()
                if 'hero_open_position' in header_lower:
                    hero_open_position_index = i
                elif 'preflop_actions' in header_lower:
                    preflop_actions_index = i
                elif 'preflop_limp' in header_lower:
                    preflop_limp_index = i
            
            if hero_open_position_index is None:
                print("找不到hero_open_position列")
                return
            
            # 统计hero_open_position的值
            position_counts = {}
            limp_samples = []
            
            for row in reader:
                if hero_open_position_index < len(row):
                    position = row[hero_open_position_index]
                    
                    # 统计
                    if position in position_counts:
                        position_counts[position] += 1
                    else:
                        position_counts[position] = 1
                    
                    # 查找limp样本
                    if position == 'no open(limp)':
                        sample = {
                            'Hero_Open_Position': position
                        }
                        if preflop_actions_index is not None and preflop_actions_index < len(row):
                            sample['Preflop_Actions'] = row[preflop_actions_index]
                        if preflop_limp_index is not None and preflop_limp_index < len(row):
                            sample['Preflop_Limp'] = row[preflop_limp_index]
                        limp_samples.append(sample)
                    
                    # 如果有preflop_limp字段且不为空，也收集样本
                    elif preflop_limp_index is not None and preflop_limp_index < len(row) and row[preflop_limp_index]:
                        sample = {
                            'Hero_Open_Position': position,
                            'Preflop_Limp': row[preflop_limp_index]
                        }
                        if preflop_actions_index is not None and preflop_actions_index < len(row):
                            sample['Preflop_Actions'] = row[preflop_actions_index]
                        limp_samples.append(sample)
            
            # 输出统计结果
            print("\n===== Hero_Open_Position 统计 =====")
            total = sum(position_counts.values())
            print(f"总行数: {total}")
            
            # 排序后输出
            sorted_counts = sorted(position_counts.items(), key=lambda x: x[1], reverse=True)
            for position, count in sorted_counts:
                print(f"{position}: {count} ({count/total*100:.2f}%)")
            
            # 检查no open(limp)
            has_limp = 'no open(limp)' in position_counts
            print(f"\nHero Limp (`no open(limp)`) 存在: {has_limp}")
            if has_limp:
                print(f"Hero Limp (`no open(limp)`) 数量: {position_counts['no open(limp)']}")
            
            # 输出limp样本
            if limp_samples:
                print("\n===== Hero Limp 样本 =====")
                for i, sample in enumerate(limp_samples[:5]):  # 只显示前5个
                    print(f"样本 {i+1}:")
                    for key, value in sample.items():
                        print(f"  {key}: {value}")
                    print()
            else:
                print("\n没有找到Hero Limp样本")
    
    except Exception as e:
        print(f"处理CSV文件时出错: {e}")

if __name__ == "__main__":
    simple_check() 