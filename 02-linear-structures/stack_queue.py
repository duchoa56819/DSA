"""
Chương 2: Stack & Queue
========================
Triển khai Stack, Queue, và các bài toán ứng dụng.
"""
from collections import deque


# ============================================================
# 1. STACK — LIFO (Last In, First Out)
# ============================================================

class Stack:
    """Stack dùng Python list — tất cả thao tác O(1)."""

    def __init__(self):
        self._items = []

    def push(self, item):
        """Thêm vào đỉnh."""
        self._items.append(item)

    def pop(self):
        """Lấy ra và xóa đỉnh."""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items.pop()

    def peek(self):
        """Xem đỉnh (không xóa)."""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __str__(self):
        return f"Stack(top→bottom): {self._items[::-1]}"


# ============================================================
# BÀI TOÁN 1: Valid Parentheses (LeetCode #20)
# ============================================================

def is_valid_parentheses(s):
    """
    Kiểm tra chuỗi ngoặc có hợp lệ không.
    Input: "({[]})" → True
    Input: "([)]"   → False

    Ý tưởng:
    - Gặp ngoặc mở → push vào stack
    - Gặp ngoặc đóng → pop và kiểm tra có khớp không
    """
    stack = []
    matching = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in '({[':
            stack.append(char)
        elif char in ')}]':
            if not stack or stack[-1] != matching[char]:
                return False
            stack.pop()

    return len(stack) == 0


# ============================================================
# BÀI TOÁN 2: Min Stack (LeetCode #155)
# ============================================================

class MinStack:
    """
    Stack có thể trả về giá trị nhỏ nhất trong O(1).

    Trick: Dùng 2 stack — 1 stack chính + 1 stack lưu min.
    """

    def __init__(self):
        self.stack = []
        self.min_stack = []  # Lưu min tại mỗi trạng thái

    def push(self, val):
        self.stack.append(val)
        # min_stack lưu min hiện tại
        current_min = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(current_min)

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def get_min(self):
        """Trả về min trong O(1)!"""
        return self.min_stack[-1]


# ============================================================
# 2. QUEUE — FIFO (First In, First Out)
# ============================================================

class Queue:
    """Queue dùng collections.deque — O(1) cho cả 2 đầu."""

    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        """Thêm vào cuối."""
        self._items.append(item)

    def dequeue(self):
        """Lấy từ đầu."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items.popleft()

    def front(self):
        """Xem đầu hàng."""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __str__(self):
        return f"Queue(front→rear): {list(self._items)}"


# ============================================================
# BÀI TOÁN 3: Queue from 2 Stacks (LeetCode #232)
# ============================================================

class QueueFromStacks:
    """
    Triển khai Queue bằng 2 Stacks.

    Ý tưởng:
    - stack_in: nhận input (push)
    - stack_out: xuất output (pop)
    - Khi stack_out rỗng, đổ toàn bộ stack_in sang
    - Amortized O(1) cho mỗi thao tác!
    """

    def __init__(self):
        self.stack_in = []   # Nhận dữ liệu vào
        self.stack_out = []  # Xuất dữ liệu ra

    def enqueue(self, x):
        self.stack_in.append(x)

    def _transfer(self):
        """Đổ stack_in sang stack_out (đảo ngược thứ tự)."""
        if not self.stack_out:
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())

    def dequeue(self):
        self._transfer()
        return self.stack_out.pop()

    def front(self):
        self._transfer()
        return self.stack_out[-1]

    def is_empty(self):
        return not self.stack_in and not self.stack_out


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("  STACK DEMO")
    print("=" * 50)

    s = Stack()
    for val in [1, 2, 3, 4, 5]:
        s.push(val)
    print(s)
    print(f"Pop: {s.pop()}")
    print(f"Peek: {s.peek()}")
    print(s)

    print(f"\n--- Valid Parentheses ---")
    tests = ["({}[])", "([)]", "{[]}", "((()))", ")("]
    for t in tests:
        print(f'  "{t}" → {is_valid_parentheses(t)}')

    print(f"\n--- Min Stack ---")
    ms = MinStack()
    for val in [5, 3, 7, 1, 4]:
        ms.push(val)
        print(f"  Push {val}, min = {ms.get_min()}")
    ms.pop()  # remove 4
    ms.pop()  # remove 1
    print(f"  After 2 pops, min = {ms.get_min()}")

    print(f"\n{'=' * 50}")
    print("  QUEUE DEMO")
    print("=" * 50)

    q = Queue()
    for val in [1, 2, 3, 4, 5]:
        q.enqueue(val)
    print(q)
    print(f"Dequeue: {q.dequeue()}")
    print(f"Front: {q.front()}")
    print(q)

    print(f"\n--- Queue from 2 Stacks ---")
    qs = QueueFromStacks()
    for val in [1, 2, 3]:
        qs.enqueue(val)
        print(f"  Enqueue {val}")
    for _ in range(3):
        print(f"  Dequeue → {qs.dequeue()}")
