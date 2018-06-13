import os

dir_in = "C:\\Users\RHB\Desktop\\test_cause2"
dir_out_top = "C:\\Users\RHB\Desktop\Test_cause_network"
list_path_in = []

def get_path_list(dir_in):
    for root, dirs, files in os.walk(dir_in):
        for filename in files:
            path_file = root + "\\" + filename
            list_path_in.append(path_file)

def divide_by_rel_by_mo_line(list_path_in, dir_out):
    for path_in in list_path_in:
        file_name = path_in.split("\\")[-1]
        with open(path_in, "r") as r_f:
            line_all = r_f.readlines()
            for i in range(len(line_all)):
                write2dev_test_by_mode_linenum(dir_out, file_name, i, line_all, 1)
                write2dev_test_by_mode_linenum(dir_out, file_name, i, line_all, 2)
                write2dev_test_by_mode_linenum(dir_out, file_name, i, line_all, 3)
                write2dev_test_by_mode_linenum(dir_out, file_name, i, line_all, 4)
                write2dev_test_by_mode_linenum(dir_out, file_name, i, line_all, 0)

def write2dev_test_by_mode_linenum(dir_out, file_name, i, line_all, num):
    if i % 5 == num:
        if num==0:
            num = 5
        # dir_top = dir_out + "\\" + "test" + str(num)
        dir_ = dir_out + "\\" + "test" + str(num) + "\\test\\"
        if os.path.exists(dir_) == False:
            os.makedirs(dir_)
        path_dev_out = dir_out + "\\" + "dev" + str(num) + "\\test\\" + file_name
        with open(path_dev_out, "a", encoding="utf-8") as w_f:
            w_f.write(line_all[i])
    else:
        if num==0:
            num = 5
        dir_ = dir_out + "\\" + "test" + str(num) + "\\dev\\"
        if os.path.exists(dir_) == False:
            os.makedirs(dir_)
        path_test_out = dir_out + "\\" + "dev" + str(num) + "\\dev\\" + file_name
        with open(path_test_out, "a", encoding="utf-8") as w_f:
            w_f.write(line_all[i])

get_path_list(dir_in)
divide_by_rel_by_mo_line(list_path_in, dir_out_top)

