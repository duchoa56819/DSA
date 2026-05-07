# Chương 1: Phân Tích Độ Phức Tạp (Complexity Analysis)

## 1.1 Tại sao cần phân tích độ phức tạp?

Khi viết chương trình, ta cần trả lời 2 câu hỏi:
- **Chương trình chạy nhanh hay chậm?** → Time Complexity (Độ phức tạp thời gian)
- **Chương trình tốn bao nhiêu bộ nhớ?** → Space Complexity (Độ phức tạp không gian)

> 💡 **Ví dụ thực tế**: Bạn có 1 triệu users. Thuật toán O(n²) sẽ cần 10¹² phép tính
> (chạy hàng giờ), trong khi O(n log n) chỉ cần ~20 triệu phép tính (chạy trong vài giây).

---

## 1.2 Ký hiệu Big O

Big O mô tả **giới hạn trên** (worst case) của tốc độ tăng trưởng khi input lớn dần.

### Các quy tắc tính Big O:

1. **Bỏ hằng số**: O(2n) → O(n)
2. **Bỏ số hạng nhỏ hơn**: O(n² + n) → O(n²)
3. **Quan tâm worst case**: Nếu best case O(1), worst case O(n) → ghi O(n)

### Bảng xếp hạng (từ nhanh → chậm):

```
O(1)        Hằng số       ████                    Truy cập array[i]
O(log n)    Logarit       ████████                Binary Search
O(n)        Tuyến tính    ████████████            Duyệt mảng
O(n log n)  Log tuyến tính ████████████████       Merge Sort
O(n²)       Bình phương   ████████████████████    Bubble Sort
O(2^n)      Mũ            ████████████████████████ Fibonacci đệ quy
O(n!)       Giai thừa     ████████████████████████████ Liệt kê hoán vị
```

### Minh họa với n = 1000:

| Big O | Số phép tính | Thời gian (~) |
|-------|-------------|---------------|
| O(1) | 1 | Tức thì |
| O(log n) | ~10 | Tức thì |
| O(n) | 1,000 | Tức thì |
| O(n log n) | ~10,000 | Tức thì |
| O(n²) | 1,000,000 | ~1 giây |
| O(2^n) | 10^301 | Vĩnh viễn ♾️ |

---

## 1.3 Cách phân tích Time Complexity

### Quy tắc 1: Vòng lặp đơn → O(n)

```python
def sum_array(arr):
    total = 0                    # O(1)
    for x in arr:                # O(n) — lặp n lần
        total += x               # O(1)
    return total                 # O(1)
# Tổng: O(1) + O(n) * O(1) + O(1) = O(n)
```

### Quy tắc 2: Vòng lặp lồng nhau → O(n²)

```python
def has_duplicate(arr):
    n = len(arr)
    for i in range(n):           # O(n)
        for j in range(i+1, n):  # O(n)
            if arr[i] == arr[j]: # O(1)
                return True
    return False
# Tổng: O(n) * O(n) = O(n²)
```

### Quy tắc 3: Chia đôi mỗi bước → O(log n)

```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:              # Mỗi bước chia đôi → log₂(n) bước
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
# Tổng: O(log n)
```

### Quy tắc 4: Đệ quy — Dùng cây đệ quy

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
# Mỗi lần gọi tách thành 2 → Cây nhị phân có n tầng
# Tổng: O(2^n) ← RẤT CHẬM!
```

### Quy tắc 5: Đệ quy chia đôi + merge → O(n log n)

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])     # T(n/2)
    right = merge_sort(arr[mid:])    # T(n/2)
    return merge(left, right)         # O(n)
# T(n) = 2*T(n/2) + O(n) → O(n log n) (Master Theorem)
```

---

## 1.4 Space Complexity (Độ phức tạp không gian)

Space Complexity = **bộ nhớ phụ** mà thuật toán sử dụng (không tính input).

```python
# O(1) Space — chỉ dùng vài biến
def find_max(arr):
    max_val = arr[0]
    for x in arr:
        if x > max_val:
            max_val = x
    return max_val

# O(n) Space — tạo mảng mới
def double_array(arr):
    result = []
    for x in arr:
        result.append(x * 2)
    return result

# O(n) Space — đệ quy dùng call stack
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)  # Call stack sâu n tầng → O(n) space
```

---

## 1.5 Master Theorem (Định lý Thầy)

Dùng cho đệ quy dạng: **T(n) = a·T(n/b) + O(n^d)**

| Điều kiện | Kết quả |
|-----------|---------|
| d > log_b(a) | O(n^d) |
| d = log_b(a) | O(n^d · log n) |
| d < log_b(a) | O(n^(log_b(a))) |

**Ví dụ**: Merge Sort → T(n) = 2·T(n/2) + O(n)
- a=2, b=2, d=1 → log₂(2) = 1 = d → **O(n log n)** ✓

---

## 1.6 Amortized Analysis (Phân tích khấu hao)

Một số thao tác **thỉnh thoảng mới chậm**, nhưng trung bình vẫn nhanh.

**Ví dụ**: Dynamic Array (Python list `append`)
- Bình thường: O(1)
- Khi đầy, phải copy toàn bộ sang mảng mới: O(n)
- Nhưng điều này chỉ xảy ra sau n lần append
- **Amortized**: O(n)/n = **O(1) amortized** mỗi lần append

---

## 📝 Bài Tập

1. Xác định Big O của đoạn code sau:
```python
for i in range(n):
    for j in range(n):
        for k in range(n):
            print(i, j, k)
```

2. So sánh 2 cách tính tổng 1+2+...+n:
```python
# Cách 1
total = 0
for i in range(1, n+1):
    total += i

# Cách 2
total = n * (n + 1) // 2
```

3. Xác định Time & Space complexity:
```python
def mystery(n):
    if n <= 0:
        return 0
    return mystery(n // 2) + 1
```

### Đáp án:
1. O(n³) — 3 vòng lặp lồng nhau
2. Cách 1: O(n), Cách 2: O(1) — công thức toán học nhanh hơn!
3. Time: O(log n), Space: O(log n) — chia đôi mỗi bước, call stack sâu log(n)
