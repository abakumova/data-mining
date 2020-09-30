from collections import Counter
import csv
from matplotlib import pyplot as plt
import numpy as np

INITIAL_FILE_NAME = 'data/sms-spam-corpus.csv'
SPAM = 'spam'
HAM = 'ham'
MESSAGE_TYPE = "v1"
MESSAGE_KEY = "v2"


def calculate_avg(d):
    x = 0
    y = 0
    for v in d:
        c = v[1]
        x += v[0] * c
        y += c
    return x / y


def main():
    with open(INITIAL_FILE_NAME) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        spam_w_list = []
        ham_w_list = []
        for row in csv_reader:
            msg_len = len(row[MESSAGE_KEY])
            if row[MESSAGE_TYPE] == SPAM:
                spam_w_list.append(msg_len)
            else:
                ham_w_list.append(msg_len)
        spam_w_list = Counter(spam_w_list).most_common()
        ham_w_list = Counter(ham_w_list).most_common()

        draw_chart(spam_w_list, SPAM)
        draw_chart(ham_w_list, HAM)


def draw_chart(cnter, msg_type):
    plt.style.use('seaborn-bright')
    plt.title('{} Message length by category chart'.format(msg_type))
    count_of_words = [c[0] for c in cnter]
    x_indexes = np.arange(len(count_of_words))
    plt.xticks(x_indexes, count_of_words)
    plt.bar(x_indexes, [c[1] for c in cnter], color='#FF1493', label='Amount of messages by length')
    plt.xlabel("Message length")
    plt.ylabel("Amount of messages")
    plt.show()
    print('Average {} message size is {}'.format(msg_type, str(calculate_avg(cnter))))


if __name__ == '__main__':
    main()
