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

        if currentCost <= stopValue:
            return (count, currentPath, currentCost)

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
                # print("No improvement")
                # if restart:
                #     print("Restarting ...")

    return (count, currentPath, currentCost)


def simulatedAnnealingTSP(graph, startingV, stopValue=-math.inf):
    ''' To solve the Traveling Salesman Problem,
    Generate pick a random path that starts and ends with "startingV".
    Swap any two vertices.
    Calculate each cost.
    If it is better, take it.
    If it is not better, take it with probability e**(delta/T).

    Repeat until the Temperature (T) is zero or you find the solution.
    Find the minimum. '''

    # only  restart if stopValue > 0

    restart = True
    count = 1
    while restart:
        T = 100.0
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

        epsilon = 0.0001
        while T > epsilon:
            T = 0.99*T

            # pick 1 to 3 pairs of vertices to swap
            howMany = random.randint(1, 3)
            possibleNewPath = currentPath[:]
            for _ in range(howMany):
                # pick two vertices and swap them
                index = random.randint(1, len(startingPath) - 1)
                index2 = random.randint(1, len(startingPath) - 1)
                while index == index2:
                    index2 = random.randint(1, len(startingPath) - 1)

                possibleNewPath[index], possibleNewPath[index2] = possibleNewPath[index2], possibleNewPath[index]
                #print("Swapping ", index, " with ", index2)

            newCost = graph.cycleCost(possibleNewPath)

            if newCost <= currentCost:
                currentCost = newCost
                currentPath = possibleNewPath[:]
                #print("Better: ", currentCost, "\tT: ", T)
                count += 1
            else:
                prob = math.e**((currentCost-newCost)/T)

                if random.random() < prob:
                    currentCost = newCost
                    currentPath = possibleNewPath[:]
                    #print("Worse: ", currentCost, "\tT: ", T, "\tProb: ", prob)
                    count += 1
                #else:
                    #print("Not taken", newCost, "\tT: ", T, "\tProb: ", prob)
            if currentCost <= stopValue:
                return (count, currentPath, currentCost)


        #print("No improvement")
        # if restart:
        #     print("Restarting ...")

    return (count, currentPath, currentCost)


def pickAParent(population):
    '''
    Randomly pick two potential candidates to be a parent.
    Choose one based on the probability 1 - (ScoreParent1)/(ScoreParent1 + ScoreParent2).
    This makes it more likely to choose a better parent, but not necessarily.

    :param population: The list of all members of the population.
    :return: The index of the chosen parent.
    '''
    n = len(population)

    index1 = random.randint(0, n-1)
    index2 = random.randint(0, n-1)
    while index2 == index1:
        index2 = random.randint(0, n - 1)

    cost1 = population[index1][1]
    cost2 = population[index2][1]

    prob1 = 1 - (cost1/(cost1+cost2))

    if random.random() < prob1:
        return index1
    else:
        return index2

def breed(population, parent1, parent2):
    '''
    Take a random slice of parent1 and insert that into the child.
    The rest of the genes are copied from parent2 in left to right order, excluding any values that
    were part of parent1's slice.

    :param population: A list of all members of the population.
    :param parent1: The index of the first parent
    :param parent2: The index of the second parent.
    :return: The "child" produced by the reproduction.
    '''

    gene1 = population[parent1][0]
    gene2 = population[parent2][0]

    n = len(gene1)
    startSequence = random.randint(1, n - 2)
    endSequence = random.randint(startSequence+1, n-1)

    childGene = n*[0]
    childGene[0] = gene1[0]   # starting vertex is the same

    # copy sequence from gene1
    for i in range(startSequence, endSequence+1):
        childGene[i] = gene1[i]

    # now fill in blanks with values from parent2 (not including ones that are already in childGene1
    childIndex = 1
    parent2Index = 1
    while childIndex < n:
        if childGene[childIndex] == 0:   # it needs a value
            while gene2[parent2Index] in childGene:
                parent2Index += 1
            childGene[childIndex] = gene2[parent2Index]
            parent2Index += 1
        childIndex += 1

    # for debugging
    #print(startSequence, endSequence)
    #print(gene1, gene2, childGene)

    return childGene

def mutate(gene):
    '''
    Pick two vertices at random and swap them.
    :param gene: The list of vertices.
    :return: Nothing returned, but the side effect is a mutuated 'gene"
    '''
    n = len(gene)
    index1 = random.randint(1, n-1)
    index2 = random.randint(1, n - 1)

    while index1 == index2:
        index2 = random.randint(1, n - 1)

    gene[index1], gene[index2] = gene[index2], gene[index1]


def geneticAlgorithmTSP(graph, startingV, stopValue=-math.inf):
    ''' To solve the Traveling Salesman Problem,
    Generate a starting population of random solutions.
    Breed them.
    Mutate children.
    Add children to population.
    Remove bad solutions.
    Repeat until solution is found (or a certain number of generations is reached.

     '''

    # only  restart if stopValue > 0

    restart = True
    count = 1

    generationCount = 0
    #maxGenerations = 100
    #maxGenerations = 250
    #maxGenerations = 500
    maxGenerations = 1000
    populationSize = 100

    # create a starting population
    population = [] # a list of current possible solutions as a tuple (Path, cost)
    for _ in range(populationSize):
        allV = list(graph.vertices.keys())  # the list of all the vertices

        # create an initial guess
        # remove startingV
        allV.remove(startingV)
        random.shuffle(allV)
        startingPath = [startingV] + allV
        startingCost = graph.cycleCost(startingPath)
        count += 1
        population.append( (startingPath[:], startingCost) )

    # sort population by cost
    population.sort(key = lambda x: x[1])

    # print(len(population))
    # for creature in population:
    #     print(creature)

    if population[0][1] <= stopValue:
        return(count, population[0][0], population[0][1])



    # don't repeat too many times
    while generationCount < maxGenerations:
        generationCount += 1
        #print("Generation: ", generationCount)
        howManyChildren = len(population)//2
        children = []
        for _ in range(howManyChildren):

            parent1 = pickAParent(population)   # returns index of parent
            parent2 = pickAParent(population)
            while parent1 == parent2:
                parent2 = pickAParent(population)

            #print("Parent1:", parent1)
            #print("Parent2:", parent2)

            child = breed(population, parent1, parent2)
            #print(child)
            if random.random() < 0.5:   # 25% of the time
                mutate(child)
                #print("Mutated: ", child)

            newCost = graph.cycleCost(child)
            children.append( (child[:], newCost) )
            count += 1

        population = population + children
        # resort
        population.sort(key=lambda x: x[1])

        # lop off worst genes
        population = population[0:populationSize]

        if population[0][1] <= stopValue:
            return (count, population[0][0], population[0][1])

        # consider whether the population has converged
        countSame = 0
        start = population[0][1]
        for i in range(1, len(population)):
            if population[i][1] == start:
                countSame += 1
        #print("Same: ", countSame)

        # if half the population has the same value,
        # delete everybody
        # start over with a new random population.
        if countSame > len(population) // 2:
            generationCount = 0
            #print("Restarting")

            # create a starting population
            population = []  # a list of current possible solutions as a tuple (Path, cost)
            for _ in range(populationSize):
                allV = list(graph.vertices.keys())  # the list of all the vertices

                # create an initial guess
                # remove startingV
                allV.remove(startingV)
                random.shuffle(allV)
                startingPath = [startingV] + allV
                startingCost = graph.cycleCost(startingPath)
                count += 1
                population.append((startingPath[:], startingCost))

            # sort population by cost
            population.sort(key=lambda x: x[1])


            if population[0][1] <= stopValue:
                return (count, population[0][0], population[0][1])


    return (count, population[0][0], population[0][1])


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
 
    perm_iterator = itertools.permutations(allV)
    #for item in perm_iterator:
    #for possiblePath in perm_generator(allV):
    for possiblePath in perm_iterator:
            possiblePath = list(possiblePath)
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
numberOfVertices = 10
myGraph = randomGraph(numberOfVertices)

#cheapSolutionCost = -math.inf
cheapSolutionCost = 10*numberOfVertices
myGraph = modifyGraphWithInexpensiveCircuit(myGraph, "A", cheapSolutionCost)

#print("Brute Force:\t", bruteForceTSP(myGraph, "A", cheapSolutionCost))

#print("Hill Climb:\t ", hillClimbingTSP(myGraph, "A", cheapSolutionCost))

#print("Sim Anneal:\t ", simulatedAnnealingTSP(myGraph, "A", cheapSolutionCost))

#print("Genetic:\t", geneticAlgorithmTSP(myGraph, "A", cheapSolutionCost))

print("# Vertices" + '\t' + '\t' + "# Guesses")
for i in range(3, 26):
    myGraph = randomGraph(i)
    cheapSolutionCost = 10 * i
    myGraph = modifyGraphWithInexpensiveCircuit(myGraph, "A", cheapSolutionCost)
    answer = geneticAlgorithmTSP(myGraph, "A", cheapSolutionCost)
    num_guesses = answer[0]
    print(str(i) + '\t' + '\t' + '\t' + '\t' + str(num_guesses))

# The following code is for determining the suboptimality with limited maxGen. The commented maxGenerations lines
# in the genetic algorithm function need to be uncommented as needed to generate results like that shown in the report.
print('# Vertices' + '\t' + 'Actual Cost' + '\t' + 'Optimal Cost')
for i in range(3, 26):
    myGraph = randomGraph(i)
    cheapSolutionCost = 10 * i
    myGraph = modifyGraphWithInexpensiveCircuit(myGraph, "A", cheapSolutionCost)
    cost = 0
    num_exp = 3
    for j in range(num_exp):
        answer = geneticAlgorithmTSP(myGraph, "A", cheapSolutionCost)
        cost += answer[2]
    print(str(i) + '\t' + str(cost//3) + '\t' + str(cheapSolutionCost))

#How expensive is it?
# numberOfVertices = 11
# for i in range(3, numberOfVertices):
#     myGraph = randomGraph(i)
#     cheapSolutionCost = 10 * i
#     myGraph = modifyGraphWithInexpensiveCircuit(myGraph, "A", cheapSolutionCost)
#
#     start = time.perf_counter()
#     if i < 11
#         (countBrute, cycleBrute, costBrute) = bruteForceTSP(myGraph, "A", cheapSolutionCost)
#     else:
#         (countBrute, cycleBrute, costBrute) = (0,0,0)
#     end = time.perf_counter()
#
#     start2 = time.perf_counter()
#     if i < 20:
#         (countHill, cycleHill, costHill) = hillClimbingTSP(myGraph, "A", cheapSolutionCost)
#     else:
#         (countHill, cycleHill, costHill) = (0,0,0)
#     end2 = time.perf_counter()
#
#     #print(i, "\t", end - start, '\t', end2 - start2, '\t', end3 - start3)
#     print(i, "\t", countBrute, '\t', countHill, '\t', countSimAnneal, '\t', countGene)
#
