import re
import csv
from typing import Dict, List, Optional

class PokerHandParser:
    def __init__(self):
        self.hand_data = {
            'hand_id': '',
            'hero_position': '',
            'hero_stack': 0.0,
            'hero_cards': '',
            'flop_cards': '',
            'turn_card': '',
            'river_card': '',
            'preflop_actions': '',
            'flop_actions': '',
            'turn_actions': '',
            'river_actions': '',
            'result': ''
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
        self.player_positions = {}  # 用于存储每个玩家的位置
    
    def reset(self):
        self.hand_data = {
            'hand_id': '',
            'hero_position': '',
            'hero_stack': 0.0,
            'hero_cards': '',
            'flop_cards': '',
            'turn_card': '',
            'river_card': '',
            'preflop_actions': '',
            'flop_actions': '',
            'turn_actions': '',
            'river_actions': '',
            'result': ''
        }
        self.current_street = 'preflop'
        self.player_positions = {}
    
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
                self.hand_data['hero_stack'] = float(match.group(2).replace('$', ''))
                print(f"Found hero info: position {position}, stack {match.group(2)}")  # Debug info
    
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
            cards = re.search(r'\[(.*?)\]', line)
            if cards:
                self.hand_data['flop_cards'] = cards.group(1)
                print(f"Found flop: {cards.group(1)}")  # Debug info
        elif '*** TURN ***' in line:
            self.current_street = 'turn'
            cards = re.search(r'\] \[(.*?)\]', line)
            if cards:
                self.hand_data['turn_card'] = cards.group(1)
                print(f"Found turn: {cards.group(1)}")  # Debug info
        elif '*** RIVER ***' in line:
            self.current_street = 'river'
            cards = re.search(r'\] \[(.*?)\]', line)
            if cards:
                self.hand_data['river_card'] = cards.group(1)
                print(f"Found river: {cards.group(1)}")  # Debug info
    
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

    def parse_action(self, line: str):
        if ':' in line and not line.startswith('Seat'):
            # 跳过包含 "Poker Hand #" 的行
            if 'Poker Hand #' in line:
                return
                
            # 跳过大小盲的投注
            if 'posts small blind' in line or 'posts big blind' in line:
                return
                
            # 只记录非fold的动作
            if 'folds' not in line:
                action = self.format_action(line.strip())
                if self.current_street == 'preflop':
                    self.hand_data['preflop_actions'] += action + '; '
                    print(f"Added preflop action: {action}")  # Debug info
                elif self.current_street == 'flop':
                    self.hand_data['flop_actions'] += action + '; '
                    print(f"Added flop action: {action}")  # Debug info
                elif self.current_street == 'turn':
                    self.hand_data['turn_actions'] += action + '; '
                    print(f"Added turn action: {action}")  # Debug info
                elif self.current_street == 'river':
                    self.hand_data['river_actions'] += action + '; '
                    print(f"Added river action: {action}")  # Debug info
    
    def parse_result(self, line: str):
        if 'collected' in line:
            self.hand_data['result'] = line.strip()
            print(f"Found result: {line.strip()}")  # Debug info
    
    def parse_hand(self, hand_text: str) -> Dict:
        self.reset()
        for line in hand_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            self.parse_hand_id(line)
            self.parse_hero_info(line)
            self.parse_players_positions(line)  # 添加解析玩家位置
            self.parse_hero_cards(line)
            self.parse_board_cards(line)
            self.parse_action(line)
            self.parse_result(line)
        
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
                all_hands.append(hand_data)
                current_hand = []
    
    # Process last hand if exists
    if current_hand:
        hand_text = ''.join(current_hand)
        print("\nProcessing last hand...")  # Debug info
        hand_data = parser.parse_hand(hand_text)
        all_hands.append(hand_data)
    
    print(f"\nTotal hands processed: {len(all_hands)}")  # Debug info
    
    # Write to CSV
    if all_hands:
        fieldnames = all_hands[0].keys()
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_hands)
            print(f"Data written to {output_file}")  # Debug info

if __name__ == '__main__':
    input_file = 'poker_input/combined_1.txt'
    output_file = 'poker_output/parsed_hands.csv'
    process_poker_file(input_file, output_file) 