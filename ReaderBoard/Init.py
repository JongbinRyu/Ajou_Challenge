import os
import sys
import json
import shutil
import traceback
import datetime
from utils import make_log_readme

def update_name_list(append_new_name=False):
    """
    Init and Update Project whenever "namelist.txt" changed
    :param append_new_name: If set it True, new name will be added to "namelist.json" when
    "namelist.txt" files changed.
    :return:
    """
    # 1. load name list
    try:
        with open('db/namelist.txt', 'r', encoding='utf-8') as f:
            new_names = [name.strip('\n') for name in f.readlines()]
            names = [{"name": name,
                      "last_submission": "Not Yet",
                      "total_count": 0,
                      "avg_accuracy": 0,
                      "total_score": 0,
                      "last_accuracy": 0,
                      "penalty": 0 } for name in new_names]
    except (FileExistsError, FileNotFoundError) as e:
        print("First make namelist.txt")
        traceback.print_exc()
        sys.exit(1)

    # 2. load ScoreRules
    try:
        with open('db/ScoreRule.json', 'rt', encoding='utf-8') as f:
            score_rules = json.load(f)
    except (FileExistsError, FileNotFoundError) as e:
        print("Second make ScoreRule.json")
        traceback.print_exc()
        sys.exit(1)

    # Case 1 : create namelist.json
    if not os.path.exists('db/namelist.json'):
        # add score rule variable
        for name in names:
            print(name['name'] + " related directory created!")
            if not os.path.exists('../submission/'+name['name']):
                os.makedirs('../submission/'+name['name'])

            for rule in score_rules:
                name[rule['var_name']] = 0

        name_list_dict = dict({"total_score_update_time":""})
        name_list_dict["namelist"] = names
        with open('db/namelist.json', 'w', encoding='utf-8') as f:
            json.dump(name_list_dict, f, ensure_ascii=False, indent=4)

    # Case 2 : create log.json
    if not os.path.exists('db/log.json'):
        if not os.path.exists('../Log'):
            os.makedirs('../Log')
        log_dict = {}
        for name in new_names:
            print(name + " related log created!")
            log_dict[name] = []
            make_log_readme(name)

        with open('db/log.json', 'w', encoding='utf-8') as f:
            json.dump(log_dict, f, ensure_ascii=False, indent=4)


    # Case 3 : update to new name list & Log Json & Log ReadMe
    elif(append_new_name):
        with open('db/namelist.json', 'rt', encoding='utf-8') as f:
            name_list_dict = json.load(f)
            name_list = [person['name'] for person in name_list_dict['namelist'] if person['name'] in new_names]

            # filter name not appeared in namelist.txt files
            new_name_list = [person for person in name_list_dict['namelist'] if person['name'] in new_names]
        with open('db/log.json', 'rt', encoding='utf-8') as f:
            log_dict = json.load(f)
            new_log_dict = {name : log for name, log in log_dict.items() if name in new_names}

        # delete Submission Folder and Read Me
        for person in name_list_dict['namelist']:
            name = person['name']
            if name not in new_names:
                print(name + " related directory removed!")
                if os.path.exists('../submission/'+name):
                    shutil.rmtree('../submission/'+name)
                if os.path.exists('../Log/'+name+'.md'):
                    os.remove('../Log/' + name + '.md')

        # append new names to new_name_list
        for name in new_names:
            if name not in name_list:
                print(name + " related directory created!")
                print(name + " related log created!")
                if not os.path.exists('../submission/' + name):
                    os.makedirs('../submission/' + name)
                # make Log ReadMe
                make_log_readme(name)
                # add score rule variable
                person = {"name": name,
                          "last_submission": "Not Yet",
                          "total_count": 0,
                          "avg_accuracy": 0,
                          "last_accuracy": 0,
                          "total_score": 0,
                          "penalty": 0 }
                for rule in score_rules:
                    person[rule['var_name']] = 0
                new_name_list.append(person)
                new_log_dict[name] = []

        name_list_dict['namelist'] = new_name_list

        # save it
        with open('db/namelist.json', 'w', encoding='utf-8') as f:
            json.dump(name_list_dict, f, ensure_ascii=False, indent=4)

        with open('db/log.json', 'w', encoding='utf-8') as f:
            json.dump(new_log_dict, f, ensure_ascii=False, indent=4)

