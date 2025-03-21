from poker_hand_parser import PokerHandParser

def test_hero_open_position():
    """测试所有与hero_open_position相关的场景"""
    
    # 测试场景1：Hero是第一个raises的玩家
    print("\n==== 测试场景1：Hero是第一个raises的玩家 ====")
    hand_text_raise = """
PokerStars Hand #RC1234567890: Hold'em No Limit ($0.25/$0.50) - 2023/06/01 12:34:56 ET
Table 'Test Table' 6-max Seat #3 is the button
Seat 1: Hero ($50)
Seat 2: Opp2 ($50)
Seat 3: Opp3 ($50)
Seat 4: Opp4 ($50)
Seat 5: Opp5 ($50)
Seat 6: Opp6 ($50)
Opp4: posts small blind $0.25
Opp5: posts big blind $0.50
*** HOLE CARDS ***
Dealt to Hero [Ah Kh]
Hero: raises $1.50 to $2.00
Opp2: folds
Opp3: folds
Opp4: folds
Opp5: folds
Uncalled bet ($1.50) returned to Hero
Hero collected $1.25 from pot
*** SUMMARY ***
Total pot $1.25 | Rake $0
Board []
Seat 1: Hero collected ($1.25)
Seat 2: Opp2 folded before Flop
Seat 3: Opp3 (button) folded before Flop
Seat 4: Opp4 (small blind) folded before Flop
Seat 5: Opp5 (big blind) folded before Flop
Seat 6: Opp6 folded before Flop
    """
    
    parser = PokerHandParser()
    hand_data = parser.parse_hand(hand_text_raise)
    
    print(f"Hero_Position: {hand_data.get('hero_position', 'N/A')}")
    print(f"Hero_Open_Position: {hand_data.get('hero_open_position', 'N/A')}")
    print(f"Preflop_Actions: {hand_data.get('preflop_actions', 'N/A')}")
    
    # 测试场景2：Hero进行limp
    print("\n==== 测试场景2：Hero进行limp ====")
    hand_text_limp = """
PokerStars Hand #RC9988776655: Hold'em No Limit ($0.25/$0.50) - 2023/06/01 12:34:56 ET
Table 'Test Table' 6-max Seat #3 is the button
Seat 1: Hero ($50)
Seat 2: Opp2 ($50)
Seat 3: Opp3 ($50)
Seat 4: Opp4 ($50)
Seat 5: Opp5 ($50)
Seat 6: Opp6 ($50)
Opp4: posts small blind $0.25
Opp5: posts big blind $0.50
*** HOLE CARDS ***
Dealt to Hero [Ah Kh]
Hero: calls $0.50
Opp2: folds
Opp3: folds
Opp4: folds
Opp5: checks
*** FLOP *** [2c 7h Ks]
Opp5: checks
Hero: bets $1.00
Opp5: folds
Uncalled bet ($1.00) returned to Hero
Hero collected $1.25 from pot
*** SUMMARY ***
Total pot $1.25 | Rake $0
Board [2c 7h Ks]
Seat 1: Hero collected ($1.25)
Seat 2: Opp2 folded before Flop
Seat 3: Opp3 (button) folded before Flop
Seat 4: Opp4 (small blind) folded before Flop
Seat 5: Opp5 (big blind) folded on the Flop
Seat 6: Opp6 folded before Flop
    """
    
    parser = PokerHandParser()
    hand_data = parser.parse_hand(hand_text_limp)
    
    print(f"Hero_Position: {hand_data.get('hero_position', 'N/A')}")
    print(f"Hero_Open_Position: {hand_data.get('hero_open_position', 'N/A')}")
    print(f"Preflop_Actions: {hand_data.get('preflop_actions', 'N/A')}")
    print(f"Preflop_Action_Limp: {hand_data.get('preflop_action_limp', 'N/A')}")
    
    # 测试场景3：Hero fold（前面没有人raises）
    print("\n==== 测试场景3：Hero fold（前面没有人raises）====")
    hand_text_fold = """
PokerStars Hand #RC8877665544: Hold'em No Limit ($0.25/$0.50) - 2023/06/01 12:34:56 ET
Table 'Test Table' 6-max Seat #3 is the button
Seat 1: Hero ($50)
Seat 2: Opp2 ($50)
Seat 3: Opp3 ($50)
Seat 4: Opp4 ($50)
Seat 5: Opp5 ($50)
Seat 6: Opp6 ($50)
Opp4: posts small blind $0.25
Opp5: posts big blind $0.50
*** HOLE CARDS ***
Dealt to Hero [2h 7c]
Hero: folds
Opp2: folds
Opp3: raises $1.50 to $2.00
Opp4: folds
Opp5: folds
Uncalled bet ($1.50) returned to Opp3
Opp3 collected $1.25 from pot
*** SUMMARY ***
Total pot $1.25 | Rake $0
Board []
Seat 1: Hero folded before Flop
Seat 2: Opp2 folded before Flop
Seat 3: Opp3 (button) collected ($1.25)
Seat 4: Opp4 (small blind) folded before Flop
Seat 5: Opp5 (big blind) folded before Flop
Seat 6: Opp6 folded before Flop
    """
    
    parser = PokerHandParser()
    hand_data = parser.parse_hand(hand_text_fold)
    
    print(f"Hero_Position: {hand_data.get('hero_position', 'N/A')}")
    print(f"Hero_Open_Position: {hand_data.get('hero_open_position', 'N/A')}")
    print(f"Preflop_Actions: {hand_data.get('preflop_actions', 'N/A')}")
    
    # 测试场景4：前面有人raises，Hero fold
    print("\n==== 测试场景4：前面有人raises，Hero fold ====")
    hand_text_na = """
PokerStars Hand #RC7766554433: Hold'em No Limit ($0.25/$0.50) - 2023/06/01 12:34:56 ET
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
Dealt to Hero [2h 7c]
Opp1: raises $1.50 to $2.00
Opp2: folds
Hero: folds
Opp4: folds
Opp5: folds
Opp6: folds
Uncalled bet ($1.50) returned to Opp1
Opp1 collected $1.25 from pot
*** SUMMARY ***
Total pot $1.25 | Rake $0
Board []
Seat 1: Opp1 collected ($1.25)
Seat 2: Opp2 folded before Flop
Seat 3: Hero folded before Flop
Seat 4: Opp4 folded before Flop
Seat 5: Opp5 (small blind) folded before Flop
Seat 6: Opp6 (big blind) folded before Flop
    """
    
    parser = PokerHandParser()
    hand_data = parser.parse_hand(hand_text_na)
    
    print(f"Hero_Position: {hand_data.get('hero_position', 'N/A')}")
    print(f"Hero_Open_Position: {hand_data.get('hero_open_position', 'N/A')}")
    print(f"Preflop_Actions: {hand_data.get('preflop_actions', 'N/A')}")
    
    # 输出总结
    print("\n==== 测试结果总结 ====")
    print("1. Hero是第一个raises的玩家: hero_open_position应为Hero位置")
    print("2. Hero进行limp: hero_open_position应为'no open(limp)'")
    print("3. Hero fold（前面没有人raises）: hero_open_position应为'fold'")
    print("4. 前面有人raises，Hero fold: hero_open_position应为'NA'")

if __name__ == "__main__":
    test_hero_open_position() 