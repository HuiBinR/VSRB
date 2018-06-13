import tensorflow as tf
import numpy as np
from tensorflow.python.ops.rnn import bidirectional_dynamic_rnn as bi_rnn

from tensorflow.contrib.rnn import LSTMCell



def _variable_on_cpu(name, shape, initializer):
    with tf.device('/cpu:0'):
        var = tf.get_variable(name, shape, initializer=initializer)
        return var

class BiRNN(object):
    """
    A CNN for text classification
    Uses an embedding layer, followed by a convolutional,max-pooling and softmax layer
    """
    def __init__(self,sequence_length,num_classes,vocab_size,embedding_size,hidden_size,attention_size):

        #placeholders for input,output and dropout
        self.input_x_arg1 = tf.placeholder(tf.int32,[None,sequence_length],name="input_x_arg1")
        self.input_x_arg2 = tf.placeholder(tf.int32,[None,sequence_length],name="input_x_arg2")
        self.input_y = tf.placeholder(tf.float32,[None,num_classes],name="input_y")
        self.dropout_keep_prob = tf.placeholder(tf.float32,name="dropout_keep_prob")

        self.actual_sequence_length1 = tf.placeholder(tf.int32,[None],name="actual_sequence_length1")
        self.actual_sequence_length2 = tf.placeholder(tf.int32,[None],name="actual_sequence_length2")

        #self.embedding_placeholder = tf.placeholder(tf.float32,[vocab_size,embedding_size],name="embedding_placeholder")

        #Keeping track of l2 regularization loss(optional)
        l2_loss = tf.constant(0.0)
        #print(sequence_length)

        #Embedding layer
        with tf.device('/cpu:0'),tf.name_scope("embedding_layer"):


            self._W_emb = _variable_on_cpu(name='embedding', shape=[vocab_size, embedding_size],  initializer=tf.random_uniform_initializer(minval=-1.0, maxval=1.0))


            self.embedded_chars1 = tf.nn.embedding_lookup(self._W_emb,self.input_x_arg1,name="arg1")
            self.embedded_chars2 = tf.nn.embedding_lookup(self._W_emb,self.input_x_arg2,name="arg2")

            print("Embedding -------------")

        #BiRNN layer
        '''
        with tf.name_scope("cell"):
            fwlist = []
            bwlist = []
            for i in range(2):
                fwlist.append(tf.contrib.rnn.BasicLSTMCell(hidden_size))
                bwlist.append(tf.contrib.rnn.BasicLSTMCell(hidden_size))
            lstm_fw = tf.contrib.rnn.MultiRNNCell(fwlist)
            lstm_bw = tf.contrib.rnn.MultiRNNCell(bwlist)
        '''

        with tf.name_scope('cell'):
            lstm_fw = tf.contrib.rnn.BasicLSTMCell(hidden_size)
            lstm_bw = tf.contrib.rnn.BasicLSTMCell(hidden_size)

        with tf.name_scope("rnn1"):
            self.rnn_outputs1, _ = bi_rnn(lstm_fw,lstm_bw,inputs=self.embedded_chars1,
                                     sequence_length=self.actual_sequence_length1,dtype=tf.float32)

        with tf.name_scope("rnn2"):
            self.rnn_outputs2, _ = bi_rnn(lstm_fw,lstm_bw,inputs=self.embedded_chars2,
                                     sequence_length=self.actual_sequence_length2,dtype=tf.float32)


        #########
        self.rnn_outputs1 = tf.concat(self.rnn_outputs1,2)
        self.rnn_outputs2 = tf.concat(self.rnn_outputs2,2)



        self.rnn_outputs = tf.concat([self.rnn_outputs1,self.rnn_outputs2],1)
        self.rnn_outputs = tf.reduce_sum(self.rnn_outputs, 1)
        #########

        # with tf.name_scope("attention"):
        #     self.attention_output1, self.alphas1 = attention(self.rnn_outputs1,attention_size,return_alphas=True)
        #     self.attention_output2, self.alphas2 = attention(self.rnn_outputs2,attention_size,return_alphas=True)
        #
        #     #self.rnn_outputs = tf.concat([self.rnn_outputs1,self.rnn_outputs2],1)
        #     #self.rnn_outputs = tf.reduce_sum(self.rnn_outputs, 1)
        #
        #     self.rnn_outputs = self.attention_output1 + self.attention_output2

        with tf.name_scope("dropout"):
            self.drop = tf.nn.dropout(self.rnn_outputs, self.dropout_keep_prob)

        with tf.name_scope("output"):
            self.W = tf.Variable(tf.truncated_normal([self.drop.get_shape()[1].value,num_classes],stddev=0.1), name="W")
            self.b = tf.Variable(tf.constant(0.1,shape = [num_classes]), name ="b")
            self.scores = tf.nn.softmax(tf.nn.xw_plus_b(self.drop,self.W,self.b),name="scores")
            self.predictions = tf.argmax(self.scores,1,name="predicitons")

        with tf.name_scope("loss"):
            losses = tf.nn.softmax_cross_entropy_with_logits(logits=self.scores, labels=self.input_y)
            self.loss = tf.reduce_mean(losses)

            #Accuracy
        with tf.name_scope("accuracy"):

            correct_predictions = tf.equal(self.predictions, tf.argmax(self.input_y, 1))  ##0表示按列 1表示按行
            self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")
            #tf.round舍入到最近的整数
            # print(self.predictions)
            all_positive_indexes = tf.where(self.predictions>0)
            all_positive_indexes = tf.reshape(all_positive_indexes,[-1])

            positive_pred = tf.nn.embedding_lookup(self.predictions, all_positive_indexes)
            positive_label = tf.nn.embedding_lookup(tf.argmax(self.input_y, 1), all_positive_indexes)

            correct_positive_prediction = tf.equal(positive_pred, positive_label)
            self.precision = tf.reduce_mean(tf.cast(correct_positive_prediction, dtype=tf.float32), name="precision")
            tp = tf.reduce_sum(tf.cast(correct_positive_prediction,dtype=tf.float32))

            self.label_index = tf.cast(tf.argmax(self.input_y,1),dtype=tf.float32)
            tpfn = tf.reduce_sum(tf.where(self.label_index > 0, tf.ones_like(self.label_index, dtype=tf.float32),
                                          tf.zeros_like(self.label_index,dtype=tf.float32)))

            self.recall = tf.truediv(tp,tpfn,name="recall")

            self.f_score = 2.0*self.precision*self.recall/(self.precision+self.recall)


    def assign_embedding(self, session, pretrained):
        session.run(tf.assign(self._W_emb, pretrained))

           





