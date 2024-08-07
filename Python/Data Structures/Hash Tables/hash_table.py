from time_this import *

# COMMENTS SECTION
# 1) Hashing function: Hashing function chosen was to determine the ord value of each character and adding them up to
# create a total ord value for the whole word. This function was chosen because it is the most straightforward
# implementation to get a numerical index value based on a given string.
#
# 2) Collision resolution scheme: To store multiple words at one index value, chaining is utilized. Hence, all anagrams
# are stored at the same index value in a list. The collision resolution scheme has two situations.
#
# Situation A: The word that has been hashed is an anagram of the word currently occupied in this spot. In this case,
# the word is simply added to the list located at that index.
#
# Situation B: The word that has been hashed does not have the same key as the key that is currently holding that index
# position. In other words, the word is not an anagram of the words currently in the list at that index; it simply
# happened to hash to that index. In this case, linear probing is used. There are, again, two cases to be considered.
#
# B. i: The word does not currently have any of its anagrams currently stored in the hash table. In this case, the
# program simply has to find an empty slot, at which point a new list is created at an empty slot, and the word's key
# and the word are stored at that new index. A probing index of + 11 is used (this was chosen because it improved the
# run time of the program).
#
# B. ii: The word currently has anagrams stored in the hash table. In this situation, an additional check must be
# made to compare the word's key against the key in the first position of a list at a non-empty index in the hash table.
# If the word's key matches, then it is an anagram of the words at that index and is appended to that list. Otherwise,
# the approach described in B. i. is employed.
#
# This collision resolution scheme was chosen because it easily allows anagrams to be stored together at the same index
# under a single key, and when a word that isn't an anagram hashes to that index, it can be stored at a different place
# in the hash table, along with its anagrams (if there are any).
#
# NOTE 11/17/2019
# In the original version of this program, for situation B, I simply did linear probing until an empty slot was found.
# However, this approach contains a very subtle logic error. If there is an index conflict with a word and something
# currently at the index, such that the word happened to hash to that index but is not an anagram of the words stored
# at that index, then it must be relocated. But this situation will occur for all anagrams of that word as well, not
# just that particular word! In other words, all of the anagrams will conflict with another set of anagrams at that
# index. By just using linear probing to find an empty index, words that were anagrams of each other were not being
# stored together, because the program was only checking for an empty slot, but was not checking for matching keys at
# already-filled indices. This caused the program to store words with the same key in different indices, and so the
# anagram search was not working correctly in some cases. My new approach, described above, corrects this logic error.


class HashTable:
    def __init__(self,  size):
        """
        Initializes the hash table. Five properties: size, data, load_factor, occupied, conflicts.
        """
        self.size = size
        self.data = [None] * self.size
        self.load_factor = 0.0
        self.occupied = 0
        self.conflicts = 0

    def __str__(self):
        """
        Creates a string representation of the hash table object

        Return:
            The string representation of the hash table
        """
        return str(len(self.data)) + ' slots' + ', ' + str(self.occupied) + ' occupied' + ', ' \
        + 'load factor = ' + str(self.load_factor)

    def sorting(self, string):
        """
        Algorithm for sorting a string - insertion sort.
        Note: this code was generated by consulting the "Insertion Sort" section in the textbook

        Parameters:
            string: the string to be sorted

        Return:
            the sorted string
        """
        temp = list(string)
        for i in range(1, len(temp)):
            current = temp[i]
            pos = i
            while pos > 0 and temp[pos - 1] > current:
                temp[pos] = temp[pos - 1]
                pos = pos - 1

            temp[pos] = current

        result = ''
        for c in temp:
            result += c

        return result

    def hash_function(self, string):
        """
        A hashing function to create an index for an item in the hash table
        Note: this code was generated during note-taking in class.

        Parameter:
            string: a string

        Return:
            total - the total ord value of all the characters in string
        """
        tot = 0
        weight = 1
        string = self.sorting(string)

        for char in string:
            tot += ord(char)*weight
            weight += 16

        idx = tot % self.size

        return idx

    def store(self, word):
        """
        Accepts a word and stores it in the HashTable. If a conflict is encountered, it implements a conflict
        resolution algorithm to resolve the conflict.
        Note: a portion of this code was generated during note-taking in class.

        Parameters:
            word: the word to be stored in the hash table

        Return:
            None
        """
        # sort letters to create a key
        key = self.sorting(word)

        # find index at which to store word
        index = self.hash_function(key)

        if self.data[index] is None:
            self.data[index] = []
            self.data[index].append(key)
            self.data[index].append(word)
            self.occupied += 1
            self.load_factor = self.occupied / self.size

        elif self.data[index] is not None:
            if key == self.data[index][0]:  # collision handling for same keys - that is, anagrams
                self.data[index].append(word)

            else:  # collision handling for different keys - linear probing
                while self.data[index] is not None:
                    index = (index + 11) % self.size
                    if self.data[index] is not None and key == self.data[index][0]:
                        # collision handling for same keys - that is, anagrams
                        self.data[index].append(word)
                        break
                if self.data[index] is None:
                    self.data[index] = []
                    self.data[index].append(key)
                    self.data[index].append(word)
                    self.occupied += 1
                    self.conflicts += 1
                    self.load_factor = self.occupied / self.size

    def get(self, key):
        """
        Accepts a key and finds and returns its anagrams in the hash table

        Parameters:
            key: an ordered combination of letters sorted using the sort_string function

        Return:
            all the anagrams of the given key
        """

        key = self.sorting(key)

        for index in range(len(self.data)):
            if self.data[index] is not None:
                if key == self.data[index][0]:
                    return str(len(self.data[index][1:])) + ': ' + ' '.join(self.data[index][1:])
        return 0

    def rehash(self):
        """
        A function that is called whenever the load factor exceeds 0.7. This method increases the number of slots in
        the HashTable to a prime number that is roughly twice the current number of slots and relocates all the data
        that is already in the HashTable to new locations consistent with the increased size of the HashTable.

        Parameters:

        Return:
            None
        """

        new_size = (self.size * 2) + 1

        prime = False

        while not prime:
            for i in range(2, new_size):
                if new_size % i == 0:
                    new_size += 1
                else:
                    prime = True

        new_ht = HashTable(new_size)

        for index in range(len(self.data)):
            if self.data[index] is not None:
                for word in self.data[index][1:]:
                    new_ht.store(word)

        return new_ht


def main():
    """
    Main function to execute the methods created in the HashTable class, write output to a file, and locate anagrams
    in a hash table

    Parameters:

    Return:
         None
    """
    h = HashTable(31)

    dictionary = open('resources/dictionary.txt', 'r')
    input_words = open('resources/example_input.txt', 'r')
    output = open('resources/output_new.txt', 'w')

    output.write('Program start' + '\n' + 'Hash table details: ' + str(h) + '\n' + 'Start reading words for ' \
                 'dictionary.txt file' + '\n')

    word_count = 0

    for line in dictionary:
        line = line.strip('\n')
        word_count += 1
        h.store(line)
        if h.load_factor > 0.7:
            print(str(word_count) + ' words read. Hash Table expansion needed.' + '\n')
            output.write('\t' + str(word_count) + ' words read. Hash Table expansion needed.' + '\n')
            output.write('\t' + '\t' + 'Hash Table details, before expansion: ' + str(h) + '\n')
            h = h.rehash()
            output.write('\t' + '\t' + 'Hash Table details, after expansion: ' + str(h) + '\n')

    output.write('End of reading words from dictionary.txt' + '\n' + 'Hash Table details: ' + str(h) + '\n' \
                 + 'Number of unique keys inserted into Hash Table = ' + str(h.occupied) + '\n' + 'Number of ' \
                 'key conflicts encountered = ' + str(h.conflicts) + '\n')

    output.write('Start reading keys from file example_input.txt' + '\n')

    for word in input_words:
        word = word.strip('\n')
        time_info = time_this(h.get, word)
        print(word + ' ' + str(h.get(word)) + ' - this annagram search took ' + str(time_info[0]) + ' seconds' + '\n')
        output.write('\t' + word + ' ' + str(h.get(word)) + ' - this annagram search took ' + str(time_info[0]) + \
                     ' seconds' + '\n')

    output.write('End reading keys from file example_input.txt' + '\n' + 'Program End')

    print(h)
    dictionary.close()
    input_words.close()
    output.close()


main()
