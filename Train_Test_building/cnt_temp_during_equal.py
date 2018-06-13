import xlwt
import os
dir_in = "C:\\Users\RHB\Desktop\cnt_cause"
dir_out = "C:\\Users\RHB\Desktop\\add_cause"
list_path = []
'''
Sorted when add
'''
def get_rel_cnt_for_dir(dir_in):
    if os.path.exists(dir_in):
        for root, dirs, files in os.walk(dir_in):
            for filename in files:
                path_file = root + "\\" + filename
                list_path.append(path_file)
def from_cnt_2_score(list_path, dir_out):
    for path_in in list_path:
        # single file
        ground_truth = path_in.split("\\")[-1]
        path_out = dir_out+"\\"+ground_truth
        print(ground_truth)
        with open(path_in, "r") as r_f:
            # a line
            num = 0
            answers = r_f.readlines()
            # single line
            for answer in answers:
                dict_rel = {}
                list_rel_cnt = answer.split("|")
                for rel_cnt in list_rel_cnt:
                    num_rel_cnt = rel_cnt.split(" ")
                    if len(num_rel_cnt)>1:
                        num_ = num_rel_cnt[0]
                        rel_id = num_rel_cnt[1].split("=")
                        relation = rel_id[0]
                        cnt = rel_id[1]

                        dict_rel.update({relation: int(cnt)})

                with open(path_out, "a", encoding="utf-8") as w_f:
                    w_f.write(num_ + " ")

                list_score_sort = []
                dict_score_sort = {}
                # if "Contingency.Cause" in dict_rel.keys() and "Contingency.Condition" in dict_rel.keys():
                #     dict_rel.update({"Contingency": dict_rel["Contingency.Cause"]+dict_rel["Contingency.Condition"]})
                # if "Contingency.Cause" in dict_rel.keys() and "Contingency.Condition" not in dict_rel.keys():
                #     dict_rel.update({"Contingency": dict_rel["Contingency.Cause"]})
                # if "Contingency.Cause" not in dict_rel.keys() and "Contingency.Condition" in dict_rel.keys():
                #     dict_rel.update({"Contingency": dict_rel["Contingency.Condition"]})

                # if "Temporal.During" in dict_rel.keys() and "Temporal.Equals" in dict_rel.keys():
                #     dict_rel.update(
                #         {"Temporal.DuringEquals": dict_rel["Temporal.During"] + dict_rel["Temporal.Equals"]})
                # if "Temporal.During" in dict_rel.keys() and "Temporal.Equals" not in dict_rel.keys():
                #     dict_rel.update({"Temporal.DuringEquals": dict_rel["Temporal.During"]})
                # if "Temporal.During" not in dict_rel.keys() and "Temporal.Equals" in dict_rel.keys():
                #     dict_rel.update({"Temporal.DuringEquals": dict_rel["Temporal.Equals"]})

                for key_ in dict_rel.keys():
                    list_score_sort.append(int(dict_rel[key_]))
                list_score_sort.sort()
                # sorted when add
                for i in range(len(list_score_sort)):
                    score = list_score_sort[-i-1]
                    key_ = ""
                    for key in  dict_rel.keys():
                        if dict_rel[key] == score:
                            key_ = key
                            dict_rel.pop(key)
                            break
                    with open(path_out, "a", encoding="utf-8") as w_f:
                        w_f.write(key_+"="+str(score)+"|")
                with open(path_out, "a", encoding="utf-8") as w_f:
                    w_f.write("\n")
                    w_f.write("\n")

def from_cnt_2_score2(list_path, dir_out):
    for path_in in list_path:
        # single file
        ground_truth = path_in.split("\\")[-1]
        path_out = dir_out+"\\"+ground_truth
        print(ground_truth)
        with open(path_in, "r") as r_f:
            # a line
            num = 0
            answers = r_f.readlines()
            # single line
            for answer in answers:
                dict_rel = {}
                list_rel_cnt = answer.split(" ")
                num_ = list_rel_cnt[0]
                for rel_cnt in list_rel_cnt:
                    if "=" in rel_cnt:
                        rel_id = rel_cnt.split("=")
                        relation = rel_id[0]
                        cnt = rel_id[1]

                        dict_rel.update({relation: int(cnt)})

                with open(path_out, "a", encoding="utf-8") as w_f:
                    w_f.write(num_ + " ")

                list_score_sort = []
                dict_score_sort = {}
                # if "Contingency.Cause" in dict_rel.keys() and "Contingency.Condition" in dict_rel.keys():
                #     dict_rel.update({"Contingency": dict_rel["Contingency.Cause"]+dict_rel["Contingency.Condition"]})
                # if "Contingency.Cause" in dict_rel.keys() and "Contingency.Condition" not in dict_rel.keys():
                #     dict_rel.update({"Contingency": dict_rel["Contingency.Cause"]})
                # if "Contingency.Cause" not in dict_rel.keys() and "Contingency.Condition" in dict_rel.keys():
                #     dict_rel.update({"Contingency": dict_rel["Contingency.Condition"]})

                # if "Temporal.During" in dict_rel.keys() and "Temporal.Equals" in dict_rel.keys():
                #     dict_rel.update(
                #         {"Temporal.DuringEquals": dict_rel["Temporal.During"] + dict_rel["Temporal.Equals"]})
                # if "Temporal.During" in dict_rel.keys() and "Temporal.Equals" not in dict_rel.keys():
                #     dict_rel.update({"Temporal.DuringEquals": dict_rel["Temporal.During"]})
                # if "Temporal.During" not in dict_rel.keys() and "Temporal.Equals" in dict_rel.keys():
                #     dict_rel.update({"Temporal.DuringEquals": dict_rel["Temporal.Equals"]})

                for key_ in dict_rel.keys():
                    list_score_sort.append(int(dict_rel[key_]))
                list_score_sort.sort()
                # sorted when add
                for i in range(len(list_score_sort)):
                    score = list_score_sort[-i-1]
                    key_ = ""
                    for key in  dict_rel.keys():
                        if dict_rel[key] == score:
                            key_ = key
                            dict_rel.pop(key)
                            break
                    with open(path_out, "a", encoding="utf-8") as w_f:
                        w_f.write(key_+"="+str(score)+"|")
                with open(path_out, "a", encoding="utf-8") as w_f:
                    w_f.write("\n")
                    w_f.write("\n")
get_rel_cnt_for_dir(dir_in)
from_cnt_2_score(list_path, dir_out)
