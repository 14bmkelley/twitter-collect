
from gensim import corpora, models

class LDA:

    def __init__():
        self.num_topics = 20
        self.num_words = 1
        self.passes = 20
        self.corpus = None
        self.model = None

    def set_num_topics(self, num_topics):
        self.num_topics = num_topics
    
    def set_corpus(self, corpus):
        dictionary = corpora.Dictionary(corpus)
        self.corpus = [ dictionary.doc2bow(tweet) for tweet in corpus ]
        self.model = models.ldamodel.LdaModel(self.corpus,
                num_topics=self.num_topics, id2word=dictionary, passes=self.passes)

    def evaluate(self):
        return self.model.print_topics(num_topics=self.num_topics, num_words=self.num_words)

