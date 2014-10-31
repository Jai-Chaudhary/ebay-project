from lxml import etree
from collections import Counter
import csv
import os
import numpy

def getTitle():

    with open('./sample-data/toys-and-hobbies/titles.csv', 'wb') as f:
        writer = csv.writer(f, delimiter=',')
        for root, dirs, files in os.walk('./sample-data/toys-and-hobbies/'):
            rows= []
            for i in xrange(1,100):
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
                        titleFreq = Counter(titles[i].split()).items()
                        titleFormat = str(len(titleFreq)) + ' '
                        for term, freq in titleFreq:
                            titleFormat += term.encode("UTF-8") + ':' + str(freq) + ' '
                        f.write(titleFormat + '\n')

if __name__ == "__main__":
    getTitle()