import os
import json
import datetime
from pytz import timezone, utc

def update_total_score(name_list_dict, score_rules, now_kst_aware, penalty_const=.1):
    """
    Update Total Score when scheduled day written in "ScoreRule.json"
    :param name_list_dict: This contains contestants score info loaded from "namelist.json"
    :param score_rules: Score rules loaded from "ScoreRule.json"
    :param now_kst_aware: Current Aware Time(UTC difference info stored) for Korea/Seoul(+9:00)
    :return: None
    """
    current_time = str(now_kst_aware)
    name_list = name_list_dict['namelist']
    # Read Score Rules and Calculate total score
    for rule in score_rules:
        date_rule = datetime.datetime.strptime(rule['date'], '%Y-%m-%d %H:%M:%S')
        if now_kst_aware.month == date_rule.month and now_kst_aware.day == date_rule.day:
            name_list_dict['total_score_update_time'] = current_time
            print("Today is {} Update scheduled as {}".format(rule["var_name"], rule['date']))
            # Todo: change 'avg_accuracy' to 'last_accuracy'
            for info in name_list:
                info[rule["var_name"]] = info['avg_accuracy']

    for info in name_list:
        total_score = 0
        for rule in score_rules:
            total_score += info[rule['var_name']] * rule['weight']
        total_score -= info["penalty"] * penalty_const
        info['total_score'] = round(total_score, 5)