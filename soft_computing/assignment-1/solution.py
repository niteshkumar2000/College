graph = {}

def addEdge(parent, child, cost):
    if parent not in graph:
        graph[parent] = {}
    graph[parent][child] = cost
    
if __name__ == '__main__':
    addEdge('a', 'b', 30)
    addEdge('a', 'c', 10)
    addEdge('b', 'd', 40)
    addEdge('b', 'e', 15)
    addEdge('c', 'f', 30)
    addEdge('c', 'g', 20)
    print(graph)
