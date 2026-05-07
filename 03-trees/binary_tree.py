"""
Chương 3: Binary Tree & BST
=============================
Triển khai Binary Tree, BST, và các bài toán kinh điển.
"""
from collections import deque


# ============================================================
# NODE
# ============================================================

class TreeNode:
    """Node của Binary Tree."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================================
# 1. BINARY TREE — TRAVERSAL (Duyệt cây)
# ============================================================

def inorder(root):
    """Inorder: Left → Root → Right. BST → thứ tự tăng dần."""
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)


def preorder(root):
    """Preorder: Root → Left → Right. Dùng để serialize cây."""
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)


def postorder(root):
    """Postorder: Left → Right → Root. Dùng để xóa cây."""
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]


def level_order(root):
    """Level-order (BFS): Duyệt theo tầng dùng Queue."""
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result


# ============================================================
# 2. BÀI TOÁN KINH ĐIỂN TRÊN BINARY TREE
# ============================================================

def max_depth(root):
    """
    LeetCode #104 — Chiều cao cây.
    Đệ quy: height = 1 + max(height(left), height(right))
    """
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def is_symmetric(root):
    """
    LeetCode #101 — Kiểm tra cây đối xứng.
    """
    def check(left, right):
        if not left and not right:
            return True
        if not left or not right:
            return False
        return (left.val == right.val and
                check(left.left, right.right) and
                check(left.right, right.left))

    return check(root.left, root.right) if root else True


def invert_tree(root):
    """
    LeetCode #226 — Lật cây nhị phân (đảo trái/phải).
    Bài toán nổi tiếng mà Homebrew creator không giải được! 😄
    """
    if not root:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root


def diameter(root):
    """
    LeetCode #543 — Đường kính cây (đường dài nhất giữa 2 node).
    """
    result = [0]

    def height(node):
        if not node:
            return 0
        left_h = height(node.left)
        right_h = height(node.right)
        result[0] = max(result[0], left_h + right_h)
        return 1 + max(left_h, right_h)

    height(root)
    return result[0]


# ============================================================
# 3. BINARY SEARCH TREE (BST)
# ============================================================

class BST:
    """
    Binary Search Tree — Cây tìm kiếm nhị phân.
    Quy tắc: left.val < node.val < right.val
    """

    def __init__(self):
        self.root = None

    def insert(self, val):
        """Chèn giá trị — O(log n) average, O(n) worst."""
        self.root = self._insert(self.root, val)

    def _insert(self, node, val):
        if not node:
            return TreeNode(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        return node

    def search(self, val):
        """Tìm kiếm — O(log n) average."""
        return self._search(self.root, val)

    def _search(self, node, val):
        if not node or node.val == val:
            return node
        if val < node.val:
            return self._search(node.left, val)
        return self._search(node.right, val)

    def delete(self, val):
        """
        Xóa node — 3 trường hợp:
        1. Node lá: Xóa trực tiếp
        2. Có 1 con: Thay bằng con
        3. Có 2 con: Thay bằng successor (nhỏ nhất bên phải)
        """
        self.root = self._delete(self.root, val)

    def _delete(self, node, val):
        if not node:
            return None

        if val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            # Tìm thấy node cần xóa
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            # Có 2 con: tìm successor
            successor = self._find_min(node.right)
            node.val = successor.val
            node.right = self._delete(node.right, successor.val)

        return node

    def _find_min(self, node):
        """Tìm node nhỏ nhất (đi trái đến cùng)."""
        while node.left:
            node = node.left
        return node

    def inorder(self):
        """Trả về list sắp xếp tăng dần."""
        return inorder(self.root)

    def is_valid_bst(self):
        """
        LeetCode #98 — Kiểm tra cây có phải BST không.
        Dùng range checking: mỗi node phải nằm trong (min, max).
        """
        def validate(node, lo, hi):
            if not node:
                return True
            if node.val <= lo or node.val >= hi:
                return False
            return (validate(node.left, lo, node.val) and
                    validate(node.right, node.val, hi))

        return validate(self.root, float('-inf'), float('inf'))


def lowest_common_ancestor(root, p, q):
    """
    LeetCode #235 (BST version) — Tổ tiên chung gần nhất.
    Trong BST: Nếu p < root < q thì root là LCA.
    """
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
    return None


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("  BINARY TREE TRAVERSAL DEMO")
    print("=" * 50)

    # Xây cây:      1
    #              /   \
    #             2     3
    #            / \
    #           4   5
    root = TreeNode(1)
    root.left = TreeNode(2, TreeNode(4), TreeNode(5))
    root.right = TreeNode(3)

    print(f"Inorder:     {inorder(root)}")
    print(f"Preorder:    {preorder(root)}")
    print(f"Postorder:   {postorder(root)}")
    print(f"Level-order: {level_order(root)}")
    print(f"Max depth:   {max_depth(root)}")
    print(f"Diameter:    {diameter(root)}")

    print(f"\n{'=' * 50}")
    print("  BST DEMO")
    print("=" * 50)

    bst = BST()
    values = [8, 3, 10, 1, 6, 14, 4, 7, 13]
    for v in values:
        bst.insert(v)

    print(f"Insert {values}")
    print(f"Inorder (sorted): {bst.inorder()}")
    print(f"Valid BST: {bst.is_valid_bst()}")
    print(f"Search 6: {'Found' if bst.search(6) else 'Not found'}")
    print(f"Search 9: {'Found' if bst.search(9) else 'Not found'}")

    bst.delete(3)
    print(f"After delete 3: {bst.inorder()}")
