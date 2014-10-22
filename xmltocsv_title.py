from lxml import etree
import csv
import os
import numpy

def getTitle():
    rows= []

    for i in xrange(1,100):
        file_path = os.getcwd() + '/womens-accessories-general/' + str(i)
        
        if os.path.exists(file_path):
            xml_file = open(file_path)
            xml_tree = etree.parse(xml_file)
            item_ids = xml_tree.xpath('//ItemID/text()')
            titles = xml_tree.xpath('//Title/text()')
            for i in xrange(len(item_ids)):
                rows.append([item_ids[i], titles[i]])

    with open('titles.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows([[column.encode("UTF-8") for column in row] for row in rows])

if __name__ == "__main__":
    getTitle()