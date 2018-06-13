import os
import sys
import shutil


temp, dir_, a_contingency, b_expansion, file, time = sys.argv
a_contingency = float(a_contingency)
b_expansion = float(b_expansion)

dir_in = dir_
dir_out = "/home/xzdong/rhb/Ding/score_dev_c"+"/" + file+ "/"+str(a_contingency)+"_"+str(b_expansion)
if os.path.exists(dir_out):
    shutil.rmtree(dir_out)
os.makedirs(dir_out)

path_result = "/home/xzdong/rhb/Ding/c_dev"+"/"+ file+time
list_rel = []   # store the relation name
list_path_in = []

'''
Need to sort the score
'''
# the number of each relation in the VSRB
dict_rel_score_single = {"Comparison.Contrast": 223852765,
                         "Temporal.Beforeafter": 102654075,
                         "Contingency.Cause": 63645726,
                         "Temporal.During": 20370938,
                         "Expansion.Confirmation": 17350847,
                         "Temporal.Equals": 9274890,
                         "Expansion.Conjunction": 10567012,
                         "Contingency.Condition": 7300612,
                         "Comparison.Coreference": 9833308,
                         "Temporal.DuringEquals":29645828,
                         "Contingency": 70946338,
                         "all": 464850173
}



# walk the dir
def get_rel_cnt_for_dir(dir_in):
    if os.path.exists(dir_in):
        for root, dirs, files in os.walk(dir_in):
            for filename in files:
                path_file = root + "/" + filename
                list_path_in.append(path_file)


def del_useless_rel_for_cnt(list_path_in, dir_out):
    """
    delete the relation and its score that we dont want from the file

    :param list_path_in: the list of the path that we read in
    :param dir_out: the dir of the path that we write out
    :param list_useless_rel: the list of the relation we want to delete
    :return:
    """
    for path_in in list_path_in:
        ground_truth = path_in.split("/")[-1]  # store the relation of the ground truth, to form a full out path
        print(ground_truth)
        path_out = dir_out + "/" + ground_truth
        with open(path_in, 'r') as r_f:
            all_ = r_f.readlines()
            for single in all_:
                # a line
                dict_rel_score = {}
                list_score = []
                list_num_other = single.split(" ")
                if len(list_num_other)>1:
                    num_ = list_num_other[0]
                    with open(path_out, "a", encoding="utf-8") as w_f:
                        w_f.write(num_+" ")
                    other = list_num_other[1]
                    list_rel_cnt = other.split("|")
                    for r in list_rel_cnt:
                        flag_write = True
                        # get the cnt of this relation
                        if "=" in r:
                            rel_ = r.split("=")[0]
                            cnt = r.split("=")[1]
                            score = 0
                            if "Contingency" in rel_:
                                score = a_contingency * int(cnt) * dict_rel_score_single["all"] / dict_rel_score_single[rel_]
                            if "Expansion" in rel_:
                                score = b_expansion * int(cnt) * dict_rel_score_single["all"] / dict_rel_score_single[rel_]
                            if "Comparison" in rel_:
                                score = int(cnt) * dict_rel_score_single["all"] / dict_rel_score_single[rel_]
                            dict_rel_score.update({rel_: score})
                            list_score.append(score)
                    list_score.sort()

                    for i in range(len(list_score)):
                        for key_ in dict_rel_score:
                            if dict_rel_score[key_] == list_score[-i-1]:
                                with open(path_out, "a", encoding="utf-8") as w_f:
                                    w_f.write(key_+"="+ str(dict_rel_score[key_])+"|")
                    with open(path_out, "a", encoding="utf-8") as w_f:
                        w_f.write("\n")
                        w_f.write("\n")

def get_path(dir_in):
    list_path = []
    if os.path.exists(dir_in):
        for root, dirs, files in os.walk(dir_in):
            for filename in files:
                path_file = root + "/" + filename
                list_path.append(path_file)
    return list_path

def get_all_cnt(list_path):
    dict_rel_allCnt = {}
    for path in list_path:
        ground_truth = path.split("/")[-1]
        print(ground_truth)
        list_answer_relations = []

        with open(path, "r") as r_f:
            # a line
            answers = r_f.readlines()
            for answer in answers:
                if answer != "\n":
                    answer_relation = answer.split("|")[0].split("=")[0].split(" ")[1]
                    list_answer_relations.append(answer_relation)

        if ground_truth in dict_rel_allCnt.keys():
            dict_rel_allCnt.update({ground_truth: list_answer_relations})
        else:
            dict_rel_allCnt.update({ground_truth: list_answer_relations})
    return dict_rel_allCnt


def compute_subPrf(dict_all_ground_ansList):
    print("%-25s\t%-20s\t%-20s\t%-20s\t" % ("Subrelation", "P", "R", "F"))
    for ground_truth in dict_all_ground_ansList.keys():
        ground_truth_rela_list = dict_all_ground_ansList[ground_truth]
        TP = 0
        FP = 0
        for answer_rel in ground_truth_rela_list:
            if answer_rel == ground_truth:
                TP = TP + 1
        for other_relation in dict_all_ground_ansList:
            if other_relation == ground_truth:
                continue
            else:
                other_answer_rela_list = dict_all_ground_ansList[other_relation]
                for other_rel in other_answer_rela_list:
                    if other_rel == ground_truth:
                        FP = FP + 1

        R = 1.0 * TP / len(ground_truth_rela_list)
        P = 0
        if TP + FP != 0:
            P = 1.0 * TP / (TP + FP)
        F = 0
        if P + R != 0:
            F = 2 * P * R / (P + R)

        print("%-25s\t%-20s\t%-20s\t%-20s\t" % (ground_truth, P, R, F))

def compute_topPrf(dict_all_ground_ansList):
    print("%-25s\t%-20s\t%-20s\t%-20s\t" % ("Toprelation", "P", "R", "F"))
    dict_top_all_g_ansList = {}
    for ground_truth in dict_all_ground_ansList.keys():
        top_ground_truth = ground_truth.split(".")[0]

        set_top_rela = []
        if top_ground_truth in dict_top_all_g_ansList.keys():
            set_top_rela = dict_top_all_g_ansList[top_ground_truth]

        list_ground_truth_rel = dict_all_ground_ansList[ground_truth]
        for rel in list_ground_truth_rel:
            rel = rel.split(".")[0]
            set_top_rela.append(rel)
        dict_top_all_g_ansList.update({top_ground_truth: set_top_rela})

    for top_ground_truth in dict_top_all_g_ansList:
        ground_truth_rela_list = dict_top_all_g_ansList[top_ground_truth]
        TP = 0
        FP = 0
        for answer_rel in ground_truth_rela_list:
            if answer_rel == top_ground_truth:
                TP = TP + 1
        for other_relation in dict_top_all_g_ansList:
            if other_relation == top_ground_truth:
                continue
            else:
                other_answer_rela_list = dict_top_all_g_ansList[other_relation]
                for other_rel in other_answer_rela_list:
                    if other_rel == top_ground_truth:
                        FP = FP + 1

        R = 1.0 * TP / len(ground_truth_rela_list)
        P = 0
        if TP + FP != 0:
            P = 1.0 * TP / (TP + FP)
        F = 0
        if (P + R) > 0:
            F = 2 * P * R / (P + R)

        print("%-25s\t%-20s\t%-20s\t%-20s\t" % (top_ground_truth, P, R, F))


def computeMacroAvgPrf(dict_all_ground_ansList):
    sum_P = 0
    sum_R = 0
    sum_F = 0
    rela_cnt = len(dict_all_ground_ansList)
    for ground_truth in dict_all_ground_ansList.keys():
        answerList_ground_truth = dict_all_ground_ansList[ground_truth]
        TP = 0
        FP = 0
        for answer in answerList_ground_truth:
            if answer == ground_truth:
                TP = TP + 1
        for other_relation in dict_all_ground_ansList.keys():
            if other_relation == ground_truth:
                continue
            else:
                answerList_other_relation = dict_all_ground_ansList[other_relation]
                for other_answer in answerList_other_relation:
                    if other_answer == ground_truth:
                        FP = FP + 1
        P = 0
        if TP + FP != 0:
            P = 1.0 * TP / (TP + FP)
        R = 1.0 * TP / len(answerList_ground_truth)
        F = 0
        if (P + R) > 0:
            F = 2 * P * R / (P + R)
        sum_P = sum_P + P
        sum_R = sum_R + R
        sum_F = sum_F + F
    avg_P = 1.0 * sum_P / rela_cnt
    avg_R = 1.0 * sum_R / rela_cnt
    macro_F = 1.0 * sum_F / rela_cnt
    print("%-25s\t%-20s\t%-20s\t%-20s\t" % ("Macro avg prf", avg_P, avg_R, macro_F))

    with open(path_result, "a", encoding="utf-8") as w_f:
        w_f.write(str(a_contingency) + " " + str(b_expansion) + " " + "%-20s\t%-20s\t%-20s\t%-20s\t" % (
            "Macro avg prf", avg_P, avg_R, macro_F))
        w_f.write("\n")


# get_single_file_single_rel(path_in, )
# get_rel_cnt_for_dir(dir_in, list_rel)
get_rel_cnt_for_dir(dir_in)
del_useless_rel_for_cnt(list_path_in, dir_out)

# get prf
list_path = get_path(dir_out)
dict_rel_all_Cnt = get_all_cnt(list_path)

compute_subPrf(dict_rel_all_Cnt)
print("\n")
compute_topPrf(dict_rel_all_Cnt)
computeMacroAvgPrf(dict_rel_all_Cnt)
