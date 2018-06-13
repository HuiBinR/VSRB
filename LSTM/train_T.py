#! /usr/bin/env python
#-*- coding:utf-8 -*-

import tensorflow as tf
import numpy as np
import os
import time
import datetime
import data_helpers_T as data_helpers2
from Text_BiRNN import BiRNN
from tensorflow.contrib import learn
from collections import defaultdict
import gensim
import sys


dev, train, test, result = sys.argv

# Parameters
# ==================================================
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
# Data loading params
outpath = './results/result_T'+"/"+ result + "/" + test
if os.path.exists(outpath) == False:
    os.makedirs(outpath)
tf.flags.DEFINE_float("dev_sample_percentage", .1, "Percentage of the training data to use for validation")
tf.flags.DEFINE_string("train_data_file","./data"+"/"+train+"/"+"T.txt","Data for Training")
tf.flags.DEFINE_string("test_data_file","./data/Test_network/Test_Temporal/"+test+"/"+"dev"+"/"+test,"Data for Testing")
tf.flags.DEFINE_string("label","T",'label for train')

# Model Hyperparameters

tf.flags.DEFINE_float("dropout_keep_prob", 0.6, "Dropout keep probability (default: 0.5)")
tf.flags.DEFINE_float("l2_reg_lambda", 0.0, "L2 regularization lambda (default: 0.0)")
tf.flags.DEFINE_integer("hidden_size",200,"LSTM hidden size(default:64)")
tf.flags.DEFINE_integer("attention_size",100,"attention size(default:32)")
tf.flags.DEFINE_integer("max_sequence_length",150,"max sequence length")

# Training parameters
tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
tf.flags.DEFINE_integer("num_epochs", 200, "Number of training epochs (default: 200)")
tf.flags.DEFINE_integer("evaluate_every", 100, "Evaluate model on dev set after this many steps (default: 100)")
tf.flags.DEFINE_integer("checkpoint_every", 100, "Save model after this many steps (default: 100)")
tf.flags.DEFINE_integer("num_checkpoints", 5, "Number of checkpoints to store (default: 5)")

# Misc Parameters
tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")
tf.flags.DEFINE_boolean("use_pretrain",True,"use pretrained embedding")


FLAGS = tf.flags.FLAGS
FLAGS._parse_flags()
print("\nParameters:")
for attr, value in sorted(FLAGS.__flags.items()):
    print("{}={}".format(attr.upper(), value))
print("")


x_train_arg1,x_train_arg2,y_train,x_test_arg1,x_test_arg2,y_test,vocabulary = data_helpers2.load_data(FLAGS.train_data_file,FLAGS.test_data_file,FLAGS.max_sequence_length,FLAGS.label)
print("train/test already!")

embedding = defaultdict(list)

model = gensim.models.KeyedVectors.load_word2vec_format("GoogleNews-vectors-negative300.bin",unicode_errors="ignore",binary=True)
words = []
for word in model.vocab:
    words.append(word)
embedding_dim = len(model[words[0]])

print("embedding_dim:{}".format(embedding_dim))

for key in vocabulary:

    try:
        embedding.update({vocabulary[key]:model[key]})
    except:
        embedding.update({vocabulary[key]:np.random.uniform(-1,1,embedding_dim)})

pretrained_embedding = list(embedding[k] for k in sorted(embedding.keys()))
pretrained_embedding = np.array(pretrained_embedding)
np.random.seed(10)
shuffle_indices = np.random.permutation(np.arange(len(y_train)))
x_train_arg1_shuffled = x_train_arg1[shuffle_indices]
x_train_arg2_shuffled = x_train_arg2[shuffle_indices]
y_train_shuffled = y_train[shuffle_indices]


print("load_successfully!")

# Training
# ==================================================

with tf.Graph().as_default():
    session_conf = tf.ConfigProto(
      allow_soft_placement=FLAGS.allow_soft_placement,
      log_device_placement=FLAGS.log_device_placement,
        gpu_options=tf.GPUOptions(per_process_gpu_memory_fraction=0.8))
    sess = tf.Session(config=session_conf)
    with sess.as_default():
        cnn = BiRNN(
            sequence_length=x_train_arg1_shuffled.shape[1],##cnt the word num of the sentence
            num_classes=y_train_shuffled.shape[1],
            vocab_size=len(vocabulary),
            embedding_size=embedding_dim,
            hidden_size=FLAGS.hidden_size,
            attention_size=FLAGS.attention_size
        )
        if FLAGS.use_pretrain:
            cnn.assign_embedding(sess, pretrained_embedding)
        # Define Training procedure

        global_step = tf.Variable(0, name="global_step", trainable=False) #record the global step
		optimizer = tf.train.AdamOptimizer(1e-3)

        grads_and_vars = optimizer.compute_gradients(cnn.loss)  ##calculate gradient
        train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step,name="train_op")

        # Output directory for models and summaries
        timestamp = str(int(time.time()))


        # Checkpoint directory. Tensorflow assumes this directory already exists so we need to create it
        checkpoint_prefix = "./models"+"/"+train+"/"+test
        if os.path.exists(checkpoint_prefix) == False:
            os.makedirs(checkpoint_prefix)
        checkpoint_prefix = checkpoint_prefix + "/" + FLAGS.label
        #if not os.path.exists(checkpoint_dir):
        #    os.makedirs(checkpoint_dir)
        saver = tf.train.Saver(tf.global_variables(), max_to_keep=FLAGS.num_checkpoints)

        # Initialize all variables
        sess.run(tf.global_variables_initializer())

        def train_step(x_arg1_batch,x_arg2_batch,y_batch):
            """
            A single training step
            """
            actual_seq_len1 = np.array([list(x).index(0)+1 for x in x_arg1_batch])
            actual_seq_len2 = np.array([list(x).index(0)+1 for x in x_arg2_batch])
            ##feed_dict contains the data for the placeholder nodes we pass to our network.
            feed_dict = {
                cnn.input_x_arg1:x_arg1_batch,
                cnn.input_x_arg2:x_arg2_batch,
                cnn.input_y:y_batch,
                cnn.dropout_keep_prob : FLAGS.dropout_keep_prob,
                cnn.actual_sequence_length1: actual_seq_len1,
                cnn.actual_sequence_length2: actual_seq_len2,

            }
            _, step, loss, accuracy= sess.run(
                [train_op, global_step, cnn.loss, cnn.accuracy],
                feed_dict)


            time_str = datetime.datetime.now().isoformat()
            print("{}: step {}, loss {:g}, acc {:g}".format(time_str, step, loss, accuracy))


        def test_step(x_arg1_batch,x_arg2_batch, y_batch):
            """
            Evaluates model on a dev set
            """
            actual_seq_len1 = np.array([list(x).index(0) + 1 for x in x_arg1_batch])
            actual_seq_len2 = np.array([list(x).index(0) + 1 for x in x_arg2_batch])
            feed_dict = {
                cnn.input_x_arg1: x_arg1_batch,
                cnn.input_x_arg2: x_arg2_batch,
                cnn.input_y:y_batch,
                cnn.dropout_keep_prob: FLAGS.dropout_keep_prob,
                cnn.actual_sequence_length1: actual_seq_len1,
                cnn.actual_sequence_length2: actual_seq_len2

            }
            step, loss, accuracy, precision, recall, prediction= sess.run(
                [global_step, cnn.loss, cnn.accuracy,cnn.precision,cnn.recall,cnn.predictions],
                feed_dict)
            f1 = 2.0 * precision * recall / (precision + recall)
            time_str = datetime.datetime.now().isoformat()
            print("comparison {}:  precision {:g}, recall {:g}, F1 {:g}"
                  .format(time_str, precision, recall, f1))




            return precision,recall,f1,prediction

        # Generate batches
        batches = data_helpers2.batch_iter(
            list(zip(x_train_arg1_shuffled,x_train_arg2_shuffled, y_train_shuffled)), FLAGS.batch_size, FLAGS.num_epochs)

        max_f1 = 0.0
        for batch in batches:
            x_arg1_batch,x_arg2_batch, y_batch = zip(*batch)
            train_step(x_arg1_batch,x_arg2_batch, y_batch)
            current_step = tf.train.global_step(sess, global_step)
            if current_step % FLAGS.evaluate_every == 0:
                p,r,f1, prediction = test_step(x_test_arg1, x_test_arg2, y_test)

                if f1 > max_f1:
                    out_path = outpath+"/"+FLAGS.label+'.txt'
                    f = open(out_path,'w')
                    for line in prediction:
                        f.write(str(line)+"\n")
			
                    f.close()
                    max_f1 = f1
                    max_p = p
                    max_r=r
                    path = saver.save(sess, checkpoint_prefix)
                    print("Saved model checkpoint to {}\n".format(path))
            if current_step == 3000:
                break
        f = open(os.path.join(outpath,"results.txt"),'a')
        f.write(FLAGS.label+':'+str(max_p)+'\t'+str(max_r)+'\t'+str(max_f1)+'\n')
        f.close()
