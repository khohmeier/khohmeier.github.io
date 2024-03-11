class Node:

    def __init__(self, item):
        """
        Initializes Node class

        Parameters:

        Returns:
            None
        """
        self.data = item
        self.next = None
        self.prev = None

    def check_value(self, value):
        """
        Determines if a value is contained in the data portion of a node

        Parameters:
            value - the value we are checking for to see if it is contained in the node

        Returns:
            a Boolean value - True if the value is contained in the node; False if it is not
        """
        if self.data == value:
            return True
        else:
            return False
