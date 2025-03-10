import re
from poker_hand_parser_ok import PokerHandParser

# 创建解析器实例
parser = PokerHandParser()

# 测试弃牌动作
print("测试弃牌动作记录:")
parser.parse_action('Hero: folds')
print(f"Preflop actions: {parser.hand_data['preflop_actions']}")

# 测试其他街的弃牌动作
parser.current_street = 'flop'
parser.parse_action('Opp(BTN): folds')
print(f"Flop actions: {parser.hand_data['flop_actions']}")

print("\n测试完成")