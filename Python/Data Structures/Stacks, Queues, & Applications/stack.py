import copy


class Stack:
    def __init__(self):
        self.data = []

    def push(self,item):
        self.data.append(item)

    def pop(self):
        return self.data.pop()

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self)

    def size(self):
        return len(self.data)

    def is_empty(self):
        return self.data == []

    def peek(self):
        return self.data[-1]

    # return a deep copy of this Stack
    def clone(self):
        s = Stack()
        s.data = copy.deepcopy(self.data)
        return s
