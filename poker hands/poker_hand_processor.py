import os
import sys
import argparse
from poker_hand_parser_ok import PokerHandParser

def process_poker_files(input_files, output_file):
    """
    处理多个扑克手牌文件并将结果输出到一个CSV文件
    
    Args:
        input_files: 输入文件路径列表
        output_file: 输出CSV文件路径
    """
    parser = PokerHandParser()
    all_hands = []
    
    # 处理每个输入文件
    for input_file in input_files:
        print(f"\n处理文件: {input_file}")
        current_hand = []
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        current_hand.append(line)
                    elif current_hand:
                        hand_text = ''.join(current_hand)
                        print("处理新的手牌...")
                        hand_data = parser.parse_hand(hand_text)
                        # 添加 BB 单位到所有底池值
                        for key in ['preflop_pot', 'flop_pot', 'turn_pot', 'river_pot', 'total_pot']:
                            if hand_data[key] > 0:
                                hand_data[key] = f"{hand_data[key]}BB"
                            else:
                                hand_data[key] = "0BB"
                        all_hands.append(hand_data)
                        current_hand = []
            
            # 处理最后一手牌（如果存在）
            if current_hand:
                hand_text = ''.join(current_hand)
                print("处理最后一手牌...")
                hand_data = parser.parse_hand(hand_text)
                # 添加 BB 单位到所有底池值
                for key in ['preflop_pot', 'flop_pot', 'turn_pot', 'river_pot', 'total_pot']:
                    if hand_data[key] > 0:
                        hand_data[key] = f"{hand_data[key]}BB"
                    else:
                        hand_data[key] = "0BB"
                all_hands.append(hand_data)
        except Exception as e:
            print(f"处理文件 {input_file} 时出错: {str(e)}")
    
    print(f"\n总共处理了 {len(all_hands)} 手牌")
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 写入CSV文件
    if all_hands:
        import csv
        fieldnames = list(all_hands[0].keys())
        # 创建自定义标题映射
        custom_headers = {
            'result': 'Result(Hero)',
            'total_pot': 'Total_Pot',
            'preflop_pot': 'Preflop_Pot',
            'flop_pot': 'Flop_Pot',
            'turn_pot': 'Turn_Pot',
            'river_pot': 'River_Pot'
        }
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            # 写入自定义标题
            header_row = {field: custom_headers.get(field, field) for field in fieldnames}
            writer.writerow(header_row)
            writer.writerows(all_hands)
            print(f"数据已写入 {output_file}")
    else:
        print("没有找到任何手牌数据")

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='扑克手牌解析工具')
    parser.add_argument('-i', '--input', nargs='+', required=True, 
                        help='输入文件路径，可以指定多个文件')
    parser.add_argument('-o', '--output', required=True, 
                        help='输出CSV文件路径')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 处理文件
    process_poker_files(args.input, args.output)

if __name__ == '__main__':
    main() 