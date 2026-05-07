"""
Chương 4: Heap & Priority Queue
================================
Min-Heap, Max-Heap, và các ứng dụng.
"""
import heapq


# ============================================================
# 1. HEAP — Cài đặt thủ công
# ============================================================

class MinHeap:
    """
    Min-Heap: Node cha luôn ≤ các node con.

    Lưu trong mảng:
    - Parent of i: (i - 1) // 2
    - Left child:  2*i + 1
    - Right child: 2*i + 2

    Ví dụ:        1
                /   \
               3     2
              / \   /
             7   4  5

    Mảng: [1, 3, 2, 7, 4, 5]
    """

    def __init__(self):
        self.heap = []

    def push(self, val):
        """Thêm phần tử — O(log n). Thêm cuối rồi sift up."""
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        """Lấy phần tử nhỏ nhất — O(log n). Swap root với cuối, sift down."""
        if not self.heap:
            raise IndexError("Heap is empty")
        if len(self.heap) == 1:
            return self.heap.pop()

        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()  # Đưa cuối lên đầu
        self._sift_down(0)
        return min_val

    def peek(self):
        """Xem phần tử nhỏ nhất — O(1)."""
        if not self.heap:
            raise IndexError("Heap is empty")
        return self.heap[0]

    def _sift_up(self, i):
        """Đẩy node lên đúng vị trí (khi node < parent)."""
        parent = (i - 1) // 2
        while i > 0 and self.heap[i] < self.heap[parent]:
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            i = parent
            parent = (i - 1) // 2

    def _sift_down(self, i):
        """Đẩy node xuống đúng vị trí (khi node > child)."""
        n = len(self.heap)
        while True:
            smallest = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest == i:
                break

            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            i = smallest

    def __len__(self):
        return len(self.heap)

    def __str__(self):
        return f"MinHeap: {self.heap}"


# ============================================================
# 2. HEAP SORT — O(n log n)
# ============================================================

def heap_sort(arr):
    """
    Heap Sort — Sắp xếp dùng heap.

    Bước 1: Xây Max-Heap O(n)
    Bước 2: Lặp n lần: swap root (max) ra cuối, sift down O(log n)
    Tổng: O(n log n), In-place, KHÔNG stable
    """
    n = len(arr)
    arr = arr.copy()

    def sift_down(i, size):
        while True:
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            if left < size and arr[left] > arr[largest]:
                largest = left
            if right < size and arr[right] > arr[largest]:
                largest = right
            if largest == i:
                break
            arr[i], arr[largest] = arr[largest], arr[i]
            i = largest

    # Build Max-Heap (bottom-up) — O(n)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(i, n)

    # Extract max → cuối mảng
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        sift_down(0, i)

    return arr


# ============================================================
# 3. ỨNG DỤNG: Top K Elements
# ============================================================

def top_k_frequent(nums, k):
    """
    LeetCode #347 — K phần tử xuất hiện nhiều nhất.
    Dùng Min-Heap size k — O(n log k).
    """
    from collections import Counter
    count = Counter(nums)

    # Dùng min-heap size k
    # heapq trong Python là min-heap
    return heapq.nlargest(k, count.keys(), key=count.get)


def kth_largest(nums, k):
    """
    LeetCode #215 — Phần tử lớn thứ k.
    Dùng Min-Heap size k: phần tử nhỏ nhất trong heap = kth largest.
    """
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)  # Bỏ nhỏ nhất
    return heap[0]  # Phần tử nhỏ nhất trong top-k


def merge_k_sorted_lists(lists):
    """
    LeetCode #23 — Merge K sorted lists dùng Heap.
    O(N log k) với N = tổng phần tử, k = số list.
    """
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))  # (val, list_idx, elem_idx)

    result = []
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return result


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("  MIN-HEAP DEMO")
    print("=" * 50)

    h = MinHeap()
    values = [7, 3, 5, 1, 4, 2, 6]
    for v in values:
        h.push(v)
    print(f"Push {values}")
    print(h)

    print(f"\nPop (ascending order):")
    while len(h) > 0:
        print(f"  Pop → {h.pop()}")

    print(f"\n{'=' * 50}")
    print("  HEAP SORT DEMO")
    print("=" * 50)

    arr = [38, 27, 43, 3, 9, 82, 10]
    sorted_arr = heap_sort(arr)
    print(f"Input:  {arr}")
    print(f"Sorted: {sorted_arr}")

    print(f"\n{'=' * 50}")
    print("  ỨNG DỤNG HEAP")
    print("=" * 50)

    # Top K Frequent
    nums = [1, 1, 1, 2, 2, 3, 3, 3, 3]
    print(f"\nTop 2 frequent in {nums}: {top_k_frequent(nums, 2)}")

    # Kth Largest
    nums = [3, 2, 1, 5, 6, 4]
    print(f"2nd largest in {nums}: {kth_largest(nums, 2)}")

    # Merge K Sorted Lists
    lists = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    print(f"Merge {lists}: {merge_k_sorted_lists(lists)}")
