class Queue:

    def __init__(self):
        """
        Initializer method

        Parameters:

        Return:
            None
        """
        self.items = []

    def is_empty(self):
        """
         Determines if the queue is empty

         Parameters:

         Return:
             a Boolean value (True or False); True if the queue is empty; False if it is not
         """
        return self.items == []

    def enqueue(self, item):
        """
         Adds items to the queue at position 0 - the "front" of the queue

         Parameters:
             item - the item to be added into the queue

         Return:
             None
         """
        self.items.insert(0, item)

    def dequeue(self):
        """
         Removes an item from the queue using the .pop() method - the "back" of the queue

         Parameters:

         Return:
             the item removed using .pop()
         """
        if not self.is_empty():
            return self.items.pop()

    def size(self):
        """
         Determines the size of the queue

         Parameters:

         Return:
             the length of the queue
         """
        return len(self.items)

    def __str__(self):
        """
        Creates a string representation of the queue object

        Parameters:

        Return:
            A string representation of the queue
        """
        return str(self.items)

    def __repr__(self):
        """
        Creates a printable representation of the queue object

        Parameters:

        Return:
            A string representation of the queue
        """
        return str(self.items)
