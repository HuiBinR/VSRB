import os

dir_in = ".\results\result_C\TERB_Train"

list_path_in = []

def get_all_path(dir_in, list_path):
    for root, dirs, files in os.walk(dir_in):
        for filename in files:
            path_file = root + "\\" + filename
            list_path.append(path_file)

get_all_path(dir_in, list_path_in)

def get_right_answer(list_path_in):
    '''
    Generate the truth answer of each test file

    :param list_path_in: the list of the path of the answer generated by Neural Networks
    :return: dict_testNum_ansList: {"number(file number 1-5): the list of is right answer"}
    '''
    dict_testNum_ansList = {}
    for path_in in list_path_in:
        list_right_answer = []

        number = path_in.split("\\")[6][-1]
        test_number = "test"+number

        path_answer_comparison = ".\data\Test_network\Test_Contingency\\"+test_number+"\dev\\Comparison.Contrast"
        with open(path_answer_comparison, "r") as r_f:
            all = r_f.readlines()
            list_right_answer.extend(["0"]*len(all))
       # print(len(list_right_answer))

        path_answer_contingency = ".\data\Test_network\Test_Contingency" + test_number + "\dev\\Contingency"
        with open(path_answer_contingency, "r") as r_f:
            all = r_f.readlines()
            list_right_answer.extend(["1"]*len(all))
        #print(len(list_right_answer))

        path_answer_expansion = ".\data\Test_network\Test_Contingency" + test_number + "\dev\\Expansion.Conjunction"
        with open(path_answer_expansion, "r") as r_f:
            all = r_f.readlines()
            list_right_answer.extend(["2"] * len(all))
            # print(len(list_right_answer))

        dict_testNum_ansList.update({number: list_right_answer})
    return dict_testNum_ansList

dict_testNum_ansList = get_right_answer(list_path_in)

def eval(list_path_in, dict_ans):
    for path_in in list_path_in:
        print(path_in)

        list_show_answer_comp = []
        list_show_answer_cont = []
        list_show_answer_expan = []

        TP_comp = 0
        FP_comp = 0
        P_comp = 0
        R_comp = 0
        F_comp = 0

        TP_cont = 0
        FP_cont = 0
        P_cont = 0
        R_cont = 0
        F_cont = 0

        TP_expan = 0
        FP_expan = 0
        P_expan= 0
        R_expan = 0
        F_expan = 0



        number = path_in.split("\\")[6][-1]
        answerList = dict_ans[number]
        index_bound_comp = answerList.count("0")-1
        number_cont = answerList.count("1")
        index_bound_cont = index_bound_comp + number_cont

        # list_is_equal = []

        judged_ansList = []
        with open(path_in, "r") as r_f:
            judged_ansList_want = r_f.readlines()
            for i in judged_ansList_want:
                judged_ansList.append(i.strip("\n"))


        list_equal_comp = judged_ansList[0: index_bound_comp+1]
        list_equal_cont = judged_ansList[index_bound_comp+1: index_bound_cont+1]
        list_equal_expan = judged_ansList[index_bound_cont+1:]

        TP_comp = list_equal_comp.count("0")
        # print(TP_b)
        FP_comp = list_equal_cont.count("0") + list_equal_expan.count("0")
        # print(FP_b)

        P_comp = 0
        if TP_comp + FP_comp > 0:
            P_comp = TP_comp / (TP_comp + FP_comp)
        R_comp= TP_comp / (index_bound_comp+1)
        F_comp = 0
        if P_comp>0:
            F_comp = 2/(1/P_comp+1/R_comp)
        list_show_answer_comp.append(P_comp)
        list_show_answer_comp.append(R_comp)
        list_show_answer_comp.append(F_comp)

        TP_cont = list_equal_cont.count("1")
        # print(TP_e)
        FP_cont = list_equal_comp.count("1") + list_equal_expan.count("1")
        # print(FP_e)

        P_cont = 0
        if TP_cont + FP_cont > 0:
            P_cont = TP_cont / (TP_cont + FP_cont)
        R_cont = TP_cont / (number_cont)
        F_cont = 0
        if P_cont > 0:
            F_cont = 2 / (1 / P_cont + 1 / R_cont)
        list_show_answer_cont.append(P_cont)
        list_show_answer_cont.append(R_cont)
        list_show_answer_cont.append(F_cont)

        TP_expan = list_equal_expan.count("2")
        # print(TP_e)
        FP_expan = list_equal_comp.count("2") + list_equal_cont.count("2")
        # print(FP_e)

        P_expan = 0
        if TP_expan + FP_expan > 0:
            P_expan = TP_expan / (TP_expan + FP_expan)
        R_expan = TP_expan / (len(answerList) - number_cont - index_bound_comp - 1)
        F_expan = 0
        if P_expan > 0:
            F_expan = 2 / (1 / P_expan + 1 / R_expan)
        list_show_answer_expan.append(P_expan)
        list_show_answer_expan.append(R_expan)
        list_show_answer_expan.append(F_expan)

        MacroP = (P_comp + P_cont + P_expan)/3
        MacroR = (R_comp + R_cont + R_expan)/3
        MacroF_avg = (F_comp+F_cont+F_expan)/3
        MacroF = 0
        if MacroP > 0:
            MacroF = 2 / (1 / MacroP + 1 / MacroR )

        print("%-20s\t%-20s\t%-20s\t%-20s\t" % ("Comparison", list_show_answer_comp[0], list_show_answer_comp[1], list_show_answer_comp[2]))
        print("%-20s\t%-20s\t%-20s\t%-20s\t" % ("Contingency", list_show_answer_cont[0], list_show_answer_cont[1], list_show_answer_cont[2]))
        print("%-20s\t%-20s\t%-20s\t%-20s\t" % ("Expansion", list_show_answer_expan[0], list_show_answer_expan[1], list_show_answer_expan[2]))
        print("%-20s\t%-20s\t%-20s\t%-20s\t%-20s\t" % ("Macro", MacroP, MacroR, MacroF_avg, MacroF))


eval(list_path_in, dict_testNum_ansList)
