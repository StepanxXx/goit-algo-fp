"""
Module for LinkedList implementation and sorting algorithms.
"""


class Node:
    """
    Represents a node in a singly linked list.
    """
    def __init__(self, data=None):
        """
        Initialize the Node with data and a pointer to the next node.
        """
        self.data = data
        self.next = None


class LinkedList:
    """
    Represents a singly linked list.
    """
    def __init__(self, data: list = None):
        """
        Initialize the LinkedList, optionally with a list of data.
        """
        self.head = None
        if data:
            for i in data:
                self.insert_at_beginning(i)

    def insert_at_end(self, data):
        """
        Insert a new node with the given data at the end of the list.
        """
        if not self.head:
            self.head = Node(data)
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = Node(data)

    def insert_at_beginning(self, data):
        """
        Insert a new node with the given data at the beginning of the list.
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_after(self, prev_node: Node, data):
        """
        Insert a new node with the given data after the specified prev_node.
        """
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def search_element(self, data) -> Node | None:
        """
        Search for a node containing the specific data.
        """
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def delete_node(self, key: int):
        """
        Delete the first node with the specified key (data).
        """
        cur = self.head
        if cur and cur.data == key:
            self.head = cur.next
            cur = None
            return
        prev = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next
        if cur is None:
            return
        prev.next = cur.next
        cur = None

    def print_list(self):
        """
        Print the elements of the list.
        """
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print()

    def reverse(self):
        """
        Reverse the linked list in place.
        """
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def sort_by_bubble(self, reverse=False):
        """
        Sort the linked list using bubble sort algorithm.
        """
        step = 1
        last_step = float('inf')
        while step < last_step:
            prev = self.head
            next_node = self.head.next
            while prev and next_node and step < last_step:
                if (not reverse and next_node.data < prev.data) \
                        or (reverse and next_node.data > prev.data):
                    prev.data, next_node.data = next_node.data, prev.data
                prev, next_node = prev.next, next_node.next
                step += 1
            last_step, step = step - 1, 1

    def sort_by_insertion(self, reverse=False):
        """
        Sort the linked list using insertion sort algorithm.
        """
        if self.head is None or self.head.next is None:
            return

        sorted_head = None
        current = self.head

        while current:
            next_node = current.next
            if sorted_head is None:
                sorted_head = current
                sorted_head.next = None
            else:
                # Determine insertion point
                if not reverse:
                    if current.data < sorted_head.data:
                        current.next = sorted_head
                        sorted_head = current
                    else:
                        search = sorted_head
                        while search.next and search.next.data <= current.data:
                            search = search.next
                        current.next = search.next
                        search.next = current
                else:
                    if current.data > sorted_head.data:
                        current.next = sorted_head
                        sorted_head = current
                    else:
                        search = sorted_head
                        while search.next and search.next.data >= current.data:
                            search = search.next
                        current.next = search.next
                        search.next = current
            current = next_node

        self.head = sorted_head

    def sort_by_merge(self, reverse=False):
        """
        Sort the linked list using merge sort algorithm.
        """
        self.head = self._merge_sort(self.head, reverse)

    def _merge_sort(self, head, reverse):
        """
        Recursive helper function for merge sort.
        """
        if head is None or head.next is None:
            return head

        middle = self._get_middle(head)
        next_to_middle = middle.next
        middle.next = None

        left = self._merge_sort(head, reverse)
        right = self._merge_sort(next_to_middle, reverse)

        return self.sorted_merge(left, right, reverse)

    def _get_middle(self, head):
        """
        Find the middle node of the linked list.
        """
        if head is None:
            return head
        slow = head
        fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next
        return slow

    def sorted_merge(self, a: Node, b: Node, reverse=False) -> Node:
        """
        Merge two sorted linked lists.
        """
        if a is None:
            return b
        if b is None:
            return a

        if not reverse:
            if a.data <= b.data:
                result = a
                result.next = self.sorted_merge(a.next, b, reverse)
            else:
                result = b
                result.next = self.sorted_merge(a, b.next, reverse)
        else:
            if a.data >= b.data:
                result = a
                result.next = self.sorted_merge(a.next, b, reverse)
            else:
                result = b
                result.next = self.sorted_merge(a, b.next, reverse)
        return result

    def merge_sorted_lists(self, other_list: 'LinkedList',
                           reverse: bool = False) -> None:
        """
        Merge another sorted LinkedList into this one.
        """
        merged_head = self.sorted_merge(self.head, other_list.head, reverse)
        self.head = merged_head


if __name__ == "__main__":

    llist = LinkedList([25, 20, 5, 10, 15])

    print("Зв'язний список:")
    llist.print_list()

    llist.reverse()
    print("\nЗв'язний список після реверсування:")
    llist.print_list()

    # Сортування бульбашкою
    print("\nЗв'язний список після сортування бульбашкою:")
    llist.sort_by_bubble()
    llist.print_list()

    # Сортування вставками
    print("\nСортування вставками (reverse=True):")
    llist.insert_at_beginning(30)
    llist.insert_at_end(5)  # Add unsorted elements
    print("До сортування:")
    llist.print_list()
    llist.sort_by_insertion(reverse=True)
    print("Після сортування:")
    llist.print_list()

    # Сортування злиттям
    print("\nСортування злиттям:")
    llist.insert_at_beginning(50)
    llist.insert_at_end(1)
    print("До сортування:")
    llist.print_list()
    llist.sort_by_merge()
    print("Після сортування:")
    llist.print_list()

    # Об'єднання двох відсортованих списків
    print("\nОб'єднання двох відсортованих списків:")
    llist1 = LinkedList([50, 30, 10])
    llist2 = LinkedList([80, 60, 40, 20])

    print("Список 1:")
    llist1.print_list()
    print("Список 2:")
    llist2.print_list()

    llist1.merge_sorted_lists(llist2)
    print("Об'єднаний список:")
    llist1.print_list()
