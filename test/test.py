
from ../lib import Collector

def main():
    collector = Collector()
    collector.read_training_data('./streamed-tweets-corpus.tsv')
    collector.set_stream_keywords([ 'trump' ])
    collector.set_corpus_size(1000)
    collector.set_topic_count(20)
    collector.train()
    print(collector.evaluate())

if __name__ == '__main__':
    main()
