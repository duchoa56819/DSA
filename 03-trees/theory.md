# Chương 3: Cây (Trees)

## 3.1 Cây là gì?

Cây là cấu trúc dữ liệu **phân cấp** (hierarchical), gồm các **node** nối với nhau.

```
Thuật ngữ:
            1          ← Root (gốc)
          /   \
         2     3       ← Internal nodes (node trong)
        / \     \
       4   5     6     ← Leaves (lá) — không có con
```

- **Root**: Node trên cùng (không có cha)
- **Parent/Child**: Node cha/con
- **Leaf**: Node không có con
- **Height**: Số cạnh từ root đến lá xa nhất
- **Depth**: Số cạnh từ node đến root
- **Subtree**: Cây con tạo bởi 1 node và tất cả hậu duệ

---

## 3.2 Binary Tree (Cây nhị phân)

Mỗi node có **tối đa 2 con** (left, right).

### Các loại Binary Tree:
- **Full**: Mỗi node có 0 hoặc 2 con
- **Complete**: Đầy từ trái sang phải, chỉ tầng cuối có thể thiếu
- **Perfect**: Mọi tầng đều đầy đủ
- **Balanced**: Chiều cao = O(log n)

### Cách duyệt (Traversal):

```
       1
      / \
     2   3
    / \
   4   5

Inorder   (Left-Root-Right):  4, 2, 5, 1, 3  ← BST sẽ cho thứ tự tăng dần!
Preorder  (Root-Left-Right):  1, 2, 4, 5, 3
Postorder (Left-Right-Root):  4, 5, 2, 3, 1
Level-order (BFS):            1, 2, 3, 4, 5
```

---

## 3.3 Binary Search Tree (BST)

**Quy tắc**: Left < Root < Right (cho mọi node)

```
       8
      / \
     3   10
    / \    \
   1   6   14
      / \  /
     4  7 13
```

| Thao tác | Average | Worst (skewed) |
|----------|---------|----------------|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |

→ Worst case xảy ra khi cây bị **lệch** (thành linked list!)

---

## 3.4 AVL Tree (Self-Balancing BST)

- **Balance Factor** = height(left) - height(right)
- Luôn duy trì |BF| ≤ 1 cho mọi node
- Dùng **rotation** (xoay) để cân bằng
- Đảm bảo mọi thao tác O(log n) worst case

### 4 loại rotation:
1. **Left Rotation**: Khi right-heavy
2. **Right Rotation**: Khi left-heavy
3. **Left-Right**: Left child right-heavy
4. **Right-Left**: Right child left-heavy

---

## 3.5 Trie (Prefix Tree)

Cây lưu trữ **chuỗi ký tự**, dùng cho autocomplete, spell check.

```
Lưu: ["cat", "car", "card", "dog"]

        (root)
       /      \
      c        d
      |        |
      a        o
     / \       |
    t   r      g*
    *   |
        d*
(* = kết thúc từ)
```

---

## 3.6 Segment Tree

Cây hỗ trợ **truy vấn đoạn** (range query) trong O(log n).
Ví dụ: Tìm tổng/min/max của đoạn [l, r] trong mảng.

---

## 📝 Bài Tập
1. Maximum Depth of Binary Tree (LeetCode #104)
2. Validate BST (LeetCode #98)
3. Lowest Common Ancestor (LeetCode #236)
4. Implement Trie (LeetCode #208)
5. Invert Binary Tree (LeetCode #226)
