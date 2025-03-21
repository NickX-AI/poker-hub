from poker_hand_parser import PokerHandParser

def test_preflop_actions():
    """测试翻前行动的记录，特别是第一次加注和3bet的情况"""
    print("\n==== 测试翻前行动记录 ====")
    
    # 测试场景：包含3bet的手牌
    hand_text_3bet = """
PokerStars Hand #RC1234567890: Hold'em No Limit ($0.25/$0.50) - 2023/06/01 12:34:56 ET
Table 'Test Table' 6-max Seat #3 is the button
Seat 1: Opp1 ($50)
Seat 2: Opp2 ($50)
Seat 3: Hero ($50)
Seat 4: Opp4 ($50)
Seat 5: Opp5 ($50)
Seat 6: Opp6 ($50)
Opp5: posts small blind $0.25
Opp6: posts big blind $0.50
*** HOLE CARDS ***
Dealt to Hero [Ah Kh]
Opp1: folds
Opp2: raises $1.50 to $2.00
Hero: raises $4.50 to $6.50
Opp4: folds
Opp5: folds
Opp6: folds
Opp2: calls $4.50
*** FLOP *** [2c 7h Ks]
Opp2: checks
Hero: bets $4.00
Opp2: calls $4.00
*** TURN *** [2c 7h Ks] [8d]
Opp2: checks
Hero: bets $10.00
Opp2: folds
*** SUMMARY ***
Total pot $20.50 | Rake $0
Board [2c 7h Ks 8d]
Hero collected $20.50
    """
    
    # 测试包含3bet的手牌
    parser = PokerHandParser()
    hand_data = parser.parse_hand(hand_text_3bet)
    
    print("\n包含3bet的手牌测试结果:")
    print(f"Preflop_Actions: {hand_data.get('preflop_actions', 'N/A')}")
    print(f"Preflop_1st_Bet: {hand_data.get('preflop_action_1st_bet', 'N/A')}")
    print(f"Preflop_3B: {hand_data.get('preflop_action_3B', 'N/A')}")
    
    # 验证第一次加注和3bet是否都被正确记录
    first_bet_recorded = hand_data.get('preflop_action_1st_bet', '') != ''
    three_bet_recorded = hand_data.get('preflop_action_3B', '') != ''
    
    # 更详细的验证
    first_raise_in_first_bet = 'raises' in hand_data.get('preflop_action_1st_bet', '')
    hero_raise_in_3b = 'Hero' in hand_data.get('preflop_action_3B', '') and 'raises' in hand_data.get('preflop_action_3B', '')
    
    if first_bet_recorded and three_bet_recorded:
        print("\n✅ 测试通过：第一次加注和3bet都被记录")
        print(f"  - 第一次加注记录: {hand_data.get('preflop_action_1st_bet', '')}")
        print(f"  - 3bet记录: {hand_data.get('preflop_action_3B', '')}")
        
        if first_raise_in_first_bet:
            print("  ✅ 第一次加注（raise）被正确记录在preflop_action_1st_bet中")
        else:
            print("  ❌ 第一次加注（raise）未正确记录在preflop_action_1st_bet中")
            
        if hero_raise_in_3b:
            print("  ✅ Hero的3bet正确记录在preflop_action_3B中")
        else:
            print("  ❌ Hero的3bet未正确记录在preflop_action_3B中")
    else:
        print("\n❌ 测试失败：字段记录不完整")
        if not first_bet_recorded:
            print("  - preflop_action_1st_bet字段为空")
        if not three_bet_recorded:
            print("  - preflop_action_3B字段为空")

if __name__ == "__main__":
    test_preflop_actions() 