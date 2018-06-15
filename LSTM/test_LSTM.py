import tensorflow as tf
import numpy as np
import os
import time
import datetime
import data_helpers_test as data_helpers2
from Text_BiRNN import BiRNN
from tensorflow.contrib import learn
import csv
import pickle
import gensim
from collections import defaultdict
# from sklearn.metrics import precision_recall_fscore_support
import sys


tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_string("checkpoint_dir", "./models", "Checkpoint directory from training run")
tf.flags.DEFINE_boolean("eval_train", False, "Evaluate on all training data")
tf.flags.DEFINE_integer("max_sequence_length", 150, "max_sequence_length")
test = "./data/Test_network/Test_Contingency/dev5/test/test5"
# Misc Parameters                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")
# tf.flags.DEFINE_string("label","Comparison.Contrast",'label for train')
FLAGS = tf.flags.FLAGS

#load pos file
x_text_test_arg1_word, x_text_test_arg2_word, y_test,vocabulary = data_helpers2.load_data(test, FLAGS.max_sequence_length, "Comparsion")
out_path = "./result/test/c.txt"

num_classes = y_test.shape[1]
print(num_classes)

graph = tf.Graph()
with graph.as_default():
    session_conf = tf.ConfigProto(
        allow_soft_placement=FLAGS.allow_soft_placement,
        log_device_placement=FLAGS.log_device_placement,
        gpu_options=tf.GPUOptions(per_process_gpu_memory_fraction=0.2))
    sess = tf.Session(config=session_conf)
    with sess.as_default():
        global_step = 0
        max_f1 = 0.0

        checkpoint_file=FLAGS.checkpoint_dir+"/"+"PDTB_Train/dev5/C"
        print('checkpoint_file: ', checkpoint_file)
        saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
        saver.restore(sess, checkpoint_file)
        print('model restored...')
        # Get the placeholders from the graph by name
        input_x_arg1 = graph.get_operation_by_name("input_x_arg1").outputs[0]
        input_x_arg2 = graph.get_operation_by_name("input_x_arg2").outputs[0]
        actual_sequence_length1 = graph.get_operation_by_name("actual_sequence_length1").outputs[0]
        actual_sequence_length2 = graph.get_operation_by_name("actual_sequence_length2").outputs[0]

        input_y = graph.get_operation_by_name("input_y").outputs[0]

        dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

        _scores = graph.get_operation_by_name("output/scores").outputs[0]

        _train_op = graph.get_operation_by_name("train_op").outputs[0]

        _accuracy = graph.get_operation_by_name("accuracy/accuracy").outputs[0]

        def test_step(x_arg1, x_arg2, y):
            total_loss = 0.0
            actual_seq_len1 = np.array([list(x).index(0) + 1 for x in x_arg1])
            actual_seq_len2 = np.array([list(x).index(0) + 1 for x in x_arg2])
            feed_dict = {
                input_x_arg1: x_arg1,
                input_x_arg2: x_arg2,
                input_y: y,
                dropout_keep_prob: 1.0,
                actual_sequence_length1: actual_seq_len1,
                actual_sequence_length2: actual_seq_len2
            }
            accuracy1, score1, = sess.run(
                [_accuracy,  _scores],
                feed_dict)

            predictions1 = np.argmax(np.array(score1), 1)
            true_label1 = np.argmax(np.array(y), 1)

            return true_label1, predictions1

        def evaluate(num_class, true_label, predicition):
            predictions = predicition.tolist()
            true_label = true_label.tolist()
            num_classes = num_class
            true_label = list(true_label)
            list_show_answer = []
            if num_classes == 3:
                # Comparison, Contingency, Expansion
                index_bound_comp = true_label.count(0) - 1
                number_cont = true_label.count(1)

                index_bound_cont = index_bound_comp + number_cont

                list_equal_comp = predictions[0: index_bound_comp + 1]
                list_equal_cont = predictions[index_bound_comp + 1: index_bound_cont + 1]
                list_equal_expan = predictions[index_bound_cont + 1:]

                # Comparison
                TP_comp = list_equal_comp.count(0)
                # print(TP_b)
                FP_comp = list_equal_cont.count(0) + list_equal_expan.count(0)
                # print(FP_b)

                P_comp = 0
                if TP_comp + FP_comp > 0:
                    P_comp = TP_comp / (TP_comp + FP_comp)
                R_comp = TP_comp / (index_bound_comp + 1)
                F_comp = 0
                if P_comp > 0:
                    F_comp = 2 / (1 / P_comp + 1 / R_comp)

                list_show_answer.append(0)
                list_show_answer.append(P_comp)
                list_show_answer.append(R_comp)
                list_show_answer.append(F_comp)

                # Contingency
                TP_cont = list_equal_cont.count(1)
                # print(TP_e)
                FP_cont = list_equal_comp.count(1) + list_equal_expan.count(1)
                # print(FP_e)

                P_cont = 0
                if TP_cont + FP_cont > 0:
                    P_cont = TP_cont / (TP_cont + FP_cont)
                R_cont = TP_cont / (number_cont)
                F_cont = 0
                if P_cont > 0:
                    F_cont = 2 / (1 / P_cont + 1 / R_cont)
                list_show_answer.append(1)
                list_show_answer.append(P_cont)
                list_show_answer.append(R_cont)
                list_show_answer.append(F_cont)

                # Expansion
                TP_expan = list_equal_expan.count(2)
                # print(TP_e)
                FP_expan = list_equal_comp.count(2) + list_equal_cont.count(2)
                # print(FP_e)

                P_expan = 0
                if TP_expan + FP_expan > 0:
                    P_expan = TP_expan / (TP_expan + FP_expan)
                R_expan = TP_expan / (len(predictions) - number_cont - index_bound_comp - 1)
                F_expan = 0
                if P_expan > 0:
                    F_expan = 2 / (1 / P_expan + 1 / R_expan)

                list_show_answer.append(2)
                list_show_answer.append(P_expan)
                list_show_answer.append(R_expan)
                list_show_answer.append(F_expan)

                MacroP = (P_comp + P_cont + P_expan) / 3
                MacroR = (R_comp + R_cont + R_expan) / 3
                MacroF_avg = (F_comp + F_cont + F_expan) / 3
                MacroF = 0
                if MacroP > 0 and MacroR > 0:
                    MacroF = 2 / (1 / MacroP + 1 / MacroR)
                list_show_answer.append(MacroP)
                list_show_answer.append(MacroR)
                list_show_answer.append(MacroF)
                list_show_answer.append(MacroF_avg)

            if num_classes == 2:

                # Beforeafter, DuringEquals
                index_bound_before = true_label.count(0) - 1
                number_during = true_label.count(1)

                list_equal_before = predictions[0: index_bound_before + 1]
                list_equal_during = predictions[index_bound_before + 1:]

                # Beforeafter
                TP_before = list_equal_before.count(0)
                # print(TP_b)
                FP_before = list_equal_during.count(0)
                # print(FP_b)

                P_before = 0
                if TP_before + FP_before > 0:
                    P_before = TP_before / (TP_before + FP_before)
                R_before = TP_before / (index_bound_before + 1)
                F_before = 0
                if P_before > 0:
                    F_before = 2 / (1 / P_before + 1 / R_before)
                list_show_answer.append(0)
                list_show_answer.append(P_before)
                list_show_answer.append(R_before)
                list_show_answer.append(F_before)

                # During
                TP_during = list_equal_during.count(1)
                # print(TP_e)
                FP_during = list_equal_during.count(1) + list_equal_during.count(1)
                # print(FP_e)

                P_during = 0
                if TP_during + FP_during > 0:
                    P_during = TP_during / (TP_during + FP_during)
                R_during = TP_during / (number_during)
                F_during = 0
                if P_during > 0:
                    F_during = 2 / (1 / P_during + 1 / R_during)

                list_show_answer.append(1)
                list_show_answer.append(P_during)
                list_show_answer.append(R_during)
                list_show_answer.append(F_during)

                MacroP = (P_before + P_during) / 2
                MacroR = (R_before + R_during) / 2
                MacroF_avg = (F_before + F_during) / 2
                MacroF = 0
                if MacroP > 0 and MacroR > 0:
                    MacroF = 2 / (1 / MacroP + 1 / MacroR)

                list_show_answer.append(MacroP)
                list_show_answer.append(MacroR)
                list_show_answer.append(MacroF)
                list_show_answer.append(MacroF_avg)
            time_str = datetime.datetime.now().isoformat()
            k = list_show_answer.index(list_show_answer[-4])
            for i in range(len(list_show_answer)):
                if i == k:
                    print("time {} MacroP {:g}:  MacroR {:g}, MacroF {:g}, MacroF_avg {:g}\n"
                          .format(time_str, list_show_answer[i], list_show_answer[i + 1], list_show_answer[i + 2],
                                  list_show_answer[i + 3]))
                    break
                if i % 4 == 0:
                    print("time {} class {:g}:  precision {:g}, recall {:g}, F1 {:g}\n"
                          .format(time_str, list_show_answer[i], list_show_answer[i + 1], list_show_answer[i + 2],
                                  list_show_answer[i + 3]))

            # print(list_show_answer)
            return MacroF_avg

        true_label, predictions = test_step(x_text_test_arg1_word, x_text_test_arg2_word, y_test)
        evaluate(num_classes,  true_label, predictions)
