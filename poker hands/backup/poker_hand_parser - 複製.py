import re
import csv
from typing import Dict, List, Optional
import os

class PokerHandParser:
    def __init__(self):
        self.hand_data = {
            'hand_id': '',
            'hero_position': '',
            'hero_position_type': '',  # 新增：IP/OOP/NA
            'hero_open_position': '',  # 新增：记录Hero open位置
            'hero_3b_position': '',    # 新增：记录Hero 3B位置
            'pot_type': '',           # 新增：底池类型(SRP/3B/4B/5B)
            'hero_squeeze': 'NO',     # 新增：Hero是否squeeze
            'final_pot_type': '',     # 新增：最终底池类型(1v1/multi)
            'hero_stack': '',  # 改为字符串类型，因为会包含 BB 单位
            'hero_cards': '',
            'SB_BB': '',  # 记录大小盲注金额
            'flop_cards': '',
            'turn_card': '',
            'river_card': '',
            'preflop_actions': '',  # 只从UTG开始记录，不记录大小盲注
            'preflop_action_1st_bet': '',  # 只记录raises和calls，到第二个raises前
            'preflop_action_3B': '',  # 只记录raises和calls，到第三个raises前
            'preflop_action_4B': '',  # 只记录raises和calls，到第四个raises前
            'preflop_action_5B': '',  # 只记录raises和calls
            'preflop_action_limp': '',  # Hero跟注
            'preflop_action_limp_fold': '',  # Hero跟注后弃牌
            'preflop_action_limp_call': '',  # Hero跟注后被加注，然后跟注
            'preflop_pot': 0.0,
            'flop_actions': '',
            'flop_pot': 0.0,
            'turn_actions': '',
            'turn_pot': 0.0,
            'river_actions': '',
            'river_pot': 0.0,
            'result': '',
            'total_pot': 0.0,
            'cash_drop': ''  # 记录红包降落
        }
        self.current_street = 'preflop'
        self.position_map = {
            '1': 'BTN',
            '2': 'SB',
            '3': 'BB',
            '4': 'UTG',
            '5': 'MP',
            '6': 'CO'
        }
        self.player_positions = {}
        self.current_pot = 0.0
        self.sb_amount = 0.02  # 默认值
        self.bb_amount = 0.05  # 默认值
        self.hero_total_bet = 0.0
        self.last_bet_amount = 0.0
        self.last_bet_player = ''
        self.bb_position_found = False
        self.bb_player = ""  # 记录BB位置的玩家
        
        # 用于记录翻前行动分类的变量
        self.preflop_all_actions = []  # 记录所有翻前行动(从UTG开始)
        self.first_bet_player = ""  # 第一个加注者
        self.first_bet_actions = []  # 第一个加注者后的行动
        self.has_first_bet = False  # 是否已有第一个加注
        self.three_bet_player = ""  # 3Bet玩家
        self.three_bet_actions = []  # 3Bet后的行动
        self.has_three_bet = False  # 是否已有3Bet
        self.four_bet_player = ""  # 4Bet玩家
        self.four_bet_actions = []  # 4Bet后的行动
        self.has_four_bet = False  # 是否已有4Bet
        self.five_bet_player = ""  # 5Bet玩家
        self.five_bet_actions = []  # 5Bet后的行动
        self.has_five_bet = False  # 是否已有5Bet
        self.hero_limped = False  # Hero是否跟注
        self.hero_limp_actions = []  # Hero跟注后的行动
        self.hero_limp_raised = False  # Hero跟注后是否被加注
        self.hero_limp_response = ""  # Hero跟注被加注后的反应
        
        # 新增变量
        self.hero_entered_pot = False  # 标记hero是否进入底池
        self.active_players_at_flop = []  # 到达翻牌圈时的活跃玩家
        self.hero_squeeze_opportunity = False  # 是否有squeeze机会(前面有人加注且有人跟注)
        self.preflop_raise_count = 0  # 记录翻前加注次数
        self.open_position = ''  # 记录第一个加注的位置
    
    def reset(self):
        self.hand_data = {
            'hand_id': '',
            'hero_position': '',
            'hero_position_type': '',  # 新增：IP/OOP/NA
            'hero_open_position': '',  # 新增：记录Hero open位置
            'hero_3b_position': '',    # 新增：记录Hero 3B位置
            'pot_type': '',           # 新增：底池类型(SRP/3B/4B/5B)
            'hero_squeeze': 'NO',     # 新增：Hero是否squeeze
            'final_pot_type': '',     # 新增：最终底池类型(1v1/multi)
            'hero_stack': '',  # 改为字符串类型，因为会包含 BB 单位
            'hero_cards': '',
            'SB_BB': '',  # 记录大小盲注金额
            'flop_cards': '',
            'turn_card': '',
            'river_card': '',
            'preflop_actions': '',  # 只从UTG开始记录，不记录大小盲注
            'preflop_action_1st_bet': '',  # 只记录raises和calls，到第二个raises前
            'preflop_action_3B': '',  # 只记录raises和calls，到第三个raises前
            'preflop_action_4B': '',  # 只记录raises和calls，到第四个raises前
            'preflop_action_5B': '',  # 只记录raises和calls
            'preflop_action_limp': '',  # Hero跟注
            'preflop_action_limp_fold': '',  # Hero跟注后弃牌
            'preflop_action_limp_call': '',  # Hero跟注后被加注，然后跟注
            'preflop_pot': 0.0,
            'flop_actions': '',
            'flop_pot': 0.0,
            'turn_actions': '',
            'turn_pot': 0.0,
            'river_actions': '',
            'river_pot': 0.0,
            'result': '',
            'total_pot': 0.0,
            'cash_drop': ''  # 记录红包降落
        }
        self.current_street = 'preflop'
        self.player_positions = {}
        self.current_pot = 0.0
        self.hero_total_bet = 0.0
        self.last_bet_amount = 0.0
        self.last_bet_player = ''
        self.bb_position_found = False
        self.bb_player = ""
        
        # 重置翻前行动分类的变量
        self.preflop_all_actions = []
        self.first_bet_player = ""
        self.first_bet_actions = []
        self.has_first_bet = False
        self.three_bet_player = ""
        self.three_bet_actions = []
        self.has_three_bet = False
        self.four_bet_player = ""
        self.four_bet_actions = []
        self.has_four_bet = False
        self.five_bet_player = ""
        self.five_bet_actions = []
        self.has_five_bet = False
        self.hero_limped = False
        self.hero_limp_actions = []
        self.hero_limp_raised = False
        self.hero_limp_response = ""
        
        # 重置新增变量
        self.hero_entered_pot = False
        self.active_players_at_flop = []
        self.hero_squeeze_opportunity = False
        self.preflop_raise_count = 0
        self.open_position = ''
        
        # 不重置sb_amount和bb_amount，保留之前解析到的值
    
    def parse_hand_id(self, line: str):
        if 'Poker Hand #' in line:
            match = re.search(r'Poker Hand #(RC\d+):', line)
            if match:
                self.hand_data['hand_id'] = match.group(1)
    
    def parse_hero_info(self, line: str):
        if 'Seat' in line and 'Hero' in line:
            match = re.search(r'Seat (\d+): Hero \((\$[\d.]+) in chips\)', line)
            if match:
                seat_num = match.group(1)
                position = self.position_map.get(seat_num, seat_num)
                self.hand_data['hero_position'] = f"Hero({position})"
                stack_amount = float(match.group(2).replace('$', ''))
                self.hand_data['hero_stack'] = f"{self.convert_to_bb(stack_amount):.0f}BB"
    
    def parse_players_positions(self, line: str):
        if 'Seat' in line:
            if 'Hero' in line:
                match = re.search(r'Seat (\d+): Hero \(', line)
                if match:
                    seat_num = match.group(1)
                    position = self.position_map.get(seat_num, seat_num)
                    self.player_positions['Hero'] = position
                    # 如果Hero在BB位置，记录BB位置的玩家是Hero
                    if position == 'BB':
                        self.bb_player = 'Hero'
            else:
                match = re.search(r'Seat (\d+): ([^(]+)', line)
                if match:
                    seat_num = match.group(1)
                    player_name = match.group(2).strip()
                    position = self.position_map.get(seat_num, seat_num)
                    self.player_positions[player_name] = position
                    # 记录BB位置的玩家
                    if position == 'BB':
                        self.bb_player = player_name
    
    def parse_hero_cards(self, line: str):
        if 'Dealt to Hero' in line:
            cards = re.search(r'\[(.*?)\]', line)
            if cards:
                self.hand_data['hero_cards'] = cards.group(1)
    
    def parse_board_cards(self, line: str):
        if '*** FLOP ***' in line:
            self.current_street = 'flop'
            self.hand_data['preflop_pot'] = round(self.convert_to_bb(self.current_pot), 1)  # 记录preflop底池
            cards = re.search(r'\[(.*?)\]', line)
            if cards:
                self.hand_data['flop_cards'] = cards.group(1)
        elif '*** TURN ***' in line:
            self.current_street = 'turn'
            self.hand_data['flop_pot'] = round(self.convert_to_bb(self.current_pot), 1)  # 记录flop底池
            cards = re.search(r'\] \[(.*?)\]', line)
            if cards:
                self.hand_data['turn_card'] = cards.group(1)
        elif '*** RIVER ***' in line:
            self.current_street = 'river'
            self.hand_data['turn_pot'] = round(self.convert_to_bb(self.current_pot), 1)  # 记录turn底池
            cards = re.search(r'\] \[(.*?)\]', line)
            if cards:
                self.hand_data['river_card'] = cards.group(1)
    
    def convert_to_bb(self, amount: float) -> float:
        """将美元金额转换为 BB 单位"""
        if self.bb_amount <= 0:  # 防止除零错误
            self.bb_amount = 0.05
        return amount / self.bb_amount
    
    def parse_action(self, line: str):
        if ':' in line and not line.startswith('Seat'):
            if 'Poker Hand #' in line:
                return
                
            # 处理红包降落
            if 'Cash Drop to Pot' in line:
                match = re.search(r'Cash Drop to Pot: total \$([\d.]+)', line)
                if match:
                    amount = float(match.group(1))
                    self.hand_data['cash_drop'] = f"${amount}"
                return
                
            # 处理大小盲注下注 - 这部分不记录到preflop_actions
            if 'posts small blind' in line or 'posts big blind' in line:
                player_name = line.split(':')[0].strip()
                is_hero = player_name == 'Hero'
                
                if 'posts small blind' in line:
                    if is_hero:
                        self.hero_total_bet += self.sb_amount
                        # Hero作为小盲强制进入底池
                        self.hero_entered_pot = True
                    self.current_pot += self.sb_amount
                    # 将玩家添加到翻牌前活跃玩家列表
                    if player_name not in self.active_players_at_flop:
                        self.active_players_at_flop.append(player_name)
                elif 'posts big blind' in line:
                    if is_hero:
                        self.hero_total_bet += self.bb_amount
                        # Hero作为大盲强制进入底池
                        self.hero_entered_pot = True
                    self.current_pot += self.bb_amount
                    # 发现BB位置投注时，记录BB所在位置的玩家
                    self.bb_player = player_name
                    # 将玩家添加到翻牌前活跃玩家列表
                    if player_name not in self.active_players_at_flop:
                        self.active_players_at_flop.append(player_name)
                return
                
            # 处理未被跟注的投注返还
            if 'Uncalled bet' in line:
                match = re.search(r'Uncalled bet \(\$([\d.]+)\)', line)
                if match:
                    returned_amount = float(match.group(1))
                    self.current_pot -= returned_amount
                    if 'returned to Hero' in line:
                        self.hero_total_bet -= returned_amount
                    self._update_pot_sizes()
                return
                
            # 获取基本信息，对所有街段共用
            action = self.format_action_with_bb(line.strip())
            player_name = line.split(':')[0].strip()
            player_position = self.player_positions.get(player_name, "")
            bet_amount = self.extract_bet_amount(line.strip())
            is_hero = player_name == 'Hero'
            
            # 更新投注信息，对所有街段共用
            if bet_amount > 0:
                self.last_bet_amount = bet_amount
                self.last_bet_player = player_name
                
                if is_hero:
                    self.hero_total_bet += bet_amount
                
                self.current_pot += bet_amount
                
            # 处理不同街段的行动
            if self.current_street == 'preflop':
                # 记录翻前行动 - 盲注下注已经在前面被排除
                # 所有其他行动（包括大小盲的非下注行动）都要记录
                self.preflop_all_actions.append(action)
                self.hand_data['preflop_actions'] = '; '.join(self.preflop_all_actions)
                
                # 跟踪Hero是否进入底池
                if is_hero and ('calls' in action or 'raises' in action or 'bets' in action):
                    self.hero_entered_pot = True
                
                # 跟踪squeeze机会(有人加注且有人跟注后)
                if self.has_first_bet and 'calls' in action and not self.has_three_bet:
                    self.hero_squeeze_opportunity = True
                
                # 检查是否是Hero的squeeze加注
                if is_hero and 'raises' in action and self.hero_squeeze_opportunity and not self.has_three_bet:
                    self.hand_data['hero_squeeze'] = 'YES'
                
                # 处理preflop行动分类逻辑
                self._classify_preflop_action(action, player_name, player_position)
                
                # 跟踪活跃的玩家(没有弃牌的玩家)
                if 'folds' in action:
                    # 如果玩家弃牌，确保他们不在活跃玩家列表中
                    if player_name in self.active_players_at_flop:
                        self.active_players_at_flop.remove(player_name)
                else:
                    # 如果玩家没有弃牌，添加到活跃玩家列表中
                    if player_name not in self.active_players_at_flop:
                        self.active_players_at_flop.append(player_name)
                        
                # 更新翻前底池
                self.hand_data['preflop_pot'] = round(self.convert_to_bb(self.current_pot), 1)
                
            elif self.current_street == 'flop':
                # 处理flop行动
                if 'folds' in line or bet_amount > 0 or 'checks' in line:
                    self.hand_data['flop_actions'] += action + '; '
                    self.hand_data['flop_pot'] = round(self.convert_to_bb(self.current_pot), 1)
                    
            elif self.current_street == 'turn':
                # 处理turn行动
                if 'folds' in line or bet_amount > 0 or 'checks' in line:
                    self.hand_data['turn_actions'] += action + '; '
                    self.hand_data['turn_pot'] = round(self.convert_to_bb(self.current_pot), 1)
                    
            elif self.current_street == 'river':
                # 处理river行动
                if 'folds' in line or bet_amount > 0 or 'checks' in line:
                    self.hand_data['river_actions'] += action + '; '
                    self.hand_data['river_pot'] = round(self.convert_to_bb(self.current_pot), 1)
                    
            # 更新总底池
            self.hand_data['total_pot'] = round(self.convert_to_bb(self.current_pot), 1)
            
    def _classify_preflop_action(self, action, player_name, player_position):
        """分类翻前行动"""
        # 排除盲注行动
        if 'posts small blind' in action or 'posts big blind' in action:
            return
            
        # 检查行动类型
        is_raise = 'raises' in action
        is_call = 'calls' in action
        is_fold = 'folds' in action
        is_check = 'checks' in action
        is_hero = player_name == 'Hero'
        
        # 处理Hero的limp情况（在处理加注之前）
        if is_hero:
            # 如果Hero之前没有人加注，且Hero选择call，记为limp
            if is_call and not self.has_first_bet:
                self.hero_limped = True
                self.hero_limp_actions = [action]
                self.hand_data['preflop_action_limp'] = action
            
            # 如果Hero之前limp，且被加注后选择fold，记为limp-fold
            elif self.hero_limped and self.hero_limp_raised and is_fold:
                self.hero_limp_response = "fold"
                self.hand_data['preflop_action_limp_fold'] = action
                
            # 如果Hero之前limp，且被加注后选择call，记为limp-call
            elif self.hero_limped and self.hero_limp_raised and is_call:
                self.hero_limp_response = "call"
                self.hand_data['preflop_action_limp_call'] = action
        
        # 如果Hero已经limp，检查是否有人在Hero之后加注
        elif self.hero_limped and is_raise and not self.hero_limp_raised:
            self.hero_limp_raised = True
            self.hero_limp_actions.append(action)
            # 更新limp记录，包含加注信息
            self.hand_data['preflop_action_limp'] = '; '.join(self.hero_limp_actions)
        
        # 跟踪加注次数
        if is_raise:
            self.preflop_raise_count += 1
            
            # 处理第一个加注者 (first raise/open)
            if not self.has_first_bet:
                self.has_first_bet = True
                self.first_bet_player = player_name
                self.first_bet_actions = [action]
                self.hand_data['preflop_action_1st_bet'] = action
                
                # 记录第一个加注的位置(open position)
                self.open_position = player_position
                
                # 如果是Hero open，记录Hero的open位置
                if is_hero:
                    self.hand_data['hero_open_position'] = player_position
                    
            # 处理第二个加注者 (3-bet)
            elif self.has_first_bet and not self.has_three_bet:
                self.has_three_bet = True
                self.three_bet_player = player_name
                self.three_bet_actions = [action]
                self.hand_data['preflop_action_3B'] = action
                
                # 如果是Hero 3bet，记录Hero的3bet位置
                if is_hero:
                    self.hand_data['hero_3b_position'] = player_position
                    
            # 处理第三个加注者 (4-bet)
            elif self.has_three_bet and not self.has_four_bet:
                self.has_four_bet = True
                self.four_bet_player = player_name
                self.four_bet_actions = [action]
                self.hand_data['preflop_action_4B'] = action
                
            # 处理第四个加注者 (5-bet)
            elif self.has_four_bet and not self.has_five_bet:
                self.has_five_bet = True
                self.five_bet_player = player_name
                self.five_bet_actions = [action]
                self.hand_data['preflop_action_5B'] = action
                
        else:
            # 记录第一个加注者后的行动
            if self.has_first_bet and not self.has_three_bet:
                self.first_bet_actions.append(action)
                self.hand_data['preflop_action_1st_bet'] = '; '.join(self.first_bet_actions)
            
            # 记录3bet后的行动
            elif self.has_three_bet and not self.has_four_bet:
                self.three_bet_actions.append(action)
                self.hand_data['preflop_action_3B'] = '; '.join(self.three_bet_actions)
                
            # 记录4bet后的行动
            elif self.has_four_bet and not self.has_five_bet:
                self.four_bet_actions.append(action)
                self.hand_data['preflop_action_4B'] = '; '.join(self.four_bet_actions)
                
            # 记录5bet后的行动
            elif self.has_five_bet:
                self.five_bet_actions.append(action)
                self.hand_data['preflop_action_5B'] = '; '.join(self.five_bet_actions)
    
    def _update_pot_sizes(self):
        """更新所有街的底池大小"""
        if self.current_street == 'preflop':
            self.hand_data['preflop_pot'] = round(self.convert_to_bb(self.current_pot), 1)
        elif self.current_street == 'flop':
            self.hand_data['flop_pot'] = round(self.convert_to_bb(self.current_pot), 1)
        elif self.current_street == 'turn':
            self.hand_data['turn_pot'] = round(self.convert_to_bb(self.current_pot), 1)
        elif self.current_street == 'river':
            self.hand_data['river_pot'] = round(self.convert_to_bb(self.current_pot), 1)
        # 更新总底池
        self.hand_data['total_pot'] = round(self.convert_to_bb(self.current_pot), 1)
    
    def format_action(self, action: str) -> str:
        # 从动作文本中提取玩家名称
        player_match = re.match(r'^([^:]+):', action)
        if player_match:
            player_name = player_match.group(1).strip()
            if player_name == 'Hero':
                return action  # 如果是Hero的动作，保持不变
            elif player_name in self.player_positions:
                # 替换玩家名称为 Opp(位置)
                position = self.player_positions[player_name]
                return f"Opp({position})" + action[len(player_name):]
        return action

    def format_action_with_bb(self, action: str) -> str:
        """将动作中的金额转换为 BB 单位，并处理玩家名称"""
        player_match = re.match(r'^([^:]+):', action)
        if not player_match:
            return action
            
        player_name = player_match.group(1).strip()
        player_part = player_name
        # 修改：为Hero添加位置信息
        if player_name == 'Hero':
            if 'Hero' in self.player_positions:
                player_part = f"Hero({self.player_positions['Hero']})"
        elif player_name in self.player_positions:
            player_part = f"Opp({self.player_positions[player_name]})"
            
        action_part = action[len(player_name)+1:].strip()
        
        if 'BB' in action_part:
            if 'raises' in action_part:
                match = re.search(r'raises [\d.]+BB to ([\d.]+)BB', action_part)
                if match:
                    return f"{player_part}: raises {match.group(1)}BB"
            return f"{player_part}: {action_part}"
            
        if 'raises' in action_part:
            match = re.search(r'raises \$([\d.]+) to \$([\d.]+)', action_part)
            if match:
                to_amount = float(match.group(2))
                return f"{player_part}: raises {self.convert_to_bb(to_amount):.1f}BB"
        elif 'calls' in action_part:
            match = re.search(r'calls \$([\d.]+)', action_part)
            if match:
                amount = float(match.group(1))
                return f"{player_part}: calls {self.convert_to_bb(amount):.1f}BB"
        elif 'bets' in action_part:
            match = re.search(r'bets \$([\d.]+)', action_part)
            if match:
                amount = float(match.group(1))
                return f"{player_part}: bets {self.convert_to_bb(amount):.1f}BB"
        elif 'checks' in action_part:
            return f"{player_part}: checks"
        elif 'folds' in action_part:
            return f"{player_part}: folds"
            
        return action

    def extract_bet_amount(self, action: str) -> float:
        """从动作中提取投注金额"""
        # 处理美元单位的情况
        if 'raises' in action:
            match = re.search(r'raises \$[\d.]+ to \$([\d.]+)', action)
            if match:
                return float(match.group(1))
        elif 'calls' in action:
            match = re.search(r'calls \$([\d.]+)', action)
            if match:
                return float(match.group(1))
        elif 'bets' in action:
            match = re.search(r'bets \$([\d.]+)', action)
            if match:
                return float(match.group(1))
        return 0.0
    
    def parse_result(self, line: str):
        # 记录总底池
        if 'Total pot' in line:
            total_pot_match = re.search(r'Total pot \$([\d.]+)', line)
            if total_pot_match:
                pot_amount = float(total_pot_match.group(1))
                self.hand_data['total_pot'] = round(self.convert_to_bb(pot_amount), 1)
                
                # 如果到这里 result 还没有设置，说明 Hero 没赢钱，记录损失的金额
                if not self.hand_data['result']:
                    hero_bet_bb = round(self.convert_to_bb(self.hero_total_bet), 1)
                    if hero_bet_bb > 0:
                        self.hand_data['result'] = f"-{hero_bet_bb}BB"
                    else:
                        self.hand_data['result'] = "0BB"
        
        # 只记录 Hero 赢得的金额
        elif 'Hero collected' in line:
            collected_match = re.search(r'Hero collected \$([\d.]+)', line)
            if collected_match:
                collected_amount = float(collected_match.group(1))
                # 正确计算净赢取金额（赢得金额减去投入金额）
                won_amount = round(self.convert_to_bb(collected_amount - self.hero_total_bet), 1)
                self.hand_data['result'] = f"{won_amount}BB"
    
    def _determine_position_types(self):
        """确定Hero的位置类型和底池类型信息"""
        # 判断底池类型，根据加注次数
        if self.preflop_raise_count == 1:
            self.hand_data['pot_type'] = 'SRP'  # 单加注底池
        elif self.preflop_raise_count == 2:
            self.hand_data['pot_type'] = '3B'   # 3B底池
        elif self.preflop_raise_count == 3:
            self.hand_data['pot_type'] = '4B'   # 4B底池
        elif self.preflop_raise_count >= 4:
            self.hand_data['pot_type'] = '5B'   # 5B底池
        else:
            self.hand_data['pot_type'] = 'limped'  # 无人加注的底池
            
        # 判断最终底池类型
        if len(self.active_players_at_flop) > 2:
            self.hand_data['final_pot_type'] = 'multi'
        elif len(self.active_players_at_flop) == 2:
            self.hand_data['final_pot_type'] = '1v1'
        else:
            # 如果活跃玩家少于2人，说明所有人都弃牌了
            self.hand_data['final_pot_type'] = 'fold'
            
        # 判断Hero最终位置类型：IP/OOP/NA
        # 如果Hero没有参与底池，设置为NA
        if not self.hero_entered_pot:
            self.hand_data['hero_position_type'] = 'NA'
            return
            
        # 如果只有Hero一个人到达翻牌圈，设置为IP
        if len(self.active_players_at_flop) == 1 and self.active_players_at_flop[0] == 'Hero':
            self.hand_data['hero_position_type'] = 'IP'
            return
            
        # 如果Hero有参与底池但没有到达翻牌圈，查看最后的位置
        if 'Hero' not in self.active_players_at_flop:
            # 尝试根据行动顺序判断
            # 暂时标记为NA
            self.hand_data['hero_position_type'] = 'NA'
            return
            
        # 如果有多个玩家，检查hero是否是最后行动的玩家(在位置)
        hero_position = self.player_positions.get('Hero', '')
        if not hero_position:
            self.hand_data['hero_position_type'] = 'NA'
            return
            
        # 位置顺序 (从早到晚): SB->BB->UTG->MP->CO->BTN
        position_order = ['SB', 'BB', 'UTG', 'MP', 'CO', 'BTN']
        
        # 获取所有活跃玩家的位置
        active_positions = []
        for player in self.active_players_at_flop:
            pos = self.player_positions.get(player, '')
            if pos:
                active_positions.append(pos)
        
        # 如果没有足够位置信息，返回NA
        if not active_positions:
            self.hand_data['hero_position_type'] = 'NA'
            return
        
        # 检查Hero是否在最后位置（IP）
        # 如果Hero在BTN，且还在游戏中，那Hero总是IP
        if hero_position == 'BTN' and 'Hero' in self.active_players_at_flop:
            self.hand_data['hero_position_type'] = 'IP'
            return
        
        # 简化判断：如果只有两个玩家进入翻牌圈，则根据位置顺序确定
        if len(self.active_players_at_flop) == 2:
            other_player = [p for p in self.active_players_at_flop if p != 'Hero'][0]
            other_position = self.player_positions.get(other_player, '')
            
            if not other_position:
                self.hand_data['hero_position_type'] = 'NA'
                return
                
            hero_index = position_order.index(hero_position) if hero_position in position_order else -1
            other_index = position_order.index(other_position) if other_position in position_order else -1
            
            if hero_index > other_index:
                self.hand_data['hero_position_type'] = 'IP'  # Hero在晚位
            else:
                self.hand_data['hero_position_type'] = 'OOP'  # Hero在早位
        else:
            # 多人底池情况下，判断Hero是否是最后行动的玩家
            # 这里简化为：如果Hero的位置最靠后，则是IP
            max_position_index = max([position_order.index(pos) for pos in active_positions if pos in position_order], default=-1)
            hero_position_index = position_order.index(hero_position) if hero_position in position_order else -1
            
            if hero_position_index == max_position_index:
                self.hand_data['hero_position_type'] = 'IP'
            else:
                self.hand_data['hero_position_type'] = 'OOP'

    def parse_hand(self, hand_text: str) -> Dict:
        self.reset()
        lines = hand_text.split('\n')
        
        # 第一次遍历，优先处理盲注信息
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 解析大小盲注金额，最先处理这个
            if 'Hold\'em No Limit' in line:
                match = re.search(r'Hold\'em No Limit \(\$([\d.]+)/\$([\d.]+)\)', line)
                if match:
                    self.sb_amount = float(match.group(1))
                    self.bb_amount = float(match.group(2))
                    if self.bb_amount <= 0:  # 防止除零错误
                        self.bb_amount = 0.05
                    self.hand_data['SB_BB'] = f"${self.sb_amount}/${self.bb_amount}"
                    break  # 找到盲注信息后立即退出
        
        # 主要处理逻辑
        i = 0
        in_preflop_section = False  # 标记是否正在处理翻前部分
        
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            # 识别翻前部分的开始和结束
            if '*** HOLE CARDS ***' in line:
                in_preflop_section = True
                self.current_street = 'preflop'
            elif '*** FLOP ***' in line:
                in_preflop_section = False
                self.current_street = 'flop'
            
            self.parse_hand_id(line)
            self.parse_hero_info(line)
            self.parse_players_positions(line)  # 添加解析玩家位置
            self.parse_hero_cards(line)
            self.parse_board_cards(line)
            
            # 只在翻前部分处理行动
            if in_preflop_section:
                # 检查是否有未被跟注的投注返还
                if 'Uncalled bet' in line and 'returned' in line:
                    match = re.search(r'Uncalled bet \(\$([\d.]+)\)', line)
                    if match:
                        returned_amount = float(match.group(1))
                        # 从底池中减去返还的金额
                        self.current_pot -= returned_amount
                        # 如果是返还给 Hero，也要从 Hero 的总投注中减去
                        if 'returned to Hero' in line:
                            self.hero_total_bet -= returned_amount
                        # 更新当前街的底池大小
                        self._update_pot_sizes()
                else:
                    self.parse_action(line)
            else:
                # 非翻前部分，正常处理其他街的动作和结果
                if 'Uncalled bet' in line and 'returned' in line:
                    match = re.search(r'Uncalled bet \(\$([\d.]+)\)', line)
                    if match:
                        returned_amount = float(match.group(1))
                        self.current_pot -= returned_amount
                        if 'returned to Hero' in line:
                            self.hero_total_bet -= returned_amount
                        self._update_pot_sizes()
                else:
                    self.parse_action(line)
                
            self.parse_result(line)
            i += 1
        
        # 确保SB_BB已设置（即使未找到盲注信息也使用默认值）
        if not self.hand_data['SB_BB']:
            self.hand_data['SB_BB'] = f"${self.sb_amount}/${self.bb_amount}"
            
        # 在处理完所有行后，确定位置和底池类型
        self._determine_position_types()
            
        return self.hand_data

def process_poker_file(input_file: str, output_file: str):
    parser = PokerHandParser()
    current_hand = []
    all_hands = []
    
    print(f"Processing file: {input_file}")  # Debug info
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                current_hand.append(line)
            elif current_hand:
                hand_text = ''.join(current_hand)
                print("\nProcessing new hand...")  # Debug info
                hand_data = parser.parse_hand(hand_text)
                # 添加 BB 单位到所有底池值
                for key in ['preflop_pot', 'flop_pot', 'turn_pot', 'river_pot', 'total_pot']:
                    if hand_data[key] > 0:
                        hand_data[key] = f"{hand_data[key]}BB"
                    else:
                        hand_data[key] = "0BB"
                all_hands.append(hand_data)
                current_hand = []
    
    # Process last hand if exists
    if current_hand:
        hand_text = ''.join(current_hand)
        print("\nProcessing last hand...")  # Debug info
        hand_data = parser.parse_hand(hand_text)
        # 添加 BB 单位到所有底池值
        for key in ['preflop_pot', 'flop_pot', 'turn_pot', 'river_pot', 'total_pot']:
            if hand_data[key] > 0:
                hand_data[key] = f"{hand_data[key]}BB"
            else:
                hand_data[key] = "0BB"
        all_hands.append(hand_data)
    
    print(f"\nTotal hands processed: {len(all_hands)}")  # Debug info
    
    # Write to CSV with custom header
    if all_hands:
        fieldnames = list(all_hands[0].keys())
        # 创建自定义标题映射
        custom_headers = {
            'result': 'Result(Hero)',
            'total_pot': 'Total_Pot',
            'preflop_pot': 'Preflop_Pot',
            'flop_pot': 'Flop_Pot',
            'turn_pot': 'Turn_Pot',
            'river_pot': 'River_Pot'
        }
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                # 写入自定义标题
                header_row = {field: custom_headers.get(field, field) for field in fieldnames}
                writer.writerow(header_row)
                writer.writerows(all_hands)
                print(f"Data written to {output_file}")  # Debug info
        except PermissionError:
            # 如果有权限问题，尝试写入到当前目录
            alt_output_file = 'parsed_hands.csv'
            with open(alt_output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                header_row = {field: custom_headers.get(field, field) for field in fieldnames}
                writer.writerow(header_row)
                writer.writerows(all_hands)
                print(f"权限问题，数据已写入到当前目录: {alt_output_file}")

def test_case():
    """测试用例，用于验证新增字段的功能"""
    # 创建一个简单的测试用例
    test_hand = """Poker Hand #10933657-19873-1698906989 - Hold'em No Limit ($0.02/$0.05)
Table 'Seokguram' 9-max Seat #1 is the button
Seat 1: Player1 ($5.72 in chips) 
Seat 2: Player2 ($4.30 in chips) 
Seat 3: Player3 ($5.00 in chips) 
Seat 4: Player4 ($4.03 in chips) 
Seat 5: Hero ($4.99 in chips) 
Seat 6: Player6 ($5.10 in chips) 
Player2: posts small blind $0.02
Player3: posts big blind $0.05
*** HOLE CARDS ***
Dealt to Hero [As Kd]
Player4: folds
Hero: raises $0.10 to $0.15
Player6: folds
Player1: folds
Player2: calls $0.13
Player3: calls $0.10
*** FLOP *** [2c 7h Ks]
Player2: checks
Player3: checks
Hero: bets $0.25
Player2: folds
Player3: calls $0.25
*** TURN *** [2c 7h Ks] [8d]
Player3: checks
Hero: checks
*** RIVER *** [2c 7h Ks 8d] [3c]
Player3: checks
Hero: bets $0.61
Player3: folds
Uncalled bet ($0.61) returned to Hero
Hero collected $0.82 from pot
*** SUMMARY ***
Total pot $0.82 | Rake $0.00 
Board [2c 7h Ks 8d 3c]
Seat 1: Player1 (button) folded before Flop (didn't bet)
Seat 2: Player2 (small blind) folded on the Flop
Seat 3: Player3 (big blind) folded on the River
Seat 4: Player4 folded before Flop (didn't bet)
Seat 5: Hero showed and won ($0.82) with One pair, Kings
Seat 6: Player6 folded before Flop (didn't bet)"""
    
    # 解析测试手牌
    parser = PokerHandParser()
    hand_data = parser.parse_hand(test_hand)
    
    # 显示测试结果
    print("\n测试单手牌解析结果:")
    for key, value in hand_data.items():
        if key in ['hero_position', 'hero_position_type', 'hero_open_position', 'hero_3b_position', 
                   'pot_type', 'hero_squeeze', 'final_pot_type']:
            print(f"{key}: {value}")
    
    print("\n请创建输入文件后再运行程序。")

if __name__ == '__main__':
    import os
    # 确保输入和输出目录存在
    os.makedirs('poker_input', exist_ok=True)
    os.makedirs('poker_output', exist_ok=True)
    
    # 使用绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, 'poker_input', 'combined_1.txt')
    output_file = os.path.join(current_dir, 'poker_output', 'parsed_hands.csv')
    
    # 检查输入文件是否存在
    if os.path.exists(input_file):
        try:
            process_poker_file(input_file, output_file)
            print(f"处理完成。结果已保存到 {output_file}")
        except Exception as e:
            print(f"处理过程中发生错误: {e}")
            # 当发生错误时，尝试使用测试用例
            print("使用测试用例进行验证...")
            test_case()
    else:
        print(f"错误：输入文件 {input_file} 不存在。")
        # 当没有输入文件时，使用测试用例
        test_case()