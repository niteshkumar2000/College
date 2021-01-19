graph = {}
open = []
close = []

def addEdge(parent, child, cost):
    if parent not in graph:
        graph[parent] = {}
    graph[parent][child] = cost

def get_child_nodes(node):
    return list(graph[node].keys())

def add_path(ds, node):
    if node not in ds:
        ds.append(node)

def dfs(start_node, goal_node):
    if start_node == goal_node:
        add_path(close, goal_node)
        return True
    else:
        for node in get_child_nodes(start_node):
            add_path(open, node)
        add_path(close, start_node)
        dfs(open.pop(), goal_node)

def bfs(start_node, goal_node):
    if start_node == goal_node:
        add_path(close, goal_node)
        return True
    else:
        for node in get_child_nodes(start_node):
            add_path(open, node)
        add_path(close, start_node)
        bfs(open.pop(0), goal_node)

if __name__ == '__main__':
    addEdge('a', 'b', 36)
    addEdge('a', 'c', 61)
    addEdge('b', 'd', 31)
    addEdge('d', 'c', 32)
    addEdge('c', 'l', 80)
    addEdge('c', 'f', 31)
    addEdge('d', 'e', 52)
    addEdge('l', 'm', 102)
    addEdge('e', 'g', 43)
    addEdge('g', 'h', 20)
    addEdge('h', 'i', 40)
    addEdge('i', 'j', 45)
    addEdge('j', 'k', 36)
    addEdge('k', 'm', 32)
    addEdge('f', 'k', 112)
    addEdge('f', 'j', 122)
    bfs('a', 'm')
    print(close)

