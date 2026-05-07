"""
Chương 2: Linked List — Danh sách liên kết
===========================================
Triển khai đầy đủ Singly & Doubly Linked List.
"""


# ============================================================
# 1. SINGLY LINKED LIST
# ============================================================

class ListNode:
    """Node của Singly Linked List."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class SinglyLinkedList:
    """
    Singly Linked List — Danh sách liên kết đơn.
    Mỗi node trỏ đến node kế tiếp.
    """

    def __init__(self):
        self.head = None
        self.size = 0

    def prepend(self, val):
        """Chèn vào đầu — O(1)."""
        new_node = ListNode(val, self.head)
        self.head = new_node
        self.size += 1

    def append(self, val):
        """Chèn vào cuối — O(n) vì phải duyệt đến cuối."""
        new_node = ListNode(val)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def insert(self, index, val):
        """Chèn vào vị trí index — O(n)."""
        if index <= 0:
            self.prepend(val)
            return
        if index >= self.size:
            self.append(val)
            return

        new_node = ListNode(val)
        current = self.head
        for _ in range(index - 1):
            current = current.next
        new_node.next = current.next
        current.next = new_node
        self.size += 1

    def delete(self, val):
        """Xóa node có giá trị val — O(n)."""
        if not self.head:
            return

        # Xóa head
        if self.head.val == val:
            self.head = self.head.next
            self.size -= 1
            return

        current = self.head
        while current.next and current.next.val != val:
            current = current.next

        if current.next:
            current.next = current.next.next
            self.size -= 1

    def search(self, val):
        """Tìm kiếm — O(n)."""
        current = self.head
        index = 0
        while current:
            if current.val == val:
                return index
            current = current.next
            index += 1
        return -1

    def reverse(self):
        """
        Đảo ngược linked list — O(n) time, O(1) space.
        LeetCode #206 — Bài kinh điển trong phỏng vấn!

        Ý tưởng: Đảo chiều mũi tên từng node.
        Trước: 1 → 2 → 3 → None
        Sau:   None ← 1 ← 2 ← 3
        """
        prev = None
        current = self.head
        while current:
            next_temp = current.next   # Lưu node kế
            current.next = prev        # Đảo mũi tên
            prev = current             # Tiến prev
            current = next_temp        # Tiến current
        self.head = prev

    def has_cycle(self):
        """
        Phát hiện vòng lặp — Floyd's Cycle Detection (Tortoise & Hare)
        LeetCode #141

        Dùng 2 con trỏ: slow (1 bước) và fast (2 bước).
        Nếu có cycle, chúng sẽ gặp nhau.
        """
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False

    def find_middle(self):
        """
        Tìm node giữa — O(n) time, O(1) space.
        LeetCode #876

        Slow đi 1 bước, Fast đi 2 bước.
        Khi Fast đến cuối, Slow ở giữa!
        """
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow.val if slow else None

    def to_list(self):
        """Chuyển linked list thành Python list."""
        result = []
        current = self.head
        while current:
            result.append(current.val)
            current = current.next
        return result

    def __str__(self):
        values = self.to_list()
        return " → ".join(map(str, values)) + " → None"

    def __len__(self):
        return self.size


# ============================================================
# 2. DOUBLY LINKED LIST
# ============================================================

class DoublyNode:
    """Node của Doubly Linked List."""
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next


class DoublyLinkedList:
    """
    Doubly Linked List — Danh sách liên kết đôi.
    Mỗi node trỏ đến cả node trước VÀ sau.
    Ưu điểm: Duyệt ngược dễ, xóa node O(1) nếu có con trỏ.
    """

    def __init__(self):
        # Dùng sentinel nodes (dummy head/tail) để code gọn hơn
        self.head = DoublyNode(0)  # dummy head
        self.tail = DoublyNode(0)  # dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def _add_after(self, node, val):
        """Thêm node mới SAU node cho trước — O(1)."""
        new_node = DoublyNode(val)
        new_node.prev = node
        new_node.next = node.next
        node.next.prev = new_node
        node.next = new_node
        self.size += 1
        return new_node

    def _remove(self, node):
        """Xóa node — O(1) khi có con trỏ."""
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
        return node.val

    def prepend(self, val):
        """Chèn đầu — O(1)."""
        self._add_after(self.head, val)

    def append(self, val):
        """Chèn cuối — O(1) nhờ tail pointer!"""
        self._add_after(self.tail.prev, val)

    def pop_front(self):
        """Xóa đầu — O(1)."""
        if self.size == 0:
            raise IndexError("List is empty")
        return self._remove(self.head.next)

    def pop_back(self):
        """Xóa cuối — O(1)."""
        if self.size == 0:
            raise IndexError("List is empty")
        return self._remove(self.tail.prev)

    def to_list(self):
        result = []
        current = self.head.next
        while current != self.tail:
            result.append(current.val)
            current = current.next
        return result

    def __str__(self):
        values = self.to_list()
        return "None ↔ " + " ↔ ".join(map(str, values)) + " ↔ None"

    def __len__(self):
        return self.size


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("  SINGLY LINKED LIST DEMO")
    print("=" * 50)

    sll = SinglyLinkedList()
    for val in [1, 2, 3, 4, 5]:
        sll.append(val)
    print(f"Ban đầu:    {sll}")

    sll.prepend(0)
    print(f"Prepend 0:  {sll}")

    sll.delete(3)
    print(f"Delete 3:   {sll}")

    print(f"Middle:     {sll.find_middle()}")
    print(f"Search(4):  index {sll.search(4)}")

    sll.reverse()
    print(f"Reversed:   {sll}")

    print(f"\n{'=' * 50}")
    print("  DOUBLY LINKED LIST DEMO")
    print("=" * 50)

    dll = DoublyLinkedList()
    for val in [1, 2, 3, 4, 5]:
        dll.append(val)
    print(f"Ban đầu:    {dll}")

    dll.prepend(0)
    print(f"Prepend 0:  {dll}")

    dll.pop_back()
    print(f"Pop back:   {dll}")

    dll.pop_front()
    print(f"Pop front:  {dll}")
