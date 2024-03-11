from node import *


class DoublyLinkedList:

    def __init__(self):
        """
        Initializes DoublyLinkedList class

        Parameters:

        Returns:
            None
        """
        # if there is only one element in the list,
        self.head = None
        self.tail = None

    def is_empty(self):
        """
        Checks to see if the list is empty by seeing if self.head is None

        Parameters:

        Return:
            a Boolean value of either True or False; True if list is empty; False is list is not empty
        """
        return self.head == None

    def add_to_head(self, item):
        """
        Adds an item to the head of the list

        Parameters:
            item: the item to be added to the list

        Return:
             None
        """
        n = Node(item)
        if self.is_empty():  # situation where list is empty
            self.head = n
            self.tail = n
        else:  # list is not empty
            n.next = self.head
            self.head.prev = n
            self.head = n

    def pop_head(self):
        """
        Pops the value at the head of the list

        Parameters:

        Return:
             result: the value at the head of the list
        """
        if not self.is_empty():
            result = self.head.data
            if self.head == self.tail:  # one thing in list
                self.head = self.tail = None
            else:  # two or more things
                self.head = self.head.next
                self.head.prev = None
            return result

    def add_to_tail(self, item):
        """
        Adds an item to the tail of the list

        Parameters:
            item: the item to be added to the list

        Return:
            None
        """
        n = Node(item)
        if self.is_empty():  # situation where list is empty
            self.head = n
            self.tail = n
        else:  # situation where list is not empty
            n.prev = self.tail
            self.tail.next = n
            self.tail = n

    def pop_tail(self):
        """
        Pops the value at the tail of the list

        Parameters:

        Return:
            result: the value at the tail of the list
        """
        if not self.is_empty():
            result = self.tail.data
            if self.head == self.tail:  # one thing in list
                self.head = self.tail = None
            else:  # two or more things
                self.tail = self.tail.prev
                self.tail.next = None
            return result

    def __str__(self):
        """
        Creates a string representation of a doubly linked list object

        Parameters:

        Return:
             a string representation of the object
        """
        result = ""
        p = self.head
        while p != None:
            result = result + str(p.data) + "<->"
            p = p.next

        return result

    def contains(self, item):
        """
        Determines if a particular item is in the list

        Parameters:
            item: the item we are checking to see if it is in the list

        Return:
             a Boolean value - True if the item is in the list; False if it is not
        """
        c_node = self.head

        while c_node is not None:
            if c_node.check_value(item):
                return True
            c_node = c_node.next
        return False

    def insert(self, index, item):
        """
        Inserts an item into the list at a particular specified index. Indexing starts at 0.

        Parameters:
            index: the index at which the item is to be inserted
            item: the item to be placed into the list

        Return:
            None
        """
        id = 0
        c_node = self.head
        n = Node(item)
        found = False

        if index == 0:
            self.add_to_head(n.data)
        elif index == self.length():
            self.add_to_tail(n.data)
        else:
            while c_node is not None:
                p_node = c_node.prev
                n_node = c_node.next

                if id == index:
                    p_node.next = n
                    p_node.next.next = c_node
                elif found:
                    if n_node is not None:
                        c_node.next = n_node

                c_node = n_node
                id = id + 1

    def remove(self, index):
        """
        Removes an item into the list at a particular specified index. Indexing starts at 0.

        Parameters:
            index: the index at which the item is to be removed

        Return:
            None
        """
        id = 0
        c_node = self.head

        while c_node is not None:
            p_node = c_node.prev
            n_node = c_node.next

            if id == index:
                if p_node is not None:
                    p_node.next = n_node
                    if n_node is not None:
                        n_node.prev = p_node
                else:
                    self.head = n_node
                    if n_node is not None:
                        n_node.prev = None

            c_node = n_node
            id = id + 1

    def length(self):
        """
        Determines the length of the doubly linked list

        Parameters:

        Return:
             count - a counter variable that stores the length of the list
        """
        count = 0
        c_node = self.head

        while c_node is not None:
            # increase counter by one
            count = count + 1
            # jump to the linked node
            c_node = c_node.next

        return count
