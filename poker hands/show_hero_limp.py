import csv

def show_hero_limp_samples():
    """展示hero limp情况的完整样本"""
    csv_file_path = 'parsed_hands.csv'  # 当前目录下的文件
    
    try:
        # 打开CSV文件
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)  # 读取标题行
            
            # 找到相关的列索引
            hero_open_position_index = None
            preflop_actions_index = None
            hero_position_index = None
            preflop_limp_index = None
            
            for i, header in enumerate(headers):
                header_lower = header.lower()
                if 'hero_open_position' in header_lower:
                    hero_open_position_index = i
                elif 'preflop_actions' in header_lower:
                    preflop_actions_index = i
                elif 'hero_position' in header_lower:
                    hero_position_index = i
                elif 'preflop_limp' in header_lower:
                    preflop_limp_index = i
            
            if hero_open_position_index is None:
                print("找不到hero_open_position列")
                return
            
            # 收集no open(limp)样本
            limp_samples = []
            
            for row in reader:
                if hero_open_position_index < len(row) and row[hero_open_position_index] == 'no open(limp)':
                    sample = {'Hero_Open_Position': 'no open(limp)'}
                    
                    if hero_position_index is not None and hero_position_index < len(row):
                        sample['Hero_Position'] = row[hero_position_index]
                    
                    if preflop_actions_index is not None and preflop_actions_index < len(row):
                        sample['Preflop_Actions'] = row[preflop_actions_index]
                    
                    if preflop_limp_index is not None and preflop_limp_index < len(row):
                        sample['Preflop_Limp'] = row[preflop_limp_index]
                    
                    limp_samples.append(sample)
                    
                    # 只收集前5个样本
                    if len(limp_samples) >= 5:
                        break
            
            # 输出样本
            print("\n===== Hero Limp 样本 (hero_open_position = 'no open(limp)') =====")
            print(f"找到 {len(limp_samples)} 个样本")
            
            for i, sample in enumerate(limp_samples):
                print(f"\n样本 {i+1}:")
                for key, value in sample.items():
                    print(f"  {key}: {value}")
    
    except Exception as e:
        print(f"处理CSV文件时出错: {e}")

if __name__ == "__main__":
    show_hero_limp_samples() 