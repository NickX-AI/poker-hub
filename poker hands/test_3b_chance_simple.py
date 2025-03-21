from poker_hand_parser import PokerHandParser

def test_case():
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
    
    # 打印特别关注的字段
    print("\n" + "="*50)
    print("特别关注的字段")
    print("="*50)
    print(f"Hero_Position: {hand_data.get('Hero_Position', 'N/A')}")
    print(f"Preflop_Actions: {hand_data.get('Preflop_Actions', 'N/A')}")
    print(f"Preflop_1st_Bet: {hand_data.get('Preflop_1st_Bet', 'N/A')}")
    print(f"Preflop_3B: {hand_data.get('Preflop_3B', 'N/A')}")
    print(f"Hero_3B_Chance: {hand_data.get('Hero_3B_Chance', 'N/A')}")
    print(f"Hero_Open_Position: {hand_data.get('Hero_Open_Position', 'N/A')}")

if __name__ == "__main__":
    test_case() 