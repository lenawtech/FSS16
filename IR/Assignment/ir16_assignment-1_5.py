from __future__ import division
import math


class Evaluator(object):
    def __init__(self, data, num_queries, non_relevant, position):
        self.data = data
        self.num_queries = num_queries
        self.non_relevant = non_relevant
        self.position = position

    def get_precision(self):
        """
            Only calculate the precision at the given position for the 1st query.
        """
        self.tp = 0
        self.fp = 0

        for i in range(self.position):
            if self.data[0][i] > non_relevant:
                self.tp += 1
        self.fp = self.position - self.tp

        return self.tp / (self.tp + self.fp)

    def get_ndcg(self):
        self.ndcg = 0

        for j in range(self.num_queries):
            self.nf = self.get_normalization_factor(self.data[j])
            dcg = self.get_dcg(self.data[j])
            self.ndcg += dcg / self.nf

        return self.ndcg / self.num_queries

    def get_normalization_factor(self, data):
        sorted_data = data[:self.position]
        sorted_data.sort(reverse=True)

        return self.get_dcg(sorted_data)

    def get_dcg(self, data):
        dcg = 0

        for m in range(self.position):
            dcg += (2 ** data[m] - 1) / math.log(2 + m, 2)

        return dcg

if __name__ == '__main__':
    print "Please enter the number of queries:"
    num_queries = int(raw_input())

    data = []
    for i in range(num_queries):
        print "\nPlease enter the document collection with relevance judgments for query %d:" % (i + 1)
        data.append([int(j) for j in raw_input().split(',')])

    print "\nPlease enter the non-relevant value:"
    non_relevant = int(raw_input())

    print "\nPlease enter how many top results you want to calculate:"
    position = int(raw_input())

    evaluator = Evaluator(data, num_queries, non_relevant, position)
    print "\n"
    print "Precision@%d is %f." % (position, evaluator.get_precision())
    print "NDCG@%d is %f." % (position, evaluator.get_ndcg())
