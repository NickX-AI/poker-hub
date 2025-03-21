import csv
import os

def check_output_csv():
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'poker_output', 'parsed_hands.csv')
    
    if not os.path.exists(csv_path):
        print(f"无法找到CSV文件: {csv_path}")
        return
    
    print(f"正在读取文件: {csv_path}")
    
    # 统计新增字段的值
    flop_fields = {
        'Flop_Cbet_IP': {},
        'Flop_Cbet_OOP': {},
        'Flop_Face_to_Cbet': {},
        'Flop_Raises_to_Cbet_IP': {},
        'Flop_Donk': {},
        'Flop_Texture': {}
    }
    
    total_records = 0
    flop_records = 0
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # 显示所有CSV字段名
        print("\nCSV文件的字段名:")
        for fieldname in reader.fieldnames:
            print(f"- {fieldname}")
        
        # 重新打开文件，因为已经迭代过reader
        f.seek(0)
        # 跳过标题行
        next(f)
        reader = csv.DictReader(f)
        
        # 检查字段是否在CSV中
        header = reader.fieldnames
        for field in flop_fields.keys():
            if field not in header:
                print(f"警告: {field} 不在CSV字段中")
        
        # 读取数据
        for row in reader:
            total_records += 1
            
            # 检查是否有翻牌
            if row.get('Flop_Cards', ''):
                flop_records += 1
                
                # 统计各字段的值
                for field in flop_fields.keys():
                    value = row.get(field, 'NA')
                    flop_fields[field][value] = flop_fields[field].get(value, 0) + 1
    
    print(f"\n总共分析了 {total_records} 条记录，其中 {flop_records} 条有翻牌")
    
    # 输出各字段的统计信息
    for field, values in flop_fields.items():
        print(f"\n{field} 字段的值分布:")
        for value, count in sorted(values.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                percentage = (count / flop_records) * 100 if flop_records > 0 else 0
                print(f"- {value}: {count} ({percentage:.2f}%)")

if __name__ == "__main__":
    check_output_csv() 