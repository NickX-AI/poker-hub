import os
from poker_hand_parser import test_case, process_poker_file

# 执行测试用例验证修复
print("\n=== 运行测试用例 ===")
test_case()

# 如果输入文件存在，运行真实数据测试
print("\n=== 检查真实数据处理 ===")
current_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(current_dir, 'poker_input', 'combined_1.txt')
output_file = os.path.join(current_dir, 'poker_output', 'parsed_hands_fixed_direct.csv')

# 确保输入和输出目录存在
os.makedirs('poker_input', exist_ok=True)
os.makedirs('poker_output', exist_ok=True)

if os.path.exists(input_file):
    print(f"找到输入文件: {input_file}")
    try:
        process_poker_file(input_file, output_file)
        print(f"处理完成。结果已保存到 {output_file}")
        
        # 检查输出文件是否存在
        if os.path.exists(output_file):
            # 读取并显示前几行CSV数据
            import csv
            with open(output_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if i >= 3:  # 只显示前3条数据
                        break
                    print(f"\n==== 第 {i+1} 行数据 ====")
                    print(f"Preflop_1st_Bet: {row['Preflop_1st_Bet'][:70]}...")
                    print(f"Preflop_3B: {row['Preflop_3B'][:70]}..." if row['Preflop_3B'] else "Preflop_3B: 空")
                    print(f"Preflop_4B: {row['Preflop_4B'][:70]}..." if row['Preflop_4B'] else "Preflop_4B: 空")
    except Exception as e:
        print(f"处理过程中发生错误: {e}")
else:
    print(f"输入文件不存在: {input_file}")
    print("请确保在poker_input目录中有combined_1.txt文件") 