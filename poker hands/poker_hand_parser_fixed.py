def _determine_pool_preflop_summary(self):
    """确定整个池的翻前行动线，记录所有玩家的行动"""
    # 确保每个牌局都有记录
    if not self.preflop_all_actions:
        self.hand_data['pool_preflop_summary'] = 'No open all folds'
        return
    
    # 根据底池类型(pot_type)记录行动线
    pot_type = self.hand_data['pot_type']
    
    # 全部弃牌的情况
    if pot_type == 'No open all folds' or (len(self.active_players_at_flop) == 0 and all('folds' in action for action in self.preflop_all_actions)):
        self.hand_data['pool_preflop_summary'] = 'No open all folds'
        return
    
    # 检查是否有limp行为
    has_limp = False
    for action in self.preflop_all_actions:
        if 'calls' in action and not self.has_first_bet:
            has_limp = True
            break
    
    # 检查是否有limp后的加注
    has_raise_after_limp = False
    if has_limp:
        # 如果有人limp并且之后有人加注
        if has_raise_after_limp:
            # 检查是否有人call了加注
            has_call_after_raise = False
            for action in self.preflop_all_actions:
                if 'calls' in action and self.has_first_bet:
                    has_call_after_raise = True
                    break
            
            if has_call_after_raise:
                # 有人跟注加注，标记为limp-calls
                self.hand_data['pool_preflop_summary'] = 'limp-calls'
            else:
                # 没人跟注加注，标记为limp-folds
                self.hand_data['pool_preflop_summary'] = 'limp-folds'
            return
        # 如果只有limp没有加注
        else:
            # 收集所有limp的玩家位置
            limpers = []
            for action in self.preflop_all_actions:
                if 'calls' in action and not self.has_first_bet:
                    match = re.match(r'^(Hero|Opp)\(([^)]+)\)', action)
                    if match:
                        limpers.append(match.group(2))
            
            if limpers:
                self.hand_data['pool_preflop_summary'] = 'limped_' + '_'.join(limpers)
            else:
                self.hand_data['pool_preflop_summary'] = 'limped'
            return
    
    # SRP底池的情况 - 记录为 "位置_R_位置_C"
    if pot_type == 'SRP':
        if self.first_bet_player and self.first_bet_player in self.player_positions:
            raiser_pos = self.player_positions[self.first_bet_player]
            # 检查是否有人跟注
            callers = []
            for action in self.preflop_all_actions:
                if 'calls' in action and self.has_first_bet:
                    caller_match = re.match(r'^(Hero|Opp)\(([^)]+)\)', action)
                    if caller_match:
                        callers.append(caller_match.group(2))
            
            if callers:
                self.hand_data['pool_preflop_summary'] = f"{raiser_pos}_R_" + "_".join(f"{pos}_C" for pos in callers)
            else:
                self.hand_data['pool_preflop_summary'] = f"{raiser_pos}_R_all_fold"
        return
    
    # 3B底池的情况 - 记录3bet玩家和反应
    if pot_type == '3B':
        if self.three_bet_player and self.three_bet_player in self.player_positions:
            three_better_pos = self.player_positions[self.three_bet_player]
            # 检查第一个加注者的反应
            if self.first_bet_player in self.active_players_at_flop:
                first_better_pos = self.player_positions.get(self.first_bet_player, '')
                self.hand_data['pool_preflop_summary'] = f"{three_better_pos}_3B_{first_better_pos}_C"
            else:
                self.hand_data['pool_preflop_summary'] = f"{three_better_pos}_3B_all_fold"
        return 