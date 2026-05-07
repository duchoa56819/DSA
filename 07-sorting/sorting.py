"""
Chương 7: Thuật Toán Sắp Xếp (Sorting Algorithms)
====================================================
Triển khai và so sánh tất cả thuật toán sắp xếp quan trọng.
"""
import time
import random


# ============================================================
# 1. BUBBLE SORT — O(n²)
# ============================================================

def bubble_sort(arr):
    """
    So sánh từng cặp liền kề, đẩy phần tử lớn về cuối.
    Như bong bóng nổi lên mặt nước 🫧

    Stable: ✅  In-place: ✅  Best: O(n)  Avg/Worst: O(n²)
    """
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:  # Tối ưu: dừng sớm nếu đã sắp xếp
            break
    return arr


# ============================================================
# 2. SELECTION SORT — O(n²)
# ============================================================

def selection_sort(arr):
    """
    Mỗi lần tìm phần tử nhỏ nhất, đặt vào đúng vị trí.
    Như chọn thẻ bài nhỏ nhất lần lượt 🃏

    Stable: ❌  In-place: ✅  Best/Avg/Worst: O(n²)
    """
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


# ============================================================
# 3. INSERTION SORT — O(n²)
# ============================================================

def insertion_sort(arr):
    """
    Chèn từng phần tử vào vị trí đúng trong phần đã sắp xếp.
    Như xếp bài trên tay 🃏

    Stable: ✅  In-place: ✅  Best: O(n)  Avg/Worst: O(n²)
    Rất tốt cho mảng gần như đã sắp xếp hoặc mảng nhỏ!
    """
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


# ============================================================
# 4. MERGE SORT — O(n log n) ⭐
# ============================================================

def merge_sort(arr):
    """
    Chia đôi mảng, sort 2 nửa, rồi merge lại.
    Divide & Conquer! 🔀

    Stable: ✅  In-place: ❌  Best/Avg/Worst: O(n log n)
    Space: O(n) — cần mảng phụ để merge
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return _merge(left, right)


def _merge(left, right):
    """Merge 2 mảng đã sắp xếp."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ============================================================
# 5. QUICK SORT — O(n log n) average ⭐
# ============================================================

def quick_sort(arr):
    """
    Chọn pivot, chia mảng thành 2 phần: < pivot và > pivot.
    Thuật toán sort NHANH NHẤT trong thực tế! ⚡

    Stable: ❌  In-place: ✅  Best/Avg: O(n log n)  Worst: O(n²)
    Worst case khi pivot luôn là min/max → tránh bằng random pivot.
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]  # Chọn pivot ở giữa
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


def quick_sort_inplace(arr, low=0, high=None):
    """Quick Sort in-place (Lomuto partition)."""
    if high is None:
        arr = arr.copy()
        high = len(arr) - 1

    if low < high:
        pivot_idx = _partition(arr, low, high)
        quick_sort_inplace(arr, low, pivot_idx - 1)
        quick_sort_inplace(arr, pivot_idx + 1, high)

    return arr


def _partition(arr, low, high):
    """Lomuto partition scheme."""
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# ============================================================
# 6. COUNTING SORT — O(n + k)
# ============================================================

def counting_sort(arr):
    """
    Đếm tần suất mỗi giá trị rồi xây lại mảng.
    Chỉ dùng cho số nguyên không âm, range nhỏ!

    Stable: ✅  Best/Avg/Worst: O(n + k) với k = max value
    Space: O(k)
    """
    if not arr:
        return arr

    max_val = max(arr)
    count = [0] * (max_val + 1)

    for num in arr:
        count[num] += 1

    result = []
    for val, freq in enumerate(count):
        result.extend([val] * freq)

    return result


# ============================================================
# 7. RADIX SORT — O(d * (n + k))
# ============================================================

def radix_sort(arr):
    """
    Sort theo từng chữ số: ones → tens → hundreds → ...
    Dùng counting sort cho mỗi chữ số.

    Stable: ✅  O(d * n) với d = số chữ số
    """
    if not arr:
        return arr

    max_val = max(arr)
    exp = 1  # 1, 10, 100, ...

    result = arr.copy()
    while max_val // exp > 0:
        # Counting sort theo chữ số tại exp
        count = [0] * 10
        output = [0] * len(result)

        for num in result:
            digit = (num // exp) % 10
            count[digit] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(len(result) - 1, -1, -1):
            digit = (result[i] // exp) % 10
            count[digit] -= 1
            output[count[digit]] = result[i]

        result = output
        exp *= 10

    return result


# ============================================================
# BẢNG SO SÁNH & DEMO
# ============================================================

def benchmark_sorts():
    """So sánh tốc độ các thuật toán sắp xếp."""
    print("=" * 70)
    print("  SO SÁNH THUẬT TOÁN SẮP XẾP")
    print("=" * 70)

    # Bảng lý thuyết
    print("\n📋 BẢNG SO SÁNH LÝ THUYẾT:")
    print("-" * 70)
    print(f"{'Thuật toán':<18} {'Best':>10} {'Average':>12} {'Worst':>10} {'Space':>8} {'Stable':>7}")
    print("-" * 70)
    data = [
        ("Bubble Sort",    "O(n)",      "O(n²)",     "O(n²)",   "O(1)",  "Yes"),
        ("Selection Sort", "O(n²)",     "O(n²)",     "O(n²)",   "O(1)",  "No"),
        ("Insertion Sort", "O(n)",      "O(n²)",     "O(n²)",   "O(1)",  "Yes"),
        ("Merge Sort",     "O(n lg n)", "O(n lg n)", "O(n lg n)","O(n)", "Yes"),
        ("Quick Sort",     "O(n lg n)", "O(n lg n)", "O(n²)",   "O(lg n)","No"),
        ("Heap Sort",      "O(n lg n)", "O(n lg n)", "O(n lg n)","O(1)", "No"),
        ("Counting Sort",  "O(n+k)",    "O(n+k)",    "O(n+k)",  "O(k)",  "Yes"),
        ("Radix Sort",     "O(dn)",     "O(dn)",     "O(dn)",   "O(n+k)","Yes"),
    ]
    for row in data:
        print(f"{row[0]:<18} {row[1]:>10} {row[2]:>12} {row[3]:>10} {row[4]:>8} {row[5]:>7}")

    # Benchmark thực tế
    sizes = [100, 1000, 5000]
    algorithms = [
        ("Bubble Sort",    bubble_sort),
        ("Selection Sort", selection_sort),
        ("Insertion Sort", insertion_sort),
        ("Merge Sort",     merge_sort),
        ("Quick Sort",     quick_sort),
        ("Counting Sort",  counting_sort),
        ("Python sorted",  sorted),
    ]

    for size in sizes:
        arr = [random.randint(0, 10000) for _ in range(size)]
        print(f"\n📊 Benchmark với n = {size:,}:")
        print("-" * 45)

        for name, func in algorithms:
            start = time.perf_counter()
            result = func(arr)
            elapsed = time.perf_counter() - start
            print(f"  {name:<18} {elapsed:.6f}s")

    print("\n💡 KẾT LUẬN:")
    print("  - Merge Sort & Quick Sort là workhorse: O(n log n)")
    print("  - Python built-in sorted() dùng Timsort (hybrid merge+insertion)")
    print("  - Counting/Radix Sort cực nhanh khi data phù hợp")
    print("  - Insertion Sort tốt cho mảng nhỏ hoặc gần sắp xếp")


if __name__ == "__main__":
    # Demo từng thuật toán
    arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"Input: {arr}\n")

    print(f"Bubble Sort:    {bubble_sort(arr)}")
    print(f"Selection Sort: {selection_sort(arr)}")
    print(f"Insertion Sort: {insertion_sort(arr)}")
    print(f"Merge Sort:     {merge_sort(arr)}")
    print(f"Quick Sort:     {quick_sort(arr)}")
    print(f"Counting Sort:  {counting_sort(arr)}")
    print(f"Radix Sort:     {radix_sort(arr)}")

    print()
    benchmark_sorts()
