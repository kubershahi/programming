from collections import deque

def bfs(graph, start):

    queue = deque([start])
    visited = set()       # To keep track of visited nodes
    traversal = []      

    while queue:
        # Pop the top node from the queue
        current = queue.popleft()
        
        if current not in visited:
            # Mark the node as visited and add it to the traversal list
            visited.add(current)
            traversal.append(current)
            
            # Push all unvisited neighbors onto the stack
            for neighbor in graph[current]:  
                if neighbor not in visited:
                    queue.append(neighbor)
    
    return traversal

# Example usage
graph = {
    'A': ['B', 'C', 'D'],
    'B': ['E', 'F'],
    'C': [],
    'D': ['G', 'H'],
    'E': [],
    'F': [],
    'G': [],
    'H': []
}

start_node = 'A'
result = bfs(graph, start_node)
print("Graph Traversal:", result)