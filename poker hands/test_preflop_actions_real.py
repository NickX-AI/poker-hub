import os
import csv
from collections import defaultdict

def analyze_preflop_actions(csv_file, max_samples=5):
    """
    分析CSV文件中的翻前行动，特别是第一次加注和3bet的情况
    
    参数:
        csv_file: CSV文件路径
        max_samples: 每种情况的最大样本数
    """
    print(f"\n==== 分析文件: {csv_file} ====")
    
    if not os.path.exists(csv_file):
        print(f"错误: 文件不存在 {csv_file}")
        return
    
    # 样本计数和存储
    samples = {
        'first_bet_only': [],  # 只有第一次加注的样本
        'first_bet_and_3b': []  # 有第一次加注和3bet的样本
    }
    
    # 统计计数
    counts = {
        'total': 0,
        'has_first_bet': 0,
        'has_3b': 0,
        'first_bet_empty': 0,
        '3b_empty': 0
    }
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                counts['total'] += 1
                
                # 获取相关字段
                first_bet = row.get('Preflop_1st_Bet', '')
                three_bet = row.get('Preflop_3B', '')
                
                # 计数
                if first_bet:
                    counts['has_first_bet'] += 1
                else:
                    counts['first_bet_empty'] += 1
                
                if three_bet:
                    counts['has_3b'] += 1
                else:
                    counts['3b_empty'] += 1
                
                # 收集样本
                if first_bet and not three_bet and len(samples['first_bet_only']) < max_samples:
                    samples['first_bet_only'].append({
                        'hand_id': row.get('Hand_ID', ''),
                        'preflop_actions': row.get('Preflop_Actions', ''),
                        'first_bet': first_bet,
                        'three_bet': three_bet
                    })
                
                if first_bet and three_bet and len(samples['first_bet_and_3b']) < max_samples:
                    samples['first_bet_and_3b'].append({
                        'hand_id': row.get('Hand_ID', ''),
                        'preflop_actions': row.get('Preflop_Actions', ''),
                        'first_bet': first_bet,
                        'three_bet': three_bet
                    })
        
        # 显示统计信息
        print("\n统计结果:")
        print(f"总手数: {counts['total']}")
        print(f"有第一次加注记录: {counts['has_first_bet']} ({counts['has_first_bet']/counts['total']*100:.2f}%)")
        print(f"有3bet记录: {counts['has_3b']} ({counts['has_3b']/counts['total']*100:.2f}%)")
        print(f"第一次加注字段为空: {counts['first_bet_empty']} ({counts['first_bet_empty']/counts['total']*100:.2f}%)")
        print(f"3bet字段为空: {counts['3b_empty']} ({counts['3b_empty']/counts['total']*100:.2f}%)")
        
        # 显示样本
        print("\n== 只有第一次加注的样本 ==")
        for i, sample in enumerate(samples['first_bet_only'], 1):
            print(f"\n样本 {i}:")
            print(f"手牌ID: {sample['hand_id']}")
            print(f"翻前行动: {sample['preflop_actions']}")
            print(f"第一次加注: {sample['first_bet']}")
        
        print("\n== 有第一次加注和3bet的样本 ==")
        for i, sample in enumerate(samples['first_bet_and_3b'], 1):
            print(f"\n样本 {i}:")
            print(f"手牌ID: {sample['hand_id']}")
            print(f"翻前行动: {sample['preflop_actions']}")
            print(f"第一次加注: {sample['first_bet']}")
            print(f"3bet: {sample['three_bet']}")
    
    except Exception as e:
        print(f"分析时出错: {e}")

if __name__ == "__main__":
    # 分析最新生成的CSV文件
    csv_file = "poker_output/parsed_hands.csv"
    analyze_preflop_actions(csv_file)
    
    # 如果存在新格式的文件，也分析它
    new_csv_file = "poker_output/parsed_hands_new_format.csv"
    if os.path.exists(new_csv_file):
        analyze_preflop_actions(new_csv_file) 