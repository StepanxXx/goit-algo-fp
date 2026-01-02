"""
Module for visualizing binary tree traversals (BFS and DFS) using NetworkX and Matplotlib.
"""
import uuid
import colorsys
from collections import deque

import networkx as nx
import matplotlib.pyplot as plt

class Node:
    """
    Represents a node in the binary tree.
    """
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color # Додатковий аргумент для зберігання кольору вузла
        self.id = str(uuid.uuid4()) # Унікальний ідентифікатор для кожного вузла

def get_color(color, step):
    """
    Generates a new color based on the previous color and step,
    creating a gradient effect.
    """
    r = int(color[1:3], 16) / 255
    g = int(color[3:5], 16) / 255
    b = int(color[5:7], 16) / 255

    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    # рухаємося від темного до світлого з помітним кроком
    h = (h + 0.4 / step) % 1.0           # повільно змінюємо відтінок
    v = min(1.0, v + 0.8 / step)         # піднімаємо яскравість
    s = max(0.15, s - 0.2 / step)        # трохи знижуємо насиченість

    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    new_color = f"#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}"
    return new_color


def bfs_add_edges(graph, node, pos):
    """
    Performs Breadth-First Search (BFS) to add edges and nodes to the graph
    for visualization.
    """
    color = "#1712FF"
    x, y, layer = 0, 0, 1
    queue = deque([(node, x, y, layer)])
    order = 0
    while queue:  # Поки черга не порожня, продовжуємо обхід
        current, x, y, layer = queue.popleft()
        color = get_color(color, 30)
        order += 1
        graph.add_node(current.id, color=color, label=current.val, order=order)
        if current.left:
            graph.add_edge(current.id, current.left.id)
            l = x - 1 / 2 ** layer
            pos[current.left.id] = (l, y - 1)
            queue.append((current.left, l, y - 1, layer + 1))
        if current.right:
            graph.add_edge(current.id, current.right.id)
            r = x + 1 / 2 ** layer
            pos[current.right.id] = (r, y - 1)
            queue.append((current.right, r, y - 1, layer + 1))
    return graph

def dfs_add_edges(graph, node, pos):
    """
    Performs Depth-First Search (DFS) to add edges and nodes to the graph
    for visualization.
    """
    color = "#1712FF"
    x, y, layer = 0, 0, 1
    stack = [(node, x, y, layer)]
    order = 0
    while stack:
        current, x, y, layer = stack.pop()
        color = get_color(color, 30)
        order += 1
        graph.add_node(current.id, color=color, label=current.val, order=order)
        if current.left:
            graph.add_edge(current.id, current.left.id)
            l = x - 1 / 2 ** layer
            pos[current.left.id] = (l, y - 1)
            stack.append((current.left, l, y - 1, layer + 1))
        if current.right:
            graph.add_edge(current.id, current.right.id)
            r = x + 1 / 2 ** layer
            pos[current.right.id] = (r, y - 1)
            stack.append((current.right, r, y - 1, layer + 1))
    return graph

def draw_tree(tree_root, add_edges_func):
    """
    Draws the binary tree using the specified traversal function to determine colors and order.
    """
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges_func(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    # Використовуйте значення вузла для міток
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, arrows=False, node_size=2500, node_color=colors)

    labels_pos = {}
    for node, coords in pos.items():
        labels_pos[node] = (coords[0], coords[1] + 0.06)
    nx.draw_networkx_labels(
        tree,
        pos=labels_pos,
        labels=labels,
        bbox=dict(boxstyle="round,pad=0.1", fc="#E0E0E0", ec="#E0E0E0", alpha=1)
    )

    additional_labels = {}
    additional_labels_pos = {}
    for node, coords in pos.items():
        key = tree.nodes[node]['order']
        additional_labels[node] = f"крок: {key}"
        additional_labels_pos[node] = (coords[0], coords[1] - 0.06)

    # 5. Малюємо порядку додавання вузлів
    nx.draw_networkx_labels(
        tree,
        pos=additional_labels_pos,
        labels=additional_labels,
        font_size=8,
        bbox=dict(boxstyle="round,pad=0.1", fc="#E0E0E0", ec="#E0E0E0", alpha=1)
    )

    plt.show()


# Створення дерева
root = Node(0)
root.left = Node(4)
root.left.left = Node(5)
root.left.right = Node(10)
root.right = Node(1)
root.right.left = Node(3)

# Відображення дерева
draw_tree(root, bfs_add_edges)
draw_tree(root, dfs_add_edges)
