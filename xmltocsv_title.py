from lxml import etree
from collections import Counter
import csv
import os
import numpy
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import itertools

def getTitle():
    stemmer = SnowballStemmer("english")
    with open('./sample-data/november-general/hdp_data.dat', 'wb') as f:
        with open('./sample-data/november-general/hdp_vocab.dat', 'wb') as v:
            with open('./sample-data/november-general/hdp-docs.dat', 'wb') as d:
                # writer = csv.writer(f, delimiter=',')
                vocab = []
                for root, dirs, files in os.walk('./sample-data/november-general'):
                    rows= []
                    for i in xrange(1,10):
                        file_path = root + '/' + str(i)
                        print file_path

                        if os.path.exists(file_path):
                            xml_file = open(file_path)
                            try:
                                xml_tree = etree.parse(xml_file)
                                item_ids = xml_tree.xpath('//ItemID/text()')
                                titles = xml_tree.xpath('//Title/text()')
                            except etree.XMLSyntaxError:
                                print "Error:" + file_path
                            finally:
                                xml_file.close()
                            for i in xrange(len(item_ids)):
                                termFreq = Counter(list(itertools.chain(*[word_tokenize(t) for t in sent_tokenize(titles[i].encode('ascii', 'ignore').lower())])))
                                termFreqStemmed = {stemmer.stem(term):freq for (term, freq) in termFreq.iteritems()}
                                titleFormat = str(len(termFreqStemmed)) + ' '

                                for term, freq in termFreqStemmed.iteritems():
                                    # if term not in vocab:
                                    #     index = len(vocab)
                                    #     vocab.append(term.encode("UTF-8"))
                                    # else:
                                    #     index  = vocab.index(term)
                                    # titleFormat += str(index) + ':' + str(freq) + ' '
                                    titleFormat += term + ':' + str(freq) + ' '
                                f.write(titleFormat + '\n')
                                d.write(titles[i].encode("UTF-8") + '\n')
            # for term in vocab:
            #     v.write("%s\n" % term)

if __name__ == "__main__":
    getTitle()
