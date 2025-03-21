import csv
import re
import os

# 创建输出目录（如果不存在）
if not os.path.exists('output'):
    os.makedirs('output')

# 初始化统计数据
stats = {
    'hands': 0,          # 手牌总数
    'PFR': 0,            # Preflop Raise次数
    'ATS': 0,            # 在CO/BTN/SB位置首次加注次数
    'VPIP': 0,           # 自愿投入底池次数
    '3B': 0,             # 3bet次数
    'fold_to_3B': 0,     # 面对3bet弃牌次数（包括隐式弃牌）
    '4B': 0,             # 4bet次数
    'fold_to_4B': 0,     # 面对4bet弃牌次数
    'call_3B': 0,        # 面对3bet跟注次数
    'call_4B': 0,        # 面对4bet跟注次数
    '5B': 0,             # 5bet次数
    'fold_to_5B': 0,     # 面对5bet弃牌次数
    'call_5B': 0,        # 面对5bet跟注次数
    '3B_opportunities': 0,  # 有机会进行3-Bet的次数
    'facing_3B': 0,      # 面对3-Bet的次数
    '4B_opportunities': 0,  # 有机会进行4-Bet的次数
    'facing_4B': 0,       # 面对4-Bet的次数
    '5B_opportunities': 0,  # 有机会进行5-Bet的次数
    'facing_5B': 0,       # 面对5-Bet的次数
    'got_3B': 0,         # 被3-Bet的次数
    'got_4B': 0,         # 被4-Bet的次数
    'got_5B': 0,          # 被5-Bet的次数
    'BB_open': 0,         # 英雄在BB位置的首次开池次数
    'BB_fold': 0,         # BB位置fold的次数
    'BB_facing_raise': 0,  # BB位置面对加注的总次数
    'SB_fold': 0,         # SB位置fold的次数
    'SB_facing_raise': 0,  # SB位置面对加注的总次数
    
    # 英雄在各个位置的开池率统计
    'SB_hands': 0,       # 英雄在SB位置的手牌数
    'BB_hands': 0,       # 英雄在BB位置的手牌数
    'UTG_hands': 0,      # 英雄在UTG位置的手牌数
    'MP_hands': 0,       # 英雄在MP位置的手牌数
    'CO_hands': 0,       # 英雄在CO位置的手牌数
    'BTN_hands': 0,      # 英雄在BTN位置的手牌数
    
    'SB_open': 0,         # 英雄在SB位置的首次开池次数
    'UTG_open': 0,        # 英雄在UTG位置的首次开池次数
    'MP_open': 0,         # 英雄在MP位置的首次开池次数
    'CO_open': 0,         # 英雄在CO位置的首次开池次数
    'BTN_open': 0,        # 英雄在BTN位置的首次开池次数
    
    # 英雄在BB位置面对不同位置加注的跟注频率统计
    'BB_facing_SB_raise': 0,    # 英雄在BB位置面对SB位置加注的次数
    'BB_call_SB_raise': 0,      # 英雄在BB位置跟注SB位置加注的次数
    
    'BB_facing_UTG_raise': 0,   # 英雄在BB位置面对UTG位置加注的次数
    'BB_call_UTG_raise': 0,     # 英雄在BB位置跟注UTG位置加注的次数
    
    'BB_facing_MP_raise': 0,    # 英雄在BB位置面对MP位置加注的次数
    'BB_call_MP_raise': 0,      # 英雄在BB位置跟注MP位置加注的次数
    
    'BB_facing_CO_raise': 0,    # 英雄在BB位置面对CO位置加注的次数
    'BB_call_CO_raise': 0,      # 英雄在BB位置跟注CO位置加注的次数
    
    'BB_facing_BTN_raise': 0,   # 英雄在BB位置面对BTN位置加注的次数
    'BB_call_BTN_raise': 0,     # 英雄在BB位置跟注BTN位置加注的次数
}

# 记录特定情况的手牌ID
special_hands = {
    'call_3B_hands': [],  # 记录英雄面对3-Bet时选择跟注的手牌ID
    'call_4B_hands': [],  # 记录英雄面对4-Bet时选择跟注的手牌ID
    'call_5B_hands': [],  # 记录英雄面对5-Bet时选择跟注的手牌ID
    'fold_to_3B_hands': [], # 记录英雄面对3-Bet时选择弃牌的手牌ID
    'fold_to_4B_hands': [],  # 记录英雄面对4-Bet时选择弃牌的手牌ID
    'fold_to_5B_hands': [],  # 记录英雄面对5-Bet时选择弃牌的手牌ID
    '4B_hands': [],  # 记录英雄进行4-Bet的手牌ID
    '5B_hands': []   # 记录英雄进行5-Bet的手牌ID
}

# 读取CSV文件
with open('input/parsed_hands.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        # 获取手牌ID
        hand_id = row['hand_id']
        
        # 计算手牌数量
        stats['hands'] += 1
        
        # 获取英雄位置
        hero_position = row['hero_position'].replace('Hero(', '').replace(')', '')
        
        # 统计英雄在各个位置的手牌数
        if hero_position == 'SB':
            stats['SB_hands'] += 1
        elif hero_position == 'BB':
            stats['BB_hands'] += 1
        elif hero_position == 'UTG':
            stats['UTG_hands'] += 1
        elif hero_position == 'MP':
            stats['MP_hands'] += 1
        elif hero_position == 'CO':
            stats['CO_hands'] += 1
        elif hero_position == 'BTN':
            stats['BTN_hands'] += 1
        
        # 分析preflop动作
        preflop_actions = row['preflop_actions']
        
        # 如果没有preflop动作，跳过此手牌的分析
        if not preflop_actions:
            continue
            
        # 分割动作序列
        actions = preflop_actions.split('; ')
        
        # 使用更简单的方法分析动作序列
        # 跟踪加注次数
        raise_count = 0
        # 跟踪英雄是否已经加注
        hero_raised = False
        # 跟踪英雄是否已经3-Bet
        hero_3bet = False
        # 跟踪英雄是否已经4-Bet
        hero_4bet = False
        # 跟踪最后一次加注是否是英雄
        last_raiser_is_hero = False
        # 跟踪英雄是否面对3-Bet
        hero_facing_3bet = False
        # 跟踪英雄是否面对4-Bet
        hero_facing_4bet = False
        # 跟踪英雄是否面对5-Bet
        hero_facing_5bet = False
        # 跟踪英雄是否已经对3-Bet做出反应
        hero_responded_to_3bet = False
        # 跟踪英雄是否已经对4-Bet做出反应
        hero_responded_to_4bet = False
        # 跟踪英雄是否已经对5-Bet做出反应
        hero_responded_to_5bet = False
        # 跟踪英雄是否有机会进行3-Bet
        hero_has_3b_opportunity = False
        # 跟踪英雄是否有机会进行4-Bet
        hero_has_4b_opportunity = False
        # 跟踪英雄是否有机会进行5-Bet
        hero_has_5b_opportunity = False
        
        # 跟踪英雄在BB位置面对的加注位置
        facing_raiser_position = None
        
        # 分析每个动作
        for i, action in enumerate(actions):
            # 检查是否是英雄的动作
            is_hero_action = action.startswith('Hero:')
            action_parts = action.split(' ')
            
            if len(action_parts) > 1:
                action_type = action_parts[1]
                player = action_parts[0]  # 获取玩家标识
                
                # 检查VPIP（自愿投入底池）
                if is_hero_action and action_type in ['calls', 'raises']:
                    stats['VPIP'] += 1
                
                # 处理加注动作
                if action_type == 'raises':
                    raise_count += 1
                    
                    # 如果有人在英雄之前加注，英雄有机会进行3-Bet
                    if raise_count == 1 and not is_hero_action:
                        hero_has_3b_opportunity = True
                        stats['3B_opportunities'] += 1
                        
                        # 如果英雄在BB位置，记录面对加注
                        if hero_position == 'BB':
                            stats['BB_facing_raise'] += 1
                            # 从player中提取位置信息，格式为"Opp(位置)"
                            if player.startswith('Opp(') and ')' in player:
                                opp_position = player.split('(')[1].split(')')[0]
                                facing_raiser_position = opp_position
                                
                                # 统计英雄在BB位置面对不同位置加注的次数
                                if opp_position == 'SB':
                                    stats['BB_facing_SB_raise'] += 1
                                elif opp_position == 'UTG':
                                    stats['BB_facing_UTG_raise'] += 1
                                elif opp_position == 'MP':
                                    stats['BB_facing_MP_raise'] += 1
                                elif opp_position == 'CO':
                                    stats['BB_facing_CO_raise'] += 1
                                elif opp_position == 'BTN':
                                    stats['BB_facing_BTN_raise'] += 1
                        
                        # 如果英雄在SB位置，记录面对加注
                        elif hero_position == 'SB':
                            stats['SB_facing_raise'] += 1
                    
                    if is_hero_action:
                        hero_raised = True
                        last_raiser_is_hero = True
                        
                        # 检查PFR（首次加注）
                        if raise_count == 1:
                            stats['PFR'] += 1
                            
                            # 统计英雄在各个位置的首次开池次数
                            if hero_position == 'SB':
                                stats['SB_open'] += 1
                            elif hero_position == 'BB':
                                stats['BB_open'] += 1
                            elif hero_position == 'UTG':
                                stats['UTG_open'] += 1
                            elif hero_position == 'MP':
                                stats['MP_open'] += 1
                            elif hero_position == 'CO':
                                stats['CO_open'] += 1
                            elif hero_position == 'BTN':
                                stats['BTN_open'] += 1
                            
                            # 检查ATS（在CO/BTN/SB位置首次加注）
                            if hero_position in ['CO', 'BTN', 'SB']:
                                stats['ATS'] += 1
                        
                        # 检查3bet
                        elif raise_count == 2:
                            stats['3B'] += 1
                            hero_3bet = True
                        
                        # 检查4bet - 只有当英雄面对3-Bet时才计入
                        elif raise_count == 3 and hero_facing_3bet:
                            stats['4B'] += 1
                            special_hands['4B_hands'].append(hand_id)
                            hero_responded_to_3bet = True
                            hero_4bet = True
                            
                        # 检查5bet - 只有当英雄面对4-Bet时才计入
                        elif raise_count == 4 and hero_facing_4bet:
                            stats['5B'] += 1
                            special_hands['5B_hands'].append(hand_id)
                            hero_responded_to_4bet = True
                            
                            # 如果英雄面对5-Bet，标记已经做出反应
                            if hero_facing_5bet:
                                hero_responded_to_5bet = True
                    else:
                        last_raiser_is_hero = False
                        
                        # 如果这是第二次加注，且英雄之前加注过，那么英雄面对3-Bet
                        if raise_count == 2 and hero_raised:
                            hero_facing_3bet = True
                            stats['facing_3B'] += 1
                            stats['got_3B'] += 1  # 英雄被3-Bet
                            
                            # 如果英雄之前加注过，对手3-Bet后，英雄有机会进行4-Bet
                            if hero_raised:
                                hero_has_4b_opportunity = True
                                stats['4B_opportunities'] += 1
                            
                        # 如果这是第三次加注，且英雄之前进行过3-Bet，那么英雄面对4-Bet
                        if raise_count == 3 and hero_3bet:
                            hero_facing_4bet = True
                            stats['facing_4B'] += 1
                            stats['got_4B'] += 1  # 英雄被4-Bet
                            
                            # 如果英雄之前进行过3-Bet，对手4-Bet后，英雄有机会进行5-Bet
                            if hero_3bet:
                                hero_has_5b_opportunity = True
                                stats['5B_opportunities'] += 1
                                
                        # 如果这是第四次加注，且英雄之前进行过4-Bet，那么英雄面对5-Bet
                        if raise_count == 4 and hero_4bet:
                            hero_facing_5bet = True
                            stats['facing_5B'] += 1
                            stats['got_5B'] += 1  # 英雄被5-Bet
                
                # 处理跟注动作
                elif action_type == 'calls':
                    if is_hero_action:
                        # 检查对3bet的反应 - 只有当英雄面对3-Bet且尚未做出反应时才计入
                        if hero_facing_3bet and not hero_responded_to_3bet:
                            stats['call_3B'] += 1
                            special_hands['call_3B_hands'].append(hand_id)
                            hero_responded_to_3bet = True
                        
                        # 检查对4bet的反应 - 只有当英雄面对4-Bet且尚未做出反应时才计入
                        elif hero_facing_4bet and not hero_responded_to_4bet:
                            stats['call_4B'] += 1
                            special_hands['call_4B_hands'].append(hand_id)
                            hero_responded_to_4bet = True
                            
                        # 检查对5bet的反应 - 只有当英雄面对5-Bet且尚未做出反应时才计入
                        elif hero_facing_5bet and not hero_responded_to_5bet:
                            stats['call_5B'] += 1
                            special_hands['call_5B_hands'].append(hand_id)
                            hero_responded_to_5bet = True
                            
                        # 如果英雄在BB位置，且面对一次加注，统计跟注不同位置加注的次数
                        elif hero_position == 'BB' and raise_count == 1 and facing_raiser_position:
                            if facing_raiser_position == 'SB':
                                stats['BB_call_SB_raise'] += 1
                            elif facing_raiser_position == 'UTG':
                                stats['BB_call_UTG_raise'] += 1
                            elif facing_raiser_position == 'MP':
                                stats['BB_call_MP_raise'] += 1
                            elif facing_raiser_position == 'CO':
                                stats['BB_call_CO_raise'] += 1
                            elif facing_raiser_position == 'BTN':
                                stats['BB_call_BTN_raise'] += 1

# 处理弃牌动作
                elif action_type == 'folds':
                    if is_hero_action:
                        # 检查对3bet的反应 - 只有当英雄面对3-Bet且尚未做出反应时才计入
                        if hero_facing_3bet and not hero_responded_to_3bet:
                            stats['fold_to_3B'] += 1
                            special_hands['fold_to_3B_hands'].append(hand_id)
                            hero_responded_to_3bet = True
                            
                        # 检查对4bet的反应 - 只有当英雄面对4-Bet且尚未做出反应时才计入
                        elif hero_facing_4bet and not hero_responded_to_4bet:
                            stats['fold_to_4B'] += 1
                            special_hands['fold_to_4B_hands'].append(hand_id)
                            hero_responded_to_4bet = True
                            
                        # 检查对5bet的反应 - 只有当英雄面对5-Bet且尚未做出反应时才计入
                        elif hero_facing_5bet and not hero_responded_to_5bet:
                            stats['fold_to_5B'] += 1
                            special_hands['fold_to_5B_hands'].append(hand_id)
                            hero_responded_to_5bet = True
                        
                        # 记录BB位置的fold
                        elif hero_position == 'BB':
                            stats['BB_fold'] += 1
                        
                        # 记录SB位置的fold
                        elif hero_position == 'SB':
                            stats['SB_fold'] += 1
        
        # 检查英雄是否面对3-Bet但没有做出反应（隐式弃牌）
        if hero_facing_3bet and not hero_responded_to_3bet:
            stats['fold_to_3B'] += 1
            special_hands['fold_to_3B_hands'].append(hand_id)
            
        # 检查英雄是否面对4-Bet但没有做出反应（隐式弃牌）
        if hero_facing_4bet and not hero_responded_to_4bet:
            stats['fold_to_4B'] += 1
            special_hands['fold_to_4B_hands'].append(hand_id)
            
        # 检查英雄是否面对5-Bet但没有做出反应（隐式弃牌）
        if hero_facing_5bet and not hero_responded_to_5bet:
            stats['fold_to_5B'] += 1
            special_hands['fold_to_5B_hands'].append(hand_id)

# 计算百分比
total_hands = stats['hands']
pfr_percentage = (stats['PFR'] / total_hands) * 100 if total_hands > 0 else 0
ats_percentage = (stats['ATS'] / total_hands) * 100 if total_hands > 0 else 0
vpip_percentage = (stats['VPIP'] / total_hands) * 100 if total_hands > 0 else 0

# 使用更合理的分母计算百分比
threeb_percentage = (stats['3B'] / stats['3B_opportunities']) * 100 if stats['3B_opportunities'] > 0 else 0
fold_to_3b_percentage = (stats['fold_to_3B'] / stats['facing_3B']) * 100 if stats['facing_3B'] > 0 else 0
fourb_percentage = (stats['4B'] / stats['4B_opportunities']) * 100 if stats['4B_opportunities'] > 0 else 0
fold_to_4b_percentage = (stats['fold_to_4B'] / stats['facing_4B']) * 100 if stats['facing_4B'] > 0 else 0
call_3b_percentage = (stats['call_3B'] / stats['facing_3B']) * 100 if stats['facing_3B'] > 0 else 0
call_4b_percentage = (stats['call_4B'] / stats['facing_4B']) * 100 if stats['facing_4B'] > 0 else 0
fiveb_percentage = (stats['5B'] / stats['5B_opportunities']) * 100 if stats['5B_opportunities'] > 0 else 0
fold_to_5b_percentage = (stats['fold_to_5B'] / stats['facing_5B']) * 100 if stats['facing_5B'] > 0 else 0
call_5b_percentage = (stats['call_5B'] / stats['facing_5B']) * 100 if stats['facing_5B'] > 0 else 0

# 计算被3B、被4B和被5B的比率
got_3b_percentage = (stats['got_3B'] / stats['PFR']) * 100 if stats['PFR'] > 0 else 0
got_4b_percentage = (stats['got_4B'] / stats['3B']) * 100 if stats['3B'] > 0 else 0
got_5b_percentage = (stats['got_5B'] / stats['4B']) * 100 if stats['4B'] > 0 else 0

# 计算英雄在各个位置的开池率
sb_open_percentage = (stats['SB_open'] / stats['SB_hands']) * 100 if stats['SB_hands'] > 0 else 0
utg_open_percentage = (stats['UTG_open'] / stats['UTG_hands']) * 100 if stats['UTG_hands'] > 0 else 0
mp_open_percentage = (stats['MP_open'] / stats['MP_hands']) * 100 if stats['MP_hands'] > 0 else 0
co_open_percentage = (stats['CO_open'] / stats['CO_hands']) * 100 if stats['CO_hands'] > 0 else 0
btn_open_percentage = (stats['BTN_open'] / stats['BTN_hands']) * 100 if stats['BTN_hands'] > 0 else 0

# 计算英雄在BB位置面对不同位置加注的跟注频率
bb_call_sb_percentage = (stats['BB_call_SB_raise'] / stats['BB_facing_SB_raise']) * 100 if stats['BB_facing_SB_raise'] > 0 else 0
bb_call_utg_percentage = (stats['BB_call_UTG_raise'] / stats['BB_facing_UTG_raise']) * 100 if stats['BB_facing_UTG_raise'] > 0 else 0
bb_call_mp_percentage = (stats['BB_call_MP_raise'] / stats['BB_facing_MP_raise']) * 100 if stats['BB_facing_MP_raise'] > 0 else 0
bb_call_co_percentage = (stats['BB_call_CO_raise'] / stats['BB_facing_CO_raise']) * 100 if stats['BB_facing_CO_raise'] > 0 else 0
bb_call_btn_percentage = (stats['BB_call_BTN_raise'] / stats['BB_facing_BTN_raise']) * 100 if stats['BB_facing_BTN_raise'] > 0 else 0

# 计算BB和SB位置的fold频率
bb_fold_percentage = (stats['BB_fold'] / stats['BB_hands']) * 100 if stats['BB_hands'] > 0 else 0
sb_fold_percentage = (stats['SB_fold'] / stats['SB_hands']) * 100 if stats['SB_hands'] > 0 else 0

# 将特殊手牌ID写入单独的CSV文件
with open('output/special_hands.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # 写入标题行
    writer.writerow(['Type', 'Hand IDs'])
    
    # 写入特殊手牌ID
    writer.writerow(['Call 3B Hands', ', '.join(special_hands['call_3B_hands'])])
    writer.writerow(['Call 4B Hands', ', '.join(special_hands['call_4B_hands'])])
    writer.writerow(['Call 5B Hands', ', '.join(special_hands['call_5B_hands'])])
    writer.writerow(['Fold to 3B Hands', ', '.join(special_hands['fold_to_3B_hands'])])
    writer.writerow(['Fold to 4B Hands', ', '.join(special_hands['fold_to_4B_hands'])])
    writer.writerow(['Fold to 5B Hands', ', '.join(special_hands['fold_to_5B_hands'])])
    writer.writerow(['4B Hands', ', '.join(special_hands['4B_hands'])])
    writer.writerow(['5B Hands', ', '.join(special_hands['5B_hands'])])

# 计算BB开池率
bb_open_percentage = (stats['BB_open'] / stats['BB_hands']) * 100 if stats['BB_hands'] > 0 else 0

# 将结果写入CSV文件
with open('output/poker_stats.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # 写入标题行
    writer.writerow(['Player', 'Stat', 'Count', 'Percentage', 'Total'])
    
    # 写入统计数据
    writer.writerow(['Hero', 'Total Hands', stats['hands'], '100%', stats['hands']])
    writer.writerow(['Hero', 'PFR', stats['PFR'], f'{pfr_percentage:.2f}%', stats['hands']])
    writer.writerow(['Hero', 'VPIP', stats['VPIP'], f'{vpip_percentage:.2f}%', stats['hands']])
    writer.writerow(['Hero', 'ATS', stats['ATS'], f'{ats_percentage:.2f}%', stats['hands']])
    writer.writerow(['Hero', 'SB Opens', stats['SB_open'], f'{sb_open_percentage:.2f}%', stats['SB_hands']])
    writer.writerow(['Hero', 'BB Opens', stats['BB_open'], f'{bb_open_percentage:.2f}%', stats['BB_hands']])
    writer.writerow(['Hero', 'UTG Opens', stats['UTG_open'], f'{utg_open_percentage:.2f}%', stats['UTG_hands']])
    writer.writerow(['Hero', 'MP Opens', stats['MP_open'], f'{mp_open_percentage:.2f}%', stats['MP_hands']])
    writer.writerow(['Hero', 'CO Opens', stats['CO_open'], f'{co_open_percentage:.2f}%', stats['CO_hands']])
    writer.writerow(['Hero', 'BTN Opens', stats['BTN_open'], f'{btn_open_percentage:.2f}%', stats['BTN_hands']])
    
    # 写入BB和SB位置的fold频率
    writer.writerow(['Hero', 'BB Fold', stats['BB_fold'], f'{bb_fold_percentage:.2f}%', stats['BB_hands']])
    writer.writerow(['Hero', 'SB Fold', stats['SB_fold'], f'{sb_fold_percentage:.2f}%', stats['SB_hands']])
    
    # 写入英雄在BB位置面对不同位置加注的跟注频率
    writer.writerow(['Hero', 'BB Call SB Raise', stats['BB_call_SB_raise'], f'{bb_call_sb_percentage:.2f}%', stats['BB_facing_SB_raise']])
    writer.writerow(['Hero', 'BB Call UTG Raise', stats['BB_call_UTG_raise'], f'{bb_call_utg_percentage:.2f}%', stats['BB_facing_UTG_raise']])
    writer.writerow(['Hero', 'BB Call MP Raise', stats['BB_call_MP_raise'], f'{bb_call_mp_percentage:.2f}%', stats['BB_facing_MP_raise']])
    writer.writerow(['Hero', 'BB Call CO Raise', stats['BB_call_CO_raise'], f'{bb_call_co_percentage:.2f}%', stats['BB_facing_CO_raise']])
    writer.writerow(['Hero', 'BB Call BTN Raise', stats['BB_call_BTN_raise'], f'{bb_call_btn_percentage:.2f}%', stats['BB_facing_BTN_raise']])
    
    writer.writerow(['Hero', '3B', stats['3B'], f'{threeb_percentage:.2f}%', stats['3B_opportunities']])
    writer.writerow(['Hero', 'Got 3B', stats['got_3B'], f'{got_3b_percentage:.2f}%', stats['PFR']])
    writer.writerow(['Hero', 'Fold to 3B', stats['fold_to_3B'], f'{fold_to_3b_percentage:.2f}%', stats['facing_3B']])
    writer.writerow(['Hero', 'Call 3B', stats['call_3B'], f'{call_3b_percentage:.2f}%', stats['facing_3B']])
    writer.writerow(['Hero', '4B', stats['4B'], f'{fourb_percentage:.2f}%', stats['4B_opportunities']])
    writer.writerow(['Hero', 'Got 4B', stats['got_4B'], f'{got_4b_percentage:.2f}%', stats['3B']])
    writer.writerow(['Hero', 'Fold to 4B', stats['fold_to_4B'], f'{fold_to_4b_percentage:.2f}%', stats['facing_4B']])
    writer.writerow(['Hero', 'Call 4B', stats['call_4B'], f'{call_4b_percentage:.2f}%', stats['facing_4B']])
    writer.writerow(['Hero', '5B', stats['5B'], f'{fiveb_percentage:.2f}%', stats['5B_opportunities']])
    writer.writerow(['Hero', 'Got 5B', stats['got_5B'], f'{got_5b_percentage:.2f}%', stats['4B']])
    writer.writerow(['Hero', 'Fold to 5B', stats['fold_to_5B'], f'{fold_to_5b_percentage:.2f}%', stats['facing_5B']])
    writer.writerow(['Hero', 'Call 5B', stats['call_5B'], f'{call_5b_percentage:.2f}%', stats['facing_5B']])

# 打印特殊手牌ID和统计信息
print(f"分析完成！结果已保存到 output/poker_stats.csv")
print(f"特殊手牌ID已保存到 output/special_hands.csv")

print(f"\n统计信息:")
print(f"总手牌数: {stats['hands']}")
print(f"PFR次数: {stats['PFR']} ({pfr_percentage:.2f}%)")

# 打印英雄在各个位置的开池率
print(f"\n英雄在各个位置的开池率:")
print(f"SB位置: {stats['SB_open']}/{stats['SB_hands']} ({sb_open_percentage:.2f}%)")
print(f"UTG位置: {stats['UTG_open']}/{stats['UTG_hands']} ({utg_open_percentage:.2f}%)")
print(f"MP位置: {stats['MP_open']}/{stats['MP_hands']} ({mp_open_percentage:.2f}%)")
print(f"CO位置: {stats['CO_open']}/{stats['CO_hands']} ({co_open_percentage:.2f}%)")
print(f"BTN位置: {stats['BTN_open']}/{stats['BTN_hands']} ({btn_open_percentage:.2f}%)")

# 打印英雄在BB位置面对不同位置加注的跟注频率
print(f"\n英雄在BB位置面对不同位置加注的跟注频率:")
print(f"面对SB加注: {stats['BB_call_SB_raise']}/{stats['BB_facing_SB_raise']} ({bb_call_sb_percentage:.2f}%)")
print(f"面对UTG加注: {stats['BB_call_UTG_raise']}/{stats['BB_facing_UTG_raise']} ({bb_call_utg_percentage:.2f}%)")
print(f"面对MP加注: {stats['BB_call_MP_raise']}/{stats['BB_facing_MP_raise']} ({bb_call_mp_percentage:.2f}%)")
print(f"面对CO加注: {stats['BB_call_CO_raise']}/{stats['BB_facing_CO_raise']} ({bb_call_co_percentage:.2f}%)")
print(f"面对BTN加注: {stats['BB_call_BTN_raise']}/{stats['BB_facing_BTN_raise']} ({bb_call_btn_percentage:.2f}%)")

# 打印BB和SB位置的fold频率
print(f"\nBB和SB位置的fold频率:")
print(f"BB位置fold: {stats['BB_fold']}/{stats['BB_hands']} ({bb_fold_percentage:.2f}%)")
print(f"SB位置fold: {stats['SB_fold']}/{stats['SB_hands']} ({sb_fold_percentage:.2f}%)")

# 在程序结束时打印出每个位置的手牌数量
print(f"\n各个位置的手牌数量:")
print(f"SB位置: {stats['SB_hands']}")
print(f"BB位置: {stats['BB_hands']}")
print(f"UTG位置: {stats['UTG_hands']}")
print(f"MP位置: {stats['MP_hands']}")
print(f"CO位置: {stats['CO_hands']}")
print(f"BTN位置: {stats['BTN_hands']}")
print(f"总计: {stats['SB_hands'] + stats['BB_hands'] + stats['UTG_hands'] + stats['MP_hands'] + stats['CO_hands'] + stats['BTN_hands']}")
print(f"总手牌数: {stats['hands']}")