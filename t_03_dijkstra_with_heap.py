"""
Module for Dijkstra's algorithm implementation.

This module contains an implementation of Dijkstra's algorithm for finding
the shortest paths in a weighted graph using a binary heap (priority queue).
"""
from collections import namedtuple
import heapq

import networkx as nx
import matplotlib.pyplot as plt

DijkstraRow = namedtuple('DijkstraRow', ['vertex', 'known', 'cost', 'weight', 'path', "full_path"] )

def dijkstra(graph, start) -> dict[str, DijkstraRow]:
    """
    Implements Dijkstra's algorithm to find the shortest paths from a start node.

    Args:
        graph (dict): The graph represented as a dictionary of dictionaries.
        start (str): The starting vertex key.

    Returns:
        dict[str, DijkstraRow]: A dictionary where keys are vertex names and values
                                are DijkstraRow named tuples containing path info.
    """
    # Ініціалізація відстаней та множини невідвіданих вершин
    distances = {
        vertex: DijkstraRow(
            vertex,False, float('infinity'), float('infinity'), "", [vertex]
        ) for vertex in graph
    }
    distances[start] = DijkstraRow(start, True, 0, 0, start, [start])
    visited = set()
    priority_queue = [(0, start)]

    while priority_queue:
        # Знаходження вершини з найменшою відстанню серед невідвіданих
        _, current_vertex = heapq.heappop(priority_queue)

        if current_vertex in visited:
            continue

        visited.add(current_vertex)

        # Якщо поточна відстань є нескінченністю, то ми завершили роботу
        if distances[current_vertex].cost == float('infinity'):
            break

        for neighbor, weight in graph[current_vertex].items():
            distance = distances[current_vertex].cost + weight

            # Якщо нова відстань коротша, то оновлюємо найкоротший шлях
            if distance < distances[neighbor].cost:
                full_path = distances[current_vertex].full_path[:-1] + [current_vertex] + [neighbor]
                distances[neighbor] = DijkstraRow(
                        neighbor, True, distance, weight, current_vertex, full_path)

                heapq.heappush(priority_queue, (distance, neighbor))


    return distances


graph_ = {
    'A': {'B': 5, 'C': 10, 'G': 10},
    'B': {'A': 5, 'D': 3, 'G': 2},
    'C': {'A': 10, 'D': 2},
    'D': {'B': 3, 'C': 2, 'E': 4, 'F': 1},
    'E': {'D': 4, 'F': 2},
    'F': {'D': 1, 'E': 2},
    'G': {'A': 10, 'B': 2}
}

# Виконання алгоритму Дейкстри
START_VERTEX = 'A'
dijkstra_results = dijkstra(graph_, START_VERTEX)

# Вивід результатів
print(f"{'vertex':<7} {'known':<7} {'cost':<7} {'weight':<7} {'path':<7} {'full_path':<20}")
print("-" * 50)
for node in sorted(dijkstra_results.keys()):
    row = dijkstra_results[node]
    print(f"{row.vertex:<7} {str(row.known):<7} {row.cost:<7} {row.weight:<7} "
          f"{str(row.path):<7} {str(row.full_path):<20}")


# Створення графа для візуалізації
G = nx.Graph()
for u, neighbors in graph_.items():
    for v, weight_ in neighbors.items():
        G.add_edge(u, v, weight=weight_)

# Візуалізація графа
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=15, width=2)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.show()
