from collections import defaultdict
import os
import re


class SpellingCorrector(object):
    def __init__(self, query_list):
        self.query_list = query_list

    def __del__(self):
        os.remove('temp')

    def set_text_file(self, file_name):
        raw_content = open(file_name).read()
        modified_content = re.sub('[^a-zA-Z0-9\n]', ' ', raw_content)
        open('temp', 'w').write(modified_content.lower())

    def get_corrected_list(self):
        self.word_dict = defaultdict(int)

        with open('temp', 'r') as file:
            for line in file:
                for word in line.split():
                    self.word_dict[word] += 1

        self.corrected_list = []

        for query in self.query_list:
            max_frequency = 0
            corrected_word = 'NOT FOUND'

            for word, frequency in self.word_dict.iteritems():
                # Reduce redundant work
                if len(word) < len(query) - 1 or len(word) > len(query) + 1 or frequency <= max_frequency:
                    continue

                levenshtein_distance = self.get_levenshtein_distance(query, word)

                if levenshtein_distance <= 1:
                    corrected_word = word
                    max_frequency = frequency

            self.corrected_list.append([corrected_word, max_frequency])

        return self.corrected_list

    def get_levenshtein_distance(self, s1, s2):
        m = [[0 for x in range(len(s2) + 1)] for x in range(len(s1) + 1)]

        for i in range(len(s1) + 1):
            m[i][0] = i

        for j in range(len(s2) + 1):
            m[0][j] = j

        for i in range(1, len(s1) + 1):
            for j in range(1, len(s2) + 1):
                if s1[i - 1] == s2[j - 1]:
                    m[i][j] = min(m[i - 1][j] + 1, m[i][j - 1] + 1, m[i - 1][j - 1])
                else:
                    m[i][j] = min(m[i - 1][j] + 1, m[i][j - 1] + 1, m[i - 1][j - 1] + 1)

        return m[len(s1)][len(s2)]

if __name__ == '__main__':
    print 'Please provide a text file:'
    file_name = raw_input('> ')
    print '\n'

    print 'Please enter the queries:'
    query_list = [j.strip() for j in raw_input('> ').split(' ')]
    print '\n'

    corrector = SpellingCorrector(query_list)
    corrector.set_text_file(file_name)

    corrected_list = corrector.get_corrected_list()

    print 'Here goes the result:'
    print '\t## QUERY_WORD => CORRECTED_WORD (FREQUENCY) ##'
    for i in range(len(query_list)):
        print '\t' + query_list[i] + ' => ' + corrected_list[i][0] + ' (' + str(corrected_list[i][1]) + ')'
