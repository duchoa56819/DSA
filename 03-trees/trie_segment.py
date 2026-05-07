"""
Chương 3: Trie (Prefix Tree) & Segment Tree
=============================================
"""


# ============================================================
# 1. TRIE — Prefix Tree
# ============================================================

class TrieNode:
    def __init__(self):
        self.children = {}      # {char: TrieNode}
        self.is_end = False     # Đánh dấu kết thúc từ


class Trie:
    """
    Trie — Cây tiền tố (LeetCode #208)

    Dùng cho: Autocomplete, Spell check, IP routing, Word games

    Ví dụ lưu ["cat", "car", "card"]:
          (root)
            |
            c
            |
            a
           / \
          t*  r*
              |
              d*
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """Chèn từ vào Trie — O(len(word))."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        """Tìm từ chính xác — O(len(word))."""
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        """Kiểm tra có từ nào bắt đầu bằng prefix — O(len(prefix))."""
        return self._find_node(prefix) is not None

    def _find_node(self, prefix):
        """Tìm node tại cuối prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def autocomplete(self, prefix):
        """Trả về tất cả từ bắt đầu bằng prefix."""
        node = self._find_node(prefix)
        if not node:
            return []
        results = []
        self._dfs(node, prefix, results)
        return results

    def _dfs(self, node, current, results):
        if node.is_end:
            results.append(current)
        for char, child in sorted(node.children.items()):
            self._dfs(child, current + char, results)


# ============================================================
# 2. SEGMENT TREE — Cây phân đoạn
# ============================================================

class SegmentTree:
    """
    Segment Tree — Truy vấn đoạn trong O(log n).

    Bài toán: Cho mảng, hỗ trợ:
    1. query(l, r): Tính tổng đoạn [l, r]
    2. update(i, val): Cập nhật arr[i] = val

    Cả 2 thao tác đều O(log n)!

    Ví dụ: arr = [1, 3, 5, 7, 9, 11]

    Cây:          36
                /     \
              9        27
            /  \     /   \
           4    5   16   11
          / \      / \
         1   3    7   9
    """

    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)  # Cây lưu trong mảng
        self._build(arr, 1, 0, self.n - 1)

    def _build(self, arr, node, start, end):
        """Xây cây — O(n)."""
        if start == end:
            self.tree[node] = arr[start]
            return
        mid = (start + end) // 2
        self._build(arr, 2 * node, start, mid)        # Con trái
        self._build(arr, 2 * node + 1, mid + 1, end)  # Con phải
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, l, r):
        """Truy vấn tổng đoạn [l, r] — O(log n)."""
        return self._query(1, 0, self.n - 1, l, r)

    def _query(self, node, start, end, l, r):
        if r < start or end < l:     # Ngoài phạm vi
            return 0
        if l <= start and end <= r:  # Nằm hoàn toàn trong
            return self.tree[node]
        mid = (start + end) // 2
        left_sum = self._query(2 * node, start, mid, l, r)
        right_sum = self._query(2 * node + 1, mid + 1, end, l, r)
        return left_sum + right_sum

    def update(self, idx, val):
        """Cập nhật arr[idx] = val — O(log n)."""
        self._update(1, 0, self.n - 1, idx, val)

    def _update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if idx <= mid:
            self._update(2 * node, start, mid, idx, val)
        else:
            self._update(2 * node + 1, mid + 1, end, idx, val)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("  TRIE DEMO")
    print("=" * 50)

    trie = Trie()
    words = ["apple", "app", "application", "apply", "banana", "band", "bat"]
    for w in words:
        trie.insert(w)
    print(f"Inserted: {words}")

    print(f'\nsearch("apple"):     {trie.search("apple")}')     # True
    print(f'search("app"):       {trie.search("app")}')         # True
    print(f'search("ap"):        {trie.search("ap")}')          # False
    print(f'starts_with("app"):  {trie.starts_with("app")}')    # True
    print(f'autocomplete("app"): {trie.autocomplete("app")}')
    print(f'autocomplete("ba"):  {trie.autocomplete("ba")}')

    print(f"\n{'=' * 50}")
    print("  SEGMENT TREE DEMO")
    print("=" * 50)

    arr = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(arr)
    print(f"Array: {arr}")
    print(f"Sum [1, 3] = {st.query(1, 3)}")   # 3+5+7 = 15
    print(f"Sum [0, 5] = {st.query(0, 5)}")   # 1+3+5+7+9+11 = 36

    st.update(2, 10)  # arr[2] = 10 (was 5)
    print(f"\nAfter update arr[2] = 10:")
    print(f"Sum [1, 3] = {st.query(1, 3)}")   # 3+10+7 = 20
