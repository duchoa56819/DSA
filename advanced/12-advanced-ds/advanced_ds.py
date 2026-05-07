"""
Chương 12: Cấu Trúc Dữ Liệu Nâng Cao
========================================
AVL Tree, Fenwick Tree (BIT), Skip List, LRU Cache.
"""
import random


# ============================================================
# 1. AVL TREE — Self-Balancing BST
# ============================================================

class AVLNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """
    AVL Tree — BST tự cân bằng.

    Tại mọi node: |height(left) - height(right)| <= 1
    Nếu vi phạm → xoay (rotation) để cân bằng lại.

    Mọi thao tác O(log n) worst case (khác BST thường có thể O(n)).

    4 loại xoay:
    - Left Rotation (LL): Right-heavy
    - Right Rotation (RR): Left-heavy
    - Left-Right (LR): Left child right-heavy
    - Right-Left (RL): Right child left-heavy
    """

    def _height(self, node):
        return node.height if node else 0

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, y):
        """
        Right Rotation:
            y           x
           / \         / \
          x   C  →    A   y
         / \             / \
        A   B           B   C
        """
        x = y.left
        B = x.right
        x.right = y
        y.left = B
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        """
        Left Rotation:
          x             y
         / \           / \
        A   y    →    x   C
           / \       / \
          B   C     A   B
        """
        y = x.right
        B = y.left
        y.left = x
        x.right = B
        self._update_height(x)
        self._update_height(y)
        return y

    def insert(self, root, val):
        """Chèn + tự cân bằng — O(log n)."""
        if not root:
            return AVLNode(val)
        if val < root.val:
            root.left = self.insert(root.left, val)
        elif val > root.val:
            root.right = self.insert(root.right, val)
        else:
            return root  # Không cho trùng

        self._update_height(root)
        bf = self._balance_factor(root)

        # Left-heavy
        if bf > 1:
            if val < root.left.val:  # LL
                return self._rotate_right(root)
            else:  # LR
                root.left = self._rotate_left(root.left)
                return self._rotate_right(root)

        # Right-heavy
        if bf < -1:
            if val > root.right.val:  # RR
                return self._rotate_left(root)
            else:  # RL
                root.right = self._rotate_right(root.right)
                return self._rotate_left(root)

        return root

    def inorder(self, root):
        if not root:
            return []
        return self.inorder(root.left) + [root.val] + self.inorder(root.right)


# ============================================================
# 2. FENWICK TREE (Binary Indexed Tree — BIT)
# ============================================================

class FenwickTree:
    """
    Fenwick Tree — Hỗ trợ:
    1. Point update: arr[i] += val    — O(log n)
    2. Prefix sum: sum(arr[0..i])     — O(log n)
    3. Range sum: sum(arr[l..r])      — O(log n)

    Đơn giản hơn Segment Tree, hằng số nhỏ hơn, nhưng ít linh hoạt hơn.

    Trick cốt lõi: i & (-i) = bit thấp nhất của i
    - Ví dụ: 12 (1100) & -12 (0100) = 4
    - Update: đi lên bằng += lowbit
    - Query: đi xuống bằng -= lowbit
    """

    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)  # 1-indexed

    def update(self, i, delta):
        """Cộng delta vào vị trí i — O(log n)."""
        i += 1  # Convert sang 1-indexed
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)  # Lên node cha

    def prefix_sum(self, i):
        """Tổng từ 0 đến i — O(log n)."""
        i += 1
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & (-i)  # Xuống node trước
        return total

    def range_sum(self, l, r):
        """Tổng từ l đến r — O(log n)."""
        if l == 0:
            return self.prefix_sum(r)
        return self.prefix_sum(r) - self.prefix_sum(l - 1)

    @classmethod
    def from_array(cls, arr):
        """Xây Fenwick Tree từ mảng — O(n log n)."""
        ft = cls(len(arr))
        for i, val in enumerate(arr):
            ft.update(i, val)
        return ft


# ============================================================
# 3. SKIP LIST — O(log n) average
# ============================================================

class SkipNode:
    def __init__(self, val, level):
        self.val = val
        self.forward = [None] * (level + 1)


class SkipList:
    """
    Skip List — Cấu trúc dữ liệu xác suất, thay thế cây cân bằng.

    Ý tưởng: Linked list nhiều tầng. Tầng trên là "express lane".

    Level 3:  Head ─────────────────────→ 9 ──→ None
    Level 2:  Head ──→ 3 ────────────→ 9 ──→ None
    Level 1:  Head ──→ 3 ──→ 5 ──→ 7 ──→ 9 ──→ None
    Level 0:  Head ──→ 1 ──→ 3 ──→ 5 ──→ 7 ──→ 9 ──→ None

    Search/Insert/Delete: O(log n) average
    Dùng trong: Redis sorted set, LevelDB.
    """
    MAX_LEVEL = 16

    def __init__(self):
        self.header = SkipNode(-1, self.MAX_LEVEL)
        self.level = 0

    def _random_level(self):
        """Mỗi node có 50% cơ hội lên tầng cao hơn."""
        lvl = 0
        while random.random() < 0.5 and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def insert(self, val):
        """Chèn giá trị — O(log n) average."""
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].val < val:
                current = current.forward[i]
            update[i] = current

        new_level = self._random_level()
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level

        new_node = SkipNode(val, new_level)
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def search(self, val):
        """Tìm kiếm — O(log n) average."""
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].val < val:
                current = current.forward[i]
        current = current.forward[0]
        return current is not None and current.val == val

    def to_list(self):
        result = []
        node = self.header.forward[0]
        while node:
            result.append(node.val)
            node = node.forward[0]
        return result


# ============================================================
# 4. LRU CACHE — O(1) (LeetCode #146)
# ============================================================

class LRUNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class LRUCache:
    """
    LRU Cache — Least Recently Used Cache.

    Kết hợp HashMap + Doubly Linked List.
    - get/put đều O(1)!
    - Khi đầy, xóa phần tử LÂU NHẤT không dùng.

    Ứng dụng: Browser cache, OS page replacement, CDN.
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key → LRUNode
        # Dummy head/tail
        self.head = LRUNode()
        self.tail = LRUNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        """Lấy giá trị — O(1). Đưa lên đầu (recently used)."""
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.val
        return -1

    def put(self, key, value):
        """Thêm/cập nhật — O(1). Nếu đầy, xóa LRU (cuối list)."""
        if key in self.cache:
            self._remove(self.cache[key])
        node = LRUNode(key, value)
        self._add_to_front(node)
        self.cache[key] = node
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  AVL TREE DEMO")
    print("=" * 55)

    avl = AVLTree()
    root = None
    values = [10, 20, 30, 40, 50, 25]
    for v in values:
        root = avl.insert(root, v)
    print(f"Insert {values}")
    print(f"Inorder: {avl.inorder(root)}")
    print(f"Root: {root.val} (height: {root.height})")

    print(f"\n{'=' * 55}")
    print("  FENWICK TREE (BIT) DEMO")
    print("=" * 55)

    arr = [1, 3, 5, 7, 9, 11]
    ft = FenwickTree.from_array(arr)
    print(f"Array: {arr}")
    print(f"Prefix sum [0..2]: {ft.prefix_sum(2)}")  # 1+3+5=9
    print(f"Range sum [1..4]:  {ft.range_sum(1, 4)}")  # 3+5+7+9=24
    ft.update(2, 5)  # arr[2] += 5 → 10
    print(f"After arr[2] += 5:")
    print(f"Prefix sum [0..2]: {ft.prefix_sum(2)}")  # 1+3+10=14

    print(f"\n{'=' * 55}")
    print("  SKIP LIST DEMO")
    print("=" * 55)

    sl = SkipList()
    for v in [3, 6, 7, 9, 12, 19, 17, 26, 21, 25]:
        sl.insert(v)
    print(f"Skip List: {sl.to_list()}")
    print(f"Search 19: {sl.search(19)}")
    print(f"Search 15: {sl.search(15)}")

    print(f"\n{'=' * 55}")
    print("  LRU CACHE DEMO")
    print("=" * 55)

    cache = LRUCache(3)
    cache.put(1, "A")
    cache.put(2, "B")
    cache.put(3, "C")
    print(f"Cache: 1=A, 2=B, 3=C")
    print(f"get(1): {cache.get(1)}")  # A (đưa 1 lên đầu)
    cache.put(4, "D")  # Đầy → xóa LRU (key=2)
    print(f"put(4, D) → evict LRU")
    print(f"get(2): {cache.get(2)}")  # -1 (đã bị xóa)
    print(f"get(3): {cache.get(3)}")  # C
