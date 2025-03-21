import csv
import os

def check_csv():
    # 使用绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, 'poker_output', 'parsed_hands.csv')
    
    # 检查文件是否存在
    if not os.path.exists(csv_file):
        print(f"错误：CSV文件 {csv_file} 不存在。")
        return
    
    print(f"检查CSV文件: {csv_file}")
    
    # 读取CSV文件并显示关键字段
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if count < 20:  # 只显示前20条记录
                print(f"记录 {count+1}:")
                print(f"  Cash_Drop: {row.get('Cash_Drop', 'N/A')}")
                print(f"  Hero_Position: {row.get('Hero_Position', 'N/A')}")
                print(f"  Hero_3B_Chance: {row.get('Hero_3B_Chance', 'N/A')}")
                print()
            count += 1
        
        print(f"总共读取了 {count} 条记录")

if __name__ == "__main__":
    check_csv() 