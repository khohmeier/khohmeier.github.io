from Graph import *
import random, itertools
import time, math

''' build a random fully connect graph '''


def randomGraph(n):
    ''' Generated a fully connected bidirectional
        graph with n nodes and random weights.  '''

    ''' Generate n vertices with names A, B, C, ... Z '''
    vertices = []
    for i in range(n):
        if i < 26:  # if we have less than 26 vertices, then just use A ... Z
            name = chr(ord('A') + i)
        else:
            name = "Node" + str(i)

        vertices.append(name)

    theGraph = Graph()
    for i in range(len(vertices)):  # for each vertex, add an edge to the other vertices
        v1 = vertices[i]
        for j in range(i + 1, len(vertices)):
            v2 = vertices[j]
            cost = random.randint(1, 10 * n)  # a random weight
            theGraph.addEdge(v1, v2, cost)
            theGraph.addEdge(v2, v1, cost)  # the graph is bi-directional

    return theGraph


def modifyGraphWithInexpensiveCircuit(graph, startingV, cost):
    allV = list(graph.vertices.keys())  # the list of all the vertices

    costPerEdge = cost//len(allV)
    #print("CostPerEdge: ", costPerEdge)
    # remove startingV
    allV.remove(startingV)
    random.shuffle(allV)

    startingPath = [startingV] + allV
    for index in range(0, len(startingPath) - 1):

        # forward
        start = startingPath[index]
        end = startingPath[index+1]
        edges = graph.vertices[start]
        for edgeCount in range(len(edges)):
            edge = edges[edgeCount]
            if edge[0] == end:
                edges[edgeCount] = (end, costPerEdge)
                break
        # backward
        start = startingPath[index+1]
        end = startingPath[index]
        edges = graph.vertices[start]
        for edgeCount in range(len(edges)):
            edge = edges[edgeCount]
            if edge[0] == end:
                edges[edgeCount] = (end, costPerEdge)
                break

    #forward
    start = startingPath[-1]
    end = startingPath[0]
    edges = graph.vertices[start]
    for edgeCount in range(len(edges)):
        edge = edges[edgeCount]
        if edge[0] == end:
            edges[edgeCount] = (end, costPerEdge)
            break
    #backward
    start = startingPath[0]
    end = startingPath[-1]
    edges = graph.vertices[start]
    for edgeCount in range(len(edges)):
        edge = edges[edgeCount]
        if edge[0] == end:
            edges[edgeCount] = (end, costPerEdge)
            break


    #graph.printEdges()
    #print("Debugging cycle cost", startingPath, graph.cycleCost(startingPath))
    return graph


def perm_generator(lst):
    ''' Generates all possible permutations of lst returning one
    at a time using "yield."
    Found on the internet. https://stackoverflow.com/questions/24979179/how-does-yield-work-in-this-permutation-generator
    '''
    if len(lst) == 1:
        yield lst
    else:
        for i in range(len(lst)):
            for perm in perm_generator(lst[:i] + lst[i+1:]):
                yield [lst[i]] + perm


def hillClimbingTSP(graph, startingV, stopValue=-math.inf):
    ''' To solve the Traveling Salesman Problem,
    Generate pick a random path that starts and ends with "startingV".
    Swap any two vertices.
    Calculate each cost.
    Choose the best.
    Repeat until you get stuck (no better cost) or you find the solution.
    Find the minimum. '''

    # only  restart if stopValue > 0
    restart = True
    count = 1
    while restart:
        # restart = False
        if stopValue <= 0:
            restart = False

        allV = list(graph.vertices.keys())  # the list of all the vertices

        # create an initial guess
        # remove startingV
        allV.remove(startingV)
        random.shuffle(allV)
        startingPath = [startingV] + allV
        startingCost = graph.cycleCost(startingPath)
        #print("Start\t\t", startingCost, startingPath)

        currentPath = startingPath[:]
        currentCost = startingCost

        stopHillClimbing = False
        while not stopHillClimbing:
            improvementFound = False
            bestCost = currentCost

            # swap all pairs of vertices (except the starting vertex) and
            # see which has the lowest cost
            for index in range(1, len(startingPath) - 1):
                for index2 in range(index+1, len(startingPath)):
                    possibleNewPath = currentPath[:]
                    possibleNewPath[index], possibleNewPath[index2] = possibleNewPath[index2], possibleNewPath[index]
                    newCost = graph.cycleCost(possibleNewPath)
                    count += 1
                    if newCost < bestCost:
                        bestCost = newCost
                        bestPath = possibleNewPath[:]
                        improvementFound = True

            if improvementFound:
                currentPath = bestPath[:]
                currentCost = bestCost
                #print("Improvement\t", bestCost, bestPath)
                if currentCost <= stopValue:
                    return (count, currentPath, currentCost)
            else:
                stopHillClimbing = True
                #print("No improvement")
                #if restart:
                    #print("Restarting ...")

    return (count, currentPath, currentCost)


def bruteForceTSP(graph, startingV, stopValue=-math.inf):
    ''' To solve the Traveling Salesman Problem,
    Generate every possible cycle starting at vertex "startingV".
    Calculate each cost.
    Find the minimum. '''

    allV = list(graph.vertices.keys())  # the list of all the vertices
    # remove startingV
    allV.remove(startingV)

    triedReverse = {}
    countPaths = 0
    minCost = math.inf
    bastPath = []

    # try every possible permutation
    for possiblePath in perm_generator(allV):
            str_PossiblePath = str(possiblePath)
            rev_PossiblePath = str(possiblePath[::-1])
            # ignore paths that are the same forward as they are
            # backwards
            if str_PossiblePath in triedReverse:
                continue
            elif rev_PossiblePath in triedReverse:
                continue
            else:
                triedReverse[str_PossiblePath] = str_PossiblePath
                triedReverse[rev_PossiblePath] = rev_PossiblePath

                # add the starting vertex back in
                possiblePath = [startingV] + possiblePath
                countPaths += 1

                cost = graph.cycleCost(possiblePath)
                if cost < minCost:
                    bestPath = possiblePath
                    minCost = cost
                    if minCost <= stopValue:
                        return (countPaths, bestPath, minCost)


    return (countPaths, bestPath, minCost)


# let's test it out
numberOfVertices = 50
myGraph = randomGraph(numberOfVertices)

# cheapSolutionCost = -math.inf
cheapSolutionCost = 10*numberOfVertices
myGraph = modifyGraphWithInexpensiveCircuit(myGraph, "A", cheapSolutionCost)

# print(myGraph.BFSOrder("A"))
# print(myGraph.DFSOrder("A"))
# myGraph.printEdges()


# print("Brute Force:\t", bruteForceTSP(myGraph, "A", cheapSolutionCost))

# print("Hill Climb:\t ", hillClimbingTSP(myGraph, "A", cheapSolutionCost))

print("# of Vertices" + '\t' + '\t' + "# of Guesses")
for i in range (4, numberOfVertices + 1):
    num_exp = 5
    num_guesses = 0
    for exp in range(num_exp):
        myGraph = randomGraph(i)
        answer = hillClimbingTSP(myGraph, "A")
        num_guesses += answer[0]
    print(str(i) + '\t' + '\t' + '\t' + '\t' + str(math.ceil(num_guesses/num_exp)))

# Code for Hill Climbing without random restart
# Note: to run this code, restart = False in line 116 must be uncommented
print("Avg Cost" + '\t' + '\t' + "Optimal Path")
for j in range(4, 41):
    num_exp = 5
    cost = 0
    for exp in range(num_exp):
        myGraph = randomGraph(j)
        answer = hillClimbingTSP(myGraph, "A")
        cost += answer[2]
    print(str(math.ceil(cost/5)) + '\t' + '\t' + str(10*j))

# How expensive is it?
# numberOfVertices = 11
# for i in range(3, numberOfVertices):
#     myGraph = randomGraph(i)
#
#     start = time.perf_counter()
#     answer = bruteForceTSP(myGraph, "A")
#     end = time.perf_counter()
#
#     start2 = time.perf_counter()
#     answer = hillClimbingTSP(myGraph, "A")
#     end2 = time.perf_counter()
#
#
#     print(i, "\t", end - start, '\t', end2 - start2)
