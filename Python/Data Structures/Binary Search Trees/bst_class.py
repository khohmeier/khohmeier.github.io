from rand_list import *
import random


class TreeNode:
    def __init__(self, item):
        self.key = item
        self.left = None
        self.right = None

    def get_key(self):
        return self.key

    def __str__(self):
        return str(self.key)

    def is_leaf(self):
        return self.left is None and self.right is None


class BinarySearchTree:
    def __init__(self):
        self.root = None          
        
    def find(self, key):  # return the number of nodes examined during the process
        """
        A find function that searches for a particular element in the BST and determines the number of nodes examined
        during the process

        Parameters:
            key: the element we are searching for in the BST

        Return:
            A call to the search method, a helper function, which will eventually return the total number of nodes
            examined during the search
        """
        if self.root is None:  # tree is empty
            return 0
        else:
            return self.search(self.root, key)

    def search(self, current_node, key):
        """
        A helper function for the find method

        Parameters:
            current_node: the starting node at which the searching is to begin (should be self.root)
            key: the element we are searching for

        Return:
            increments a counter and makes a recursive call to search
        """
        current_key = current_node.get_key()
        counter = 1
        if current_key == key:
            return counter
        elif key > current_key and current_node.right:
            return counter + self.search(current_node.right, key)
        elif key < current_key and current_node.left:
            return counter + self.search(current_node.left, key)
        else:
            return counter
        
    def store(self, key):
        if self.root is None:  # empty BST
            self.root = TreeNode(key)
        else:   # non-empty tree
            self._add_node(self.root, key)

    def _add_node(self, current_node, item):
        if item > current_node.get_key():  # add to right sub-tree
            if current_node.right is None:
                current_node.right = TreeNode(item)
            else:
                self._add_node(current_node.right, item)
        elif item < current_node.get_key():  # add to left sub-tree
            if current_node.left is None:
                current_node.left = TreeNode(item)
            else:
                self._add_node(current_node.left, item)

    def __str__(self):
        if self.root:
            return self._pretty_print(self.root, 0)

    def _pretty_print(self, current_node, offset):
        spacer = 5
        print_string = ""
        if current_node.right:
            print_string += self._pretty_print(current_node.right, offset + spacer)

        if not current_node.is_leaf():
            print_string += "\n" + ' ' * offset + str(current_node) + '-'*spacer
        else:
            print_string += "\n" + ' ' * offset + str(current_node)

        if current_node.left:
            print_string += self._pretty_print(current_node.left, offset + spacer)

        return print_string

    def count_nodes(self):
        """
        A recursive function that counts the total number of nodes in the binary search tree

        Parameters:

        Return:
            a call to the helper function, _count_nodes, which will provide a count of the total number of nodes
        """
        # must be recursive!!!!
        if self.root is None:
            return 0
        else:
            return self._count_nodes(self.root)

    def _count_nodes(self, current_node):
        """
        A helper function for count_nodes

        Parameters:
            current_node: the starting node at which the node counting is to begin (should be self.root)

        Return:
            the final count of all nodes in the tree
        """
        if current_node.right is None:
            right_count = 0
        else:
            right_count = self._count_nodes(current_node.right)

        if current_node.left is None:
            left_count = 0
        else:
            left_count = self._count_nodes(current_node.left)

        return right_count + left_count + 1

    def get_height(self):
        """
        A recursive function that determines the height of the binary search tree. The height is defined as the maximum
        number of levels in the tree.

        Parameters:

        Return:
            A call to the helper function, _get_height, which will ultimately return the height of the tree
        """
        # see textbook for definition of height of tree - note that the root is level 0. So it's like indexing
        # must be recursive
        if self.root is None:
            return 0
        else:
            return self._get_height(self.root)

    def _get_height(self, current_node):
        """
        A helper function for the get_height method
        
        Parameters:
            current_node: the starting node at which the level counting is to begin (should be self.root) 
        
        Return:
            the height of the BST
        """
        if current_node.right is None:
            level_count_right = 0
        else:
            level_count_right = 1 + self._get_height(current_node.right)

        if current_node.left is None:
            level_count_left = 0
        else:
            level_count_left = 1 + self._get_height(current_node.left)

        return max(level_count_left, level_count_right)


# PART I - PERFORMING EXPERIMENTS WITH BINARY SEARCH TREE SIZE 16, 1000, 2000, and 4000


def create_tree(size):
    """
    Create a binary search tree of a specific size

    Parameters:
        size: an integer value used to create a BST of that size

    Return:
        None
    """

    t = BinarySearchTree()
    num_list = random_list(size-1, 10, 10000)

    for n in num_list:
        t.store(n)

    t.store(1)

    return t.count_nodes(), t.get_height(), t.find(1), t.find(1000000)


def main(size):
    """
    Function to run ten experiments to find the average number of nodes examined during searches, the average size
    of the trees, and the average heights of the tree

    Parameter:
        size: an integer value used to create a BST of that size

    Return:
        a string representation of the relevant information
    """

    num_present = 0  # this will store the number of searches when element is present in tree
    num_not_present = 0  # this will store the number of searches when element is not present in tree
    height = 0
    num_nodes = 0

    for r in range(0, 10):
        info_tuple = create_tree(size)
        num_nodes += info_tuple[0]
        height += info_tuple[1]
        num_present += info_tuple[2]
        num_not_present += info_tuple[3]

    avg_present = num_present//10
    avg_not_present = num_not_present//10
    avg_size = num_nodes//10
    avg_height = height // 10

    return 'avg # nodes examined, item present = ' + str(avg_present) + ' avg # nodes examined, item not present = ' \
           + str(avg_not_present) + ' avg size of tree = ' + str(avg_size) + ' avg height = ' + str(avg_height)


# SINGLE EXPERIMENT
print(create_tree(16))

# TEN EXPERIMENTS
print(main(16))
print(main(1000))
print(main(2000))
print(main(4000))


# PART II - PERFORMING SSN SEARCH


def search_file():
    """
    A function to search a file with 1,000,000 SSNs and store them in a binary search tree and to test finding a random
    element in the BST

    Parameters:

    Return:
        None
    """
    output = open('results_P2.txt', 'w')
    input_file = open('ssn.txt', 'r')
    t = BinarySearchTree()

    output.write('PART II' + '\n')
    print("Opened ssn.txt - begin storing SSNs into a BST" + '\n')
    output.write("Opened ssn.txt - begin storing SSNs into a BST" + '\n')

    for line in input_file:
        line = line.strip('\n')
        t.store(int(line))

    print('Number of nodes in binary search tree: ' + str(t.count_nodes()) + '\n')
    print('Height of binary search tree: ' + str(t.get_height()))

    output.write('Number of nodes in binary search tree: ' + str(t.count_nodes()) + '\n')
    output.write('Height of binary search tree: ' + str(t.get_height()) + '\n')

    # creating a randomly generated SSN
    ssn = ''

    for r in range(0, 9):
        ssn += str(random.randint(0, 9))

    print(ssn)
    num_comparisons = t.find(int(ssn))

    print('Number of comparisons needed to perform a search for a randomly selected SSN: ' + \
                 str(num_comparisons))
    output.write('Number of comparisons needed to perform a search for a randomly selected SSN: ' + \
                 str(num_comparisons))


search_file()
