import numpy as np
import re
import itertools
from collections import Counter
import gensim
from collections import defaultdict
import pickle

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def pad_every_sentences(sentences, sequence_length,padding_word="<PAD/>"):
    padded_sentences = []
    # for i in range(len(sentences)):
    #     sentence = sentences[i]
    #     num_padding = sequence_length - len(sentence)
    #     new_sentence = sentence+ [padding_word]*num_padding
    #     padded_sentences.append(new_sentence)
    padded_sentences = [x[:sequence_length - 1] + [padding_word] * max(sequence_length - len(x), 1) for x in sentences]

    return padded_sentences


def pad_sentences(sentence1, sentence2,sequence_length, padding_word="<PAD/>"):
    """
    Pads all sentences to the same length. The length is defined by the longest sentence.
    Returns padded sentences.
    """

    # padded_sentences = []
    # for i in range(len(sentences)):
    #     sentence = sentences[i]
    #     num_padding = sequence_length - len(sentence)
    #     new_sentence = sentence + [padding_word] * num_padding
    #     padded_sentences.append(new_sentence)
    # return padded_sentences
    padd_sentences1 = pad_every_sentences(sentence1, sequence_length)
    padd_sentences2 = pad_every_sentences(sentence2, sequence_length)


    return [padd_sentences1,padd_sentences2]


def load_data_and_labels(train_data_file,label_1):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    label_arg1_arg2 = list(open(train_data_file, "r").readlines())
    length = len(label_arg1_arg2)
    labels = []
    x_arg1 = []
    x_arg2 = []
    y = []
    for i in range(0, length):
        temp = label_arg1_arg2[i].split("###")
        labels.append(temp[0])
        x_arg1.append(temp[1])
        x_arg2.append(temp[2])

    x_arg1_text = [clean_str(sent) for sent in x_arg1]
    x_arg2_text = [clean_str(sent) for sent in x_arg2]

    x_arg1_text = [s.split(" ") for s in x_arg1_text]
    x_arg2_text = [s.split(" ") for s in x_arg2_text]
    # Generate labels

    for label in labels:
        if "Comparison" in label:
            y.append([1, 0 ,0 ])
        elif "Contingency" in label:
            y.append([0, 1 ,0 ])
        elif "Expansion" in label:
            y.append([0, 0, 1 ])

        # if label!=label_1:
        #     y.append([1, 0])
        # else:
        #     y.append([0, 1])

    y = np.array(y)

    return [x_arg1_text, x_arg2_text, y]

def build_input_data(sentences1,sentences2, labels, vocabulary):
    """
    Maps sentencs and labels to vectors based on a vocabulary.
    """
    x_arg1 = np.array([[vocabulary[word] for word in sentence] for sentence in sentences1])
    x_arg2 = np.array([[vocabulary[word] for word in sentence] for sentence in sentences2])
    y = np.array(labels)
    return [x_arg1,x_arg2, y]



def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int((len(data) - 1) / batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]

def build_vocab(sentences):
    """
    Builds a vocabulary mapping from word to index based on the sentences.
    Returns vocabulary mapping and inverse vocabulary mapping.
    """
    # Build vocabulary
    word_counts = Counter(itertools.chain(*sentences))
    # Mapping from index to word
    vocabulary_inv = [x[0] for x in word_counts.most_common()]
    # Mapping from word to index
    vocabulary = {x: i for i, x in enumerate(vocabulary_inv)}
    return [vocabulary, vocabulary_inv]


def load_data(test_file,sequence_length ,label):
    """
    Loads and preprocessed data for the MR dataset.
    Returns input vectors, labels, vocabulary, and inverse vocabulary.
    """
    # load and preprocess data
    #x_train_arg1, x_train_arg2, train_labels = load_data_and_labels(train_file , label)
    x_test_arg1, x_test_arg2, test_labels = load_data_and_labels(test_file ,label)
  #  x_explicit_arg1, x_explicit_arg2,explicit_labels = load_data_and_labels(explicit_file)

    #sentences =  x_train_arg1+x_train_arg2+x_test_arg1+ x_test_arg2
    # for x in sentences:
    #     if len(x) == 390:
    #         print(x)

   # x_train_arg1_padded, x_train_arg2_padded = pad_sentences(x_train_arg1, x_train_arg2,sequence_length)
    x_test_arg1_padded, x_test_arg2_padded = pad_sentences(x_test_arg1,x_test_arg2,sequence_length)
#    x_explicit_arg1_padded,x_explicit_arg2_padded = pad_sentences(x_explicit_arg1, x_explicit_arg2,sequence_length)
    #print(x_explicit_arg1_padded)


    sentences_padded = x_test_arg1_padded +x_test_arg2_padded
    vocabulary,vocabulary_inv = build_vocab(sentences_padded)

    # x,y,z = build_input_data(x_train_arg1_padded, x_train_arg2_padded,train_labels,vocabulary)
    u,v,w = build_input_data(x_test_arg1_padded, x_test_arg2_padded,test_labels,vocabulary)
    return [u,v,w,vocabulary]
    #explicit_arg1, explicit_arg2,explicit_labels = build_input_data(x_explicit_arg1_padded,x_explicit_arg2_padded,explicit_labels,vocabulary)

    # output = open('explicit.pkl', 'wb')
    # pickle.dump([explicit_arg1, explicit_arg2,explicit_labels,vocabulary], output)
    # output.close()

'''
    output = open('vocabulary.pkl', 'wb')
    pickle.dump(vocabulary, output)
    output.close()

    output = open('train.pkl', 'wb')
    pickle.dump([x,y,z], output)
    output.close()


    output = open('test.pkl', 'wb')
    pickle.dump([u,v,w], output)
    output.close()
'''
  #  return [x,y,z,u,v,w,vocabulary]



