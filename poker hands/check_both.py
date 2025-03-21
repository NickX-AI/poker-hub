import csv

def count_records_with_fields():
    with open('parsed_hands.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        total = 0
        hero_summary_count = 0
        pool_summary_count = 0
        both_count = 0
        none_count = 0
        
        for row in reader:
            total += 1
            has_hero = bool(row.get('Hero_Preflop_Summary', '').strip())
            has_pool = bool(row.get('Pool_Preflop_Summary', '').strip())
            
            if has_hero and has_pool:
                both_count += 1
            elif has_hero:
                hero_summary_count += 1
            elif has_pool:
                pool_summary_count += 1
            else:
                none_count += 1
        
        print(f"总记录数: {total}")
        print(f"同时包含Hero和Pool Preflop Summary的记录数: {both_count}")
        print(f"只包含Hero Preflop Summary的记录数: {hero_summary_count}")
        print(f"只包含Pool Preflop Summary的记录数: {pool_summary_count}")
        print(f"两者都不包含的记录数: {none_count}")

if __name__ == "__main__":
    count_records_with_fields() 