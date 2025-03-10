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
    '3B_oop': 0,         # OOP位置3bet次数
    '3B_ip': 0,          # IP位置3bet次数
    'fold_to_3B': 0,     # 面对3bet弃牌次数（包括隐式弃牌）
    'fold_to_3B_oop': 0, # OOP位置面对3bet弃牌次数
    'fold_to_3B_ip': 0,  # IP位置面对3bet弃牌次数
    '4B': 0,             # 4bet次数
    'fold_to_4B': 0,     # 面对4bet弃牌次数
    'call_3B': 0,        # 面对3bet跟注次数
    'call_3B_oop': 0,    # OOP位置面对3bet跟注次数
    'call_3B_ip': 0,     # IP位置面对3bet跟注次数
    'call_4B': 0,        # 面对4bet跟注次数
    '5B': 0,             # 5bet次数
    'fold_to_5B': 0,     # 面对5bet弃牌次数
    'call_5B': 0,        # 面对5bet跟注次数
    '3B_opportunities': 0,  # 有机会进行3-Bet的次数
    '3B_opportunities_oop': 0, # OOP位置有机会进行3-Bet的次数
    '3B_opportunities_ip': 0,  # IP位置有机会进行3-Bet的次数
    'facing_3B': 0,      # 面对3-Bet的次数
    'facing_3B_oop': 0,  # OOP位置面对3-Bet的次数
    'facing_3B_ip': 0,   # IP位置面对3-Bet的次数
    '4B_opportunities': 0,  # 有机会进行4-Bet的次数
    'facing_4B': 0,       # 面对4-Bet的次数
    '5B_opportunities': 0,  # 有机会进行5-Bet的次数
    'facing_5B': 0,       # 面对5-Bet的次数
    'got_3B': 0,         # 被3-Bet的次数
    'got_3B_oop': 0,     # OOP位置被3-Bet的次数
    'got_3B_ip': 0,      # IP位置被3-Bet的次数
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
    
    # 翻后行动统计
    'flop_hands': 0,            # hero进入到flop的手牌数量
    
    # Single raise pot统计
    'srp_hands': 0,             # Single raise pot手牌数量
    'srp_hero_pfr': 0,          # 翻前为hero raises的Single raise pot手牌数量
    'srp_hero_cbet': 0,         # 翻前为hero raises且翻后hero第一个bets的次数
    'srp_hero_calls': 0,        # 翻前为hero calls的Single raise pot手牌数量
    'srp_opp_cbet': 0,          # 翻前为hero calls且翻后opp第一个bets的次数
    'srp_fold_to_cbet': 0,      # 翻前为hero calls且翻后opp第一个bets且hero folds的次数
    'srp_call_cbet': 0,         # 翻前为hero calls且翻后opp第一个bets且hero calls的次数
    'srp_raise_cbet': 0,        # 翻前为hero calls且翻后opp第一个bets且hero raise的次数
    'srp_donk': 0,              # 翻前为hero calls且hero raise in oop的次数
    
    # 3B pot统计
    '3b_pot_hands': 0,          # 3B pot手牌数量
    '3b_pot_hero_pfr': 0,       # 翻前为hero raises的3B pot手牌数量
    '3b_pot_hero_cbet': 0,      # 翻前为hero raises且翻后hero第一个bets的次数
    '3b_pot_hero_calls': 0,     # 翻前为hero calls的3B pot手牌数量
    '3b_pot_opp_cbet': 0,       # 翻前为hero calls且翻后opp第一个bets的次数
    '3b_pot_fold_to_cbet': 0,   # 翻前为hero calls且翻后opp第一个bets且hero folds的次数
    '3b_pot_call_cbet': 0,      # 翻前为hero calls且翻后opp第一个bets且hero calls的次数
    '3b_pot_raise_cbet': 0,     # 翻前为hero calls且翻后opp第一个bets且hero raise的次数
    '3b_pot_donk': 0,           # 翻前为hero calls且hero raise in oop的次数
    
    # 4B pot统计
    '4b_pot_hands': 0,          # 4B pot手牌数量
    '4b_pot_hero_pfr': 0,       # 翻前为hero raises的4B pot手牌数量
    '4b_pot_hero_cbet': 0,      # 翻前为hero raises且翻后hero第一个bets的次数
    '4b_pot_hero_calls': 0,     # 翻前为hero calls的4B pot手牌数量
    '4b_pot_opp_cbet': 0,       # 翻前为hero calls且翻后opp第一个bets的次数
    '4b_pot_fold_to_cbet': 0,   # 翻前为hero calls且翻后opp第一个bets且hero folds的次数
    '4b_pot_call_cbet': 0,      # 翻前为hero calls且翻后opp第一个bets且hero calls的次数
    '4b_pot_raise_cbet': 0,     # 翻前为hero calls且翻后opp第一个bets且hero raise的次数
    '4b_pot_donk': 0,           # 翻前为hero calls且hero raise in oop的次数
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

# 定义位置到座位号的映射函数
def position_to_seat_number(position):
    seat_map = {'SB': 1, 'BB': 2, 'UTG': 3, 'MP': 4, 'CO': 5, 'BTN': 6}
    return seat_map.get(position, 0)

# 判断是否是OOP位置
def is_oop(hero_position, opp_position):
    if not opp_position:
        # 如果无法确定对手位置，使用默认逻辑
        return hero_position in ['SB', 'BB']
    
    hero_seat = position_to_seat_number(hero_position)
    opp_seat = position_to_seat_number(opp_position)
    
    # 如果英雄座位号小于对手，则英雄是OOP
    return hero_seat < opp_seat

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
        # 跟踪英雄是否在OOP位置
        hero_is_oop = False
        # 跟踪底池类型
        pot_type = 'none'  # 'srp' (single raise pot), '3b' (3-bet pot), '4b' (4-bet pot)
        # 跟踪英雄在翻前是否跟注
        hero_called = False
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
                        
                        # 从player中提取对手位置信息，格式为"Opp(位置)"
                        opp_position = None
                        if player.startswith('Opp(') and ')' in player:
                            opp_position = player.split('(')[1].split(')')[0]
                        
                        # 判断英雄是否在OOP位置，根据座位号比较
                        if opp_position:
                            hero_seat = position_to_seat_number(hero_position)
                            opp_seat = position_to_seat_number(opp_position)
                            
                            # 如果英雄座位号小于对手，则英雄是OOP
                            if hero_seat < opp_seat:
                                hero_is_oop = True
                                stats['3B_opportunities_oop'] += 1
                            else:
                                stats['3B_opportunities_ip'] += 1
                        else:
                            # 如果无法确定对手位置，使用默认逻辑
                            if hero_position in ['SB', 'BB']:
                                hero_is_oop = True
                                stats['3B_opportunities_oop'] += 1
                            else:
                                stats['3B_opportunities_ip'] += 1
                        
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
                            
                            # 获取对手位置信息
                            opp_position = None
                            # 查找前一个动作，获取对手位置
                            for prev_action in actions[:i]:
                                if prev_action.startswith('Opp(') and 'raises' in prev_action:
                                    if ')' in prev_action:
                                        opp_position = prev_action.split('(')[1].split(')')[0]
                                        break
                            
                            # 根据座位号比较确定IP/OOP
                            if opp_position:
                                hero_seat = position_to_seat_number(hero_position)
                                opp_seat = position_to_seat_number(opp_position)
                                
                                # 如果英雄座位号小于对手，则英雄是OOP
                                if hero_seat < opp_seat:
                                    stats['3B_oop'] += 1
                                else:
                                    stats['3B_ip'] += 1
                            else:
                                # 如果无法确定对手位置，使用默认逻辑
                                if hero_position in ['SB', 'BB']:
                                    stats['3B_oop'] += 1
                                else:
                                    stats['3B_ip'] += 1
                        
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
                            
                            # 获取对手位置信息
                            opp_position = None
                            # 查找前一个动作，获取对手位置
                            for prev_action in actions[:i]:
                                if prev_action.startswith('Opp(') and 'raises' in prev_action and raise_count >= 2:
                                    if ')' in prev_action:
                                        opp_position = prev_action.split('(')[1].split(')')[0]
                                        break
                            
                            # 根据座位号比较确定IP/OOP
                            if opp_position:
                                hero_seat = position_to_seat_number(hero_position)
                                opp_seat = position_to_seat_number(opp_position)
                                
                                # 如果英雄座位号小于对手，则英雄是OOP
                                if hero_seat < opp_seat:
                                    stats['fold_to_3B_oop'] += 1
                                else:
                                    stats['fold_to_3B_ip'] += 1
                            else:
                                # 如果无法确定对手位置，使用默认逻辑
                                if hero_position in ['SB', 'BB']:
                                    stats['fold_to_3B_oop'] += 1
                                else:
                                    stats['fold_to_3B_ip'] += 1
                            
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
            
            # 尝试找到对手位置信息
            opp_position = None
            for action in actions:
                if action.startswith('Opp(') and 'raises' in action and ')' in action:
                    opp_position = action.split('(')[1].split(')')[0]
                    # 我们只关心最后一个3bet的对手
                    if actions.index(action) > actions.index([a for a in actions if a.startswith('Hero:') and 'raises' in a][-1]):
                        break
            
            # 根据座位号比较确定IP/OOP
            if opp_position:
                hero_seat = position_to_seat_number(hero_position)
                opp_seat = position_to_seat_number(opp_position)
                
                # 如果英雄座位号小于对手，则英雄是OOP
                if hero_seat < opp_seat:
                    stats['fold_to_3B_oop'] += 1
                else:
                    stats['fold_to_3B_ip'] += 1
            else:
                # 如果无法确定对手位置，使用默认逻辑
                if hero_position in ['SB', 'BB']:
                    stats['fold_to_3B_oop'] += 1
                else:
                    stats['fold_to_3B_ip'] += 1
            
        # 检查英雄是否面对4-Bet但没有做出反应（隐式弃牌）
        if hero_facing_4bet and not hero_responded_to_4bet:
            stats['fold_to_4B'] += 1
            special_hands['fold_to_4B_hands'].append(hand_id)
            
        # 检查英雄是否面对5-Bet但没有做出反应（隐式弃牌）
        if hero_facing_5bet and not hero_responded_to_5bet:
            stats['fold_to_5B'] += 1
            special_hands['fold_to_5B_hands'].append(hand_id)
        
        # 确定底池类型
        if raise_count == 1:
            pot_type = 'srp'  # Single Raise Pot
            # 先不增加srp_hands计数，等到确认有flop时再增加
            if hero_raised:
                stats['srp_hero_pfr'] += 1
            elif hero_called:
                stats['srp_hero_calls'] += 1
        elif raise_count == 2 and (hero_3bet or hero_facing_3bet):
            pot_type = '3b'  # 3-Bet Pot
            stats['3b_pot_hands'] += 1
            if hero_3bet:
                stats['3b_pot_hero_pfr'] += 1
            elif hero_called and hero_facing_3bet:
                stats['3b_pot_hero_calls'] += 1
        elif raise_count >= 3 and (hero_4bet or hero_facing_4bet):
            pot_type = '4b'  # 4-Bet Pot
            stats['4b_pot_hands'] += 1
            if hero_4bet:
                stats['4b_pot_hero_pfr'] += 1
            elif hero_called and hero_facing_4bet:
                stats['4b_pot_hero_calls'] += 1
        
        # 分析翻后行动
        flop_cards = row['flop_cards']
        flop_actions = row['flop_actions']
        
        # 如果有翻牌，则hero进入到flop
        if flop_cards:
            stats['flop_hands'] += 1
            
            # 只有当进入到flop阶段时才计算srp_hands
            if pot_type == 'srp':
                stats['srp_hands'] += 1
            
            # 如果有翻牌动作，分析翻牌动作
            if flop_actions:
                flop_actions_list = flop_actions.split('; ')
                
                # 确定翻牌圈第一个行动的玩家和行动类型
                first_action = flop_actions_list[0] if flop_actions_list else None
                
                if first_action:
                    is_hero_first_action = first_action.startswith('Hero:')
                    action_parts = first_action.split(' ')
                    
                    if len(action_parts) > 1:
                        first_action_type = action_parts[1]
                        
                        # 分析不同底池类型的翻后行动
                        if pot_type == 'srp':
                            # 分析Single Raise Pot的翻后行动
                            # 判断hero是否在OOP位置
                            hero_is_oop = is_oop(hero_position, None)
                            
                            # 情况1: hero在OOP位置且是第一个行动者下注 - 这是标准的OOP位置Cbet
                            if is_hero_first_action and first_action_type == 'bets' and hero_raised and hero_is_oop:
                                # 翻前为hero raises且翻后hero第一个bets (OOP位置的Cbet)
                                stats['srp_hero_cbet'] += 1
                            # 情况2: hero在IP位置，对手check后hero下注 - 这也是Cbet
                            elif len(flop_actions_list) > 1 and hero_raised and not hero_is_oop:
                                # 检查第一个动作是否是对手check
                                if not is_hero_first_action and first_action_type == 'checks':
                                    # 检查第二个动作是否是hero下注
                                    second_action = flop_actions_list[1]
                                    if second_action.startswith('Hero:') and 'bets' in second_action:
                                        # 翻前为hero raises且翻后opp checks然后hero bets (IP位置的Cbet)
                                        stats['srp_hero_cbet'] += 1
                            elif not is_hero_first_action and first_action_type == 'bets' and hero_called:
                                # 翻前为hero calls且翻后opp第一个bets
                                stats['srp_opp_cbet'] += 1
                                
                                # 分析hero对opp cbet的反应
                                if len(flop_actions_list) > 1:
                                    hero_response = flop_actions_list[1] if flop_actions_list[1].startswith('Hero:') else None
                                    
                                    if hero_response:
                                        response_parts = hero_response.split(' ')
                                        if len(response_parts) > 1:
                                            response_type = response_parts[1]
                                            
                                            if response_type == 'folds':
                                                # 翻前为hero calls且翻后opp第一个bets且hero folds
                                                stats['srp_fold_to_cbet'] += 1
                                            elif response_type == 'calls':
                                                # 翻前为hero calls且翻后opp第一个bets且hero calls
                                                stats['srp_call_cbet'] += 1
                                            elif response_type == 'raises':
                                                # 翻前为hero calls且翻后opp第一个bets且hero raise
                                                stats['srp_raise_cbet'] += 1
                            elif is_hero_first_action and first_action_type == 'bets' and hero_called and hero_is_oop:
                                # 翻前为hero calls且hero在oop位置第一个bets (Donk)
                                stats['srp_donk'] += 1
                        
                        elif pot_type == '3b':
                            # 分析3-Bet Pot的翻后行动
                            if is_hero_first_action and first_action_type == 'bets' and hero_3bet:
                                # 翻前为hero raises (3bet)且翻后hero第一个bets (Cbet)
                                stats['3b_pot_hero_cbet'] += 1
                            elif not is_hero_first_action and first_action_type == 'bets' and hero_facing_3bet and hero_called:
                                # 翻前为hero calls (call 3bet)且翻后opp第一个bets
                                stats['3b_pot_opp_cbet'] += 1
                                
                                # 分析hero对opp cbet的反应
                                if len(flop_actions_list) > 1:
                                    hero_response = flop_actions_list[1] if flop_actions_list[1].startswith('Hero:') else None
                                    
                                    if hero_response:
                                        response_parts = hero_response.split(' ')
                                        if len(response_parts) > 1:
                                            response_type = response_parts[1]
                                            
                                            if response_type == 'folds':
                                                # 翻前为hero calls且翻后opp第一个bets且hero folds
                                                stats['3b_pot_fold_to_cbet'] += 1
                                            elif response_type == 'calls':
                                                # 翻前为hero calls且翻后opp第一个bets且hero calls
                                                stats['3b_pot_call_cbet'] += 1
                                            elif response_type == 'raises':
                                                # 翻前为hero calls且翻后opp第一个bets且hero raise
                                                stats['3b_pot_raise_cbet'] += 1
                            elif is_hero_first_action and first_action_type == 'bets' and hero_facing_3bet and hero_called and hero_is_oop:
                                # 翻前为hero calls (call 3bet)且hero在oop位置第一个bets (Donk)
                                stats['3b_pot_donk'] += 1
                        
                        elif pot_type == '4b':
                            # 分析4-Bet Pot的翻后行动
                            if is_hero_first_action and first_action_type == 'bets' and hero_4bet:
                                # 翻前为hero raises (4bet)且翻后hero第一个bets (Cbet)
                                stats['4b_pot_hero_cbet'] += 1
                            elif not is_hero_first_action and first_action_type == 'bets' and hero_facing_4bet and hero_called:
                                # 翻前为hero calls (call 4bet)且翻后opp第一个bets
                                stats['4b_pot_opp_cbet'] += 1
                                
                                # 分析hero对opp cbet的反应
                                if len(flop_actions_list) > 1:
                                    hero_response = flop_actions_list[1] if flop_actions_list[1].startswith('Hero:') else None
                                    
                                    if hero_response:
                                        response_parts = hero_response.split(' ')
                                        if len(response_parts) > 1:
                                            response_type = response_parts[1]
                                            
                                            if response_type == 'folds':
                                                # 翻前为hero calls且翻后opp第一个bets且hero folds
                                                stats['4b_pot_fold_to_cbet'] += 1
                                            elif response_type == 'calls':
                                                # 翻前为hero calls且翻后opp第一个bets且hero calls
                                                stats['4b_pot_call_cbet'] += 1
                                            elif response_type == 'raises':
                                                # 翻前为hero calls且翻后opp第一个bets且hero raise
                                                stats['4b_pot_raise_cbet'] += 1
                            elif is_hero_first_action and first_action_type == 'bets' and hero_called and hero_is_oop:
                                # 翻前为hero calls (call 4bet)且hero在oop位置第一个bets (Donk)
                                stats['4b_pot_donk'] += 1

# 计算百分比
total_hands = stats['hands']
pfr_percentage = (stats['PFR'] / total_hands) * 100 if total_hands > 0 else 0
ats_percentage = (stats['ATS'] / total_hands) * 100 if total_hands > 0 else 0
vpip_percentage = (stats['VPIP'] / total_hands) * 100 if total_hands > 0 else 0

# 使用更合理的分母计算百分比
# 3B百分比计算
threeb_percentage_all = (stats['3B'] / stats['3B_opportunities']) * 100 if stats['3B_opportunities'] > 0 else 0
threeb_percentage_oop = (stats['3B_oop'] / stats['3B_opportunities_oop']) * 100 if stats['3B_opportunities_oop'] > 0 else 0
threeb_percentage_ip = (stats['3B_ip'] / stats['3B_opportunities_ip']) * 100 if stats['3B_opportunities_ip'] > 0 else 0

# Fold to 3B百分比计算
fold_to_3b_percentage_all = (stats['fold_to_3B'] / stats['facing_3B']) * 100 if stats['facing_3B'] > 0 else 0
fold_to_3b_percentage_oop = (stats['fold_to_3B_oop'] / stats['facing_3B_oop']) * 100 if stats['facing_3B_oop'] > 0 else 0
fold_to_3b_percentage_ip = (stats['fold_to_3B_ip'] / stats['facing_3B_ip']) * 100 if stats['facing_3B_ip'] > 0 else 0

# Call 3B百分比计算
call_3b_percentage_all = (stats['call_3B'] / stats['facing_3B']) * 100 if stats['facing_3B'] > 0 else 0
call_3b_percentage_oop = (stats['call_3B_oop'] / stats['facing_3B_oop']) * 100 if stats['facing_3B_oop'] > 0 else 0
call_3b_percentage_ip = (stats['call_3B_ip'] / stats['facing_3B_ip']) * 100 if stats['facing_3B_ip'] > 0 else 0

# 其他百分比计算
fourb_percentage = (stats['4B'] / stats['4B_opportunities']) * 100 if stats['4B_opportunities'] > 0 else 0
fold_to_4b_percentage = (stats['fold_to_4B'] / stats['facing_4B']) * 100 if stats['facing_4B'] > 0 else 0
call_4b_percentage = (stats['call_4B'] / stats['facing_4B']) * 100 if stats['facing_4B'] > 0 else 0
fiveb_percentage = (stats['5B'] / stats['5B_opportunities']) * 100 if stats['5B_opportunities'] > 0 else 0
fold_to_5b_percentage = (stats['fold_to_5B'] / stats['facing_5B']) * 100 if stats['facing_5B'] > 0 else 0
call_5b_percentage = (stats['call_5B'] / stats['facing_5B']) * 100 if stats['facing_5B'] > 0 else 0

# 计算被3B、被4B和被5B的比率
got_3b_percentage_all = (stats['got_3B'] / stats['PFR']) * 100 if stats['PFR'] > 0 else 0
got_3b_percentage_oop = (stats['got_3B_oop'] / stats['PFR']) * 100 if stats['PFR'] > 0 else 0
got_3b_percentage_ip = (stats['got_3B_ip'] / stats['PFR']) * 100 if stats['PFR'] > 0 else 0
got_4b_percentage = (stats['got_4B'] / stats['3B']) * 100 if stats['3B'] > 0 else 0
got_5b_percentage = (stats['got_5B'] / stats['4B']) * 100 if stats['4B'] > 0 else 0

# 计算英雄在各个位置的开池率
sb_open_percentage = (stats['SB_open'] / stats['SB_hands']) * 100 if stats['SB_hands'] > 0 else 0
bb_open_percentage = (stats['BB_open'] / stats['BB_hands']) * 100 if stats['BB_hands'] > 0 else 0
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

# 计算翻后行动的百分比
# 计算进入flop的百分比
flop_percentage = (stats['flop_hands'] / total_hands) * 100 if total_hands > 0 else 0

# Single Raise Pot百分比计算
srp_hero_cbet_percentage = (stats['srp_hero_cbet'] / stats['srp_hero_pfr']) * 100 if stats['srp_hero_pfr'] > 0 else 0
srp_fold_to_cbet_percentage = (stats['srp_fold_to_cbet'] / stats['srp_opp_cbet']) * 100 if stats['srp_opp_cbet'] > 0 else 0
srp_call_cbet_percentage = (stats['srp_call_cbet'] / stats['srp_opp_cbet']) * 100 if stats['srp_opp_cbet'] > 0 else 0
srp_raise_cbet_percentage = (stats['srp_raise_cbet'] / stats['srp_opp_cbet']) * 100 if stats['srp_opp_cbet'] > 0 else 0
srp_donk_percentage = (stats['srp_donk'] / stats['srp_hero_calls']) * 100 if stats['srp_hero_calls'] > 0 else 0

# 3B Pot百分比计算
_3b_pot_hero_cbet_percentage = (stats['3b_pot_hero_cbet'] / stats['3b_pot_hero_pfr']) * 100 if stats['3b_pot_hero_pfr'] > 0 else 0
_3b_pot_fold_to_cbet_percentage = (stats['3b_pot_fold_to_cbet'] / stats['3b_pot_opp_cbet']) * 100 if stats['3b_pot_opp_cbet'] > 0 else 0
_3b_pot_call_cbet_percentage = (stats['3b_pot_call_cbet'] / stats['3b_pot_opp_cbet']) * 100 if stats['3b_pot_opp_cbet'] > 0 else 0
_3b_pot_raise_cbet_percentage = (stats['3b_pot_raise_cbet'] / stats['3b_pot_opp_cbet']) * 100 if stats['3b_pot_opp_cbet'] > 0 else 0
_3b_pot_donk_percentage = (stats['3b_pot_donk'] / stats['3b_pot_hero_calls']) * 100 if stats['3b_pot_hero_calls'] > 0 else 0

# 4B Pot百分比计算
_4b_pot_hero_cbet_percentage = (stats['4b_pot_hero_cbet'] / stats['4b_pot_hero_pfr']) * 100 if stats['4b_pot_hero_pfr'] > 0 else 0
_4b_pot_fold_to_cbet_percentage = (stats['4b_pot_fold_to_cbet'] / stats['4b_pot_opp_cbet']) * 100 if stats['4b_pot_opp_cbet'] > 0 else 0
_4b_pot_call_cbet_percentage = (stats['4b_pot_call_cbet'] / stats['4b_pot_opp_cbet']) * 100 if stats['4b_pot_opp_cbet'] > 0 else 0
_4b_pot_raise_cbet_percentage = (stats['4b_pot_raise_cbet'] / stats['4b_pot_opp_cbet']) * 100 if stats['4b_pot_opp_cbet'] > 0 else 0
_4b_pot_donk_percentage = (stats['4b_pot_donk'] / stats['4b_pot_hero_calls']) * 100 if stats['4b_pot_hero_calls'] > 0 else 0

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

# 将翻前统计结果写入CSV文件
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
    
    # 写入3B相关统计数据，区分OOP和IP
    writer.writerow(['Hero', '3B(all)', stats['3B'], f'{threeb_percentage_all:.2f}%', stats['3B_opportunities']])
    writer.writerow(['Hero', '3B(oop)', stats['3B_oop'], f'{threeb_percentage_oop:.2f}%', stats['3B_opportunities_oop']])
    writer.writerow(['Hero', '3B(ip)', stats['3B_ip'], f'{threeb_percentage_ip:.2f}%', stats['3B_opportunities_ip']])
    
    writer.writerow(['Hero', 'Got 3B(all)', stats['got_3B'], f'{got_3b_percentage_all:.2f}%', stats['PFR']])
    writer.writerow(['Hero', 'Got 3B(oop)', stats['got_3B_oop'], f'{got_3b_percentage_oop:.2f}%', stats['PFR']])
    writer.writerow(['Hero', 'Got 3B(ip)', stats['got_3B_ip'], f'{got_3b_percentage_ip:.2f}%', stats['PFR']])
    
    writer.writerow(['Hero', 'Fold to 3B(all)', stats['fold_to_3B'], f'{fold_to_3b_percentage_all:.2f}%', stats['facing_3B']])
    writer.writerow(['Hero', 'Fold to 3B(oop)', stats['fold_to_3B_oop'], f'{fold_to_3b_percentage_oop:.2f}%', stats['facing_3B_oop']])
    writer.writerow(['Hero', 'Fold to 3B(ip)', stats['fold_to_3B_ip'], f'{fold_to_3b_percentage_ip:.2f}%', stats['facing_3B_ip']])
    
    writer.writerow(['Hero', 'Call 3B(all)', stats['call_3B'], f'{call_3b_percentage_all:.2f}%', stats['facing_3B']])
    writer.writerow(['Hero', 'Call 3B(oop)', stats['call_3B_oop'], f'{call_3b_percentage_oop:.2f}%', stats['facing_3B_oop']])
    writer.writerow(['Hero', 'Call 3B(ip)', stats['call_3B_ip'], f'{call_3b_percentage_ip:.2f}%', stats['facing_3B_ip']])
    
    # 写入4B和5B相关统计数据
    writer.writerow(['Hero', '4B', stats['4B'], f'{fourb_percentage:.2f}%', stats['4B_opportunities']])
    writer.writerow(['Hero', 'Got 4B', stats['got_4B'], f'{got_4b_percentage:.2f}%', stats['3B']])
    writer.writerow(['Hero', 'Fold to 4B', stats['fold_to_4B'], f'{fold_to_4b_percentage:.2f}%', stats['facing_4B']])
    writer.writerow(['Hero', 'Call 4B', stats['call_4B'], f'{call_4b_percentage:.2f}%', stats['facing_4B']])
    writer.writerow(['Hero', '5B', stats['5B'], f'{fiveb_percentage:.2f}%', stats['5B_opportunities']])
    writer.writerow(['Hero', 'Got 5B', stats['got_5B'], f'{got_5b_percentage:.2f}%', stats['4B']])
    writer.writerow(['Hero', 'Fold to 5B', stats['fold_to_5B'], f'{fold_to_5b_percentage:.2f}%', stats['facing_5B']])
    writer.writerow(['Hero', 'Call 5B', stats['call_5B'], f'{call_5b_percentage:.2f}%', stats['facing_5B']])

# 将翻后行动统计结果写入新的CSV文件
with open('output/poker_stats_post_flop.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # 写入标题行
    writer.writerow(['Player', 'Stat', 'Count', 'Percentage', 'Total'])
    
    # 写入进入flop的手牌数量
    writer.writerow(['Hero', 'Flop Hands', stats['flop_hands'], f'{flop_percentage:.2f}%', stats['hands']])
    
    # 写入Single Raise Pot统计数据
    writer.writerow(['Hero', 'SRP Hands', stats['srp_hands'], f'{(stats["srp_hands"] / stats["flop_hands"] * 100):.2f}%' if stats['flop_hands'] > 0 else '0.00%', stats['flop_hands']])
    writer.writerow(['Hero', 'SRP Cbet', stats['srp_hero_cbet'], f'{srp_hero_cbet_percentage:.2f}%', stats['srp_hero_pfr']])
    writer.writerow(['Hero', 'SRP Fold to Cbet', stats['srp_fold_to_cbet'], f'{srp_fold_to_cbet_percentage:.2f}%', stats['srp_opp_cbet']])
    writer.writerow(['Hero', 'SRP Call Cbet', stats['srp_call_cbet'], f'{srp_call_cbet_percentage:.2f}%', stats['srp_opp_cbet']])
    writer.writerow(['Hero', 'SRP Raise Cbet', stats['srp_raise_cbet'], f'{srp_raise_cbet_percentage:.2f}%', stats['srp_opp_cbet']])
    writer.writerow(['Hero', 'SRP Donk', stats['srp_donk'], f'{srp_donk_percentage:.2f}%', stats['srp_hero_calls']])
    
    # 写入3B Pot统计数据
    writer.writerow(['Hero', '3B Pot Hands', stats['3b_pot_hands'], f'{(stats["3b_pot_hands"] / stats["flop_hands"] * 100):.2f}%' if stats['flop_hands'] > 0 else '0.00%', stats['flop_hands']])
    writer.writerow(['Hero', '3B Pot Cbet', stats['3b_pot_hero_cbet'], f'{_3b_pot_hero_cbet_percentage:.2f}%', stats['3b_pot_hero_pfr']])
    writer.writerow(['Hero', '3B Pot Fold to Cbet', stats['3b_pot_fold_to_cbet'], f'{_3b_pot_fold_to_cbet_percentage:.2f}%', stats['3b_pot_opp_cbet']])
    writer.writerow(['Hero', '3B Pot Call Cbet', stats['3b_pot_call_cbet'], f'{_3b_pot_call_cbet_percentage:.2f}%', stats['3b_pot_opp_cbet']])
    writer.writerow(['Hero', '3B Pot Raise Cbet', stats['3b_pot_raise_cbet'], f'{_3b_pot_raise_cbet_percentage:.2f}%', stats['3b_pot_opp_cbet']])
    writer.writerow(['Hero', '3B Pot Donk', stats['3b_pot_donk'], f'{_3b_pot_donk_percentage:.2f}%', stats['3b_pot_hero_calls']])
    
    # 写入4B Pot统计数据
    writer.writerow(['Hero', '4B Pot Hands', stats['4b_pot_hands'], f'{(stats["4b_pot_hands"] / stats["flop_hands"] * 100):.2f}%' if stats['flop_hands'] > 0 else '0.00%', stats['flop_hands']])
    writer.writerow(['Hero', '4B Pot Cbet', stats['4b_pot_hero_cbet'], f'{_4b_pot_hero_cbet_percentage:.2f}%', stats['4b_pot_hero_pfr']])
    writer.writerow(['Hero', '4B Pot Fold to Cbet', stats['4b_pot_fold_to_cbet'], f'{_4b_pot_fold_to_cbet_percentage:.2f}%', stats['4b_pot_opp_cbet']])
    writer.writerow(['Hero', '4B Pot Call Cbet', stats['4b_pot_call_cbet'], f'{_4b_pot_call_cbet_percentage:.2f}%', stats['4b_pot_opp_cbet']])
    writer.writerow(['Hero', '4B Pot Raise Cbet', stats['4b_pot_raise_cbet'], f'{_4b_pot_raise_cbet_percentage:.2f}%', stats['4b_pot_opp_cbet']])
    writer.writerow(['Hero', '4B Pot Donk', stats['4b_pot_donk'], f'{_4b_pot_donk_percentage:.2f}%', stats['4b_pot_hero_calls']])

# 打印统计信息
print(f"分析完成！翻前结果已保存到 output/poker_stats.csv")
print(f"翻后结果已保存到 output/poker_stats_post_flop.csv")
print(f"特殊手牌ID已保存到 output/special_hands.csv")

print(f"\n翻后统计信息:")
print(f"进入flop的手牌数量: {stats['flop_hands']} ({flop_percentage:.2f}%)")

print(f"\nSingle Raise Pot统计:")
print(f"SRP手牌数量: {stats['srp_hands']}")
print(f"Cbet频率: {stats['srp_hero_cbet']}/{stats['srp_hero_pfr']} ({srp_hero_cbet_percentage:.2f}%)")
print(f"Fold to Cbet频率: {stats['srp_fold_to_cbet']}/{stats['srp_opp_cbet']} ({srp_fold_to_cbet_percentage:.2f}%)")
print(f"Call Cbet频率: {stats['srp_call_cbet']}/{stats['srp_opp_cbet']} ({srp_call_cbet_percentage:.2f}%)")
print(f"Raise Cbet频率: {stats['srp_raise_cbet']}/{stats['srp_opp_cbet']} ({srp_raise_cbet_percentage:.2f}%)")
print(f"Donk频率: {stats['srp_donk']}/{stats['srp_hero_calls']} ({srp_donk_percentage:.2f}%)")

print(f"\n3B Pot统计")
print(f"3B Pot手牌数量: {stats['3b_pot_hands']}")
print(f"Cbet频率: {stats['3b_pot_hero_cbet']}/{stats['3b_pot_hero_pfr']} ({_3b_pot_hero_cbet_percentage:.2f}%)")
print(f"Fold to Cbet频率: {stats['3b_pot_fold_to_cbet']}/{stats['3b_pot_opp_cbet']} ({_3b_pot_fold_to_cbet_percentage:.2f}%)")
print(f"Call Cbet频率: {stats['3b_pot_call_cbet']}/{stats['3b_pot_opp_cbet']} ({_3b_pot_call_cbet_percentage:.2f}%)")
print(f"Raise Cbet频率: {stats['3b_pot_raise_cbet']}/{stats['3b_pot_opp_cbet']} ({_3b_pot_raise_cbet_percentage:.2f}%)")
print(f"Donk频率: {stats['3b_pot_donk']}/{stats['3b_pot_hero_calls']} ({_3b_pot_donk_percentage:.2f}%)")

print(f"\n4B Pot统计:")
print(f"4B Pot手牌数量: {stats['4b_pot_hands']}")
print(f"Cbet频率: {stats['4b_pot_hero_cbet']}/{stats['4b_pot_hero_pfr']} ({_4b_pot_hero_cbet_percentage:.2f}%)")
print(f"Fold to Cbet频率: {stats['4b_pot_fold_to_cbet']}/{stats['4b_pot_opp_cbet']} ({_4b_pot_fold_to_cbet_percentage:.2f}%)")
print(f"Call Cbet频率: {stats['4b_pot_call_cbet']}/{stats['4b_pot_opp_cbet']} ({_4b_pot_call_cbet_percentage:.2f}%)")
print(f"Raise Cbet频率: {stats['4b_pot_raise_cbet']}/{stats['4b_pot_opp_cbet']} ({_4b_pot_raise_cbet_percentage:.2f}%)")
print(f"Donk频率: {stats['4b_pot_donk']}/{stats['4b_pot_hero_calls']} ({_4b_pot_donk_percentage:.2f}%)")