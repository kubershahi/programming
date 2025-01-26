import heapq

def dijkstra_with_min_heap(graph, start):
    """
    Dijkstra's Algorithm using Min-Heap
    :param graph: Dictionary where keys are nodes and values are lists of (neighbor, weight) pairs
    :param start: The source node
    :return: Dictionary with shortest distances from the start node to all other nodes
    """
    # Initialize distances and min-heap
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    min_heap = [(0, start)]  # (distance, node)

    while min_heap:
        current_distance, current_node = heapq.heappop(min_heap)

        # If the distance is outdated, skip processing
        if current_distance <= distances[current_node]:
            # Explore neighbors
            for neighbor, weight in graph[current_node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(min_heap, (distance, neighbor))

    return distances

# Example usage
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('C', 2), ('D', 6)],
    'C': [('A', 4), ('B', 2), ('D', 3)],
    'D': [('B', 6), ('C', 3)]
}

start_node = 'A'
shortest_distances = dijkstra_with_min_heap(graph, start_node)
print("Shortest distances from", start_node, ":", shortest_distances)
