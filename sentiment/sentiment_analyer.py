#!usr/bin/env python
# coding:utf-8

import jieba
from sentiment.langconv import *


def simple2tradition(line):
    # Simplified font to Traditional font
    line = Converter('zh-hant').convert(line)
    return line


def tradition2simple(line):
    # Traditional font to Simplified font
    line = Converter('zh-hans').convert(line.decode('utf-8'))
    line = line.encode('utf-8')
    return line


class SentimentAnalyer:
    # init config and read sentiment dict data into dict
    def __init__(self, config):
        self.config = config
        self.__readFile()

    def get_sentiment_dicts(self):
        return {
            "sentiment": self.__sentList,
            "noword": self.__noword,
            "adverb": self.__adverb,
            "stopword": self.__stopword,
        }

    # read dict
    def __readFile(self):
        sentiment = self.config['sentiment']
        noword = self.config['noword']
        adverb = self.config['adverb']
        stopword = self.config['stopword']
        self.__sentList = {}
        self.__noword = []
        self.__adverb = {}
        self.__stopword = []
        sentList = open(sentiment, 'r', encoding="utf-8")
        for s in sentList.readlines():
            try:
                s = s.replace('\r\n', '').replace('\n', '')
                self.__sentList[simple2tradition(s.split(' ')[0])] = s.split(' ')[1]
            except:
                print("sentiment except")
                pass
        sentList.close()
        nowordList = open(noword, 'r', encoding="utf-8")
        for s in nowordList.readlines():
            try:
                s = s.replace('\r\n', '').replace('\n', '')
                self.__noword.append(simple2tradition(s))
            except:
                print("noword except")
        nowordList.close()
        adverbList = open(adverb, 'r', encoding="utf-8")
        for s in adverbList.readlines():
            try:
                s = s.replace('\r\n', '').replace('\n', '')
                self.__adverb[simple2tradition(s.split(',')[0])] = s.split(',')[1]
            except:
                print("adverb except")
        adverbList.close()
        stopwordList = open(stopword, 'r', encoding="utf-8")
        for s in stopwordList.readlines():
            try:
                s = s.replace('\r\n', '').replace('\n', '')
                self.__stopword.append(simple2tradition(s))
            except:
                print("stopword except")
        stopwordList.close()

    def setSentence(self, sentence):
        self.__sentence = sentence.lstrip()

    # 预处理
    def preDetail(self):
        word_list = jieba.cut(self.__sentence, cut_all=False)
        # print(list(word_list))
        new_words = {}
        i = 0
        for w in word_list:
            if w not in self.__stopword:
                new_words[str(i)] = w
                i = i + 1
        sen_words = {}
        not_words = {}
        degree_words = {}
        m = 0
        for index in new_words.keys():
            if new_words[index] in self.__sentList.keys() and new_words[index] not in self.__noword and new_words[
                index] not in self.__adverb.keys():
                sen_words[index] = self.__sentList[new_words[index]]
            elif new_words[index] in self.__noword and new_words[index] not in self.__adverb.keys():
                not_words[index] = -1
            elif new_words[index] in self.__adverb.keys():
                degree_words[index] = self.__adverb[new_words[index]]
            else:
                sen_words[index] = 0
        return sen_words, not_words, degree_words, new_words

    def get_review_sentiment_score(self):
        sen_words, not_words, degree_words, new_words = self.preDetail()
        print(sen_words, not_words, degree_words, new_words)
        W = 1
        score = 0
        # A list of locations for all sentimental words
        sen_loc_list = []
        not_loc = []
        degree_loc = []
        for i in sen_words.keys():
            sen_loc_list.append(int(i))
        for i in not_words.keys():
            not_loc.append(int(i))
        for i in degree_words.keys():
            degree_loc.append(int(i))
        sen_loc_list.sort()
        not_loc.sort()
        degree_loc.sort()
        sen_loc = -1
        for i in range(0, len(new_words)):
            # If the word is an emotional word
            if i in sen_loc_list:
                # loc is the serial number of the list of emotion word locations
                sen_loc += 1
                score += W * float(sen_words[str(i)])
                print("score", W * float(sen_words[str(i)]))
                # print "score = %f" % score
                if sen_loc < len(sen_loc_list) - 1:
                    # Determine if there is a negative or degree adverb between this affective word and the next affective word
                    if sen_loc_list[sen_loc + 1] - sen_loc_list[sen_loc] > 1:
                        for j in range(sen_loc_list[sen_loc] + 1, sen_loc_list[sen_loc + 1]):
                            if j in not_loc:
                                W *= -1
                            elif j in degree_loc:
                                W *= float(degree_words[str(j)])
                    else:
                        W = 1
            if sen_loc < len(sen_loc_list) - 1:
                i = sen_loc_list[sen_loc + 1]

        return score


def getSentimentAnalyer(config):
    return SentimentAnalyer(config)


def main():
    print("Start")
    config = {
        "sentiment": '../dict/BosonNLP_sentiment_score.txt',
        "noword": '../dict/nowords.txt',
        "adverb": '../dict/degree.txt',
        "stopword": '../dict/stopwords.txt',
    }
    s = getSentimentAnalyer(config)
    print(s.get_sentiment_dicts())
    s.setSentence('我不覺得非常聰明"')
    # Positive score if article is positive
    # Negative score if article is negative
    print(s.get_review_sentiment_score())
    print("Done")


if __name__ == '__main__':
    main()
