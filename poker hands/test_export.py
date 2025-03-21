import csv
from poker_hand_parser import PokerHandParser

def test_export():
    """Export test case to CSV file"""
    # 使用一个简单的测试案例
    hand_text = """
PokerStars Hand #RC3334603458: Hold'em No Limit ($0.25/$0.50) - 2023/06/01 12:34:56 ET
Table 'Test Table' 6-max Seat #1 is the button
Seat 1: Opp1 ($50)
Seat 2: Opp2 ($50)
Seat 3: Opp3 ($50)
Seat 4: Opp4 ($50)
Seat 5: Opp5 ($50)
Seat 6: Hero ($50)
Opp2: posts small blind $0.25
Hero: posts big blind $0.50
*** HOLE CARDS ***
Dealt to Hero [Ah Kh]
Opp3: raises $1 to $1.50
Opp4: folds
Opp5: folds
Opp1: raises $4.60 to $6.10
Opp2: folds
Hero: folds
Opp3: folds
Uncalled bet ($4.60) returned to Opp1
Opp1 collected $3.75 from pot
*** SUMMARY ***
Total pot $3.75 | Rake $0
Board []
Seat 1: Opp1 (button) collected ($3.75)
Seat 2: Opp2 (small blind) folded before Flop
Seat 3: Opp3 folded before Flop
Seat 4: Opp4 folded before Flop
Seat 5: Opp5 folded before Flop
Seat 6: Hero (big blind) folded before Flop
    """
    
    parser = PokerHandParser()
    hand_data = parser.parse_hand(hand_text)
    
    # 打印解析结果
    print("解析结果:")
    for key, value in hand_data.items():
        print(f"{key}: {value}")
    
    # 特别关注Hero_3B_Chance字段
    print("\n特别关注的字段:")
    print(f"Hero_Position: {hand_data.get('Hero_Position', 'N/A')}")
    print(f"Preflop_Actions: {hand_data.get('Preflop_Actions', 'N/A')}")
    print(f"Preflop_1st_Bet: {hand_data.get('Preflop_1st_Bet', 'N/A')}")
    print(f"Preflop_3B: {hand_data.get('Preflop_3B', 'N/A')}")
    print(f"Hero_3B_Chance: {hand_data.get('Hero_3B_Chance', 'N/A')}")
    print(f"Hero_Open_Position: {hand_data.get('Hero_Open_Position', 'N/A')}")
    
    # 将数值型底池转为字符串
    for key in ['preflop_pot', 'flop_pot', 'turn_pot', 'river_pot', 'total_pot']:
        if hand_data[key] > 0:
            hand_data[key] = f"{hand_data[key]}BB"
        else:
            hand_data[key] = "0BB"
    
    # 输出所有键值对，找出其中的Flop动作字段
    print("\nAll fields and values in hand data:")
    for key, value in hand_data.items():
        if key in ['ip_cbet_flop', 'oop_cbet_flop', 'ip_cbet_response', 'oop_cbet_response',
                  'oop_donk_flop', 'ip_face_donk_flop', 'miss_cbet_oop_flop', 'oop_miss_cbet_IP_bet', 
                  'miss_cbet_ip_flop', 'IP_miss_cbet_OOP_bet_turn', 'last_preflop_raiser', 'oop_player', 'ip_player']:
            print(f"{key}: {value}")
    
    # 将数据写入CSV
    with open('test_hand.csv', 'w', newline='', encoding='utf-8') as f:
        # 获取所有字段
        field_names = list(hand_data.keys())
        # 创建writer对象
        writer = csv.DictWriter(f, fieldnames=field_names)
        # 写入表头
        writer.writeheader()
        # 写入数据
        writer.writerow(hand_data)
    
    print("\nTest data exported to test_hand.csv")
    
# 运行测试用例
if __name__ == "__main__":
    test_export() 