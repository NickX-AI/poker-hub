from poker_hand_parser import PokerHandParser

def test_hero_limp():
    """测试Hero limp时hero_open_position的值设置为'no open(limp)'"""
    print("\n==== 测试Hero limp场景 ====")
    
    # 手牌文本：Hero在UTG位置limp
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
    
    # 测试Hero limp
    parser = PokerHandParser()
    hand_data = parser.parse_hand(hand_text_limp)
    
    print(f"Hero_Position: {hand_data.get('hero_position', 'N/A')}")
    print(f"Hero_Open_Position: {hand_data.get('hero_open_position', 'N/A')}")
    print(f"Preflop_Actions: {hand_data.get('preflop_actions', 'N/A')}")
    print(f"Preflop_Action_Limp: {hand_data.get('preflop_action_limp', 'N/A')}")
    
    # 检查是否正确设置了hero_open_position
    if hand_data.get('hero_open_position') == 'no open(limp)':
        print("\n✅ 测试通过：Hero limp时hero_open_position正确设置为'no open(limp)'")
    else:
        print(f"\n❌ 测试失败：Hero limp时hero_open_position的值是 {hand_data.get('hero_open_position', 'N/A')}，而不是期望的'no open(limp)'")

if __name__ == "__main__":
    test_hero_limp() 