import csv
import os
import re

# 统计每个位置的PFR次数
position_pfr_count = {
    'CO': 0,
    'BTN': 0,
    'SB': 0,
    'BB': 0,
    'UTG': 0,
    'MP': 0
}

# 读取带标记的手牌文件
with open('output/parsed_hands_with_stats_new.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        hero_position = row.get('hero_position', '')
        if hero_position.startswith('Hero('):
            # 提取position部分
            hero_position = hero_position[5:-1]  # 例如从 "Hero(CO)" 提取 "CO"
        
        # 如果是PFR，则累计位置计数
        if row['PFR'] == 'Yes':
            if hero_position in position_pfr_count:
                position_pfr_count[hero_position] += 1

# 打印位置PFR统计
print("位置PFR统计:")
print("=" * 30)
for position, count in position_pfr_count.items():
    print(f"{position}: {count}")

# 计算CO, BTN, SB的PFR总数，这应该等于ATS
ats_positions_pfr = position_pfr_count['CO'] + position_pfr_count['BTN'] + position_pfr_count['SB']
print(f"\nCO+BTN+SB的PFR总数（理论上的ATS）: {ats_positions_pfr}")

# 读取原始统计文件，获取官方统计
official_stats = {}
with open('output/poker_stats.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        if len(row) >= 3 and row[0] == 'Hero':
            stat_name = row[1]
            try:
                count = int(row[2])
                official_stats[stat_name] = count
            except ValueError:
                pass

print("\n官方统计数据:")
print("=" * 30)
print(f"VPIP: {official_stats.get('VPIP', 'N/A')}")
print(f"PFR: {official_stats.get('PFR', 'N/A')}")
print(f"ATS: {official_stats.get('ATS', 'N/A')}")
print(f"CO Opens: {official_stats.get('CO Opens', 'N/A')}")
print(f"BTN Opens: {official_stats.get('BTN Opens', 'N/A')}")
print(f"SB Opens: {official_stats.get('SB Opens', 'N/A')}")
print(f"CO+BTN+SB的总和: {official_stats.get('CO Opens', 0) + official_stats.get('BTN Opens', 0) + official_stats.get('SB Opens', 0)}")

# 创建输出目录（如果不存在）
if not os.path.exists('output'):
    os.makedirs('output')

# 首先检查poker_stats.csv文件是否与原始输入文件基于相同的手牌集合
official_total = official_stats.get('Total Hands', 0)
print(f"\n官方手牌总数: {official_total}")

# 加载所有原始手牌
original_hand_ids = set()
with open('input/parsed_hands.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    total_hands = 0
    for row in reader:
        total_hands += 1
        original_hand_ids.add(row['hand_id'])

print(f"原始手牌文件总数: {total_hands}")
print(f"原始手牌文件中的唯一手牌ID数: {len(original_hand_ids)}")

# 提取所有VPIP情况的手牌
vpip_hands_old = []  # 原始poker_stats.py中标记为VPIP的手牌
vpip_hands_new = []  # 我们的脚本中标记为VPIP的手牌

# 加载所有手牌，按照poker_stats.py的逻辑计算VPIP
with open('input/parsed_hands.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        hand_id = row['hand_id']
        hero_position_raw = row.get('hero_position', '')
        hero_position = hero_position_raw
        if hero_position_raw.startswith('Hero(') and hero_position_raw.endswith(')'):
            hero_position = hero_position_raw[5:-1]  # 提取位置
        
        preflop_actions = row.get('preflop_actions', '')
        
        # 按照poker_stats.py的逻辑判断VPIP
        is_vpip_old = False
        
        if preflop_actions:
            actions = preflop_actions.split('; ')
            
            for action in actions:
                action = action.strip()
                if not action:
                    continue
                
                if action.startswith('Hero:'):
                    action_parts = action.split(' ')
                    if len(action_parts) > 1:
                        action_type = action_parts[1]
                        # poker_stats.py的VPIP逻辑
                        if action_type in ['calls', 'raises']:
                            is_vpip_old = True
                            break
        
        # 按照我们的逻辑判断VPIP
        is_vpip_new = False
        
        if preflop_actions:
            actions = preflop_actions.split(';')
            
            for action in actions:
                action = action.strip()
                if not action:
                    continue
                
                if action.startswith('Hero:'):
                    # 我们的VPIP逻辑
                    if 'raises' in action:
                        is_vpip_new = True
                        break
                    elif 'calls' in action:
                        is_vpip_new = True
                        break
        
        # 记录差异
        if is_vpip_old:
            vpip_hands_old.append(hand_id)
        
        if is_vpip_new:
            vpip_hands_new.append(hand_id)

# 找出仅在旧版本中标记的VPIP手牌
only_in_old = set(vpip_hands_old) - set(vpip_hands_new)
# 找出仅在新版本中标记的VPIP手牌
only_in_new = set(vpip_hands_new) - set(vpip_hands_old)

print(f"\nVPIP分析:")
print("=" * 30)
print(f"共有 {len(vpip_hands_old)} 个手牌在原始poker_stats.py中被标记为VPIP")
print(f"共有 {len(vpip_hands_new)} 个手牌在我们的脚本中被标记为VPIP")
print(f"差异: {len(vpip_hands_old) - len(vpip_hands_new)}")
print(f"只在原始poker_stats.py中被标记为VPIP的手牌数: {len(only_in_old)}")
print(f"只在我们的脚本中被标记为VPIP的手牌数: {len(only_in_new)}")

# 检查是否有其他可能的VPIP情况
print("\n检查其他可能的VPIP情况:")
print("=" * 30)

# 检查是否有翻牌后的动作被计入VPIP
print("\n检查是否有翻牌后的动作被计入VPIP:")
print("=" * 30)

# 检查是否有翻牌后的动作
flop_action_hands = []
with open('input/parsed_hands.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        hand_id = row['hand_id']
        flop_actions = row.get('flop_actions', '')
        turn_actions = row.get('turn_actions', '')
        river_actions = row.get('river_actions', '')
        
        # 检查是否有翻牌后的动作
        if (flop_actions and 'Hero:' in flop_actions) or \
           (turn_actions and 'Hero:' in turn_actions) or \
           (river_actions and 'Hero:' in river_actions):
            flop_action_hands.append(hand_id)

print(f"有翻牌后动作的手牌数: {len(flop_action_hands)}")

# 检查是否有翻牌后的动作但没有翻牌前的VPIP
flop_action_no_vpip_hands = []
for hand_id in flop_action_hands:
    if hand_id not in vpip_hands_old:
        flop_action_no_vpip_hands.append(hand_id)

print(f"有翻牌后动作但没有翻牌前VPIP的手牌数: {len(flop_action_no_vpip_hands)}")

# 检查是否有BB位置的check手牌
bb_check_vpip_hands = []
with open('input/parsed_hands.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        hand_id = row['hand_id']
        hero_position_raw = row.get('hero_position', '')
        hero_position = hero_position_raw
        if hero_position_raw.startswith('Hero(') and hero_position_raw.endswith(')'):
            hero_position = hero_position_raw[5:-1]  # 提取位置
        
        if hero_position != 'BB':
            continue
            
        preflop_actions = row.get('preflop_actions', '')
        
        # 检查BB位置的check
        if preflop_actions and 'Hero: checks' in preflop_actions:
            bb_check_vpip_hands.append(hand_id)

print(f"BB位置check的手牌数: {len(bb_check_vpip_hands)}")

# 检查"calls 0"的情况
bb_calls_0_hands = []
with open('input/parsed_hands.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        hand_id = row['hand_id']
        hero_position_raw = row.get('hero_position', '')
        hero_position = hero_position_raw
        if hero_position_raw.startswith('Hero(') and hero_position_raw.endswith(')'):
            hero_position = hero_position_raw[5:-1]  # 提取位置
        
        if hero_position != 'BB':
            continue
            
        preflop_actions = row.get('preflop_actions', '')
        
        # 检查BB位置的"calls 0"
        if preflop_actions and 'Hero: calls 0' in preflop_actions:
            bb_calls_0_hands.append(hand_id)

print(f"BB位置的'calls 0'手牌数: {len(bb_calls_0_hands)}")

# 检查是否有SB位置的limp手牌
sb_limp_hands = []
with open('input/parsed_hands.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        hand_id = row['hand_id']
        hero_position_raw = row.get('hero_position', '')
        hero_position = hero_position_raw
        if hero_position_raw.startswith('Hero(') and hero_position_raw.endswith(')'):
            hero_position = hero_position_raw[5:-1]  # 提取位置
        
        if hero_position != 'SB':
            continue
            
        preflop_actions = row.get('preflop_actions', '')
        
        # 检查SB位置的limp
        if preflop_actions and 'Hero: calls' in preflop_actions:
            sb_limp_hands.append(hand_id)

print(f"SB位置limp的手牌数: {len(sb_limp_hands)}")

# 检查是否有BB位置的check和SB位置的limp总数接近差异
total_special_cases = len(bb_check_vpip_hands) + len(sb_limp_hands)
print(f"BB位置check和SB位置limp的总数: {total_special_cases}")

# 检查是否有其他特殊情况
# 检查是否有BB位置的check和有翻牌后动作但没有翻牌前VPIP的总数接近差异
total_special_cases2 = len(bb_check_vpip_hands) + len(flop_action_no_vpip_hands)
print(f"BB位置check和有翻牌后动作但没有翻牌前VPIP的总数: {total_special_cases2}")

# 检查是否有SB位置的limp但不在VPIP中的手牌
sb_limp_not_vpip = []
for hand_id in sb_limp_hands:
    if hand_id not in vpip_hands_old:
        sb_limp_not_vpip.append(hand_id)

print(f"SB位置limp但不在VPIP中的手牌数: {len(sb_limp_not_vpip)}")

# 检查是否有BB位置的check但在官方VPIP中的手牌
# 这需要知道官方VPIP中的具体手牌ID，但我们没有这个信息
# 我们可以检查一下BB位置的check手牌是否都不在VPIP中
bb_check_in_vpip = []
for hand_id in bb_check_vpip_hands:
    if hand_id in vpip_hands_old:
        bb_check_in_vpip.append(hand_id)

print(f"BB位置check但在VPIP中的手牌数: {len(bb_check_in_vpip)}")

# 检查是否有BB位置的check和SB位置的limp但不在VPIP中的总数接近差异
total_special_cases3 = len(bb_check_vpip_hands) + len(sb_limp_not_vpip)
print(f"BB位置check和SB位置limp但不在VPIP中的总数: {total_special_cases3}")

# 检查VPIP和官方VPIP的差异
vpip_diff = official_stats.get('VPIP', 0) - len(vpip_hands_old)
print(f"\n官方VPIP({official_stats.get('VPIP', 0)})与计算VPIP({len(vpip_hands_old)})差异: {vpip_diff}")

if abs(vpip_diff - total_special_cases) < 10:
    print("差异接近BB位置check和SB位置limp的总数，官方可能将这些情况都计入VPIP")

if abs(vpip_diff - total_special_cases2) < 10:
    print("差异接近BB位置check和有翻牌后动作但没有翻牌前VPIP的总数，官方可能将这些情况都计入VPIP")

if abs(vpip_diff - total_special_cases3) < 10:
    print("差异接近BB位置check和SB位置limp但不在VPIP中的总数，官方可能将这些情况都计入VPIP")

# 如果差异存在，检查前几个差异手牌的具体情况
if flop_action_no_vpip_hands:
    print("\n有翻牌后动作但没有翻牌前VPIP的前几个手牌:")
    
    # 分析这些手牌的具体情况
    count = 0
    with open('input/parsed_hands.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if row['hand_id'] in flop_action_no_vpip_hands:
                count += 1
                if count > 5:  # 只显示前5个差异
                    break
                
                print(f"\n手牌ID: {row['hand_id']}")
                print(f"位置: {row['hero_position']}")
                print(f"翻牌前动作: {row['preflop_actions']}")
                print(f"翻牌动作: {row['flop_actions']}")
                print(f"转牌动作: {row['turn_actions']}")
                print(f"河牌动作: {row['river_actions']}")

# 如果差异存在，检查是否有BB位置的特殊情况
if abs(vpip_diff - len(bb_check_vpip_hands)) < 10:
    print("差异接近BB位置的check手牌数，官方可能将BB位置的check也计入VPIP")
elif abs(vpip_diff - len(bb_calls_0_hands)) < 10:
    print("差异接近BB位置的'calls 0'手牌数，官方可能将BB位置的'calls 0'也计入VPIP")
else:
    print("差异原因不明，需要进一步分析")

# 读取文件并应用修复后的逻辑
with open('input/parsed_hands.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    fieldnames = reader.fieldnames
    
    # 准备写入新文件
    with open('output/parsed_hands_fixed.csv', 'w', newline='', encoding='utf-8') as outfile:
        new_fieldnames = fieldnames + ['VPIP', 'PFR', 'ATS']
        writer = csv.DictWriter(outfile, fieldnames=new_fieldnames)
        writer.writeheader()
        
        vpip_count = 0
        pfr_count = 0
        ats_count = 0
        
        for row in reader:
            # 解析hero位置
            hero_position = row.get('hero_position', '')
            if hero_position.startswith('Hero('):
                # 提取position部分
                hero_position = hero_position[5:-1]  # 例如从 "Hero(CO)" 提取 "CO"
            
            # 处理preflop_actions
            preflop_actions = row.get('preflop_actions', '')
            
            # 直接手动应用原始统计逻辑
            is_pfr = False
            is_vpip = False
            is_ats = False
            
            if preflop_actions:
                actions = preflop_actions.split(';')
                raise_count = 0
                
                for action in actions:
                    action = action.strip()
                    if not action:
                        continue
                    
                    # 检查VPIP
                    if action.startswith('Hero:'):
                        if 'raises' in action:
                            is_vpip = True
                        elif 'calls' in action and not (hero_position == 'BB' and 'calls 0' in action):
                            is_vpip = True
                    
                    # 检查加注次数
                    if 'raises' in action:
                        raise_count += 1
                        
                        # 检查PFR
                        if action.startswith('Hero:') and raise_count == 1:
                            is_pfr = True
                            # 检查ATS
                            if hero_position in ['CO', 'BTN', 'SB']:
                                is_ats = True
            
            # 更新统计
            if is_vpip:
                vpip_count += 1
            if is_pfr:
                pfr_count += 1
            if is_ats:
                ats_count += 1
                
            # 添加标记
            row['VPIP'] = 'Yes' if is_vpip else 'No'
            row['PFR'] = 'Yes' if is_pfr else 'No'
            row['ATS'] = 'Yes' if is_ats else 'No'
            
            # 写入行
            writer.writerow(row)

print("\n使用修复逻辑的结果:")
print("=" * 30)
print(f"VPIP: {vpip_count}")
print(f"PFR: {pfr_count}")
print(f"ATS: {ats_count}")
print(f"与官方VPIP差异: {vpip_count - official_stats.get('VPIP', 0)}")
print(f"与官方PFR差异: {pfr_count - official_stats.get('PFR', 0)}")
print(f"与官方ATS差异: {ats_count - official_stats.get('ATS', 0)}")

print("\n分析完成！修复数据已保存到 output/parsed_hands_fixed.csv") 