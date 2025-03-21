from poker_hand_parser import PokerHandParser
import os
import csv

def test_real_data():
    """处理少量真实数据并检查Hero_3B_Chance字段的状态"""
    input_file = 'poker_input/combined_1.txt'
    output_file = 'poker_output/test_3b_chance_real.csv'
    
    if not os.path.exists(input_file):
        print(f"错误：找不到输入文件 {input_file}")
        return
    
    # 这里我们只处理前500个手牌来快速验证
    max_hands = 500
    
    # 初始化解析器
    parser = PokerHandParser()
    
    # 统计数据
    hero_3b_chance_counts = {
        'NO': 0,
        'Yes-3B': 0,
        'Yes-Calls': 0,
        'Yes-folds': 0,
        'YES': 0,  # 旧的YES状态应该不再出现
        'Other': 0
    }
    
    # 收集样本数据
    samples = {
        'NO': [],
        'Yes-3B': [],
        'Yes-Calls': [],
        'Yes-folds': [],
        'YES': []
    }
    
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 分割为单独的手牌
    hands = content.split('\n\n\n')
    print(f"总共找到 {len(hands)} 个手牌，将处理前 {max_hands} 个")
    
    # 处理手牌
    processed_hands = []
    for i, hand_text in enumerate(hands[:max_hands]):
        if i % 100 == 0:
            print(f"处理第 {i+1} 个手牌...")
            
        if not hand_text.strip():
            continue
            
        hand_data = parser.parse_hand(hand_text)
        processed_hands.append(hand_data)
        
        # 统计Hero_3B_Chance状态
        hero_3b_chance = hand_data.get('hero_3b_chance', 'N/A')
        if hero_3b_chance in hero_3b_chance_counts:
            hero_3b_chance_counts[hero_3b_chance] += 1
            # 收集样本
            if len(samples[hero_3b_chance]) < 3:
                sample_data = {
                    'Hand_ID': hand_data.get('hand_id', 'N/A'),
                    'Hero_Position': hand_data.get('hero_position', 'N/A'),
                    'Hero_3B_Chance': hero_3b_chance,
                    'Preflop_Actions': hand_data.get('preflop_actions', 'N/A')[:100] + '...' if len(hand_data.get('preflop_actions', 'N/A')) > 100 else hand_data.get('preflop_actions', 'N/A'),
                    'Preflop_3B': hand_data.get('preflop_action_3B', 'N/A')
                }
                samples[hero_3b_chance].append(sample_data)
        else:
            hero_3b_chance_counts['Other'] += 1
    
    # 输出统计结果
    print("\n" + "="*50)
    print("Hero_3B_Chance 统计")
    print("="*50)
    total_processed = len(processed_hands)
    print(f"处理的手牌数: {total_processed}")
    for status, count in hero_3b_chance_counts.items():
        if count > 0:
            print(f"{status}: {count} ({count/total_processed*100:.2f}%)")
    
    # 计算有3B机会的总行数（Yes-3B + Yes-Calls + Yes-folds + YES）
    yes_total = hero_3b_chance_counts['Yes-3B'] + hero_3b_chance_counts['Yes-Calls'] + hero_3b_chance_counts['Yes-folds'] + hero_3b_chance_counts['YES']
    print(f"\n有3B机会的总行数: {yes_total} ({yes_total/total_processed*100:.2f}%)")
    if yes_total > 0:
        print(f"在有3B机会中，选择3B的比例: {hero_3b_chance_counts['Yes-3B']/yes_total*100:.2f}%")
        print(f"在有3B机会中，选择Calls的比例: {hero_3b_chance_counts['Yes-Calls']/yes_total*100:.2f}%")
        print(f"在有3B机会中，选择folds的比例: {hero_3b_chance_counts['Yes-folds']/yes_total*100:.2f}%")
        if hero_3b_chance_counts['YES'] > 0:
            print(f"在有3B机会中，仍标记为YES的比例: {hero_3b_chance_counts['YES']/yes_total*100:.2f}%")
    
    # 输出每种状态的样本
    for status, sample_list in samples.items():
        if sample_list:
            print("\n" + "="*50)
            print(f"Hero_3B_Chance 为 {status} 的样本")
            print("="*50)
            for i, sample in enumerate(sample_list):
                print(f"样本 {i+1}:")
                for key, value in sample.items():
                    print(f"  {key}: {value}")
                print()
    
    # 将处理结果写入CSV文件
    if processed_hands:
        keys = processed_hands[0].keys()
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(processed_hands)
            print(f"处理结果已保存到 {output_file}")

if __name__ == "__main__":
    test_real_data() 