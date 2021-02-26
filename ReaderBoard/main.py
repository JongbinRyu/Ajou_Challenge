from glob import glob
import os
import sys
import json
import datetime
from pytz import timezone, utc
from mdutils.mdutils import MdUtils
from mdutils.fileutils.fileutils import MarkDownFile
from pathlib import Path

# append local directory
cur_path = Path(__file__).parent.absolute()
os.chdir(cur_path)
sys.path.append('./')
from Score import update_total_score
from utils import read_json, read_txt, write_json
from Init import update_name_list, make_log_readme

def main(update=True, penalty_count = 3):
    KST = timezone(zone='Asia/Seoul')
    now = datetime.datetime.utcnow()
    # UTC 기준 naive datetime : datetime.datetime(2019, 2, 15, 4, 18, 28, 805879)
    utc.localize(now)
    # UTC 기준 aware datetime : datetime.datetime(2019, 2, 15, 4, 18, 28, 805879, tzinfo=<UTC>)
    KST.localize(now)
    # UTC 시각, 시간대만 KST : datetime.datetime(2019, 2, 15, 4, 18, 28, 805879, tzinfo=<DstTzInfo 'Asia/Seoul' KST+9:00:00 STD>)
    now_kst_aware = utc.localize(now).astimezone(KST)
    current_time = str(now_kst_aware)
    # KST 기준 aware datetime : datetime.datetime(2019, 2, 15, 13, 18, 28, 805879, tzinfo=<DstTzInfo 'Asia/Seoul' KST+9:00:00 STD>)

    # init and update name list
    update_name_list(update)

    # load data
    name_list_dict = read_json('db/namelist.json')
    name_list = name_list_dict['namelist']
    answer = read_txt('db/ans.txt')
    score_rules = read_json("db/ScoreRule.json")
    log = read_json("db/log.json")

    for person in name_list:
        name = person['name']
        if 'penalty' not in person:
            person['penalty'] = 0
        submissions = glob('../submission/{}/*'.format(name))
        if len(submissions) < 3:
            continue

        avg_accuracy = 0

        for submission in submissions:
            with open(submission, 'rt') as f:
                pred_list = list(f.readlines())
                avg_accuracy += sum([x == y for x, y in zip(pred_list, answer)]) / len(answer) * 100

        avg_accuracy = round(avg_accuracy / 3, 5)

        if avg_accuracy != person['last_accuracy']:
            person['total_count'] += 1
            person['last_submission'] = current_time
            day_cnt = 1
            for row in log[name]:
                submission_time = row[1].split(" ")[0].split("-")
                if now_kst_aware.month == int(submission_time[1]) and now_kst_aware.day == int(submission_time[2]):
                    day_cnt += 1
            if day_cnt > penalty_count:
                day_cnt = penalty_count - day_cnt
                person['penalty'] += -day_cnt
            accord = [avg_accuracy, current_time, day_cnt]
            log[name].append(accord)
            make_log_readme(name, log[name])

        if avg_accuracy > person['avg_accuracy']:
            person['avg_accuracy'] = avg_accuracy
        person['last_accuracy'] = avg_accuracy

    name_list.sort(key=lambda x : (x['total_score'], x['avg_accuracy']), reverse=True)
    avg_accuracy = round(sum([person['avg_accuracy'] for person in name_list]) / len(name_list), 2)
    top_ranker = name_list[0]['name']

    # new readme create
    new_readme = MdUtils(file_name='Example_Markdown')

    # update scheduled event
    update_total_score(name_list_dict, score_rules, now_kst_aware)

    # applied rule
    now_rule_id = -1
    for rule_id, rule in enumerate(score_rules):
        date_rule = datetime.datetime.strptime(rule['date'], '%Y-%m-%d %H:%M:%S')
        date_rule = KST.localize(date_rule)
        if date_rule <= now_kst_aware:
            now_rule_id = rule_id

    if len(score_rules) == 0:
        current_rule = "Total Score 업데이트 계획이 없습니다."
    else:
        if now_rule_id == -1:
            current_rule = "- Total Score가 아직 업데이트되지 않았습니다. \n - 다음 업데이트 일정은 {}({}) 입니다.\n".format(score_rules[0]['rule_name'], score_rules[0]['date'].split(' ')[0])
        elif now_rule_id == len(score_rules)-1:
            current_rule = "{}({}): Total Score가 최종 업데이트 되었습니다.".format(score_rules[-1]['rule_name'], name_list_dict['total_score_update_time'])
        else:
            current_rule = "- {}({}): Total Score가 업데이트 되었습니다.  \n - 다음 업데이트 일정은 {}({}) 입니다.\n".format(score_rules[now_rule_id]['rule_name'], name_list_dict['total_score_update_time'], score_rules[now_rule_id+1]['rule_name'], score_rules[now_rule_id+1]['date'].split(' ')[0])


    new_readme.new_line(current_rule)

    # top score
    if now_rule_id == len(score_rules)-1:
        new_readme.new_line(f"**최종 랭킹 1위는 {top_ranker} 입니다. 평균 accuracy는 {avg_accuracy}% 입니다.**")
    else:
        new_readme.new_line(f"**현재 랭킹 1위는 {top_ranker} 입니다. 평균 accuracy는 {avg_accuracy}% 입니다.**")

    # make reader board
    list_of_strings = ["Ranking", "Name", "Penalty", "Accuracy(%)", "Last Submission", "Total Submission Count", "Total Score(%)"]
    for x in range(len(name_list)):
        item = name_list[x]
        list_of_strings.extend([str(x+1), item['name'], str(item["penalty"]), str(item['avg_accuracy']), item['last_submission'], str(item['total_count']), str(item['total_score'])])
    new_readme.new_table(columns=7, rows=len(name_list)+1, text=list_of_strings, text_align='center')
    new_readme.new_paragraph("**정확도는 소숫점 5자리 까지 출력됩니다.**\n**Time zone is seoul,korea (UTC+9:00)**\n")

    readme_path = "../README.md"
    readme_content = MarkDownFile.read_file(readme_path)

    readme = MarkDownFile(readme_path)
    from_ = readme_content.find("## 퍼블릭 랭킹") + 11
    to_ = readme_content.find("## 퍼블릭 랭킹 제출 방법")
    readme_content = readme_content[:from_] + new_readme.file_data_text + readme_content[to_:]
    readme.rewrite_all_file(readme_content)

    write_json('db/namelist.json', name_list_dict)
    write_json("db/log.json", log)

if __name__ == '__main__':
    main()