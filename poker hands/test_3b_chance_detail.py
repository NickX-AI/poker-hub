from poker_hand_parser import PokerHandParser

def test_case():
    # 测试案例1: Hero有3bet机会并且进行了raises (Yes-3B)
    print("\n==== 测试案例1: Hero有3bet机会并且进行了raises (Yes-3B) ====")
    hand_text_3b = """
PokerStars Hand #RC3334563614: Hold'em No Limit ($0.25/$0.50) - 2023/06/01 12:34:56 ET
Table 'Test Table' 6-max Seat #1 is the button
Seat 1: Opp1 ($50)
Seat 2: Opp2 ($50)
Seat 3: Opp3 ($50)
Seat 4: Hero ($50)
Seat 5: Opp5 ($50)
Seat 6: Opp6 ($50)
Opp2: posts small blind $0.25
Opp3: posts big blind $0.50
*** HOLE CARDS ***
Dealt to Hero [Ah Kh]
Opp1: raises $1 to $1.50
Opp2: folds
Opp3: folds
Hero: raises $4.90 to $6.40
Opp5: folds
Opp6: folds
Opp1: raises $18.20 to $24.60
Hero: folds
Uncalled bet ($18.20) returned to Opp1
Opp1 collected $12.80 from pot
*** SUMMARY ***
Total pot $12.80 | Rake $0
Board []
Seat 1: Opp1 (button) collected ($12.80)
Seat 2: Opp2 (small blind) folded before Flop
Seat 3: Opp3 (big blind) folded before Flop
Seat 4: Hero folded before Flop
Seat 5: Opp5 folded before Flop
Seat 6: Opp6 folded before Flop
    """
    
    parser = PokerHandParser()
    hand_data = parser.parse_hand(hand_text_3b)
    
    print(f"Hero_Position: {hand_data.get('hero_position', 'N/A')}")
    print(f"Hero_3B_Chance: {hand_data.get('hero_3b_chance', 'N/A')}")
    print(f"Preflop_Actions: {hand_data.get('preflop_actions', 'N/A')}")
    
    # 测试案例2: Hero有3bet机会并且calls (Yes-Calls)
    print("\n==== 测试案例2: Hero有3bet机会并且calls (Yes-Calls) ====")
    hand_text_calls = """
PokerStars Hand #RC3334563615: Hold'em No Limit ($0.25/$0.50) - 2023/06/01 12:35:56 ET
Table 'Test Table' 6-max Seat #1 is the button
Seat 1: Opp1 ($50)
Seat 2: Opp2 ($50)
Seat 3: Opp3 ($50)
Seat 4: Hero ($50)
Seat 5: Opp5 ($50)
Seat 6: Opp6 ($50)
Opp2: posts small blind $0.25
Opp3: posts big blind $0.50
*** HOLE CARDS ***
Dealt to Hero [Ah Kh]
Opp1: raises $1 to $1.50
Opp2: folds
Opp3: folds
Hero: calls $1.50
Opp5: folds
Opp6: folds
*** FLOP *** [2c 7h Ks]
Opp1: checks
Hero: bets $2.00
Opp1: folds
Uncalled bet ($2.00) returned to Hero
Hero collected $3.50 from pot
*** SUMMARY ***
Total pot $3.50 | Rake $0
Board [2c 7h Ks]
Seat 1: Opp1 (button) folded on the Flop
Seat 2: Opp2 (small blind) folded before Flop
Seat 3: Opp3 (big blind) folded before Flop
Seat 4: Hero collected ($3.50)
Seat 5: Opp5 folded before Flop
Seat 6: Opp6 folded before Flop
    """
    
    parser = PokerHandParser()
    hand_data = parser.parse_hand(hand_text_calls)
    
    print(f"Hero_Position: {hand_data.get('hero_position', 'N/A')}")
    print(f"Hero_3B_Chance: {hand_data.get('hero_3b_chance', 'N/A')}")
    print(f"Preflop_Actions: {hand_data.get('preflop_actions', 'N/A')}")
    
    # 测试案例3: Hero有3bet机会并且folds (Yes-folds)
    print("\n==== 测试案例3: Hero有3bet机会并且folds (Yes-folds) ====")
    hand_text_folds = """
PokerStars Hand #RC3334563616: Hold'em No Limit ($0.25/$0.50) - 2023/06/01 12:36:56 ET
Table 'Test Table' 6-max Seat #1 is the button
Seat 1: Opp1 ($50)
Seat 2: Opp2 ($50)
Seat 3: Opp3 ($50)
Seat 4: Hero ($50)
Seat 5: Opp5 ($50)
Seat 6: Opp6 ($50)
Opp2: posts small blind $0.25
Opp3: posts big blind $0.50
*** HOLE CARDS ***
Dealt to Hero [Ah Kh]
Opp1: raises $1 to $1.50
Opp2: folds
Opp3: folds
Hero: folds
Opp5: folds
Opp6: folds
Uncalled bet ($1.00) returned to Opp1
Opp1 collected $1.25 from pot
*** SUMMARY ***
Total pot $1.25 | Rake $0
Board []
Seat 1: Opp1 (button) collected ($1.25)
Seat 2: Opp2 (small blind) folded before Flop
Seat 3: Opp3 (big blind) folded before Flop
Seat 4: Hero folded before Flop
Seat 5: Opp5 folded before Flop
Seat 6: Opp6 folded before Flop
    """
    
    parser = PokerHandParser()
    hand_data = parser.parse_hand(hand_text_folds)
    
    print(f"Hero_Position: {hand_data.get('hero_position', 'N/A')}")
    print(f"Hero_3B_Chance: {hand_data.get('hero_3b_chance', 'N/A')}")
    print(f"Preflop_Actions: {hand_data.get('preflop_actions', 'N/A')}")
    
    # 测试案例4: Hero没有3bet机会 (NO)
    print("\n==== 测试案例4: Hero没有3bet机会 (NO) ====")
    hand_text_no = """
PokerStars Hand #RC3334601319: Hold'em No Limit ($0.25/$0.50) - 2023/06/01 12:34:56 ET
Table 'Test Table' 6-max Seat #1 is the button
Seat 1: Opp1 ($50)
Seat 2: Opp2 ($50)
Seat 3: Hero ($50)
Seat 4: Opp4 ($50)
Seat 5: Opp5 ($50)
Seat 6: Opp6 ($50)
Opp2: posts small blind $0.25
Opp3: posts big blind $0.50
*** HOLE CARDS ***
Dealt to Hero [Ah Kh]
Hero: raises $1 to $1.50
Opp4: folds
Opp5: folds
Opp6: folds
Opp1: folds
Opp2: calls $1.25
Opp3: folds
*** FLOP *** [2h 3h 4h]
Opp2: checks
Hero: bets $2
Opp2: folds
Uncalled bet ($2) returned to Hero
Hero collected $3 from pot
*** SUMMARY ***
Total pot $3 | Rake $0
Board [2h 3h 4h]
Seat 1: Opp1 (button) folded before Flop
Seat 2: Opp2 (small blind) folded on the Flop
Seat 3: Hero collected ($3)
Seat 4: Opp4 folded before Flop
Seat 5: Opp5 folded before Flop
Seat 6: Opp6 (big blind) folded before Flop
    """
    
    parser = PokerHandParser()
    hand_data = parser.parse_hand(hand_text_no)
    
    print(f"Hero_Position: {hand_data.get('hero_position', 'N/A')}")
    print(f"Hero_3B_Chance: {hand_data.get('hero_3b_chance', 'N/A')}")
    print(f"Preflop_Actions: {hand_data.get('preflop_actions', 'N/A')}")

if __name__ == "__main__":
    test_case() 