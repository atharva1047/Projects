import math
import re


class Bayes_Classifier:

    def __init__(self):
        self.countPositive = 0
        self.countNegative = 0
        self.uniqueWords = {}
        self.dict_of_positive = {}
        self.dict_of_negative = {}
        self.positive_bigrams = {}
        self.negative_bigrams = {}

    def train(self, lines):

        rating = []
        userId = []

        for line in lines:
            line = line.replace('\n', '')
            separated = line.split('|')
            rating.append(separated[0])
            userId.append(separated[1])

            separated[2] = self.improve_text(separated[2])
            self.get_bigrams_and_split(separated[0], separated[2])

            if separated[0] == '5':
                for word in separated[2].split():
                    self.countPositive += 1
                    if word in self.dict_of_positive:
                        self.dict_of_positive[word] += 1
                    else:
                        self.dict_of_positive[word] = 1

            if separated[0] == '1':
                for word in separated[2].split():
                    self.countNegative += 1
                    if word in self.dict_of_negative:
                        self.dict_of_negative[word] += 1
                    else:
                        self.dict_of_negative[word] = 1

        self.uniqueWords.update(self.dict_of_positive)
        self.uniqueWords.update(self.dict_of_negative)

        self.probability_positive = math.log2((rating.count('5') + 1) / (len(rating) + 2))
        self.probability_negative = math.log2((rating.count('1') + 1) / (len(rating) + 2))

    def improve_text(self, line):
        stopwords = ['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
                     'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
                     'to', 'was', 'were', 'will', 'with']

        # Remove punchuation
        line = re.sub(r'[^\w\s]', '', line)


        # Remove stopwords and capitalization
        line = ' '.join(
            ['' if word in stopwords else word for word in line.lower().split()])

        line = self.stem(line)

        return line

    def stem(self, line: str):
        new_line = ''

        for word in line.split():
            word = re.sub('ies$', 'ie', word)
            word = re.sub('ing$', '', word)
            word = re.sub('es$', 'e', word)
            word = re.sub('ed$', '', word)
            word = re.sub('bly$', 'e', word)
            word = re.sub('ly$', '', word)
            word = re.sub(r'[^A-Za-z]', '', word)

            new_line = new_line + ' ' + word

        return new_line

    def get_bigrams_and_split(self, rating, line):

        word_list = line.split()

        for i in range(len(word_list) - 1):
            if hash(word_list[i]) < hash(word_list[i + 1]):
                temp = (word_list[i], word_list[i+1])
            else:
                temp = (word_list[i+1], word_list[i])

            if rating == '5':
                if temp in self.positive_bigrams:
                    self.positive_bigrams[temp] += 1
                else:
                    self.positive_bigrams[temp] = 1

            if rating == '1':
                if temp in self.negative_bigrams:
                    self.negative_bigrams[temp] += 1
                else:
                    self.negative_bigrams[temp] = 1

    def get_bigrams(self, line):

        word_list = line.split()
        bigram_list = []

        for i in range(len(word_list) - 1):
            if hash(word_list[i]) < hash(word_list[i + 1]):
                temp = (word_list[i], word_list[i+1])
            else:
                temp = (word_list[i+1], word_list[i])
            bigram_list.append(temp)

        return bigram_list

    def classify(self, lines):
        results = []

        for line in lines:
            probability_word_given_positive = 0
            probability_word_given_negative = 0

            line = line.replace('\n', '')
            separated = line.split("|")
            separated[2] = self.improve_text(separated[2])

            for word in separated[2].split():
                if word in self.dict_of_positive:
                    probability_word_given_positive = (probability_word_given_positive +
                                                       math.log2((self.dict_of_positive[word] + 1) / (self.countPositive + len(self.dict_of_positive))))
                
                else:
                    probability_word_given_positive = (probability_word_given_positive +
                                                       math.log2((1) / (self.countPositive + len(self.dict_of_positive))))

                if word in self.dict_of_negative:
                    probability_word_given_negative = (probability_word_given_negative +
                                                       math.log2((self.dict_of_negative[word] + 1) / (self.countNegative + len(self.dict_of_negative))))
                else:
                    probability_word_given_negative = (probability_word_given_negative +
                                                       math.log2((1) / (self.countNegative + len(self.dict_of_negative))))
                
                # pdb.set_trace()

            bigram_list = self.get_bigrams(separated[2])

            overall_bigram_score = 0
            positive_bigram_score = 0
            negative_bigram_score = 0

            for bigram in bigram_list:
                if (bigram in self.positive_bigrams) and (bigram in self.negative_bigrams):
                    overall_bigram_score = abs(self.positive_bigrams[bigram] - self.negative_bigrams[bigram])

                if (bigram in self.positive_bigrams) and (bigram not in self.negative_bigrams):
                    positive_bigram_score = self.positive_bigrams[bigram]

                if (bigram not in self.positive_bigrams) and (bigram in self.negative_bigrams):
                    negative_bigram_score = self.negative_bigrams[bigram]

            probability_positive_given_line = (self.probability_positive + probability_word_given_positive
                                               + (positive_bigram_score + overall_bigram_score))

            probability_negative_given_line = (self.probability_negative + probability_word_given_negative
                                               + (negative_bigram_score + overall_bigram_score))
            

            if probability_positive_given_line > probability_negative_given_line:
                results.append('5')
            else:
                results.append('1')

        return results
