import csv
import re
import os

# 创建输出目录（如果不存在）
if not os.path.exists('output'):
    os.makedirs('output')

# 读取CSV文件
try:
    with open('input/parsed_hands.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        # 获取原始列名
        fieldnames = reader.fieldnames
        
        if not fieldnames:
            print("警告: 无法读取列名，CSV文件可能为空")
            exit(1)
        
        # 添加新的统计列
        new_fieldnames = fieldnames + ['VPIP', 'PFR', 'ATS', '3B', '4B', '5B', 'Call_3B', 'Fold_to_3B']
        
        # 准备写入新文件
        with open('output/parsed_hands_with_stats_new.csv', 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=new_fieldnames)
            writer.writeheader()
            
            # 处理每一行
            for row in reader:
                # 解析hero位置
                hero_position_raw = row.get('hero_position', '')
                hero_position = hero_position_raw
                if hero_position_raw.startswith('Hero(') and hero_position_raw.endswith(')'):
                    hero_position = hero_position_raw[5:-1]  # 例如从 "Hero(CO)" 提取 "CO"
                
                # 处理preflop_actions
                preflop_actions = row.get('preflop_actions', '')
                
                # 直接手动应用原始统计逻辑
                is_pfr = False
                is_vpip = False
                is_ats = False
                is_3b = False
                is_4b = False
                is_5b = False
                is_call_3b = False
                is_fold_to_3b = False
                
                if preflop_actions:
                    actions = preflop_actions.split(';')
                    raise_count = 0
                    hero_raised = False
                    last_raiser_was_hero = False
                    
                    for i, action in enumerate(actions):
                        action = action.strip()
                        if not action:
                            continue
                        
                        # 检查VPIP
                        if action.startswith('Hero:'):
                            # 模拟poker_stats.py的逻辑，但排除BB位置的checks
                            if 'raises' in action:
                                is_vpip = True
                            elif 'calls' in action:
                                # 注意：这里不再排除BB位置的'calls 0'，与poker_stats.py保持一致
                                is_vpip = True
                            # 确保BB位置的checks不算作VPIP
                            elif 'checks' in action and hero_position == 'BB':
                                # BB位置的checks不计入VPIP
                                pass
                            # 其他可能的VPIP情况
                            elif 'bets' in action:
                                is_vpip = True
                        
                        # 检查加注次数
                        if 'raises' in action:
                            is_hero_action = action.startswith('Hero:')
                            raise_count += 1
                            
                            # 检查PFR
                            if is_hero_action and raise_count == 1:
                                is_pfr = True
                                # 检查ATS
                                if hero_position in ['CO', 'BTN', 'SB']:
                                    is_ats = True
                            
                            # 记录最后加注者是否是英雄
                            if is_hero_action:
                                last_raiser_was_hero = True
                                # 检查3bet
                                if raise_count == 2:
                                    is_3b = True
                                # 检查4bet
                                elif raise_count == 3:
                                    is_4b = True
                                # 检查5bet
                                elif raise_count == 4:
                                    is_5b = True
                            else:
                                # 如果是对手加注，并且是对英雄的加注（3-bet），检查英雄后续是否弃牌或跟注
                                if raise_count == 2 and last_raiser_was_hero:
                                    # 查找后续英雄的行动
                                    for j in range(i+1, len(actions)):
                                        next_action = actions[j].strip()
                                        if next_action.startswith('Hero:'):
                                            if 'folds' in next_action:
                                                is_fold_to_3b = True
                                            elif 'calls' in next_action:
                                                is_call_3b = True
                                            break
                                    # 如果没有找到后续行动，可能是隐式弃牌
                                    if j == len(actions) - 1 and not next_action.startswith('Hero:'):
                                        is_fold_to_3b = True
                                last_raiser_was_hero = False
                
                # 添加标记
                row['VPIP'] = 'Yes' if is_vpip else 'No'
                row['PFR'] = 'Yes' if is_pfr else 'No'
                row['ATS'] = 'Yes' if is_ats else 'No'
                row['3B'] = 'Yes' if is_3b else 'No'
                row['4B'] = 'Yes' if is_4b else 'No'
                row['5B'] = 'Yes' if is_5b else 'No'
                row['Call_3B'] = 'Yes' if is_call_3b else 'No'
                row['Fold_to_3B'] = 'Yes' if is_fold_to_3b else 'No'
                
                # 写入行
                writer.writerow(row)

    print("分析完成！结果已保存到 output/parsed_hands_with_stats_new.csv")
except Exception as e:
    print(f"处理过程中发生错误: {e}")
    exit(1) 