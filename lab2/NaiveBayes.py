from lab1.DataProcessing import *

SET_WORD = "word"
SET_TIMES = "times"
OUTPUT_DIRECTORY_WITH_DATA = '../lab1/output'
DATA_DIRECTORY = '../lab1/data'
OUTPUT_DIRECTORY = 'output'
DATA_INPUT_FILE = 'sms-spam-corpus.csv'
SPAM_OUTPUT_FILE = 'spam_words.csv'
HAM_OUTPUT_FILE = 'ham_words.csv'


def csv_dict_reader(file_obj):
    logging.info('Returning csv reader')
    return csv.DictReader(file_obj, delimiter=',')


# P(ham) P(spam)
def calc_probability_for_mesages(category):
    count_message = 0
    count_category_message = 0
    with open(DATA_DIRECTORY + '/' + DATA_INPUT_FILE) as csv_file:
        reader = csv_dict_reader(csv_file)
        for line in reader:
            if line["v1"] == category:
                count_category_message += 1
            count_message += 1
    return count_category_message / count_message


def create_statistic_dictionary(file):
    statistic_dictionary = {}
    with open(OUTPUT_DIRECTORY_WITH_DATA + '/' + file) as csv_file:
        logging.info('Calculate statistic of word frequency')
        reader = csv_dict_reader(csv_file)
        for line in reader:
            statistic_dictionary[line[SET_WORD]] = int(line[SET_TIMES])
    return statistic_dictionary


def words_in_set(words):
    logging.info('words_in_set')
    amount = 0
    for word in words:
        amount += int(words[word])
    return amount


def words_not_in_set(words, message):
    logging.info('words_not_in_set')
    unknown_words = 0
    known_words = words.keys()
    for word in message:
        if word not in known_words:
            unknown_words += 1
    return unknown_words


def calculate_probability(words, message, p_probab):
    logging.info('calculate_probability')
    words_amount_in_set = words_in_set(words)
    unknown_words_amount = words_not_in_set(words, message)
    probability = 1
    for word in message:
        word_count = 0
        if word in words:
            word_count = int(words[word])
        probability *= (word_count + 1) * p_probab / (words_amount_in_set + unknown_words_amount)
    return probability


def main():
    message = input('Enter the message: ')
    tokenized_message = processor_line(message)
    print(tokenized_message)

    statistic_spam_dictionary = create_statistic_dictionary(SPAM_OUTPUT_FILE)
    statistic_ham_dictionary = create_statistic_dictionary(HAM_OUTPUT_FILE)

    p_spam = calc_probability_for_mesages("spam")
    spam_probability = calculate_probability(statistic_spam_dictionary, tokenized_message, p_spam)

    p_ham = calc_probability_for_mesages("ham")
    ham_probability = calculate_probability(statistic_ham_dictionary, tokenized_message, p_ham)

    sum_of_probabilities = spam_probability + ham_probability
    spam_normalized_probability = spam_probability / sum_of_probabilities
    ham_normalized_probability = ham_probability / sum_of_probabilities

    print("This message is SPAM with {} probability".format(spam_normalized_probability))
    print("This message is HAM with {} probability".format(ham_normalized_probability))


if __name__ == '__main__':
    main()
