
import tensorflow as tf
import numpy as np

class BagOfWordsClassifier:

    def __init__(self, bag_of_words):

        self.session = tf.InteractiveSession()
        self.training_data = []
        self.error_func = None
        self.train_func = None
        self.inputs = None
        self.outputs = None
        self.output_layer = None
        self.bag_of_words = None
        self.set_bag_of_words(bag_of_words)
        self.generate_neural_net()

    
    def set_bag_of_words(self, bag_of_words):

        freq_dict = {}

        for word in bag_of_words:
            word = self.sanitize(word)
            if word in freq_dict:
                freq_dict[word] += 1
            elif word != '' and word != 'rt':
                freq_dict[word] = 1

        sorted_freqs = sorted([(key, freq_dict[key]) for key in freq_dict],
                key=lambda item: item[1], reverse=True)

        self.bag_of_words = [ item[0] for item in sorted_freqs ]
        print(self.bag_of_words)


    def use_training_data(self, text, sentiment):

        inputs = np.array(self.generate_input_array(text))
        outputs = [ sentiment ]

        self.training_data.append(( inputs, outputs ))


    def train(self):

        input_array = np.array([ data[0] for data in self.training_data ])
        output_array = np.array([ data[1] for data in self.training_data ])

        for i in range(1000):
            self.session.run([ self.train_func, self.error_func ], feed_dict={
                self.inputs: input_array,
                self.outputs: output_array
            })


    def evaluate(self, text):

        return self.session.run(self.output_layer, feed_dict={
            self.inputs: np.array([ self.generate_input_array(text) ])
        })[0][0]


    def generate_neural_net(self):

        input_count = len(self.bag_of_words)
        hidden1_count = 100
        hidden2_count = 10
        output_count = 1

        self.inputs  = tf.placeholder(tf.float32, shape=[None, input_count])
        self.outputs = tf.placeholder(tf.float32, shape=[None, output_count])

        layer1_weights = tf.Variable(tf.truncated_normal([ input_count, hidden1_count ]))
        layer1_biases  = tf.Variable(tf.zeros([ hidden1_count ]))
        layer1_outputs = tf.matmul(self.inputs, layer1_weights) + layer1_biases

        layer2_weights = tf.Variable(tf.truncated_normal([ hidden1_count, hidden2_count ]))
        layer2_biases  = tf.Variable(tf.zeros([ hidden2_count ]))
        layer2_outputs = tf.matmul(layer1_outputs, layer2_weights) + layer2_biases

        layer3_weights = tf.Variable(tf.truncated_normal([ hidden2_count, output_count ]))
        layer3_biases  = tf.Variable(tf.zeros([ output_count ]))
        self.output_layer = tf.nn.sigmoid(tf.matmul(layer2_outputs, layer3_weights) + layer3_biases)

        self.error_func = 0.5 * tf.reduce_sum(tf.subtract(self.output_layer, self.outputs) ** 2)
        self.train_func = tf.train.GradientDescentOptimizer(0.05).minimize(self.error_func)

        self.session.run(tf.global_variables_initializer())


    def generate_input_array(self, text):

        result = [ 0.0 ] * len(self.bag_of_words)

        for word in text:
            word = self.sanitize(word)
            if word in self.bag_of_words:
                result[self.bag_of_words.index(word)] += 1

        return result


    def sanitize(self, word):
        
        result = ''
        word_len = len(word)

        if word_len == 0:
            return ''

        char = word[0]
        index = 0

        while not char.isalpha():
            index += 1
            if index == word_len:
                return ''
            char = word[index]

        if index < word_len:
            while char.isalpha():
                result += char
                index += 1
                if index == word_len:
                    return result.lower()
                char = word[index]

        return result.lower()

