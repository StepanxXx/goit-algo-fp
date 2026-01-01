"""
Module for visualizing a binary heap.

This module provides functions to visualize a binary heap both as a tree printed to the console
and as a graphical tree using NetworkX and Matplotlib.
"""
import heapq

import networkx as nx
import matplotlib.pyplot as plt

def print_heap_iterative(heap: list):
    """Ітеративна візуалізація купи, представленої списком (праворуч→вузол→ліворуч)."""
    if not heap:
        print("(порожня купа)")
        return

    def has_idx(idx):
        return 0 <= idx < len(heap) and heap[idx] is not None

    stack = [(0, "", False, True, False)]  # (idx, prefix, is_left, is_root, processed)

    while stack:
        idx, prefix, is_left, is_root, processed = stack.pop()
        if not has_idx(idx):
            continue

        left_idx = 2 * idx + 1
        right_idx = 2 * idx + 2
        has_left = has_idx(left_idx)
        has_right = has_idx(right_idx)

        if processed:
            if is_root:
                print(heap[idx])
            else:
                connector = "└── " if is_left else "┌── "
                print(prefix + connector + str(heap[idx]))
        else:
            if is_root:
                right_prefix = ""
                left_prefix = ""
            else:
                right_prefix = prefix + ("│   " if is_left else "    ")
                left_prefix = prefix + ("    " if is_left else "│   ")

            if has_left:
                stack.append((left_idx, left_prefix, True, False, False))

            stack.append((idx, prefix, is_left, is_root, True))

            if has_right:
                stack.append((right_idx, right_prefix, False, False, False))

def add_edges(graph, heap, pos, idx=0, x=0, y=0, layer=1):
    """
    Recursively adds nodes and edges to the graph to represent the heap structure.

    Args:
        graph (nx.DiGraph): The graph to add nodes and edges to.
        heap (list): The list representing the heap.
        pos (dict): A dictionary to store the positions of the nodes.
        idx (int): The current index in the heap.
        x (float): The x-coordinate of the current node.
        y (float): The y-coordinate of the current node.
        layer (int): The current depth layer of the tree.

    Returns:
        nx.DiGraph: The updated graph.
    """
    if heap:
        graph.add_node(idx, label=heap[idx], color="skyblue")
        left_idx = 2 * idx + 1
        right_idx = 2 * idx + 2
        has_left = 0 <= left_idx < len(heap) and heap[left_idx] is not None
        has_right = 0 <= right_idx < len(heap) and heap[right_idx] is not None
        if has_left:
            graph.add_edge(idx, left_idx)
            l = x - 1 / 2 ** layer
            pos[left_idx] = (l, y - 1)
            l = add_edges(graph, heap, pos, left_idx, x=l, y=y - 1, layer=layer + 1)
        if has_right:
            graph.add_edge(idx, right_idx)
            r = x + 1 / 2 ** layer
            pos[right_idx] = (r, y - 1)
            r = add_edges(graph, heap, pos, right_idx, x=r, y=y - 1, layer=layer + 1)
    return graph



def draw_tree(heap: list):
    """Візуалізація купи, представленої списком."""
    if not heap:
        print("(порожня купа)")
        return

    tree = nx.DiGraph()
    pos = {0: (0, 0)}
    tree = add_edges(tree, heap, pos)
    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()


nums = [4, 10, 3, 5, 1, 10, 3, 7, 332, 4, 2, 6, 8, 9]
heapq.heapify(nums)
print("Список після heapify:", nums)
print("Візуалізація купи:")
print_heap_iterative(nums)
draw_tree(nums)
