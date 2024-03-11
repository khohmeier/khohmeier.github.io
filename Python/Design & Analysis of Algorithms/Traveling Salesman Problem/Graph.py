

class Graph:
    ''' This graph uses adjacency lists to store the edges.
    For each vertex, we store its edges in a hash table.
    Each edge is just a tuple of the ending vertex and the cost.  '''

    def __init__(self):
        ''' A graph is initially created as an empty hash table of vertices. '''
        self.vertices = {}

    def addV(self, name):
        ''' A vertex could be added by passing its name (assumed to be a string).  '''
        self.vertices.put(name, [])  # or self.vertices[name] = []

    def addEdge(self, v1, v2, cost):
        ''' To add an edge, you must pass the starting vertex (v1),
        the ending vertex (v2), and the cost.  '''
        if v1 in self.vertices:  # if the vertex is already in the hash table,
                                 # append this edge to the list.
            edges = self.vertices[v1]
            edges.append( (v2, cost))
        else: # add this vertex to the hash table
            self.vertices[v1] = [ (v2, cost)]
        if not v2 in self.vertices:
            self.vertices[v2] = []

    def DFSOrder(self, startV):
        ''' this produces a depth-first ordering of vertices
        beginning with startV.  '''
        ordered = []
        stack = []
        stack.append(startV)
        while stack != []:
            v = stack.pop()  # grab the top element
            if not v in ordered:
                ordered.append(v)
                for edge in self.vertices[v]:
                        stack.append(edge[0]) # push to the top
        return ordered

    def BFSOrder(self, startV):
        ''' This returns a breadth-first ordering of vertices
          beginning with startV.  '''
        ordered = []
        stack = []
        stack.append(startV)
        while stack != []:
            v = stack.pop(0)  # dequeue from the front
            if not v in ordered:
                ordered.append(v)
                for edge in self.vertices[v]:
                        stack.append(edge[0]) # enqueue to the rear
        return ordered

    def cycleCost(self, cycle):
        ''' A cycle is a list of vertices.
        Don't forget to connect the last vertex to the first vertex.
        This can be done by cheating -- add the first vertex to the end'''

        cost = 0
        path = list(cycle) # just in case cycle is a tuple, I convert it to a list
        path.append(path[0])  # my cheat to get the full cost to return back to the beginning
        for i in range(len(path) - 1):
            v1 = path[i]
            v2 = path[i+1]
            # find the cost of the edge
            j = 0
            found = False
            edges = self.vertices[v1]
            while j < len(edges) and not found:
                if edges[j][0] == v2:
                    extraCost = edges[j][1]
                    found = True
                j += 1
            if not found:
                raise Exception("No edge from " + str(v1) + " to " + str(v2))
            cost += extraCost
        # add cost from last vertex to first vertex
        return cost

    def printEdges(self):
        ''' Simple printing of edges.  '''
        for v in self.vertices:
            for edge in self.vertices[v]:
                print(v, edge[0], edge[1])
