import os
import csv
from poker_hand_parser import PokerHandParser

def process_hands_with_new_format():
    """处理所有手牌并确保使用新的Hero_3B_Chance状态格式"""
    input_file = 'poker_input/combined_1.txt'
    output_file = 'poker_output/parsed_hands_new_format.csv'
    
    if not os.path.exists(input_file):
        print(f"错误：找不到输入文件 {input_file}")
        return
    
    print(f"开始处理手牌文件: {input_file}")
    
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 分割为单独的手牌
    hands = content.split('\n\n\n')
    total_hands = len(hands)
    print(f"总共找到 {total_hands} 个手牌")
    
    # 统计数据
    hero_3b_chance_counts = {
        'NO': 0,
        'Yes-3B': 0,
        'Yes-Calls': 0,
        'Yes-folds': 0,
        'YES': 0,  # 可能仍然有部分老的YES格式
        'Other': 0
    }
    
    # 翻前行动字段统计
    preflop_action_stats = {
        'has_first_bet': 0,
        'has_3b': 0
    }
    
    # 处理手牌
    processed_hands = []
    for i, hand_text in enumerate(hands):
        if i % 500 == 0:
            print(f"处理进度: {i}/{total_hands} ({i/total_hands*100:.1f}%)")
            
        if not hand_text.strip():
            continue
            
        parser = PokerHandParser()
        hand_data = parser.parse_hand(hand_text)
        
        # 确保使用新的Hero_3B_Chance状态格式
        if hand_data['hero_3b_chance'] == 'YES':
            # 如果是旧的YES格式，根据preflop_actions判断真实状态
            preflop_actions = hand_data['preflop_actions']
            hero_position = hand_data['hero_position']
            
            if hero_position and 'raises' in preflop_actions and f"Hero({hero_position})" in preflop_actions:
                # 检查Hero是否在有人raise后又raise了（3bet）
                first_raise_index = preflop_actions.find('raises')
                # 找到Hero raise的位置
                hero_raise_index = preflop_actions.find(f"Hero({hero_position}): raises")
                
                if hero_raise_index > first_raise_index and hero_raise_index != -1:
                    hand_data['hero_3b_chance'] = 'Yes-3B'
                elif f"Hero({hero_position}): calls" in preflop_actions:
                    hand_data['hero_3b_chance'] = 'Yes-Calls'
                elif f"Hero({hero_position}): folds" in preflop_actions:
                    hand_data['hero_3b_chance'] = 'Yes-folds'
        
        # 确保翻前行动字段被正确记录
        if 'preflop_action_1st_bet' in hand_data and hand_data['preflop_action_1st_bet']:
            preflop_action_stats['has_first_bet'] += 1
            
        if 'preflop_action_3B' in hand_data and hand_data['preflop_action_3B']:
            preflop_action_stats['has_3b'] += 1
            
        processed_hands.append(hand_data)
        
        # 统计Hero_3B_Chance状态
        hero_3b_chance = hand_data['hero_3b_chance']
        if hero_3b_chance in hero_3b_chance_counts:
            hero_3b_chance_counts[hero_3b_chance] += 1
        else:
            hero_3b_chance_counts['Other'] += 1
    
    # 输出统计结果
    print("\n" + "="*50)
    print("Hero_3B_Chance 字段状态统计")
    print("="*50)
    print(f"总行数: {len(processed_hands)}")
    for status, count in hero_3b_chance_counts.items():
        if count > 0:
            print(f"{status}: {count} ({count/len(processed_hands)*100:.2f}%)")
    
    # 计算有3B机会的总行数（Yes-3B + Yes-Calls + Yes-folds + YES）
    yes_total = hero_3b_chance_counts['Yes-3B'] + hero_3b_chance_counts['Yes-Calls'] + hero_3b_chance_counts['Yes-folds'] + hero_3b_chance_counts['YES']
    print(f"\n有3B机会的总行数: {yes_total} ({yes_total/len(processed_hands)*100:.2f}%)")
    if yes_total > 0:
        print(f"在有3B机会中，选择3B的比例: {hero_3b_chance_counts['Yes-3B']/yes_total*100:.2f}%")
        print(f"在有3B机会中，选择Calls的比例: {hero_3b_chance_counts['Yes-Calls']/yes_total*100:.2f}%")
        print(f"在有3B机会中，选择folds的比例: {hero_3b_chance_counts['Yes-folds']/yes_total*100:.2f}%")
        if hero_3b_chance_counts['YES'] > 0:
            print(f"在有3B机会中，仍标记为YES的比例: {hero_3b_chance_counts['YES']/yes_total*100:.2f}%")
    
    # 输出翻前行动字段统计
    print("\n" + "="*50)
    print("翻前行动字段统计")
    print("="*50)
    print(f"有第一次加注记录的手数: {preflop_action_stats['has_first_bet']} ({preflop_action_stats['has_first_bet']/len(processed_hands)*100:.2f}%)")
    print(f"有3bet记录的手数: {preflop_action_stats['has_3b']} ({preflop_action_stats['has_3b']/len(processed_hands)*100:.2f}%)")
    
    # 将处理结果写入CSV文件
    if processed_hands:
        # 确保自定义列头
        keys = list(processed_hands[0].keys())
        
        # 自定义标题映射
        custom_headers = {
            'hand_id': 'Hand_ID',
            'SB_BB': 'Stakes',
            'cash_drop': 'Cash_Drop',
            'hero_position': 'Hero_Position',
            'hero_stack': 'Hero_Stack',
            'hero_cards': 'Hero_Cards',
            'flop_cards': 'Flop_Cards',
            'turn_card': 'Turn_Card',
            'river_card': 'River_Card',
            'preflop_actions': 'Preflop_Actions',
            'preflop_action_1st_bet': 'Preflop_1st_Bet',
            'preflop_action_3B': 'Preflop_3B',
            'preflop_action_4B': 'Preflop_4B',
            'preflop_action_5B': 'Preflop_5B',
            'preflop_pot': 'Preflop_Pot',
            'hero_position_type': 'Hero_Position_Type',
            'hero_open_position': 'Hero_Open_Position',
            'hero_3b_chance': 'Hero_3B_Chance',
            'pot_type': 'Pot_Type',
            'hero_squeeze': 'Hero_Squeeze',
            'final_pot_type': 'Final_Pot_Type',
            'flop_actions': 'Flop_Actions',
            'flop_pot': 'Flop_Pot',
            'turn_actions': 'Turn_Actions',
            'turn_pot': 'Turn_Pot',
            'river_actions': 'River_Actions',
            'river_pot': 'River_Pot',
            'result': 'Result',
            'total_pot': 'Total_Pot'
        }
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                
                # 写入自定义标题
                header_row = {field: custom_headers.get(field, field) for field in keys}
                writer.writerow(header_row)
                
                # 在写入数据前，确保所有数据字段与标题字段一致
                for hand in processed_hands:
                    # 确保每个手牌数据都包含所有字段，且与字段顺序一致
                    for field in keys:
                        if field not in hand:
                            hand[field] = ''
                
                # 写入所有手牌数据
                writer.writerows(processed_hands)
                print(f"\n处理结果已保存到 {output_file}")
        except PermissionError:
            # 如果有权限问题，尝试写入到当前目录
            alt_output_file = 'parsed_hands_new_format.csv'
            with open(alt_output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                header_row = {field: custom_headers.get(field, field) for field in keys}
                writer.writerow(header_row)
                writer.writerows(processed_hands)
                print(f"\n由于权限问题，处理结果已保存到 {alt_output_file}")

if __name__ == "__main__":
    process_hands_with_new_format() 