import tensorflow as tf
import numpy as np



def _variable_on_cpu(name, shape, initializer):
    with tf.device('/cpu:0'):
        var = tf.get_variable(name, shape, initializer=initializer)
        return var


class TextCNN(object):
    """
    A CNN for text classification.
    Uses an embedding layer, followed by a convolutional, max-pooling and softmax layer.
    """
    def __init__(
      # parameter: object is a new method in python 3.5, means the para belongs to the object's class
      self, sequence_length: object, num_classes: object, vocab_size: object,
            embedding_size: object, filter_sizes: object, num_filters: object, l2_reg_lambda: object = 0.0) -> object:

        # Placeholders for input, output and dropout
        self.input_x_arg1 = tf.placeholder(tf.int32, [None, sequence_length], name="input_x_arg1")
        # []是张量的维度，None代表任意维度，sequence_length是固定温�?
        self.input_x_arg2 = tf.placeholder(tf.int32, [None, sequence_length], name="input_x_arg2")

        self.input_y = tf.placeholder(tf.float32, [None, num_classes], name="input_y")
        # float32; 第二维num_classes：类别数�?
        self.dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")

        # Keeping track of l2 regularization loss (optional)
        l2_loss = tf.constant(0.0)  # 常量矩阵

        # Embedding layer
        with tf.device('/cpu:0'), tf.name_scope("embedding"):
            self._W_emb = _variable_on_cpu(name='embedding', shape=[vocab_size, embedding_size],  initializer=tf.random_uniform_initializer(minval=-1.0, maxval=1.0))

            self.W_arg1 = tf.Variable(
                tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0),
                name="W_arg1")
            self.W_arg2 = tf.Variable(
                tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0),
                name="W_arg2"
			)
			
            self.embedded_chars_arg1 = tf.nn.embedding_lookup(self.W_arg1, self.input_x_arg1)
            self.embedded_chars_arg2 = tf.nn.embedding_lookup(self.W_arg2, self.input_x_arg2)

            self.embedded_chars_expanded_arg1 = tf.expand_dims(self.embedded_chars_arg1, -1)
            self.embedded_chars_expanded_arg2 = tf.expand_dims(self.embedded_chars_arg2, -1)

        # Create a convolution + maxpool layer for each filter size
        pooled_outputs_arg1 = []
        pooled_outputs_arg2 = []
        for i, filter_size in enumerate(filter_sizes):
            with tf.name_scope("conv-maxpool-%s" % filter_size):
                # Convolution Layer
                filter_shape = [filter_size, embedding_size, 1, num_filters]
                # 构建正太分布
                W_arg1 = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W_arg1")
                W_arg2 = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W_arg2")
                print(W_arg1)
                b = tf.Variable(tf.constant(0.1, shape=[num_filters]), name="b")

                conv_arg1 = tf.nn.conv2d(
                    self.embedded_chars_expanded_arg1,
                    W_arg1,
                    strides=[1, 1, 1, 1],
                    padding="VALID",
                    name="conv_arg1")
                conv_arg2 = tf.nn.conv2d(
                    self.embedded_chars_expanded_arg2,
                    W_arg2,
                    strides=[1, 1, 1, 1],
                    padding="VALID",
                    name="conv_arg2")

                # Apply nonlinearity
                h_arg1 = tf.nn.relu(tf.nn.bias_add(conv_arg1, b), name="relu_arg1")
                h_arg2 = tf.nn.relu(tf.nn.bias_add(conv_arg2, b), name="relu_arg2")

                # Maxpooling over the outputs
                pooled_arg1 = tf.nn.max_pool(
                    h_arg1,
                    ksize=[1, sequence_length - filter_size + 1, 1, 1],
                    strides=[1, 1, 1, 1],
                    padding='VALID',
                    name="pool_arg1")
                pooled_outputs_arg1.append(pooled_arg1)

                pooled_arg2 = tf.nn.max_pool(
                    h_arg2,
                    ksize=[1, sequence_length - filter_size + 1, 1, 1],
                    strides=[1, 1, 1, 1],
                    padding='VALID',
                    name="pool_arg2")
                pooled_outputs_arg2.append(pooled_arg2)



        # Combine all the pooled features
        num_filters_total = num_filters * len(filter_sizes)
        self.h_pool_arg1 = tf.concat(pooled_outputs_arg1, 3)
        self.h_pool_flat_arg1 = tf.reshape(self.h_pool_arg1, [-1, num_filters_total])

        self.h_pool_arg2 = tf.concat(pooled_outputs_arg2, 3)
        self.h_pool_flat_arg2 = tf.reshape(self.h_pool_arg2, [-1, num_filters_total])

        # Add dropout
        with tf.name_scope("dropout"):
            self.h_drop_arg1 = tf.nn.dropout(self.h_pool_flat_arg1, self.dropout_keep_prob)
            self.h_drop_arg2 = tf.nn.dropout(self.h_pool_flat_arg2, self.dropout_keep_prob)

        print(self.h_drop_arg1.shape)




        #concatenate two args

        self.h_drop = tf.concat([self.h_drop_arg1,self.h_drop_arg2],1)
        print(self.h_drop.shape)
        print("this step........")


        # Final (unnormalized) scores and predictions
        with tf.name_scope("output"):
            W = tf.get_variable(
                "W",
                shape=[num_filters_total*2, num_classes],
                initializer=tf.contrib.layers.xavier_initializer())
            b = tf.Variable(tf.constant(0.1, shape=[num_classes]), name="b")
            l2_loss += tf.nn.l2_loss(W)
            l2_loss += tf.nn.l2_loss(b)

            self.scores = tf.nn.xw_plus_b(self.h_drop, W, b, name="scores")

            self.predictions = tf.argmax(self.scores, 1, name="predictions")

        # CalculateMean cross-entropy loss
        with tf.name_scope("loss"):

            losses = tf.nn.softmax_cross_entropy_with_logits(logits=self.scores, labels=self.input_y)

            self.loss = tf.reduce_mean(losses) + l2_reg_lambda * l2_loss


        # Accuracy
        with tf.name_scope("accuracy"):
            correct_predictions = tf.equal(self.predictions, tf.argmax(self.input_y, 1))##0表示按列 1表示按行
            self.accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")

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

            self.f_score = 2*self.precision*self.recall/(self.precision+self.recall)

    def assign_embedding(self, session, pretrained):
         session.run(tf.assign(self._W_emb, pretrained))


