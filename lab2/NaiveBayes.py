from lab1.DataProcessing import *

SET_WORD = "word"
SET_TIMES = "times"
OUTPUT_DIRECTORY_WITH_DATA = '../lab1/output'
OUTPUT_DIRECTORY = 'output'
SPAM_OUTPUT_FILE = 'spam_words.csv'
HAM_OUTPUT_FILE = 'ham_words.csv'


def csv_dict_reader(file_obj):
    logging.info('Returning csv reader')
    return csv.DictReader(file_obj, delimiter=',')


def calculate_sum_of_word_frequency(file):
    general_frequency = 0
    with open(OUTPUT_DIRECTORY_WITH_DATA + '/' + file) as csv_file:
        logging.info('Calculate sum of word frequency')
        reader = csv_dict_reader(csv_file)
        for line in reader:
            general_frequency += int(line[SET_TIMES])
    return general_frequency


def create_statistic_dictionary(file):
    statistic_dictionary = {}
    with open(OUTPUT_DIRECTORY_WITH_DATA + '/' + file) as csv_file:
        logging.info('Calculate statistic of word frequency')
        reader = csv_dict_reader(csv_file)
        for line in reader:
            statistic_dictionary[line[SET_WORD]] = int(line[SET_TIMES])
    return statistic_dictionary


def create_statistic_file(file, statistic_dictionary):
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    with open(OUTPUT_DIRECTORY + '/' + file, 'w', newline='') as csv_file:
        logging.info('Write to file statistic of word frequency')
        writer = csv.writer(csv_file)
        writer.writerow(["word", "frequency"])
        for key, value in statistic_dictionary.items():
            writer.writerow([key, value])


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


def calculate_probability(words, message):
    logging.info('calculate_probability')
    words_amount_in_set = words_in_set(words)
    unknown_words_amount = words_not_in_set(words, message)
    probability = 1
    for word in message:
        word_count = 0
        if word in words:
            word_count = int(words[word])
        probability *= (word_count + 1) / (words_amount_in_set + unknown_words_amount)
    return probability


def main():
    message = input('Enter the message: ')
    tokenized_message = processor_line(message)
    print(tokenized_message)

    statistic_spam_dictionary = create_statistic_dictionary(SPAM_OUTPUT_FILE)
    statistic_ham_dictionary = create_statistic_dictionary(HAM_OUTPUT_FILE)

    spam_probability = calculate_probability(statistic_spam_dictionary, tokenized_message)
    ham_probability = calculate_probability(statistic_ham_dictionary, tokenized_message)

    sum_of_probabilities = spam_probability + ham_probability
    spam_normalized_probability = spam_probability / sum_of_probabilities
    ham_normalized_probability = ham_probability / sum_of_probabilities

    print("This message is SPAM with {} probability".format(spam_normalized_probability))
    print("This message is HAM with {} probability".format(ham_normalized_probability))


if __name__ == '__main__':
    main()
