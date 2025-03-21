import re
import csv
from typing import Dict, List, Optional
import datetime
import os

class PokerHandParser:
    def __init__(self):
        self.hand_data = {
            'hand_id': '',
            'date_and_time': '',
            'table_name': '',
            'hero_position': '',
            'hero_position_type': '',  # 新增：IP/OOP/NA
            'hero_open_position': '',  # 新增：记录Hero open位置
            'hero_3b_position': '',    # 新增：记录Hero 3B位置
            'pot_type': '',           # 新增：底池类型(SRP/3B/4B/5B)
            'hero_squeeze': 'NO',     # 新增：Hero是否squeeze
            'final_pot_type': '',     # 新增：最终底池类型(1v1/multi)
            'table_size': 0,
            'stakes': '',
            'total_pot': 0,
            'preflop_pot': 0,
            'flop_pot': 0,
            'turn_pot': 0,
            'river_pot': 0,
            'cash_drop': '',  # 红包降落
            'rake': 0.0,
            'hero_cards': '',
            'board_cards': '',
            'player_cards': '',
            'hero_action': '',
            'preflop_actions': '',
            'preflop_action_1st_bet': '',  # 新增：只记录raises和calls，到第二个raises前
            'preflop_action_3B': '',  # 新增：只记录raises和calls，到第三个raises前
            'preflop_action_4B': '',  # 新增：只记录raises和calls，到第四个raises前
            'preflop_action_5B': '',  # 新增：只记录raises和calls
            'preflop_action_limp': '',  # 新增：Hero跟注
            'preflop_action_limp_fold': '',  # 新增：Hero跟注后弃牌
            'preflop_action_limp_call': '',  # 新增：Hero跟注后被加注，然后跟注
            'flop_actions': '',
            'turn_actions': '',
            'river_actions': '',
            'preflop_description': '',
            'hand_result': '',
            'hand_won': False,
            'hand_profit': 0.0,
            'hero_stack': 0.0
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
        self.sb_amount = 0.0
        self.bb_amount = 0.0
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
        self.hero_squeeze_action = False  # hero是否进行了挤压加注
        
        # 新增变量
        self.preflop_raise_count = 0
        self.open_position = ''
        
        # 新增变量
        self.street_boundary_mode = False
    
    def reset(self):
        # 重置手牌数据为默认值
        self.hand_data = {
            'hand_id': '',
            'date_and_time': '',
            'table_name': '',
            'hero_position': '',
            'hero_position_type': '',  # 新增：IP/OOP/NA
            'hero_open_position': '',  # 新增：记录Hero open位置
            'hero_3b_position': '',    # 新增：记录Hero 3B位置
            'pot_type': '',           # 新增：底池类型(SRP/3B/4B/5B)
            'hero_squeeze': 'NO',     # 新增：Hero是否squeeze
            'final_pot_type': '',     # 新增：最终底池类型(1v1/multi)
            'table_size': 0,
            'stakes': '',
            'total_pot': 0,
            'preflop_pot': 0,
            'flop_pot': 0,
            'turn_pot': 0,
            'river_pot': 0,
            'cash_drop': '',
            'rake': 0.0,
            'hero_cards': '',
            'board_cards': '',
            'player_cards': '',
            'hero_action': '',
            'preflop_actions': '',
            'preflop_action_1st_bet': '',  # 新增：只记录raises和calls，到第二个raises前
            'preflop_action_3B': '',  # 新增：只记录raises和calls，到第三个raises前
            'preflop_action_4B': '',  # 新增：只记录raises和calls，到第四个raises前
            'preflop_action_5B': '',  # 新增：只记录raises和calls
            'preflop_action_limp': '',  # 新增：Hero跟注
            'preflop_action_limp_fold': '',  # 新增：Hero跟注后弃牌
            'preflop_action_limp_call': '',  # 新增：Hero跟注后被加注，然后跟注
            'flop_actions': '',
            'turn_actions': '',
            'river_actions': '',
            'preflop_description': '',
            'hand_result': '',
            'hand_won': False,
            'hand_profit': 0.0,
            'hero_stack': 0.0
        }
        
        # 重置其他跟踪信息
        self.hero_total_bet = 0.0
        self.db_amount = 0.0
        self.bb_amount = 0.0
        self.sb_amount = 0.0
        self.current_pot = 0.0
        self.current_street = ''
        self.last_bet_amount = 0.0
        self.last_bet_player = ''
        self.player_positions = {}
        self.bb_player = ''
        self.has_first_bet = False
        self.has_three_bet = False
        self.first_bet_position = ''
        self.three_bet_position = ''
        self.hero_entered_pot = False  # 新增：跟踪Hero是否进入底池
        self.open_position = ''
        self.preflop_all_actions = []
        self.preflop_raise_count = 0
        self.active_players_at_flop = []  # 新增：跟踪到达翻牌圈的活跃玩家
        self.hero_squeeze_opportunity = False  # 新增：是否有squeeze机会
        self.hero_squeeze_action = False  # 新增：Hero是否进行了squeeze
        self.button_seat = 0  # 新增：按钮位置
        self.hand_text = ""  # 新增：手牌文本
        
        # 重置Street界限模式
        self.street_boundary_mode = False
    
    def parse_hand_id(self, line: str):
        """解析手牌ID，包括游戏类型和盲注信息"""
        if 'Poker Hand #' in line:
            # 提取手牌ID
            self.hand_data['hand_id'] = line.strip()
            
            # 尝试提取时间信息
            try:
                # 时间通常在手牌ID后面的括号中，如 Poker Hand #12345678-12345-1234567890 - ...
                match = re.search(r'Poker Hand #.*-.*-(.*) -', line)
                if match:
                    timestamp = int(match.group(1))
                    date_time = datetime.datetime.fromtimestamp(timestamp)
                    self.hand_data['date_and_time'] = date_time.strftime('%Y-%m-%d %H:%M:%S')
            except:
                pass
                
            # 尝试提取游戏类型和盲注信息
            match = re.search(r'Hold\'em No Limit \(\$([\d.]+)/\$([\d.]+)\)', line)
            if match:
                self.sb_amount = float(match.group(1))
                self.bb_amount = float(match.group(2))
                self.hand_data['stakes'] = f"${self.sb_amount}/${self.bb_amount}"
                
            # 尝试提取桌子名称
            match = re.search(r"Table '([^']+)'", line)
            if match:
                self.hand_data['table_name'] = match.group(1)
                
            # 尝试提取桌子大小
            match = re.search(r"Table '[^']+' (\d+)-max", line)
            if match:
                self.hand_data['table_size'] = int(match.group(1))
    
    def parse_seat(self, line: str):
        """解析座位信息，包括玩家名称、位置和筹码"""
        if 'Seat' in line and ':' in line and 'chips' in line:
            # 提取座位号
            seat_match = re.search(r'Seat (\d+):', line)
            if not seat_match:
                return
                
            seat_number = int(seat_match.group(1))
            
            # 提取玩家名称
            player_match = re.search(r'Seat \d+: ([^(]+)', line)
            if not player_match:
                return
                
            player_name = player_match.group(1).strip()
            
            # 提取玩家筹码
            chips_match = re.search(r'\(\$([\d.]+) in chips\)', line)
            if not chips_match:
                return
                
            chips_amount = float(chips_match.group(1))
            
            # 如果是Hero，记录筹码数
            if player_name == 'Hero':
                hero_stack_bb = round(self.convert_to_bb(chips_amount), 1)
                self.hand_data['hero_stack'] = hero_stack_bb
        
        # 检查是否有按钮位置信息
        if 'button' in line:
            button_match = re.search(r'Seat #(\d+) is the button', line)
            if button_match:
                self.button_seat = int(button_match.group(1))
                
    def _assign_positions(self):
        """根据按钮位置为所有玩家分配位置"""
        # 检查是否已经有了按钮位置
        if not hasattr(self, 'button_seat') or not hasattr(self, 'hand_text'):
            return
            
        button_seat = self.button_seat
        
        # 从hand_text中找出所有玩家的座位信息
        seat_players = {}
        for line in self.hand_text.split('\n'):
            if 'Seat' in line and ':' in line and 'chips' in line:
                seat_match = re.search(r'Seat (\d+): ([^(]+)', line)
                if seat_match:
                    seat_num = int(seat_match.group(1))
                    player_name = seat_match.group(2).strip()
                    seat_players[seat_num] = player_name
        
        # 获取桌子总大小
        table_size = len(seat_players)
        self.hand_data['table_size'] = table_size  # 更新桌子大小
        
        # 位置映射表
        positions = {
            9: ['BTN', 'SB', 'BB', 'UTG', 'UTG+1', 'MP', 'MP+1', 'HJ', 'CO'],  # 9人桌
            8: ['BTN', 'SB', 'BB', 'UTG', 'UTG+1', 'MP', 'HJ', 'CO'],          # 8人桌
            7: ['BTN', 'SB', 'BB', 'UTG', 'MP', 'HJ', 'CO'],                   # 7人桌
            6: ['BTN', 'SB', 'BB', 'UTG', 'MP', 'CO'],                         # 6人桌
            5: ['BTN', 'SB', 'BB', 'UTG', 'CO'],                               # 5人桌
            4: ['BTN', 'SB', 'BB', 'CO'],                                       # 4人桌
            3: ['BTN', 'SB', 'BB'],                                             # 3人桌
            2: ['BTN/SB', 'BB']                                                 # 2人桌
        }
        
        # 使用与桌子大小对应的位置列表
        table_positions = positions.get(table_size, positions[9][:table_size])
        
        # 从按钮开始依次分配位置
        seat_nums_sorted = sorted(seat_players.keys())
        
        # 找到按钮在排序座位中的索引
        button_index = seat_nums_sorted.index(button_seat) if button_seat in seat_nums_sorted else 0
        
        # 按照从按钮开始的顺序分配位置
        for i in range(table_size):
            seat_index = (button_index + i) % table_size
            seat_num = seat_nums_sorted[seat_index]
            player_name = seat_players[seat_num]
            
            # 分配位置
            position = table_positions[i]
            self.player_positions[player_name] = position
            
            # 如果是Hero，记录Hero的位置
            if player_name == 'Hero':
                self.hand_data['hero_position'] = position
    
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
        """解析Hero的手牌"""
        if 'Hero cards:' in line:
            cards_match = re.search(r'Hero cards: (.+)', line)
            if cards_match:
                self.hand_data['hero_cards'] = cards_match.group(1).strip()
                
    def parse_board_cards(self, line: str):
        if '*** FLOP ***' in line:
            self.current_street = 'flop'
            self.hand_data['preflop_pot'] = round(self.convert_to_bb(self.current_pot), 1)  # 记录preflop底池
            cards = re.search(r'\[(.*?)\]', line)
            if cards:
                self.hand_data['board_cards'] = cards.group(1)
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
            player_name = line.split(':')[0].strip()
            player_position = self.player_positions.get(player_name, "")
            bet_amount = self.extract_bet_amount(line.strip())
            is_hero = player_name == 'Hero'
            
            # 格式化行动信息
            action = self.format_action_with_bb(line.strip())
            
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
                self.preflop_all_actions.append(action)  # 确保使用格式化后的行动
                self.hand_data['preflop_actions'] = '; '.join(self.preflop_all_actions)
                
                # 跟踪Hero是否进入底池
                if is_hero and ('calls' in action or 'raises' in action or 'bets' in action):
                    self.hero_entered_pot = True
                
                # 跟踪squeeze机会(有人加注且有人跟注后)
                if self.has_first_bet and 'calls' in action and not self.has_three_bet:
                    self.hero_squeeze_opportunity = True
                
                # 检查是否是Hero的squeeze加注
                if is_hero and 'raises' in action and self.hero_squeeze_opportunity and not self.has_three_bet:
                    self.hero_squeeze_action = True
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
                    if not self.hand_data['flop_actions']:
                        self.hand_data['flop_actions'] = action
                    else:
                        self.hand_data['flop_actions'] += '; ' + action
                    self.hand_data['flop_pot'] = round(self.convert_to_bb(self.current_pot), 1)
                    
            elif self.current_street == 'turn':
                # 处理turn行动
                if 'folds' in line or bet_amount > 0 or 'checks' in line:
                    if not self.hand_data['turn_actions']:
                        self.hand_data['turn_actions'] = action
                    else:
                        self.hand_data['turn_actions'] += '; ' + action
                    self.hand_data['turn_pot'] = round(self.convert_to_bb(self.current_pot), 1)
                    
            elif self.current_street == 'river':
                # 处理river行动
                if 'folds' in line or bet_amount > 0 or 'checks' in line:
                    if not self.hand_data['river_actions']:
                        self.hand_data['river_actions'] = action
                    else:
                        self.hand_data['river_actions'] += '; ' + action
                    self.hand_data['river_pot'] = round(self.convert_to_bb(self.current_pot), 1)
                    
            # 更新总底池
            self.hand_data['total_pot'] = round(self.convert_to_bb(self.current_pot), 1)
            
    def _classify_preflop_action(self, action: str, player_name: str, player_position: str):
        """分类翻前行动，并跟踪加注次数"""
        is_hero = player_name == 'Hero'
        
        # 跟踪玩家行动类型
        is_raise = 'raises' in action
        is_call = 'calls' in action
        is_fold = 'folds' in action
        is_check = 'checks' in action
        
        # 确保action已经是格式化后的，如果不是则格式化
        if player_name in self.player_positions:
            # 检查action是否已经包含"Opp("或"Hero("
            if not action.startswith('Opp(') and not action.startswith('Hero('):
                # 进行格式化
                if is_hero:
                    formatted_player = f"Hero({self.player_positions[player_name]})"
                else:
                    formatted_player = f"Opp({self.player_positions[player_name]})"
                action = action.replace(player_name + ":", formatted_player + ":")
        
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
        
        if 'raises' in action:
            self.preflop_raise_count += 1
            
            # 记录第一个加注者 (first raise/open)
            if not self.has_first_bet:
                self.has_first_bet = True
                self.first_bet_position = player_position
                # 记录open位置
                self.open_position = player_position
                
                if is_hero:
                    self.hand_data['hero_open_position'] = player_position
                
                # 添加到first_bet记录
                self.first_bet_actions = [action]
                self.hand_data['preflop_action_1st_bet'] = action
                    
            # 记录第二个加注者 (3-bet)
            elif self.has_first_bet and not self.has_three_bet:
                self.has_three_bet = True
                self.three_bet_position = player_position
                
                if is_hero:
                    self.hand_data['hero_3b_position'] = player_position
                
                # 添加到3B记录
                self.three_bet_actions = [action]
                self.hand_data['preflop_action_3B'] = action
                
            # 记录第三个加注者 (4-bet)
            elif self.has_three_bet and not self.has_four_bet:
                self.has_four_bet = True
                self.four_bet_player = player_name
                
                # 添加到4B记录
                self.four_bet_actions = [action]
                self.hand_data['preflop_action_4B'] = action
                
            # 记录第四个加注者 (5-bet)
            elif self.has_four_bet and not self.has_five_bet:
                self.has_five_bet = True
                self.five_bet_player = player_name
                
                # 添加到5B记录
                self.five_bet_actions = [action]
                self.hand_data['preflop_action_5B'] = action
                
            # Hero行动分析
            if is_hero:
                # 依据当前加注次数进行分类
                if self.preflop_raise_count == 1:
                    self.hand_data['hero_action'] = 'OPEN'
                elif self.preflop_raise_count == 2:
                    self.hand_data['hero_action'] = '3BET'
                    self.hand_data['hero_3b_position'] = player_position  # 确保设置3B位置
                elif self.preflop_raise_count == 3:
                    self.hand_data['hero_action'] = '4BET'
                elif self.preflop_raise_count >= 4:
                    self.hand_data['hero_action'] = '5BET+'
                
        # 处理calls、folds和checks等非加注行动
        else:
            # 根据当前翻前加注状态，将行动添加到对应的区块
            if self.has_first_bet and not self.has_three_bet:
                # 添加到1st_bet后的行动
                self.first_bet_actions.append(action)
                self.hand_data['preflop_action_1st_bet'] = '; '.join(self.first_bet_actions)
            elif self.has_three_bet and not self.has_four_bet:
                # 添加到3B后的行动
                self.three_bet_actions.append(action)
                self.hand_data['preflop_action_3B'] = '; '.join(self.three_bet_actions)
            elif self.has_four_bet and not self.has_five_bet:
                # 添加到4B后的行动
                self.four_bet_actions.append(action)
                self.hand_data['preflop_action_4B'] = '; '.join(self.four_bet_actions)
            elif self.has_five_bet:
                # 添加到5B后的行动
                self.five_bet_actions.append(action)
                self.hand_data['preflop_action_5B'] = '; '.join(self.five_bet_actions)
                
            # 对Hero跟注的行为分析
            if is_hero and is_call:
                if not self.has_first_bet:
                    # 前面无人加注，这是limping
                    self.hand_data['hero_action'] = 'LIMP'
                elif self.has_first_bet and not self.has_three_bet:
                    # 前面已有人加注，这是call一个raise
                    self.hand_data['hero_action'] = 'CALL_R'
                elif self.has_three_bet:
                    # 前面已有3bet，这是call一个3bet
                    self.hand_data['hero_action'] = 'CALL_3B'
            
            # 对Hero弃牌的行为分析
            elif is_hero and is_fold:
                if not self.has_first_bet:
                    # 前面无人加注就弃牌(很少见)
                    self.hand_data['hero_action'] = 'FOLD'
                elif self.has_first_bet and not self.has_three_bet:
                    # 面对一个加注弃牌
                    self.hand_data['hero_action'] = 'FOLD_R'
                elif self.has_three_bet:
                    # 面对3bet弃牌
                    self.hand_data['hero_action'] = 'FOLD_3B'
                    
            # 对Hero检查的行为分析
            elif is_hero and is_check:
                # 检查行为通常只在大盲位置免费看牌
                self.hand_data['hero_action'] = 'CHECK'
    
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
        
        # 格式化玩家名称
        if player_name == 'Hero':
            # 确保Hero位置信息已经设置
            if player_name in self.player_positions and self.player_positions[player_name]:
                player_part = f"Hero({self.player_positions[player_name]})"
            else:
                player_part = "Hero"
        else:
            # 对于非Hero玩家，显示为Opp(位置)
            if player_name in self.player_positions and self.player_positions[player_name]:
                player_part = f"Opp({self.player_positions[player_name]})"
            else:
                player_part = player_name
            
        action_part = action[len(player_name)+1:].strip()
        
        # 处理已经是BB单位的情况
        if 'BB' in action_part:
            if 'raises' in action_part:
                match = re.search(r'raises [\d.]+BB to ([\d.]+)BB', action_part)
                if match:
                    return f"{player_part}: raises {match.group(1)}BB"
            return f"{player_part}: {action_part}"
            
        # 将美元金额转换为BB单位
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
            
        # 默认情况
        return f"{player_part}: {action_part}"

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
                if not self.hand_data['hand_result']:
                    hero_bet_bb = round(self.convert_to_bb(self.hero_total_bet), 1)
                    if hero_bet_bb > 0:
                        self.hand_data['hand_result'] = f"-{hero_bet_bb}BB"
                    else:
                        self.hand_data['hand_result'] = "0BB"
        
        # 只记录 Hero 赢得的金额
        elif 'Hero collected' in line:
            collected_match = re.search(r'Hero collected \$([\d.]+)', line)
            if collected_match:
                collected_amount = float(collected_match.group(1))
                # 正确计算净赢取金额（赢得金额减去投入金额）
                won_amount = round(self.convert_to_bb(collected_amount - self.hero_total_bet), 1)
                self.hand_data['hand_result'] = f"{won_amount}BB"
    
    def _determine_hero_position_types(self):
        """确定Hero的位置类型和底池类型信息"""
        # 如果Hero没有参与底池，将位置类型设置为NA
        if not self.hero_entered_pot:
            self.hand_data['hero_position_type'] = 'NA'
            return
            
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
            
        # 判断Hero加注位置
        if self.first_bet_position and self.first_bet_position == self.hand_data['hero_position']:
            self.hand_data['hero_open_position'] = self.hand_data['hero_position']
            
        if self.three_bet_position and self.three_bet_position == self.hand_data['hero_position']:
            self.hand_data['hero_3b_position'] = self.hand_data['hero_position']
            
        # 如果Hero的行动是3BET，确保设置3B位置
        if self.hand_data['hero_action'] == '3BET':
            self.hand_data['hero_3b_position'] = self.hand_data['hero_position']
            
        # 判断最终底池类型
        if len(self.active_players_at_flop) > 2:
            self.hand_data['final_pot_type'] = 'multi'
        elif len(self.active_players_at_flop) == 2:
            self.hand_data['final_pot_type'] = '1v1'
        else:
            # 如果活跃玩家少于2人，说明所有人都弃牌了
            self.hand_data['final_pot_type'] = 'fold'
            
        # 判断Hero最终位置类型：IP/OOP
        hero_position = self.hand_data['hero_position']
        # 如果Hero没有参与到翻牌圈，设置为NA
        if 'Hero' not in self.active_players_at_flop:
            self.hand_data['hero_position_type'] = 'NA'
            return
            
        # 如果只有Hero一个人到达翻牌圈，设置为IP
        if len(self.active_players_at_flop) == 1 and self.active_players_at_flop[0] == 'Hero':
            self.hand_data['hero_position_type'] = 'IP'
            return
            
        # 进行位置顺序判断
        position_order = ['SB', 'BB', 'UTG', 'UTG+1', 'MP', 'MP+1', 'HJ', 'CO', 'BTN']
        
        # 如果Hero是BTN且已经进入底池，则Hero在位置最后
        if hero_position == 'BTN' and 'Hero' in self.active_players_at_flop:
            self.hand_data['hero_position_type'] = 'IP'
            return
            
        # 如果只有两个玩家到达翻牌圈且Hero不是BTN，我们需要判断谁在最后位置
        active_positions = []
        for player in self.active_players_at_flop:
            pos = self.player_positions.get(player, '')
            if pos:
                active_positions.append(pos)
                
        # 如果没有足够的位置信息，默认为NA
        if len(active_positions) < 2:
            self.hand_data['hero_position_type'] = 'NA'
            return
            
        # 根据位置顺序判断谁是最后行动的玩家
        max_index = -1
        max_index_position = ''
        for pos in active_positions:
            if pos in position_order:
                pos_index = position_order.index(pos)
                if pos_index > max_index:
                    max_index = pos_index
                    max_index_position = pos
                    
        # 判断Hero是否是最后行动的玩家
        if hero_position == max_index_position:
            self.hand_data['hero_position_type'] = 'IP'
        else:
            self.hand_data['hero_position_type'] = 'OOP'

    def parse_hand(self, hand_text: str) -> Dict:
        """解析整个手牌文本并返回结果"""
        self.reset()
        
        # 保存手牌文本
        self.hand_text = hand_text
        
        # 首先处理座位和位置信息
        # 第一次遍历，获取按钮位置和玩家座位信息
        for line in hand_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # 检查按钮位置
            if 'button' in line:
                button_match = re.search(r'Seat #(\d+) is the button', line)
                if button_match:
                    self.button_seat = int(button_match.group(1))
            
            # 解析座位信息
            if 'Seat' in line and ':' in line and 'chips' in line:
                self.parse_seat(line)
        
        # 分配玩家位置，确保在解析行动前就有正确的位置信息
        self._assign_positions()
        
        # 第二次遍历，处理其他信息
        for line in hand_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # 解析手牌ID
            if 'Poker Hand #' in line:
                self.parse_hand_id(line)
                continue
                
            # 解析Hero信息
            if 'Hero cards' in line:
                self.parse_hero_cards(line)
                continue
                
            # 处理街段
            if '*** HOLE CARDS ***' in line:
                self.current_street = 'preflop'
                continue
                
            if '*** FLOP ***' in line:
                self.current_street = 'flop'
                cards = re.search(r'\[(.*?)\]', line)
                if cards:
                    self.hand_data['board_cards'] = cards.group(1)
                continue
                
            if '*** TURN ***' in line:
                self.current_street = 'turn'
                cards = re.search(r'\[(.*?)\]', line)
                if cards:
                    # 添加到之前的板面
                    self.hand_data['board_cards'] += ' ' + cards.group(1).split()[-1]
                continue
                
            if '*** RIVER ***' in line:
                self.current_street = 'river'
                cards = re.search(r'\[(.*?)\]', line)
                if cards:
                    # 添加到之前的板面
                    self.hand_data['board_cards'] += ' ' + cards.group(1).split()[-1]
                continue
                
            if '*** SUMMARY ***' in line:
                self.current_street = 'summary'
                continue
                
            # 处理赢牌结果
            if 'collected' in line and 'from pot' in line:
                self.parse_collected(line)
                continue
                
            # 处理各街段的行动
            self.parse_action(line)
                
        # 如果没有解析到玩家收集底池的信息，则假设玩家输掉投入的所有筹码
        if not self.hand_data['hand_result']:
            # 如果到这里 result 还没有设置，说明 Hero 没赢钱，记录损失的金额
            hero_bet_bb = round(self.convert_to_bb(self.hero_total_bet), 1)
            if hero_bet_bb > 0:
                self.hand_data['hand_result'] = f"-{hero_bet_bb}BB"
                self.hand_data['hand_profit'] = -hero_bet_bb
            else:
                self.hand_data['hand_result'] = "0BB"
                self.hand_data['hand_profit'] = 0
            
        # 确保stakes已设置（即使未找到盲注信息也使用默认值）
        if not self.hand_data['stakes']:
            self.hand_data['stakes'] = f"${self.sb_amount}/${self.bb_amount}"
            
        # 在处理完所有行后，确定位置和底池类型
        self._determine_hero_position_types()
            
        return self.hand_data

    def parse_collected(self, line: str):
        """解析收集底池信息"""
        if 'collected' in line and 'from pot' in line:
            # 提取玩家名
            player_name = line.split(' collected')[0].strip()
            
            # 提取收集的金额
            match = re.search(r'collected \$([\d.]+)', line)
            if not match:
                return
                
            collected_amount = float(match.group(1))
            
            # 如果是Hero收集底池，计算赢取金额
            if player_name == 'Hero':
                self.hand_data['hand_won'] = True
                # 正确计算净赢取金额（赢得金额减去投入金额）
                won_amount = round(self.convert_to_bb(collected_amount - self.hero_total_bet), 1)
                self.hand_data['hand_result'] = f"{won_amount}BB"
                self.hand_data['hand_profit'] = won_amount

def process_poker_file(input_file: str, output_file: str):
    parser = PokerHandParser()
    current_hand = []
    all_hands = []
    
    print(f"处理文件: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                current_hand.append(line)
            elif current_hand:
                hand_text = ''.join(current_hand)
                print("\n处理新手牌...")
                hand_data = parser.parse_hand(hand_text)
                # 将数字底池值转换为字符串格式
                for key in ['preflop_pot', 'flop_pot', 'turn_pot', 'river_pot', 'total_pot']:
                    if isinstance(hand_data[key], (int, float)) and hand_data[key] > 0:
                        hand_data[key] = f"{hand_data[key]}BB"
                    elif isinstance(hand_data[key], (int, float)):
                        hand_data[key] = "0BB"
                all_hands.append(hand_data)
                current_hand = []
    
    # 处理最后一手牌
    if current_hand:
        hand_text = ''.join(current_hand)
        print("\n处理最后一手牌...")
        hand_data = parser.parse_hand(hand_text)
        # 将数字底池值转换为字符串格式
        for key in ['preflop_pot', 'flop_pot', 'turn_pot', 'river_pot', 'total_pot']:
            if isinstance(hand_data[key], (int, float)) and hand_data[key] > 0:
                hand_data[key] = f"{hand_data[key]}BB"
            elif isinstance(hand_data[key], (int, float)):
                hand_data[key] = "0BB"
        all_hands.append(hand_data)
    
    print(f"\n共处理了 {len(all_hands)} 手牌")
    
    # 写入CSV文件，使用自定义标题
    if all_hands:
        fieldnames = list(all_hands[0].keys())
        # 创建自定义标题映射
        custom_headers = {
            'hand_result': 'Result(Hero)',
            'total_pot': 'Total_Pot',
            'preflop_pot': 'Preflop_Pot',
            'flop_pot': 'Flop_Pot',
            'turn_pot': 'Turn_Pot',
            'river_pot': 'River_Pot'
        }
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            # 写入自定义标题
            header_row = {field: custom_headers.get(field, field) for field in fieldnames}
            writer.writerow(header_row)
            writer.writerows(all_hands)
            print(f"数据已写入到 {output_file}")

def test_parser():
    """测试解析器功能"""
    parser = PokerHandParser()
    
    # 测试样例：一个包含各种情况的手牌记录
    test_hand_text = """Poker Hand #10933657-19873-1698906989 - Hold'em No Limit ($0.02/$0.05)
Table 'Seokguram' 9-max Seat #7 is the button
Seat 1: Player1 ($5.72 in chips) 
Seat 2: Player2 ($4.30 in chips) 
Seat 3: Hero ($5.00 in chips) 
Seat 4: Player4 ($4.03 in chips) 
Seat 5: Player5 ($4.99 in chips) 
Seat 6: Player6 ($5.10 in chips) 
Seat 7: Player7 ($5.00 in chips) 
Seat 8: Player8 ($5.65 in chips) 
Seat 9: Player9 ($5.02 in chips) 
Player8: posts small blind $0.02
Player9: posts big blind $0.05
*** HOLE CARDS ***
Hero cards: As Kd
Player1: folds
Player2: raises $0.10 to $0.15
Hero: raises $0.35 to $0.50
Player4: folds
Player5: folds
Player6: folds
Player7: folds
Player8: folds
Player9: calls $0.45
Player2: calls $0.35
*** FLOP *** [2c 7h Ks]
Player9: checks
Player2: checks
Hero: bets $0.52
Player9: folds
Player2: calls $0.52
*** TURN *** [2c 7h Ks] [8d]
Player2: checks
Hero: checks
*** RIVER *** [2c 7h Ks 8d] [3c]
Player2: checks
Hero: bets $1.30
Player2: folds
Uncalled bet ($1.30) returned to Hero
Hero collected $1.71 from pot
*** SUMMARY ***
Total pot $1.81 | Rake $0.10 
Board [2c 7h Ks 8d 3c]
Seat 1: Player1 folded before Flop (didn't bet)
Seat 2: Player2 folded River
Seat 3: Hero showed [As Kd] and won ($1.71) with One pair, Kings
Seat 4: Player4 folded before Flop (didn't bet)
Seat 5: Player5 folded before Flop (didn't bet)
Seat 6: Player6 folded before Flop (didn't bet)
Seat 7: Player7 (button) folded before Flop (didn't bet)
Seat 8: Player8 (small blind) folded before Flop
Seat 9: Player9 (big blind) folded on the Flop"""
    
    # 解析手牌
    result = parser.parse_hand(test_hand_text)
    
    # 打印结果
    print("解析结果:")
    for key, value in result.items():
        print(f"{key}: {value}")
    
    # 验证特定字段 - 更新为正确的位置
    assert result['hero_position'] == 'MP', f"Hero位置错误: {result['hero_position']}"
    assert result['hero_action'] == '3BET', f"Hero行动错误: {result['hero_action']}"
    assert result['pot_type'] == '3B', f"底池类型错误: {result['pot_type']}"
    assert result['hero_position_type'] in ['IP', 'OOP', 'NA'], f"Hero位置类型错误: {result['hero_position_type']}"
    assert result['final_pot_type'] in ['1v1', 'multi'], f"最终底池类型错误: {result['final_pot_type']}"
    assert result['hero_3b_position'] == 'MP', f"Hero 3B位置错误: {result['hero_3b_position']}"
    assert result['hero_squeeze'] == 'NO', f"Hero squeeze状态错误: {result['hero_squeeze']}"
    
    print("测试通过!")
    
    # 测试Squeeze情况
    test_hand_text_squeeze = """Poker Hand #10933657-19873-1698906989 - Hold'em No Limit ($0.02/$0.05)
Table 'Seokguram' 9-max Seat #7 is the button
Seat 1: Player1 ($5.72 in chips) 
Seat 2: Player2 ($4.30 in chips) 
Seat 3: Hero ($5.00 in chips) 
Seat 4: Player4 ($4.03 in chips) 
Seat 5: Player5 ($4.99 in chips) 
Seat 6: Player6 ($5.10 in chips) 
Seat 7: Player7 ($5.00 in chips) 
Seat 8: Player8 ($5.65 in chips) 
Seat 9: Player9 ($5.02 in chips) 
Player8: posts small blind $0.02
Player9: posts big blind $0.05
*** HOLE CARDS ***
Hero cards: As Kd
Player1: folds
Player2: raises $0.10 to $0.15
Player4: calls $0.15
Player5: folds
Player6: folds
Hero: raises $0.35 to $0.50
Player7: folds
Player8: folds
Player9: folds
Player2: folds
Player4: folds
Uncalled bet ($0.35) returned to Hero
Hero collected $0.52 from pot
*** SUMMARY ***
Total pot $0.52 | Rake $0.00 
Seat 1: Player1 folded before Flop (didn't bet)
Seat 2: Player2 folded before Flop
Seat 3: Hero showed [As Kd] and won ($0.52) with High card, Ace
Seat 4: Player4 folded before Flop
Seat 5: Player5 folded before Flop (didn't bet)
Seat 6: Player6 folded before Flop (didn't bet)
Seat 7: Player7 (button) folded before Flop (didn't bet)
Seat 8: Player8 (small blind) folded before Flop
Seat 9: Player9 (big blind) folded before Flop"""
    
    # 解析Squeeze情况的手牌
    result_squeeze = parser.parse_hand(test_hand_text_squeeze)
    
    # 验证squeeze字段
    assert result_squeeze['hero_squeeze'] == 'YES', f"Hero squeeze状态错误: {result_squeeze['hero_squeeze']}"
    print("Squeeze测试通过!")
    
    # 返回解析器供进一步测试
    return parser
    
if __name__ == "__main__":
    # 创建必要的文件夹
    if not os.path.exists('poker_input'):
        os.makedirs('poker_input')
    if not os.path.exists('poker_output'):
        os.makedirs('poker_output')
    
    # 测试解析器
    test_parser()
    
    # 处理实际文件
    input_file = 'poker_input/combined_1.txt'  # 输入文件路径
    output_file = 'poker_output/parsed_hands.csv'  # 输出文件路径
    
    # 如果输入文件存在，则处理它
    if os.path.exists(input_file):
        process_poker_file(input_file, output_file)
        print(f"\n处理完成！结果已保存到 {output_file}")
    else:
        print(f"\n输入文件 {input_file} 不存在，请将扑克手牌记录放入该文件中。")