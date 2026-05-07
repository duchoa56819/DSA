# Chương 2: Cấu Trúc Dữ Liệu Tuyến Tính

## 2.1 Array (Mảng)

### Mảng là gì?
Mảng là tập hợp các phần tử **cùng kiểu**, lưu trữ **liên tiếp** trong bộ nhớ.

```
Index:    0     1     2     3     4
        ┌─────┬─────┬─────┬─────┬─────┐
Array:  │  10 │  20 │  30 │  40 │  50 │
        └─────┴─────┴─────┴─────┴─────┘
```

### Truy cập array[i] là O(1) vì:
`địa chỉ = base_address + i * kích_thước_phần_tử`

### Độ phức tạp:

| Thao tác | Array | Dynamic Array |
|----------|-------|---------------|
| Truy cập `arr[i]` | O(1) | O(1) |
| Tìm kiếm | O(n) | O(n) |
| Chèn cuối | N/A | O(1) amortized |
| Chèn đầu/giữa | O(n) | O(n) |
| Xóa | O(n) | O(n) |

---

## 2.2 Linked List

Mỗi node chứa **data** + **con trỏ đến node kế**.

```
Singly: [1|→] → [2|→] → [3|→] → [4|None]
Doubly: None←[←|1|→]↔[←|2|→]↔[←|3|→]→None
```

### So sánh Array vs Linked List:

| Tiêu chí | Array | Linked List |
|----------|-------|-------------|
| Truy cập ngẫu nhiên | O(1) ✅ | O(n) ❌ |
| Chèn/Xóa đầu | O(n) | O(1) ✅ |
| Cache friendly | ✅ | ❌ |

---

## 2.3 Stack — LIFO (Last In, First Out)
- `push(x)`, `pop()`, `peek()` — tất cả O(1)
- Ứng dụng: Undo/Redo, Call Stack, DFS, Kiểm tra ngoặc

## 2.4 Queue — FIFO (First In, First Out)
- `enqueue(x)`, `dequeue()` — O(1)
- Biến thể: Deque, Priority Queue, Circular Queue
- Ứng dụng: BFS, Task scheduling, Message queue

## 📝 Bài Tập
1. Reverse String bằng Stack
2. Valid Parentheses (LeetCode #20)
3. Implement Queue using 2 Stacks (LeetCode #232)
4. Reverse Linked List (LeetCode #206)
