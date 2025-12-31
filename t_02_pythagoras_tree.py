"""
This module recursively draws a Pythagoras tree using Matplotlib.
"""
import math
import matplotlib.pyplot as plt


def get_line_length(p1, p2):
    """Calculates the Euclidean distance between two points p1 and p2."""
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

def get_next_point(p1, p2, angle):
    """
    Calculates the next point in the tree branch based on the previous line segment
    and the given angle, assuming a split angle that preserves the Pythagoras tree geometry.
    """
    line_length = get_line_length(p1, p2) * math.sqrt(2) / 2
    radian_angle = math.radians(angle)
    x = p2[0] + line_length * math.sin(radian_angle)
    y = p2[1] + line_length * math.cos(radian_angle)
    return [x, y]

def pythagoras_tree(p1, p2, depth, angle = 0):
    """
    Recursively draws the Pythagoras tree.
    
    Args:
        p1: Start point of the current branch segment.
        p2: End point of the current branch segment.
        depth: Current recursion depth.
        angle: Current angle of the branch.
    """
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color='blue')
    if depth > 0:
        left_p1 = p2
        left_p2 = get_next_point(p1, p2, angle + 45)
        right_p1 = p2
        right_p2 = get_next_point(p1, p2, angle - 45)
        pythagoras_tree(left_p1, left_p2, depth - 1, angle + 45)
        pythagoras_tree(right_p1, right_p2, depth -1, angle - 45)

def draw_pythagoras_tree(size = 400, depth = 5):
    """
    Initializes the plot and starts the recursive drawing of the Pythagoras tree.
    
    Args:
        size: Size parameter (used to determine initial trunk size).
        depth: Maximum recursion depth.
    """
    pythagoras_tree(p1 = (size/2, 10), p2 = (size/2, 20), depth = depth)
    plt.axis('off')
    plt.show()

def main():
    """Main function to handle user input and draw the tree."""
    try:
        depth = int(input("Enter the depth of the tree: "))
        draw_pythagoras_tree(depth = depth if depth > 0 else 5)
    except ValueError:
        draw_pythagoras_tree()

if __name__ == '__main__':
    main()
