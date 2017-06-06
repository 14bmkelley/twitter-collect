
from BagOfWordsClassifier import BagOfWordsClassifier
from Streamer import Streamer
from LDA import LDA

class Collector:

    def __init__(self):
        self.classifier = None
        self.lda = LDA()
        self.training_collection = []
        self.corpus_size = 10000
        self.topic_count = 5
        self.corpus = []
        self.keywords = []

    def set_stream_keywords(self, keywords):
        self.keywords = list(keywords)

    def set_corpus_size(self, size):
        self.corpus_size = size

    def set_topic_count(self, topic_count):
        self.topic_count = topic_count

    def stream(self, on_data=None):

        self.streamer = Streamer()
        self.streamer.set_credentials(
            "2392021202-5pL3qI6aXGloucwinyOwEp5XScU9f4LyXihDHA6",
            "5j6Wqsx7V6GH7oGhII8XYGXDtmUnrfJe6IkjyCAtoYgdb",
            "W7DE359Mjc8NJlaR5E6bdBv8d",
            "G4SQ5OTR6lyRIthyFIDY2bOgzW8WUGIwrMM6axxGseaPUiI2s9")

        data_count = 0
        data_size  = self.corpus_size
        data_stream = self.streamer
        data_list  = self.corpus

        def the_real_on_data(data):
            
            data_count += 1
            
            if data_count == data_size:
                data_stream.close()
            elif on_data != None:
                result = on_data(data)
                self.corpus.append(result)

        self.streamer.set_on_data(the_real_on_data)
        self.streamer.stream(keywords)

    def read_training_data(self, filename):
        
        self.training_collection = []

        for line in open(filename, 'r'):

            items = line.split('\t')

            tweet_id_str = items[0]
            tweet_text = items[1]
            tweet_sentiment = items[2]

            self.training_collection.append(self.CollectionItem(tweet_text, tweet_sentiment))

    def generate_bag_of_words(self):

        bag_of_words = []

        for item in self.training_collection:
            bag_of_words.extend(item.get_text().split())

        self.classifier = BagOfWordsClassifier(bag_of_words)

    def train(self):
        
        self.generate_bag_of_words()

        for training_item in self.training_collection:
            self.classifier.use_training_data(training_item.get_text(), training_item.get_sentiment())

        self.classifier.train()

    def evaluate(self):
        
        sentiments = []

        if len(self.corpus) < self.corpus_size:
            self.stream()

        for text in self.corpus:
            sentiment = self.classifier.evaluate(text)
            sentiments.append(CollectionItem(text, sentiment))

        positivities = sorted(sentiments, key=lambda item: item.get_sentiment())

        top_positivities = positivities[0 : self.corpus_size / 10.0]

        self.lda.set_num_topics(self.topic_count)
        self.lda.set_corpus(top_positivities)
        return self.lda.evaluate()
        

    class CollectionItem:

        def __init__(self, text, sentiment):
            self.text = text
            self.sentiment = sentiment

        def get_text(self):
            return self.text

        def get_sentiment(self):
            return self.sentiment


