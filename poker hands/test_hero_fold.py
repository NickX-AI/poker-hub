import os
from poker_hand_parser import PokerHandParser

def test_hero_fold():
    print("开始测试Hero弃牌标记...")
    
    # 打开GG文件
    current_dir = os.path.dirname(os.path.abspath(__file__))
    hands_file = os.path.join(current_dir, 'poker_input', 'GG20250217-1205 - RushAndCash638879 - 0.02 - 0.05 - 6max.txt')
    
    if not os.path.exists(hands_file):
        print(f"文件不存在: {hands_file}")
        return
        
    with open(hands_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # 按照手牌分割文件内容，使用"Poker Hand #"作为分隔符
    hands = content.split('Poker Hand #')
    
    # 测试前20个手牌
    test_count = 0
    fold_count = 0
    folds_to_open_count = 0
    
    for i, hand in enumerate(hands[1:50]):  # 跳过第一个空元素，测试前50个手牌
        hand_text = 'Poker Hand #' + hand  # 注意这里使用的是Poker Hand #
        parser = PokerHandParser()
        
        try:
            # 解析手牌
            print(f"\n\n测试手牌 #{i+1} ...")
            hand_data = parser.parse_hand(hand_text)
            
            # 检查是否有Hero_Preflop_Summary
            hero_summary = hand_data.get('hero_preflop_summary', '')
            print(f"手牌ID: {hand_data.get('hand_id', '')}")
            print(f"Hero位置: {hand_data.get('hero_position', '')}")
            print(f"Hero_Preflop_Summary: {hero_summary}")
            
            if 'fold' in hero_summary.lower():
                test_count += 1
                print(f"Preflop_Actions: {hand_data.get('preflop_actions', '')}")
                # 打印preflop_all_actions，帮助诊断问题
                print(f"Preflop_All_Actions: {parser.preflop_all_actions}")
                
                # 统计不同类型的fold
                if hero_summary == 'folds':
                    fold_count += 1
                elif hero_summary == 'folds to open':
                    folds_to_open_count += 1
                
        except Exception as e:
            print(f"解析手牌出错: {e}")
            print(f"错误手牌内容: {hand_text[:200]}...")
    
    print(f"\n总共测试了 {test_count} 个包含Hero弃牌的手牌")
    print(f"其中 'folds' 类型有 {fold_count} 个")
    print(f"其中 'folds to open' 类型有 {folds_to_open_count} 个")

if __name__ == "__main__":
    test_hero_fold() 