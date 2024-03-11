from queue import Queue
from stack import Stack
from time_this import *


def read_words(filename):
    """
    Reads the words in the specified file and returns a dictionary containing those words

    Parameters:
        filename: name of file containing all legal words

    Return:
        dictionary containing all the legal words
    """
    # words are keys, not values!
    # the values are used to indicate whether the word is available for use - True
    # the value is changed to False for whenever the word is used
    # at the start of a new search, all the values are reset to True
    file = open(filename, 'r')
    d = {}

    for line in file:
        line = line.strip('\n')
        d[line] = True

    file.close()

    return d


def get_next_words(word, dict):
    """
    Returns a list of "unused" words in dictionary that are one letter different from word

    Parameters:
        word: a word
        dict: dictionary containing all the legal words

    Return:
        a  list of "unused" words in dictionary that are exactly one letter different from word
    """
    unused = []
    count = 0

    for key in dict:
        if len(key) == len(word):
            for i in range(len(word)):
                if key[i] != word[i]:
                    count += 1
        if count == 1:
            unused.append(key)
        count = 0

    return unused


def find_ladder(start_word, end_word, dict):
    """
    Finds and returns a stack representing the word ladder between start_word and end_word

    Parameters:
        start_word: the starting word for the ladder
        end_word: the ending word for the ladder
        dict: dictionary containing all the legal words

    Return:
        a stack representing the word ladder between start_word and end_word, if one exists, None otherwise
    """
    q = Queue()
    s = Stack()

    s.push(start_word)
    q.enqueue(s)

    while not q.is_empty():
        s = q.dequeue()
        if s.peek() == end_word:
            return s
        elif s.peek() != end_word:
            word_list = get_next_words(s.peek(), dict)
            for item in word_list:
                s_new = s.clone()
                if dict[item] == True:
                    s_new.push(item)
                    q.enqueue(s_new)
                    dict[item] = False
                if s_new.peek() == end_word:
                    return s_new

    if q.is_empty():
        return None


def main():
    """
    method to execute the other functions and open input file that contains the word pairs
    used for the find_ladder function

    Parameters:

    Return:
         None
    """
    # we have to open input.txt in order to grab the words to be used
    # open input.txt and read first word pair
    # line[0] = start_word, line[1] = end_word

    file = open('resources/input.txt', 'r')
    dictionary = read_words('resources/dictionary.txt')
    temp_dict = {}

    for line in file:

        line = line.strip('\n')
        line = line.split(' ')
        length = len(line[0])

        for item in dictionary:
            if len(item) == length:
                temp_dict[item] = True

        print("Finding word ladder for", line[0], 'and', line[1])
        if line[0] not in dictionary:
            print("There is no word ladder between", line[0], line[1])
        else:
            # output = find_ladder(line[0], line[1], dictionary)
            output = time_this(find_ladder, line[0], line[1], temp_dict)
            if output[1] is not None:
                print(output[0], "seconds:", "ladder length = ", output[1].size(), ": ", output[1])
            elif output[1] is None:
                print(output[0], "seconds:", "There is no word ladder between ", line[0], " and ", line[1], "!")
        # print(time_this(find_ladder, line[0], line[1], temp_dict)[0], 'seconds')
        dictionary = read_words('resources/dictionary.txt')


main()
