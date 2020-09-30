from lab1.DataProcessing import *

SET_WORD = "word"
SET_TIMES = "times"
SPAM_STATISTIC_FILE = 'spam_stat.csv'
HAM_STATISTIC_FILE = 'ham_stat.csv'
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


def create_statistic_dictionary(file, general_frequency):
    statistic_dictionary = {}
    with open(OUTPUT_DIRECTORY_WITH_DATA + '/' + file) as csv_file:
        logging.info('Calculate statistic of word frequency')
        reader = csv_dict_reader(csv_file)
        for line in reader:
            statistic_dictionary[line[SET_WORD]] = int(line[SET_TIMES]) / general_frequency
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


def main():
    # Prepare test set
    general_spam_frequency = calculate_sum_of_word_frequency(SPAM_OUTPUT_FILE)
    general_ham_frequency = calculate_sum_of_word_frequency(HAM_OUTPUT_FILE)

    statistic_spam_dictionary = create_statistic_dictionary(SPAM_OUTPUT_FILE, general_spam_frequency)
    statistic_ham_dictionary = create_statistic_dictionary(HAM_OUTPUT_FILE, general_ham_frequency)

    create_statistic_file(SPAM_STATISTIC_FILE, statistic_spam_dictionary)
    create_statistic_file(HAM_STATISTIC_FILE, statistic_ham_dictionary)

    message = input('Enter the message: ')
    tokenized_msg = processor_line(message)


if __name__ == '__main__':
    main()
