def dfs(graph, start):
    visited = set()       # To keep track of visited nodes
    stack = [start]       # Initialize the stack with the starting node
    traversal = []        # List to store the DFS traversal order

    while stack:
        # Pop the top node from the stack
        current = stack.pop()
        
        if current not in visited:
            # Mark the node as visited and add it to the traversal list
            visited.add(current)
            traversal.append(current)
            
            # Push all unvisited neighbors onto the stack
            for neighbor in graph[current]:  # Reverse to mimic recursive DFS order
                if neighbor not in visited:
                    stack.append(neighbor)
    
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
dfs_result = dfs(graph, start_node)
print("Graph Traversal:", dfs_result)
