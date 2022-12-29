from expand import expand
import queue as Qu

# we will need a separate class for A* path finding

class Node(object):
    def __init__(self, nodeName, path, h, g):
        self.nodeName = nodeName
        self.path = []
        self.path = path
        self.h = h
        self.g = g
        self.f = h + g

def a_star_search (dis_map, time_map, start, end):
    
    # since we need to maintain the count of expand function, converting data to graph like previous examples is not logical
    # we will use the expand function as and when needed
    
    path = []
    outerKeys = dis_map.keys()  # gets a list of nodes (since we dont have a graph)
    
    if start not in outerKeys or end not in outerKeys:
        return "Invalid Input"
    
    # we initialize an opened and a closed list, just like we did in BFS and DFS
    
    openedList = []
    closed = []
    openedList.append(start)
    
    # we will use a priority queue so that everytime an element is poped, queue will be sorted automatically
    
    listOfNodes = Qu.PriorityQueue()
    currentNode = start
    currentDist = 0
    explored = 0

    while currentNode != end and explored == 0:
        if currentNode not in closed:
            neighbours = expand(currentNode, time_map)
            closed.append(currentNode)

            if neighbours:  # if not dead end
                for i in neighbours:  # For each neighbours location
                    try:
                        h = dis_map[i][end]
                        g = currentDist + time_map[currentNode][i]
                        f = int(h + g)            # calculating f
                        newNode = Node(i, openedList + [i], h, g)
                        listOfNodes.put((f, i, newNode))
                    except KeyError:
                        print('No path found')
        if not listOfNodes.empty():
            neighboursQueue= listOfNodes.get()[2]
            currentNode = neighboursQueue.nodeName
            currentDist = neighboursQueue.g
            openedList = neighboursQueue.path
        else:
            openedList=[]
            explored = 1
    path = openedList
    return path
    

def depth_first_search(time_map, start, end):
    
    # first we convert the data given into a graph.
    # Here we have used expand function, so the only acceptable data types are dictionaries or nested dictionaries
    
    outerKeys2 = list(time_map.keys())
    dictGraph2 = {}

    for i in outerKeys2:
        destination = expand(i, time_map)
        if i in dictGraph2:
            dictGraph2[i].append(destination)
        else:
            dictGraph2[i] = destination
    
    # Now we check if the data provided by user is correct or not
    
    if start is None or start not in dictGraph2:
        return "Invalid start"
    
    if end is None or end not in dictGraph2:
        return "Invalid end"
    
    # we initialise two lists, one opened and one closed
    
    path = []
    openList = [start]

    while len(openList) != 0:
        nodes = openList.pop()        # pop the last element
        
        if nodes not in path:              # append to open list
            path.append(nodes)
            
        if nodes == end:                   # check of the current node is the destination
            return path
        
        if nodes not in dictGraph2:
            continue
        
        # if we reach the last element of the branch and still have not found the destination, current branch is wrong
        # so we clear the path from open list so that we can return the shortest path
        
        if dictGraph2[nodes] == []:        
            lenPath = len(path)
            for i in range(1 , lenPath):
                path.remove(path[1])
        
        
        if end in dictGraph2[nodes]:
            path.append(end)
            return path

        # find the nieghbour and append to closed list for the nest iteration
        
        for neighbor in dictGraph2[nodes]:
            openList.append(neighbor)

    return "Path does not exist"

def breadth_first_search(time_map, start, end):
    
    # first we convert the data given into a graph.
    # Here we have used expand function, so the only acceptable data types are dictionaries or nested dictionaries
    
    outerKeys = list(time_map.keys())
    dictGraph = {}

    for i in outerKeys:
        destination = expand(i, time_map)
        if i in dictGraph:
            dictGraph[i].append(destination)
        else:
            dictGraph[i] = destination
    
    # Now we check if the data provided by user is correct or not
    
    if start is None or start not in dictGraph:
        return "Invalid start"
    
    if end is None or end not in dictGraph:
        return "Invalid end"
    
    # we initialise two lists, one opened and one closed
    
    visited = []
    shortestPath = [[start]]
    
    if start == end:
        return [start, end]
        
 
    while shortestPath:
        path = shortestPath.pop(0)
        node = path[-1]
        
        if node not in visited:
            visited.append(node)
            neighbours = dictGraph[node]
 
            for neighbour in neighbours:
                new_path=list(path)
                new_path.append(neighbour)
                shortestPath.append(new_path)
                
                if neighbour == end:
                    return new_path
            
    return "Path does not exist"