import re
import csv
from typing import Dict, List, Optional
import os

class PokerHandParser:
    def __init__(self):
        # 基本信息
        self.hand_data = {
            'hand_id': '',
            'SB_BB': '',  # 记录大小盲注金额
            'cash_drop': 'NO',  # 记录红包降落，默认为NO
            'hero_position': '',
            'hero_stack': '',  # 改为字符串类型，因为会包含 BB 单位
            'hero_cards': '', 
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
            'hero_position_type': '',  # 新增：IP/OOP/NA
            'hero_open_position': '',  # 新增：记录Hero open位置  -->也要一起紀錄如果前位沒有人raises，但hero folds，記錄folds。如果前位有人先raises則紀錄NA
            'hero_3b_chance': 'NO',    # 修改：从hero_3b_position改为hero_3b_chance，记录Hero是否有3B机会
            'pot_type': '',           # 新增：底池类型(SRP/3B/4B/5B)
            'hero_squeeze': 'NO',     # 新增：Hero是否squeeze
            'final_pot_type': '',     # 新增：最终底池类型(1v1/multi)
            'preflop_summary': '',     #紀錄preflop最後結果， BB/SB call open/fold to 3B/call 3B/fold to 4B/ call 4B/ limp-fold/limp-calls
            'flop_actions': '',
            'flop_pot': 0.0,
            'turn_actions': '',
            'turn_pot': 0.0,
            'river_actions': '',
            'river_pot': 0.0,
            'result': '',
            'total_pot': 0.0,
            # 新增flop动作细节字段
            'ip_cbet_flop': '',      # IP玩家是否在flop做cbet
            'oop_cbet_flop': '',     # OOP玩家是否在flop做cbet
            'ip_cbet_response': '',  # OOP对IP的cbet反应：fold/call/raise
            'oop_cbet_response': '', # IP对OOP的cbet反应：fold/call/raise
            'oop_donk_flop': 'NO',   # OOP玩家是否donk
            'ip_donk_reaction': '',  # IP玩家对OOP donk的反应
            'miss_cbet_oop': '',     # OOP玩家未cbet的情况
            'miss_cbet_oop_response': '', # IP对OOP未cbet的反应：bet/check
            'miss_cbet_ip': '',      # IP玩家未cbet的情况
            'miss_cbet_ip_response': '',  # OOP对IP未cbet的反应：bet/check
            'hero_win': 'NO',
            'hero_win_amount': 0
        }
        
        # 状态跟踪变量
        self.current_street = None
        self.current_pot = 0
        self.last_bet_amount = 0
        self.last_bet_player = None
        self.bb_amount = 0
        self.sb_amount = 0
        self.hero_total_bet = 0
        self.bb_player = None
        
        # 翻前行动追踪
        self.has_first_bet = False  # 第一次加注
        self.has_three_bet = False  # 3-bet
        self.has_four_bet = False   # 4-bet
        self.hero_squeeze_opportunity = False  # Hero是否有squeeze机会
        self.hero_entered_pot = False  # Hero是否进入底池
        self.preflop_all_actions = []  # 记录所有翻前行动
        
        # 玩家位置相关
        self.player_positions = {}  # 记录每个玩家的位置
        self.active_players_at_flop = []  # 记录翻牌前活跃的玩家
        
        # Flop行动追踪
        self.first_flop_action_player = None  # 记录第一个flop行动的玩家
        self.ip_first_action = None  # IP玩家的第一个行动
        self.oop_first_action = None  # OOP玩家的第一个行动
        self.ip_cbet_done = False  # 是否已经判断过IP的Cbet
        self.oop_cbet_done = False  # 是否已经判断过OOP的Cbet
        self.oop_donk_done = False  # 是否已经判断过OOP的Donk bet
        self.flop_actions_list = []  # 记录flop所有动作
        
        # 翻前最后加注者
        self.last_preflop_raiser = None
        
        # Turn行动追踪
        self.turn_actions_list = []  # 记录turn所有动作
        self.oop_first_turn_action = None  # OOP在turn的第一个行动
        
        self.position_map = {
            '1': 'BTN',
            '2': 'SB',
            '3': 'BB',
            '4': 'UTG',
            '5': 'MP',
            '6': 'CO'
        }
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
        
        # 翻牌圈行动跟踪变量
        self.flop_actions_list = []  # 记录翻牌圈的所有行动
        self.ip_player = ""  # 记录IP玩家
        self.oop_player = ""  # 记录OOP玩家
        self.first_flop_action_player = ""  # 记录第一个在flop行动的玩家
        self.ip_first_action = ""  # 记录IP玩家在flop的第一个行动
        self.oop_first_action = ""  # 记录OOP玩家在flop的第一个行动
        self.ip_cbet_done = False  # IP玩家是否已完成cbet
        self.oop_cbet_done = False  # OOP玩家是否已完成cbet
        self.oop_donk_done = False  # OOP玩家是否执行了donk bet
        
        # 新增: 记录翻前最后加注者
        self.last_preflop_raiser = ""  # 翻前最后的加注者
        self.turn_actions_list = []  # 记录转牌圈的所有行动
        self.oop_first_turn_action = ""  # 记录OOP玩家在turn的第一个行动
        
        # 添加一个变量，用于跟踪 Hero 3B 机会
        self.hero_acted = False  # 标记 Hero 是否已经行动过
        self.hero_has_3b_chance = False  # 标记 Hero 是否有3B机会
    
    def reset(self):
        self.hand_data = {
            'hand_id': '',
            'SB_BB': '',  # 记录大小盲注金额
            'cash_drop': 'NO',  # 记录红包降落，默认为NO
            'hero_position': '',
            'hero_stack': '',  # 改为字符串类型，因为会包含 BB 单位
            'hero_cards': '', 
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
            'hero_position_type': '',  # 新增：IP/OOP/NA
            'hero_open_position': '',  # 新增：记录Hero open位置  -->也要一起紀錄如果前位沒有人raises，但hero folds，記錄folds。如果前位有人先raises則紀錄NA
            'hero_3b_chance': 'NO',    # 修改：从hero_3b_position改为hero_3b_chance，记录Hero是否有3B机会
            'pot_type': '',           # 新增：底池类型(SRP/3B/4B/5B)
            'hero_squeeze': 'NO',     # 新增：Hero是否squeeze
            'final_pot_type': '',     # 新增：最终底池类型(1v1/multi)
            'preflop_summary': '',     #紀錄preflop最後結果， BB/SB call open/fold to 3B/call 3B/fold to 4B/ call 4B/ limp-fold/limp-calls
            'flop_actions': '',
            'flop_pot': 0.0,
            'turn_actions': '',
            'turn_pot': 0.0,
            'river_actions': '',
            'river_pot': 0.0,
            'result': '',
            'total_pot': 0.0,
            # 新增flop动作细节字段
            'ip_cbet_flop': '',      # IP玩家是否在flop做cbet
            'oop_cbet_flop': '',     # OOP玩家是否在flop做cbet
            'ip_cbet_response': '',  # OOP对IP的cbet反应：fold/call/raise
            'oop_cbet_response': '', # IP对OOP的cbet反应：fold/call/raise
            'oop_donk_flop': 'NO',   # OOP玩家是否donk
            'ip_donk_reaction': '',  # IP玩家对OOP donk的反应
            'miss_cbet_oop': '',     # OOP玩家未cbet的情况
            'miss_cbet_oop_response': '', # IP对OOP未cbet的反应：bet/check
            'miss_cbet_ip': '',      # IP玩家未cbet的情况
            'miss_cbet_ip_response': '',  # OOP对IP未cbet的反应：bet/check
            'hero_win': 'NO',
            'hero_win_amount': 0
        }
        self.current_street = None
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
        
        # 重置翻牌圈行动跟踪变量
        self.flop_actions_list = []
        self.ip_player = ""
        self.oop_player = ""
        self.first_flop_action_player = ""
        self.ip_first_action = ""
        self.oop_first_action = ""
        self.ip_cbet_done = False
        self.oop_cbet_done = False
        self.oop_donk_done = False
        
        # 重置新增变量
        self.last_preflop_raiser = ""
        self.turn_actions_list = []
        self.oop_first_turn_action = ""
        
        # 重置 Hero 3B 机会相关变量
        self.hero_acted = False
        self.hero_has_3b_chance = False
    
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
                # 修改：只保存位置，不要前缀
                self.hand_data['hero_position'] = position
                # 设置hero_stack字段
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
                    # 如果Hero在BB位置，记录BB位置的玩家
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
            
            # 到达flop时，确定IP和OOP玩家
            self._determine_ip_oop_players()
            
        elif '*** TURN ***' in line:
            self.current_street = 'turn'
            self.hand_data['flop_pot'] = round(self.convert_to_bb(self.current_pot), 1)  # 记录flop底池
            cards = re.search(r'\] \[(.*?)\]', line)
            if cards:
                self.hand_data['turn_card'] = cards.group(1)
            
            # Turn街段开始前，记录flop街段的Cbet情况
            self._analyze_flop_cbet_actions()
            
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
                
            # 处理红包降落 - 修改为明确检查'Cash Drop to Pot'
            if 'Cash Drop to Pot' in line:
                self.hand_data['cash_drop'] = 'YES'
                # 增加10BB到current_pot
                self.current_pot += 10 * self.bb_amount
                # 更新翻前底池
                self.hand_data['preflop_pot'] = round(self.convert_to_bb(self.current_pot), 1)
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
                # 在处理行动前检查这是否是第一个加注
                # 注释掉这段代码，因为它会导致hero_open_position无法正确设置
                # 将设置has_first_bet的逻辑完全集中在_classify_preflop_action方法中
                # if 'raises' in action and not self.has_first_bet:
                #     self.has_first_bet = True
                #     self.first_bet_player = player_name
                
                # 在处理行动前就判断 Hero 是否有 3B 机会
                # 如果当前行动是 Hero 的，而且已经有人进行了第一次加注，且第一个加注者不是 Hero
                # 那么 Hero 有 3B 机会
                if is_hero and not self.hero_acted and self.has_first_bet and self.first_bet_player != 'Hero':
                    self.hand_data['hero_3b_chance'] = 'YES'
                
                # 记录翻前行动 - 盲注下注已经在前面被排除
                # 所有其他行动（包括大小盲的非下注行动）都要记录
                self.preflop_all_actions.append(action)
                self.hand_data['preflop_actions'] = '; '.join(self.preflop_all_actions)
                
                # 标记 Hero 是否已经行动
                if is_hero:
                    self.hero_acted = True
                
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
                
                # 记录翻前最后加注者
                if 'raises' in action:
                    self.last_preflop_raiser = player_name
                
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
                    self.flop_actions_list.append((player_name, action))
                    
                    # 处理第一个flop行动的玩家
                    if not self.first_flop_action_player:
                        self.first_flop_action_player = player_name
                    
                    # 记录IP和OOP玩家的第一个行动
                    if player_name == self.ip_player and not self.ip_first_action:
                        self.ip_first_action = action
                    elif player_name == self.oop_player and not self.oop_first_action:
                        self.oop_first_action = action
                        
                        # 检查OOP是否donk bet（作为OOP先行动且下注）
                        if 'bets' in action:
                            self.hand_data['oop_donk_flop'] = 'YES'
                            self.oop_donk_done = True
                            
                            # 当OOP donk时，设置IP_Cbet_Flop, OOP_Cbet_Flop和Miss_Cbet_IP为NA
                            self.hand_data['ip_cbet_flop'] = 'NA'
                            self.hand_data['oop_cbet_flop'] = 'NA'
                            self.hand_data['miss_cbet_ip'] = 'NA'
                            
                            # 记录IP对donk的反应
                            # 这里先不设置，等IP的行动
                    
                    # 当OOP donk时，记录IP的反应
                    if self.oop_donk_done and player_name == self.ip_player:
                        if 'folds' in action:
                            self.hand_data['ip_donk_reaction'] = 'IP fold'
                        elif 'calls' in action:
                            self.hand_data['ip_donk_reaction'] = 'IP call'
                        elif 'raises' in action:
                            self.hand_data['ip_donk_reaction'] = 'IP R'
                    
                    # 根据翻前最后加注者情况判断Cbet
                    if not self.oop_donk_done:  # 只有在没有donk的情况下才考虑Cbet
                        # 如果翻前最后加注者是IP
                        if self.last_preflop_raiser == self.ip_player:
                            # IP玩家的行动
                            if player_name == self.ip_player:
                                if 'bets' in action and (not self.oop_first_action or 'checks' in self.oop_first_action):
                                    self.hand_data['ip_cbet_flop'] = 'YES'
                                    self.ip_cbet_done = True
                                    # OOP玩家没有Cbet的机会
                                    self.hand_data['oop_cbet_flop'] = 'NA'
                                elif 'checks' in action:
                                    self.hand_data['ip_cbet_flop'] = 'NO'
                                    self.hand_data['miss_cbet_ip'] = 'YES'
                                    self.ip_cbet_done = True
                            
                            # OOP对IP的Cbet反应
                            if self.hand_data['ip_cbet_flop'] == 'YES' and player_name == self.oop_player:
                                if 'folds' in action:
                                    self.hand_data['ip_cbet_response'] = 'OOP fold'
                                elif 'calls' in action:
                                    self.hand_data['ip_cbet_response'] = 'OOP call'
                                elif 'raises' in action:
                                    self.hand_data['ip_cbet_response'] = 'OOP XR'
                        
                        # 如果翻前最后加注者是OOP
                        elif self.last_preflop_raiser == self.oop_player:
                            # OOP玩家的行动
                            if player_name == self.oop_player:
                                if 'bets' in action:
                                    self.hand_data['oop_cbet_flop'] = 'YES'
                                    self.oop_cbet_done = True
                                    # IP玩家没有Cbet的机会
                                    self.hand_data['ip_cbet_flop'] = 'NA'
                                elif 'checks' in action:
                                    self.hand_data['oop_cbet_flop'] = 'NO'
                                    self.hand_data['miss_cbet_oop'] = 'YES'
                                    self.oop_cbet_done = True
                            
                            # IP对OOP的Cbet反应
                            if self.hand_data['oop_cbet_flop'] == 'YES' and player_name == self.ip_player:
                                if 'folds' in action:
                                    self.hand_data['oop_cbet_response'] = 'IP fold'
                                elif 'calls' in action:
                                    self.hand_data['oop_cbet_response'] = 'IP call'
                                elif 'raises' in action:
                                    self.hand_data['oop_cbet_response'] = 'IP R'
                        
                        # 处理OOP check后IP也check（Miss Cbet IP）
                        if self.oop_first_action and 'checks' in self.oop_first_action and player_name == self.ip_player and 'checks' in action:
                            # 如果IP是翻前最后加注者，但在flop选择check，记为Miss Cbet
                            if self.last_preflop_raiser == self.ip_player:
                                self.hand_data['ip_cbet_flop'] = 'NO'
                                self.hand_data['miss_cbet_ip'] = 'YES'
                                self.ip_cbet_done = True
                    
                    self.hand_data['flop_pot'] = round(self.convert_to_bb(self.current_pot), 1)
                    
            elif self.current_street == 'turn':
                # 处理turn行动
                if 'folds' in line or bet_amount > 0 or 'checks' in line:
                    self.hand_data['turn_actions'] += action + '; '
                    self.turn_actions_list.append((player_name, action))
                    
                    # 记录OOP在turn的第一个行动，用于Miss_Cbet_OOP_Response
                    if player_name == self.oop_player and not self.oop_first_turn_action:
                        self.oop_first_turn_action = action
                        # 如果OOP在flop错过了Cbet，记录其在turn的行动
                        if self.hand_data['miss_cbet_oop'] == 'YES':
                            if 'checks' in action:
                                self.hand_data['miss_cbet_oop_response'] = 'OOP check'
                            elif 'bets' in action:
                                self.hand_data['miss_cbet_oop_response'] = 'OOP bet'
                    
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
            
            # 如果前面没有人加注，但Hero选择fold，记录hero_open_position为fold
            if not self.has_first_bet and is_fold:
                self.hand_data['hero_open_position'] = 'fold'
            # 如果前面没有人加注，且Hero选择raises，记录hero_open_position为Hero位置
            elif not self.has_first_bet and is_raise:
                self.hand_data['hero_open_position'] = player_position
            # 如果前面已有人加注，无论Hero做什么都记录为NA
            elif self.has_first_bet:
                self.hand_data['hero_open_position'] = 'NA'
        
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
                    self.hand_data['hero_position'] = player_position
                    # 更新hero_open_position为Hero的位置
                    # 这部分逻辑已在Hero的条件部分处理，这里删除避免覆盖
                    # 但是我们发现在Hero的条件部分可能无法正确处理，所以在这里重新设置
                    self.hand_data['hero_open_position'] = player_position
                else:
                    # 如果不是Hero open，那么Hero不能open，设置为NA
                    # 这部分逻辑已在Hero的条件部分处理，这里删除避免覆盖
                    pass  # 保持缩进一致性
                    
            # 处理第二个加注者 (3-bet)
            elif self.has_first_bet and not self.has_three_bet:
                self.has_three_bet = True
                self.three_bet_player = player_name
                self.three_bet_actions = [action]
                self.hand_data['preflop_action_3B'] = action
                
                # 如果是Hero 3bet，不更改hero_3b_chance，因为我们只关心是否有机会，不关心是否做了
                
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
                # 更新hero_win字段
                self.hand_data['hero_win'] = 'YES'
    
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
                
        # 确定preflop_summary
        self._determine_preflop_summary()
        
    def _determine_preflop_summary(self):
        """确定preflop_summary字段"""
        # 根据Hero的位置和行动确定preflop_summary
        hero_position = self.player_positions.get('Hero', '')
        if not hero_position:
            return
            
        # 如果Hero是BB且跟注了open
        if hero_position == 'BB' and self.has_first_bet and 'Hero' in self.active_players_at_flop:
            if not self.has_three_bet:
                self.hand_data['preflop_summary'] = 'BB call open'
                
        # 如果Hero是SB且跟注了open
        elif hero_position == 'SB' and self.has_first_bet and 'Hero' in self.active_players_at_flop:
            if not self.has_three_bet:
                self.hand_data['preflop_summary'] = 'SB call open'
                
        # 如果Hero弃牌了3bet
        elif self.has_three_bet and self.first_bet_player == 'Hero' and 'Hero' not in self.active_players_at_flop:
            self.hand_data['preflop_summary'] = 'fold to 3B'
            
        # 如果Hero跟注了3bet
        elif self.has_three_bet and self.first_bet_player == 'Hero' and 'Hero' in self.active_players_at_flop:
            if not self.has_four_bet:
                self.hand_data['preflop_summary'] = 'call 3B'
                
        # 如果Hero弃牌了4bet
        elif self.has_four_bet and self.three_bet_player == 'Hero' and 'Hero' not in self.active_players_at_flop:
            self.hand_data['preflop_summary'] = 'fold to 4B'
            
        # 如果Hero跟注了4bet
        elif self.has_four_bet and self.three_bet_player == 'Hero' and 'Hero' in self.active_players_at_flop:
            if not self.has_five_bet:
                self.hand_data['preflop_summary'] = 'call 4B'
                
        # 如果Hero limp后弃牌
        elif self.hero_limped and self.hero_limp_response == 'fold':
            self.hand_data['preflop_summary'] = 'limp-fold'
            
        # 如果Hero limp后跟注
        elif self.hero_limped and self.hero_limp_response == 'call':
            self.hand_data['preflop_summary'] = 'limp-calls'

    def _determine_ip_oop_players(self):
        """确定IP和OOP玩家"""
        # 如果没有足够的活跃玩家，不能确定IP和OOP
        if len(self.active_players_at_flop) < 2:
            return
            
        # 位置顺序 (从早到晚): SB->BB->UTG->MP->CO->BTN
        position_order = ['SB', 'BB', 'UTG', 'MP', 'CO', 'BTN']
        
        # 获取活跃玩家的位置
        players_with_positions = []
        for player in self.active_players_at_flop:
            pos = self.player_positions.get(player, '')
            if pos in position_order:
                players_with_positions.append((player, pos, position_order.index(pos)))
        
        # 按位置排序
        players_with_positions.sort(key=lambda x: x[2])
        
        # 如果有至少两个玩家，则最后一个是IP，其他是OOP
        if len(players_with_positions) >= 2:
            # OOP是位置较早的玩家（除了最后一个）
            self.oop_player = players_with_positions[0][0]
            # IP是位置最晚的玩家
            self.ip_player = players_with_positions[-1][0]
            
            # 更新hand_data字典
            self.hand_data['oop_player'] = self.oop_player
            self.hand_data['ip_player'] = self.ip_player

    def _analyze_flop_cbet_actions(self):
        """在flop结束时分析Cbet相关行动"""
        # 如果没有进行过flop分析，不需要再分析
        if not self.flop_actions_list:
            return
            
        # 如果未能识别IP/OOP玩家，不能进行分析
        if not self.ip_player or not self.oop_player:
            return
            
        # 确保所有的Cbet相关字段都有值
        if not self.hand_data['ip_cbet_flop']:
            self.hand_data['ip_cbet_flop'] = 'NO'
            
        if not self.hand_data['oop_cbet_flop']:
            self.hand_data['oop_cbet_flop'] = 'NO'
            
        # 如果没有Cbet但也没有记录为Miss Cbet，补充记录
        if self.hand_data['ip_cbet_flop'] == 'NO' and not self.hand_data['miss_cbet_ip']:
            self.hand_data['miss_cbet_ip'] = 'YES'
            
        if self.hand_data['oop_cbet_flop'] == 'NO' and not self.hand_data['miss_cbet_oop']:
            self.hand_data['miss_cbet_oop'] = 'YES'

    def parse_hand(self, hand_text: str) -> Dict:
        self.reset()
        lines = hand_text.split('\n')
        
        # 第一次遍历，优先处理盲注信息和预先判断Hero位置
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 解析大小盲注金额
            if 'Hold\'em No Limit' in line:
                match = re.search(r'Hold\'em No Limit \(\$([\d.]+)/\$([\d.]+)\)', line)
                if match:
                    self.sb_amount = float(match.group(1))
                    self.bb_amount = float(match.group(2))
                    if self.bb_amount <= 0:  # 防止除零错误
                        self.bb_amount = 0.05
                    # 保存stakes信息
                    self.hand_data['SB_BB'] = f"(${self.sb_amount}/${self.bb_amount})"
                    break  # 找到盲注信息后立即退出
            
            # 如果是Hero的位置信息，记录下来以便后续判断3B机会
            if 'Seat' in line and 'Hero' in line:
                match = re.search(r'Seat (\d+): Hero \(', line)
                if match:
                    seat_num = match.group(1)
                    position = self.position_map.get(seat_num, seat_num)
                    self.player_positions['Hero'] = position
        
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
        
        # 在处理完所有行后，确定位置和底池类型
        self._determine_position_types()
        
        # 后处理：修正Hero_Open_Position
        # 检查preflop_actions中是否有Hero raises，且是第一个raises
        preflop_actions = self.hand_data['preflop_actions']
        hero_position = self.hand_data['hero_position']
        
        if preflop_actions and hero_position:
            # 使用正则表达式检查Hero是否是第一个raises的玩家
            if 'raises' in preflop_actions:
                match = re.search(r'([^;]+raises[^;]+)', preflop_actions)
                if match:
                    first_raise = match.group(1)
                    # 检查这个raise是否由Hero做出
                    if f"Hero({hero_position})" in first_raise:
                        # 如果Hero是第一个raises的玩家，设置hero_open_position为Hero的位置
                        self.hand_data['hero_open_position'] = hero_position
        
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
    
    # 修复翻前行动字段的数据位移问题（在写入CSV前）
    for hand in all_hands:
        # 暂存原始数据
        temp_1st_bet = hand['preflop_action_1st_bet']
        temp_3b = hand['preflop_action_3B']
        temp_4b = hand['preflop_action_4B']
        temp_5b = hand['preflop_action_5B']
        
        # 修正数据位移
        # 将3B中的数据移到1st_bet
        if temp_3b:
            hand['preflop_action_1st_bet'] = temp_3b
        
        # 将4B中的数据移到3B
        if temp_4b:
            hand['preflop_action_3B'] = temp_4b
        else:
            hand['preflop_action_3B'] = ''
            
        # 将5B中的数据移到4B
        if temp_5b:
            hand['preflop_action_4B'] = temp_5b
        else:
            hand['preflop_action_4B'] = ''
            
        # 清空5B
        hand['preflop_action_5B'] = ''
    
    # Write to CSV with custom header
    if all_hands:
        # 创建一个空的模板手牌数据，确保包含所有可能的字段
        template_hand = parser.hand_data.copy()
        # 获取所有字段名
        field_names = list(template_hand.keys())
        
        # 创建自定义标题映射
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
            'preflop_action_limp': 'Preflop_Limp',
            'preflop_action_limp_fold': 'Preflop_Limp_Fold',
            'preflop_action_limp_call': 'Preflop_Limp_Call',
            'preflop_pot': 'Preflop_Pot',
            'hero_position_type': 'Hero_Position_Type',
            'hero_open_position': 'Hero_Open_Position',
            'hero_3b_chance': 'Hero_3B_Chance',  # 修改：从Hero_3B_Position改为Hero_3B_Chance
            'pot_type': 'Pot_Type',
            'hero_squeeze': 'Hero_Squeeze',
            'final_pot_type': 'Final_Pot_Type',
            'preflop_summary': 'Preflop_Summary',
            'flop_actions': 'Flop_Actions',
            'flop_pot': 'Flop_Pot',
            'turn_actions': 'Turn_Actions',
            'turn_pot': 'Turn_Pot',
            'river_actions': 'River_Actions',
            'river_pot': 'River_Pot',
            'result': 'Result',
            'total_pot': 'Total_Pot',
            'ip_cbet_flop': 'IP_Cbet_Flop',
            'oop_cbet_flop': 'OOP_Cbet_Flop',
            'ip_cbet_response': 'IP_Cbet_Response',
            'oop_cbet_response': 'OOP_Cbet_Response',
            'oop_donk_flop': 'OOP_Donk_Flop',
            'ip_donk_reaction': 'IP_Donk_Reaction',
            'miss_cbet_oop': 'Miss_Cbet_OOP',
            'miss_cbet_oop_response': 'Miss_Cbet_OOP_Response',
            'miss_cbet_ip': 'Miss_Cbet_IP',
            'miss_cbet_ip_response': 'Miss_Cbet_IP_Response',
            'hero_win': 'Hero_Win',
            'hero_win_amount': 'Hero_Win_Amount'
        }
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=field_names)
                # 写入自定义标题
                header_row = {field: custom_headers.get(field, field) for field in field_names}
                writer.writerow(header_row)
                
                # 在写入数据前，确保所有数据字段与标题字段一致
                for hand in all_hands:
                    # 确保每个手牌数据都包含所有字段，且与字段顺序一致
                    for field in field_names:
                        if field not in hand:
                            hand[field] = ''
                
                # 写入所有手牌数据
                writer.writerows(all_hands)
                print(f"Data written to {output_file}")  # Debug info
        except PermissionError:
            # 如果有权限问题，尝试写入到当前目录
            alt_output_file = 'parsed_hands.csv'
            with open(alt_output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=field_names)
                header_row = {field: custom_headers.get(field, field) for field in field_names}
                writer.writerow(header_row)
                
                # 确保每个手牌数据都包含所有字段，且与字段顺序一致
                for hand in all_hands:
                    # 检查是否有缺失的字段，如果有则添加空值
                    for field in field_names:
                        if field not in hand:
                            hand[field] = ''
                
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
    
    # 显示测试结果 - 位置和底池信息
    print("\n测试单手牌解析结果:")
    print("位置和底池信息:")
    for key, value in hand_data.items():
        if key in ['hero_position', 'hero_position_type', 'hero_open_position', 'hero_3b_chance', 
                   'pot_type', 'hero_squeeze', 'final_pot_type']:
            print(f"{key}: {value}")
    
    # 显示翻牌圈动作细节
    print("\n翻牌圈动作细节:")
    for key, value in hand_data.items():
        if key in ['ip_cbet_flop', 'oop_cbet_flop', 'ip_cbet_response', 'oop_cbet_response',
                  'oop_donk_flop', 'ip_donk_reaction', 'miss_cbet_oop', 'miss_cbet_oop_response', 
                  'miss_cbet_ip', 'miss_cbet_ip_response']:
            print(f"{key}: {value}")
    
    # 显示内部状态（调试用）
    print("\n内部状态:")
    print(f"IP玩家: {parser.ip_player}")
    print(f"OOP玩家: {parser.oop_player}")
    print(f"活跃玩家: {parser.active_players_at_flop}")
    
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