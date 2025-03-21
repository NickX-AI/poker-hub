import sys
from poker_hand_parser import PokerHandParser

def test_opponent_formatting():
    """测试对手显示格式"""
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
    
    # 检查preflop行动
    print("翻前行动:")
    print(result['preflop_actions'])
    print("\n翻前第一次加注行动:")
    print(result['preflop_action_1st_bet'])
    print("\n翻前3B行动:")
    print(result['preflop_action_3B'])
    
    # 检查其他街段行动
    print("\n翻牌圈行动:")
    print(result['flop_actions'])
    print("\n转牌圈行动:")
    print(result['turn_actions'])
    print("\n河牌圈行动:")
    print(result['river_actions'])
    
    # 检查玩家位置
    print("\n玩家位置信息:")
    for player, position in parser.player_positions.items():
        print(f"{player}: {position}")
    
    # 测试格式化函数
    print("\n测试格式化函数:")
    test_actions = [
        "Player1: folds",
        "Player2: raises $0.10 to $0.15",
        "Hero: raises $0.35 to $0.50",
        "Player9: calls $0.45"
    ]
    for action in test_actions:
        formatted = parser.format_action_with_bb(action)
        print(f"原始: {action}")
        print(f"格式化: {formatted}")
        print("---")

if __name__ == "__main__":
    test_opponent_formatting() 