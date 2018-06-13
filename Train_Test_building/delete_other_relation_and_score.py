import xlwt
import os

dir_in = "C:\\Users\RHB\Desktop\\add_condition"
dir_out = "C:\\Users\RHB\Desktop\\part_add_condition"
list_rel = []   # store the relation name
list_path_in = []
list_useless_rel = ["Comparison.Coreference",
                    "Expansion.Confirmation",
                    #"Contingency.Cause", "Contingency.Condition",
                    "Comparison.Contrast", "Expansion.Conjunction",
                    "Temporal.During", "Temporal.Equals", "Temporal.Beforeafter"]
                    # "Temporal.During", "Temporal.Equals"]


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

a_contingency = 1.01
b_contingency = 1.0
wb = xlwt.Workbook()

# def get_single_file_single_rel(path_in, list_r):
#     dict_rel_score = {}
#     ground_truth = path_in.split("\\")[-1]
#     with open(path_in, 'r') as r_f:
#         all_ = r_f.readlines()
#         for single in all_:
#             # a line
#             num_ = 0
#             list_rel_cnt= single.split("|")
#             for rel_cnt in list_rel_cnt:
#                 first_one = rel_cnt.split(" ")
#                 if len(first_one)>1:
#                     num = first_one[0]
#                     rel_id = first_one[1].split(" ")
#                     relation = rel_id[0]
#                     id = int(rel_id[1])
#                     if ""
#                     dict_rel_score.update({relation_: id*dict_rel_score_single["all"]/dict_rel_score_single[relation]})
#
#             for r in list_single:
#                 # get the cnt of this relation
#                 if "=" in r:
#                     rel_ = r.split("=")[0]
#                     if rel_ not in dict_rel_cnt.keys():
#                         dict_rel_cnt.update({rel_: 0})
#                     cnt = int(r.split("=")[-1].split("|")[0])
#                     dict_rel_cnt.update({rel_: dict_rel_cnt[rel_]+cnt})
#     w2excel(path_in, dict_rel_cnt, list_r)
#     # print(dict_rel_cnt)

# walk the dir
def get_rel_cnt_for_dir(dir_in):
    if os.path.exists(dir_in):
        for root, dirs, files in os.walk(dir_in):
            for filename in files:
                path_file = root + "\\" + filename
                list_path_in.append(path_file)


def del_useless_rel_for_cnt(list_path_in, dir_out, list_useless_rel):
    """
    delete the relation and its score that we dont want from the file

    :param list_path_in: the list of the path that we read in
    :param dir_out: the dir of the path that we write out
    :param list_useless_rel: the list of the relation we want to delete
    :return:
    """
    for path_in in list_path_in:
        ground_truth = path_in.split("\\")[-1]  # store the relation of the ground truth, to form a full out path
        print(ground_truth)
        path_out = dir_out + "\\" + ground_truth
        with open(path_in, 'r') as r_f:
            all_ = r_f.readlines()
            for single in all_:
                # a line
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
                            for rel_del in list_useless_rel:
                                if rel_ == rel_del:
                                    flag_write = False
                            if flag_write == True:
                                with open(path_out, "a", encoding="utf-8") as w_f:
                                    w_f.write(rel_+"="+cnt+"|")
                    with open(path_out, "a", encoding="utf-8") as w_f:
                        w_f.write("\n")
                        w_f.write("\n")

def del_useless_rel_for_score(list_path_in, dir_out, list_useless_rel):
    """
    delete the relation and its score that we dont want from the file

    :param list_path_in: the list of the path that we read in
    :param dir_out: the dir of the path that we write out
    :param list_useless_rel: the list of the relation we want to delete
    :return:
    """
    for path_in in list_path_in:
        ground_truth = path_in.split("\\")[-1]  # store the relation of the ground truth, to form a full out path
        print(ground_truth)
        path_out = dir_out + "\\" + ground_truth
        with open(path_in, 'r') as r_f:
            all_ = r_f.readlines()
            cnt_all = 0
            for single_line in all_:
                list_single = single_line.split("|")
                for r in list_single:
                    flag_write = True
                    if "=" in r:
                        rel_ = r.split("=")[0]
                        first_one = rel_.split(" ")
                        if len(first_one) > 1:
                            rel_ = first_one[1]
                            num_ = first_one[0]
                            with open(path_out, "a", encoding="utf-8") as w_f:
                                w_f.write(num_ + " ")
                        cnt = r.split("=")[-1].split("|")[0]
                        for rel_del in list_useless_rel:
                            if rel_ == rel_del:
                                flag_write = False
                                break
                        if flag_write == True:
                            with open(path_out, "a", encoding="utf-8") as w_f:
                                w_f.write(rel_+"="+cnt+"|")
                with open(path_out, "a", encoding="utf-8") as w_f:
                    w_f.write("\n")

def w2excel(path_in, dict_, list_r):
    ground_truth = path_in.split("\\")[-1]
    path_out = "C:\\Users\RHB\Desktop\\pic_id_rel40\\all.xls"

    if ground_truth == "all40":
        list_c = []
        for r in dict_.keys():
            list_c.append(dict_[r])
        list_c.sort()
        print(list_c)
        ws = wb.add_sheet(ground_truth, cell_overwrite_ok=True)
        ws.write(0, 0, ground_truth)
        print(ground_truth)
        for i in range(len(list_c)):
            value = list_c[-i-1]
            for r in dict_:
                if dict_[r] == value:
                    list_r.append(r)
                    ws.write(i+1, 0, r)
                    ws.write(i+1, 1, value)
        print(list_r)
    else:
        ws = wb.add_sheet(ground_truth, cell_overwrite_ok=True)
        print(ground_truth)
        ws.write(0, 0, ground_truth)
        for i in range(len(list_r)):
            ws.write(i + 1, 0, list_r[i])
            ws.write(i + 1, 1, dict_[list_r[i]])
    wb.save(path_out)

# get_single_file_single_rel(path_in, )
# get_rel_cnt_for_dir(dir_in, list_rel)
get_rel_cnt_for_dir(dir_in)
del_useless_rel_for_cnt(list_path_in, dir_out, list_useless_rel)

