import re
import csv
from typing import Dict, List, Optional

class PokerHandParser:
    def __init__(self):
        self.hand_data = {
            'hand_id': '',
            'hero_position': '',
            'hero_stack': '',  # 改为字符串类型，因为会包含 BB 单位
            'hero_cards': '',
            'flop_cards': '',
            'turn_card': '',
            'river_card': '',
            'preflop_actions': '',
            'preflop_pot': 0.0,
            'flop_actions': '',
            'flop_pot': 0.0,
            'turn_actions': '',
            'turn_pot': 0.0,
            'river_actions': '',
            'river_pot': 0.0,
            'result': '',
            'total_pot': 0.0
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
        self.sb_amount = 0.02  # 小盲注金额
        self.bb_amount = 0.05  # 大盲注金额
        self.hero_total_bet = 0.0  # 记录 Hero 的总投注金额
        self.last_bet_amount = 0.0  # 记录最后一次投注金额
        self.last_bet_player = ''  # 记录最后一次投注的玩家
    
    def reset(self):
        self.hand_data = {
            'hand_id': '',
            'hero_position': '',
            'hero_stack': '',  # 改为字符串类型，因为会包含 BB 单位
            'hero_cards': '',
            'flop_cards': '',
            'turn_card': '',
            'river_card': '',
            'preflop_actions': '',
            'preflop_pot': 0.0,
            'flop_actions': '',
            'flop_pot': 0.0,
            'turn_actions': '',
            'turn_pot': 0.0,
            'river_actions': '',
            'river_pot': 0.0,
            'result': '',
            'total_pot': 0.0
        }
        self.current_street = 'preflop'
        self.player_positions = {}
        self.current_pot = 0.0
        self.hero_total_bet = 0.0
        self.last_bet_amount = 0.0
        self.last_bet_player = ''
    
    def parse_hand_id(self, line: str):
        if 'Poker Hand #' in line:
            match = re.search(r'Poker Hand #(RC\d+):', line)
            if match:
                self.hand_data['hand_id'] = match.group(1)
                print(f"Found hand ID: {match.group(1)}")  # Debug info
    
    def parse_hero_info(self, line: str):
        if 'Seat' in line and 'Hero' in line:
            match = re.search(r'Seat (\d+): Hero \((\$[\d.]+) in chips\)', line)
            if match:
                seat_num = match.group(1)
                position = self.position_map.get(seat_num, seat_num)
                self.hand_data['hero_position'] = f"Hero({position})"
                stack_amount = float(match.group(2).replace('$', ''))
                self.hand_data['hero_stack'] = f"{self.convert_to_bb(stack_amount):.0f}BB"
                print(f"Found hero info: position {position}, stack {self.convert_to_bb(stack_amount):.0f}BB")
    
    def parse_players_positions(self, line: str):
        if 'Seat' in line:
            if 'Hero' in line:
                match = re.search(r'Seat (\d+): Hero \(', line)
                if match:
                    seat_num = match.group(1)
                    position = self.position_map.get(seat_num, seat_num)
                    self.player_positions['Hero'] = position
            else:
                match = re.search(r'Seat (\d+): ([^(]+)', line)
                if match:
                    seat_num = match.group(1)
                    player_name = match.group(2).strip()
                    position = self.position_map.get(seat_num, seat_num)
                    self.player_positions[player_name] = position
    
    def parse_hero_cards(self, line: str):
        if 'Dealt to Hero' in line:
            cards = re.search(r'\[(.*?)\]', line)
            if cards:
                self.hand_data['hero_cards'] = cards.group(1)
                print(f"Found hero cards: {cards.group(1)}")  # Debug info
    
    def parse_board_cards(self, line: str):
        if '*** FLOP ***' in line:
            self.current_street = 'flop'
            self.hand_data['preflop_pot'] = round(self.convert_to_bb(self.current_pot), 1)  # 记录preflop底池
            cards = re.search(r'\[(.*?)\]', line)
            if cards:
                self.hand_data['flop_cards'] = cards.group(1)
                print(f"Found flop: {cards.group(1)}")
        elif '*** TURN ***' in line:
            self.current_street = 'turn'
            self.hand_data['flop_pot'] = round(self.convert_to_bb(self.current_pot), 1)  # 记录flop底池
            cards = re.search(r'\] \[(.*?)\]', line)
            if cards:
                self.hand_data['turn_card'] = cards.group(1)
                print(f"Found turn: {cards.group(1)}")
        elif '*** RIVER ***' in line:
            self.current_street = 'river'
            self.hand_data['turn_pot'] = round(self.convert_to_bb(self.current_pot), 1)  # 记录turn底池
            cards = re.search(r'\] \[(.*?)\]', line)
            if cards:
                self.hand_data['river_card'] = cards.group(1)
                print(f"Found river: {cards.group(1)}")
    
    def convert_to_bb(self, amount: float) -> float:
        """将美元金额转换为 BB 单位"""
        return amount / self.bb_amount
    
    def parse_action(self, line: str):
        if ':' in line and not line.startswith('Seat'):
            # 跳过包含 "Poker Hand #" 的行
            if 'Poker Hand #' in line:
                return
                
            # 处理大小盲注
            if 'posts small blind' in line:
                if 'Hero' in line:
                    self.hero_total_bet += self.sb_amount
                self.current_pot += self.sb_amount
                return
            elif 'posts big blind' in line:
                if 'Hero' in line:
                    self.hero_total_bet += self.bb_amount
                self.current_pot += self.bb_amount
                return
                
            # 处理未被跟注的投注返还
            if 'Uncalled bet' in line:
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
                return
                
            # 处理其他动作
            if 'folds' in line:
                # 跳过记录弃牌动作，不添加到输出中
                return
            else:
                # 提取投注金额（从原始动作中提取）
                bet_amount = self.extract_bet_amount(line.strip())
                player_name = line.split(':')[0].strip()
                
                # 记录最后一次投注信息
                if bet_amount > 0:
                    self.last_bet_amount = bet_amount
                    self.last_bet_player = player_name
                
                # 如果是 Hero 的动作，记录投注金额
                if line.startswith('Hero:'):
                    self.hero_total_bet += bet_amount
                
                # 更新底池
                self.current_pot += bet_amount
                
                # 转换玩家名称和金额为 BB
                action = self.format_action_with_bb(line.strip())
                
                if self.current_street == 'preflop':
                    self.hand_data['preflop_actions'] += action + '; '
                    self.hand_data['preflop_pot'] = round(self.convert_to_bb(self.current_pot), 1)
                    print(f"Added preflop action: {action}, pot: {self.convert_to_bb(self.current_pot):.1f}BB")
                elif self.current_street == 'flop':
                    self.hand_data['flop_actions'] += action + '; '
                    self.hand_data['flop_pot'] = round(self.convert_to_bb(self.current_pot), 1)
                    print(f"Added flop action: {action}, pot: {self.convert_to_bb(self.current_pot):.1f}BB")
                elif self.current_street == 'turn':
                    self.hand_data['turn_actions'] += action + '; '
                    self.hand_data['turn_pot'] = round(self.convert_to_bb(self.current_pot), 1)
                    print(f"Added turn action: {action}, pot: {self.convert_to_bb(self.current_pot):.1f}BB")
                elif self.current_street == 'river':
                    self.hand_data['river_actions'] += action + '; '
                    self.hand_data['river_pot'] = round(self.convert_to_bb(self.current_pot), 1)
                    print(f"Added river action: {action}, pot: {self.convert_to_bb(self.current_pot):.1f}BB")
                # 更新总底池
                self.hand_data['total_pot'] = round(self.convert_to_bb(self.current_pot), 1)
                
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
        print(f"Updated pot size: {self.convert_to_bb(self.current_pot):.1f}BB")

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
        # 先处理玩家名称
        player_match = re.match(r'^([^:]+):', action)
        if not player_match:
            return action
            
        player_name = player_match.group(1).strip()
        player_part = player_name
        if player_name != 'Hero' and player_name in self.player_positions:
            player_part = f"Opp({self.player_positions[player_name]})"
            
        action_part = action[len(player_name)+1:].strip()
        
        # 处理已经是 BB 单位的情况
        if 'BB' in action_part:
            if 'raises' in action_part:
                match = re.search(r'raises [\d.]+BB to ([\d.]+)BB', action_part)
                if match:
                    return f"{player_part}: raises {match.group(1)}BB"
            return f"{player_part}: {action_part}"
            
        # 处理美元金额的情况
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
                print(f"Found total pot: {self.convert_to_bb(pot_amount):.1f}BB")
                
                # 如果到这里 result 还没有设置，说明 Hero 没赢钱，记录损失的金额
                if not self.hand_data['result']:
                    hero_bet_bb = round(self.convert_to_bb(self.hero_total_bet), 1)
                    if hero_bet_bb > 0:
                        self.hand_data['result'] = f"-{hero_bet_bb}BB"
                        print(f"Hero lost: {hero_bet_bb}BB")
                    else:
                        self.hand_data['result'] = "0BB"
                        print("Hero didn't bet")
        
        # 只记录 Hero 赢得的金额
        elif 'Hero collected' in line:
            collected_match = re.search(r'Hero collected \$([\d.]+)', line)
            if collected_match:
                collected_amount = float(collected_match.group(1))
                won_amount = round(self.convert_to_bb(collected_amount/2), 1)
                self.hand_data['result'] = f"{won_amount}BB"
                print(f"Hero won: {won_amount}BB")
    
    def parse_hand(self, hand_text: str) -> Dict:
        self.reset()
        lines = hand_text.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            self.parse_hand_id(line)
            self.parse_hero_info(line)
            self.parse_players_positions(line)  # 添加解析玩家位置
            self.parse_hero_cards(line)
            self.parse_board_cards(line)
            
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
                    print(f"Found uncalled bet: ${returned_amount}, updated pot: {self.convert_to_bb(self.current_pot):.1f}BB")
            else:
                self.parse_action(line)
                
            self.parse_result(line)
            i += 1
        
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
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            # 写入自定义标题
            header_row = {field: custom_headers.get(field, field) for field in fieldnames}
            writer.writerow(header_row)
            writer.writerows(all_hands)
            print(f"Data written to {output_file}")  # Debug info

if __name__ == '__main__':
    input_file = 'poker_input/combined_1.txt'
    output_file = 'poker_output/parsed_hands.csv'
    process_poker_file(input_file, output_file) 