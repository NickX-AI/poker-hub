import csv
import os
import sys

def check_hero_open_position(csv_file_path=None):
    """检查生成的CSV文件中hero_open_position字段的统计情况"""
    # 如果没有指定CSV文件路径，则使用默认路径
    if not csv_file_path:
        # 查找CSV文件
        csv_file_paths = [
            'poker_output/parsed_hands.csv',  # 默认路径
            'parsed_hands.csv',               # 当前目录
        ]
        
        for path in csv_file_paths:
            if os.path.exists(path):
                csv_file_path = path
                break
    else:
        # 使用指定的CSV文件路径
        if not os.path.exists(csv_file_path):
            print(f"错误：找不到指定的CSV文件 {csv_file_path}")
            return
    
    if not csv_file_path:
        print("错误：找不到CSV文件")
        return
    
    print(f"开始检查文件: {csv_file_path}")
    
    # 统计数据
    hero_open_position_counts = {}
    samples = {}
    
    try:
        # 读取CSV文件
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # 获取字段名，兼容大小写
            fieldnames = reader.fieldnames
            if not fieldnames:
                print("错误：CSV文件没有字段名")
                return
                
            print(f"CSV字段名: {fieldnames}")
            
            hero_open_position_field = None
            preflop_actions_field = None
            hero_position_field = None
            preflop_limp_field = None
            
            for field in fieldnames:
                if field.lower() == 'hero_open_position':
                    hero_open_position_field = field
                if field.lower() == 'preflop_actions':
                    preflop_actions_field = field
                if field.lower() == 'hero_position':
                    hero_position_field = field
                if field.lower() == 'preflop_limp':
                    preflop_limp_field = field
            
            if not hero_open_position_field:
                print("错误：找不到Hero_Open_Position字段")
                return
            
            # 读取数据
            total_rows = 0
            for row in reader:
                total_rows += 1
                
                # 统计Hero_Open_Position
                open_position = row.get(hero_open_position_field, '')
                if not open_position:
                    open_position = '空'
                    
                if open_position in hero_open_position_counts:
                    hero_open_position_counts[open_position] += 1
                else:
                    hero_open_position_counts[open_position] = 1
                    samples[open_position] = []
                
                # 收集有limp的样本
                preflop_limp = row.get(preflop_limp_field, '')
                if preflop_limp and len(samples.get('no open(limp)', [])) < 5:
                    preflop_actions = row.get(preflop_actions_field, 'N/A')
                    hero_position = row.get(hero_position_field, 'N/A')
                    
                    if 'calls' in preflop_actions and f"Hero({hero_position})" in preflop_actions:
                        samples.setdefault('no open(limp)', []).append({
                            'Hero_Position': hero_position,
                            'Hero_Open_Position': open_position,
                            'Preflop_Actions': preflop_actions[:100] + '...' if len(preflop_actions) > 100 else preflop_actions,
                            'Preflop_Limp': preflop_limp
                        })
                
                # 收集其他样本
                if open_position != '空' and len(samples.get(open_position, [])) < 2:
                    preflop_actions = row.get(preflop_actions_field, 'N/A')
                    hero_position = row.get(hero_position_field, 'N/A')
                    
                    samples.setdefault(open_position, []).append({
                        'Hero_Position': hero_position,
                        'Hero_Open_Position': open_position,
                        'Preflop_Actions': preflop_actions[:100] + '...' if len(preflop_actions) > 100 else preflop_actions
                    })
        
        # 输出统计结果
        print("\n" + "="*50)
        print("Hero_Open_Position 统计")
        print("="*50)
        print(f"总行数: {total_rows}")
        
        # 按数量排序
        sorted_counts = sorted(hero_open_position_counts.items(), key=lambda x: x[1], reverse=True)
        for position, count in sorted_counts:
            print(f"{position}: {count} ({count/total_rows*100:.2f}%)")
        
        # 检查有没有no open(limp)类型
        has_limp = 'no open(limp)' in hero_open_position_counts
        print(f"\nHero Limp (`no open(limp)`) 存在: {has_limp}")
        if has_limp:
            print(f"Hero Limp (`no open(limp)`) 数量: {hero_open_position_counts.get('no open(limp)', 0)}")
        
        # 检查有limp动作的样本
        if 'no open(limp)' in samples:
            print("\n" + "="*50)
            print("可能的Hero Limp样本 (根据Preflop_Limp字段)")
            print("="*50)
            for i, sample in enumerate(samples['no open(limp)']):
                print(f"样本 {i+1}:")
                for key, value in sample.items():
                    print(f"  {key}: {value}")
                print()
        
        # 输出其他类型的样本
        important_positions = ['fold', 'NA', 'BB', 'SB', 'BTN', 'CO', 'MP', 'UTG']
        for position in important_positions:
            if position in samples and samples[position]:
                print("\n" + "="*50)
                print(f"Hero_Open_Position 为 {position} 的样本")
                print("="*50)
                for i, sample in enumerate(samples[position]):
                    print(f"样本 {i+1}:")
                    for key, value in sample.items():
                        print(f"  {key}: {value}")
                    print()
    
    except Exception as e:
        print(f"处理CSV文件时出错: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_hero_open_position(sys.argv[1])
    else:
        check_hero_open_position() 