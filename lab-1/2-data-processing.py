import csv
import re
from collections import Counter
import os
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

SYMBOLS_REGEX = 'amp;|gt;|lt;|[=!,*)@#%(&$_?.^:;/\\\\"\'\\-]'
DIGITS_REGEX = "[0-9]"
MESSAGE_TYPE = "v1"
MESSAGE_KEY = "v2"
SPAM = 'spam'
HAM = 'ham'
OUTPUT_DIRECTORY = 'output'
INITIAL_FILE_NAME = 'data/sms-spam-corpus.csv'
SPAM_OUTPUT_FILE = 'spam_words.csv'
HAM_OUTPUT_FILE = 'ham_words.csv'

porter = PorterStemmer()


def csv_dict_reader(file_obj):
    return csv.DictReader(file_obj, delimiter=',')


def processor_line(line):
    line = remove_digits(line)
    line = remove_symbols(line)
    line = line.lower()
    line = remove_stop_words(line)
    return str(line)


def remove_digits(line):
    return re.sub(DIGITS_REGEX, '', line)


def remove_symbols(line):
    return re.sub(SYMBOLS_REGEX, '', line)


def remove_stop_words(line):
    return [word for word in word_tokenize(line) if not word in stopwords.words()]


def stemming(line):
    token_words = word_tokenize(line)
    stem_sentence = []
    for word in token_words:
        stem_sentence.append(porter.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)


def write_to_file(list, file_name):
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    with open(OUTPUT_DIRECTORY + '/' + file_name, 'w', newline='') as f:
        fieldnames = ['word', 'times']
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writeheader()
        for key, value in list:
            csv_writer.writerow({'word': key, 'times': value})


def main():
    with open(INITIAL_FILE_NAME) as file:
        reader = csv_dict_reader(file)
        spam_counter = Counter()
        ham_counter = Counter()
        for line in reader:
            tokenized_msg = word_tokenize(processor_line(line[MESSAGE_KEY]))
            if line[MESSAGE_KEY] == SPAM:
                spam_counter.update(tokenized_msg)
            else:
                ham_counter.update(tokenized_msg)

        write_to_file(spam_counter.most_common(), SPAM_OUTPUT_FILE)
        write_to_file(ham_counter.most_common(), HAM_OUTPUT_FILE)


if __name__ == '__main__':
    main()
