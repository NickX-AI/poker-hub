import csv

# 打开CSV文件
with open('poker_output/parsed_hands.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    
    # 打印标题行长度
    print(f"标题行长度: {len(header)}")
    
    # 打印所有标题
    for i, title in enumerate(header):
        print(f"{i+1}. {title}")
    
    # 检查是否包含Pool_Preflop_Summary和Hero_Preflop_Summary
    if 'Pool_Preflop_Summary' in header:
        print(f"Pool_Preflop_Summary在第{header.index('Pool_Preflop_Summary')+1}列")
    else:
        print("未找到Pool_Preflop_Summary")
        
    if 'Hero_Preflop_Summary' in header:
        print(f"Hero_Preflop_Summary在第{header.index('Hero_Preflop_Summary')+1}列")
    else:
        print("未找到Hero_Preflop_Summary")
        
    # 检查是否包含preflop_summary和hero_summary
    if 'preflop_summary' in header:
        print(f"preflop_summary在第{header.index('preflop_summary')+1}列")
    else:
        print("未找到preflop_summary")
        
    if 'hero_summary' in header:
        print(f"hero_summary在第{header.index('hero_summary')+1}列")
    else:
        print("未找到hero_summary")
        
    # 检查数据
    rows = list(reader)
    print(f"\n总共有 {len(rows)} 行数据")
    
    # 检查Pool_Preflop_Summary和Hero_Preflop_Summary列的数据
    if 'Pool_Preflop_Summary' in header:
        pool_preflop_summary_index = header.index('Pool_Preflop_Summary')
        pool_preflop_summary_values = [row[pool_preflop_summary_index] for row in rows if row[pool_preflop_summary_index]]
        print(f"Pool_Preflop_Summary列有 {len(pool_preflop_summary_values)} 个非空值")
        print(f"Pool_Preflop_Summary列的前5个值: {pool_preflop_summary_values[:5]}")
        
    if 'Hero_Preflop_Summary' in header:
        hero_preflop_summary_index = header.index('Hero_Preflop_Summary')
        hero_preflop_summary_values = [row[hero_preflop_summary_index] for row in rows if row[hero_preflop_summary_index]]
        print(f"Hero_Preflop_Summary列有 {len(hero_preflop_summary_values)} 个非空值")
        print(f"Hero_Preflop_Summary列的前5个值: {hero_preflop_summary_values[:5]}")
        
    # 检查preflop_summary和hero_summary列的数据
    if 'preflop_summary' in header:
        preflop_summary_index = header.index('preflop_summary')
        preflop_summary_values = [row[preflop_summary_index] for row in rows if row[preflop_summary_index]]
        print(f"preflop_summary列有 {len(preflop_summary_values)} 个非空值")
        print(f"preflop_summary列的前5个值: {preflop_summary_values[:5]}")
        
    if 'hero_summary' in header:
        hero_summary_index = header.index('hero_summary')
        hero_summary_values = [row[hero_summary_index] for row in rows if row[hero_summary_index]]
        print(f"hero_summary列有 {len(hero_summary_values)} 个非空值")
        print(f"hero_summary列的前5个值: {hero_summary_values[:5]}") 