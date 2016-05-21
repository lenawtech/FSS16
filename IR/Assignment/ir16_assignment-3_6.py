from collections import defaultdict
from bs4 import BeautifulSoup
from progressbar import ProgressBar
import re
import math
import operator


class VSMRetrievalSystem(object):
    def __init__(self):
        self.docs = {}
        self.num_doc = 0
        self.score = defaultdict(float)
        self.length = defaultdict(float)

    def parse_articles(self, file_name):
        raw_articles = open(file_name).read()
        parsed_articles = BeautifulSoup(raw_articles, 'lxml')

        doc_nos = parsed_articles.find_all('docno')
        doc_texts = parsed_articles.find_all('text')
        self.num_doc = len(doc_nos)

        bar = ProgressBar()

        for i in bar(range(self.num_doc)):
            doc_no = doc_nos[i].string.strip()
            self.docs[str(doc_no)] = defaultdict(int)

            for word in re.sub('[^a-zA-Z0-9\n]', ' ', doc_texts[i].get_text()).lower().split():
                self.docs[doc_no][word] += 1

    def get_sorted_results(self, query):
        self.query_items = defaultdict(int)
        query_length = 0.0

        for i in query.lower().split():
            self.query_items[i] += 1

        for i in self.query_items:
            df = 0

            for d in self.docs:
                if self.docs[d][i]:
                    df += 1

            if df:
                w = self.get_tf_idf(self.query_items[i], df)
                query_length += math.pow(w, 2)

                for d in self.docs:
                    if self.docs[d][i]:
                        tf_idf = self.get_tf_idf(self.docs[d][i], df)
                        self.score[d] += tf_idf * w
                        self.length[d] += math.pow(tf_idf, 2)

        for d in self.docs:
            if self.length[d]:
                self.score[d] = self.score[d] / (math.sqrt(self.length[d] * query_length))
                self.score[d] = round(self.score[d], 5)

        return sorted(self.score.items(), key=operator.itemgetter(1), reverse=True)

    def get_tf_idf(self, tf, df):
        return (1 + math.log(tf, 10)) * math.log(self.num_doc / df, 10)

if __name__ == '__main__':
    print 'Please provide a text file:'
    file_name = raw_input('> ')
    print '\n'

    print 'Please enter the query:'
    query = raw_input('> ')
    print '\n'

    vsm_rs = VSMRetrievalSystem()
    vsm_rs.parse_articles(file_name)

    print 'Here goes the result:'
    results = vsm_rs.get_sorted_results(query)

    for i in range(len(results)):
        if i < 10:
            print 'No. %02d: ' % (i + 1) +  ''.join(str(results[i]))
        else:
            break
