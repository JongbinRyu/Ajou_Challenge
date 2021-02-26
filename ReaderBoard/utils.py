import json
from mdutils.mdutils import MdUtils
from mdutils.fileutils.fileutils import MarkDownFile


def write_json(fileName, data):
    with open(fileName, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read_json(fileName):
    with open(fileName, 'rt', encoding='utf-8') as f:
         json_data = json.load(f)
    return json_data

def read_txt(fileName):
    with open(fileName, 'rt') as f:
        list_data = list(f.readlines())
    return list_data

def make_log_readme(name, log=None):
    # new readme create
    new_readme = MdUtils(file_name="../Log/"+name)
    new_readme.new_line("## 제출 기록")
    new_readme.new_line("이름 : " + name)
    if log:
        accs = [row[0] for row in log]
        avg_acc = sum(accs) / len(accs)
        max_acc = max(accs)
        new_readme.new_line("**현재 평균 정확도는 {} 입니다. 최고 정확도는 {} 입니다.**".format(avg_acc, max_acc))
        new_readme.new_line("**Day Count가 음수인 경우 감점 제출을 의미 합니다.(해당 날짜에 많이 제출 할 수록 페널티 점수가 커집니다.)**")
        # make log history
        list_of_strings = ["No", "Accuracy(%)", "Submission Time", "Day Count"]
        for row, item in enumerate(log):
            list_of_strings.extend(
                [str(row + 1), str(item[0]), item[1], str(item[2])])
        new_readme.new_table(columns=4, rows=len(log) + 1, text=list_of_strings, text_align='center')
        new_readme.new_paragraph("**정확도는 소숫점 5자리 까지 출력됩니다.**\n**Time zone is seoul,korea (UTC+9:00)**\n")
    else:
        new_readme.new_line("아직 제출이 없습니다. 첫번째 제출을 서둘러주세요!")
    new_readme.create_md_file()


