import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import math
import csv
with open('StanTopic/lda-2afcb432-30-f6432ddc/document-topic-distributions.csv', 'rb') as csvfile:
    topic_item = []
    topic_item_file = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in topic_item_file:
        topic_item.append([float(element) for element in row[1:]])



def plot_heat_map():
    plt.pcolor(topic_item, norm=None, cmap='Blues')
    plt.yticks(np.arange(topic_item.shape[0])+0.5, docnames);
    plt.xticks(np.arange(topic_item.shape[1])+0.5, topic_labels);

def plot_graph():
    similarity_matrix = np.matrix(topic_item[1:20]) * np.matrix(topic_item[1:20]).T
    G=nx.from_numpy_matrix(similarity_matrix)
    nx.draw(G)
    plt.draw()
    plt.show()

def plot_topic_words():
    topic_words_file = open('StanTopic/lda-2afcb432-30-f6432ddc/01000/summary.txt')

    num_topics = 0
    word_topic = []
    word_topic_wt = []
    for line in topic_words_file:
        if (len(line.split()) > 0):
            if (line.find('Topic') != -1):
                num_topics += 1
                word_topic.append([])
                word_topic_wt.append([])
            else:
                word_prob_dict = line.split()
                word_topic[num_topics-1].append(word_prob_dict[0])
                word_topic_wt[num_topics-1].append(float(word_prob_dict[1]))

    word_topic_wt = np.array(word_topic_wt)

    num_top_words = 20 #(len(word_topic[0]))
    num_topics = 10
    fontsize_base = 300 / np.max(word_topic_wt[:num_topics,:]) # font size for word with largest share in corpus
    for t in range(num_topics):
        plt.subplot(1, num_topics, t + 1)  # plot numbering starts with 1
        plt.ylim(0, num_top_words + 0.5)  # stretch the y-axis to accommodate the words
        plt.xticks([])  # remove x-axis markings ('ticks')
        plt.yticks([]) # remove y-axis markings ('ticks')
        plt.title('Topic #{}'.format(t))
        for i, (word, share) in enumerate(zip(word_topic[t], word_topic_wt[t])):
            plt.text(0.1, num_top_words-i-0.5, word, fontsize=fontsize_base*math.sqrt(share))  

    plt.show()

if __name__ == "__main__":
    # plot_topic_words()
    plot_graph()