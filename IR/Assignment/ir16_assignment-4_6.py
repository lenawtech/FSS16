import lucene, re
from bs4 import BeautifulSoup
from progressbar import ProgressBar
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.index import FieldInfo, IndexReader, IndexWriter, IndexWriterConfig, Term
from org.apache.lucene.queryparser.classic import MultiFieldQueryParser
from org.apache.lucene.search.similarities import BM25Similarity
from org.apache.lucene.search import BooleanClause, IndexSearcher, PhraseQuery, Query, TopScoreDocCollector
from org.apache.lucene.store import RAMDirectory
from org.apache.lucene.util import Version
import math


class PyLuceneRetrievalSystem(object):
    def __init__(self):
        self.num_doc = 0
        self.directory = RAMDirectory()
        self.analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
        self.config = IndexWriterConfig(Version.LUCENE_CURRENT, self.analyzer)
        self.writer = IndexWriter(self.directory, self.config)

    def parse_articles(self, file_name):
        raw_articles = open(file_name).read()
        parsed_articles = BeautifulSoup(raw_articles, 'lxml')

        doc_nos = parsed_articles.find_all('docno')
        doc_texts = parsed_articles.find_all('text')
        self.num_doc = len(doc_nos)

        bar = ProgressBar()

        for i in bar(range(self.num_doc)):
            doc = Document()
            doc.add(Field('docno', doc_nos[i].string.strip(), StringField.TYPE_STORED))
            doc.add(Field('content', re.sub('[^a-zA-Z0-9\n]', ' ', doc_texts[i].get_text()).lower(), TextField.TYPE_STORED))
            self.writer.addDocument(doc)

        self.writer.close()

    def get_sorted_results(self, query):
        SHOULD = BooleanClause.Occur.SHOULD
        parsed_query = MultiFieldQueryParser.parse(Version.LUCENE_CURRENT, query, ['docno', 'content'], [SHOULD, SHOULD], self.analyzer)

        reader = IndexReader.open(self.directory)
        searcher = IndexSearcher(reader)

        searcher.setSimilarity(BM25Similarity())
        topDocs = searcher.search(parsed_query, 10)

        j = 0
        for i in topDocs.scoreDocs:
            d = searcher.doc(i.doc)

            print 'No. %02d: ' % (j + 1) + d['docno'] + ' ' + str(i.score)

            j += 1

if __name__ == '__main__':
    print 'Please provide a text file:'
    file_name = raw_input('> ')
    print '\n'

    print 'Please enter the query:'
    query = raw_input('> ')
    print '\n'

    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    rs = PyLuceneRetrievalSystem()
    rs.parse_articles(file_name)

    print 'Here goes the result:'
    rs.get_sorted_results(query)

