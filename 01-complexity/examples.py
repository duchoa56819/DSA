"""
Chương 1: Phân Tích Độ Phức Tạp — Code Minh Họa
=================================================
Chạy file này để thấy sự khác biệt giữa các độ phức tạp.
"""

import time
import math


# ============================================================
# 1. O(1) — Hằng số: Không phụ thuộc vào kích thước input
# ============================================================
def get_first_element(arr):
    """Lấy phần tử đầu tiên — luôn 1 bước dù mảng to cỡ nào."""
    return arr[0] if arr else None


# ============================================================
# 2. O(log n) — Logarit: Chia đôi mỗi bước
# ============================================================
def binary_search(arr, target):
    """Tìm kiếm nhị phân — mỗi bước loại bỏ nửa mảng."""
    lo, hi = 0, len(arr) - 1
    steps = 0
    while lo <= hi:
        steps += 1
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid, steps
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1, steps


# ============================================================
# 3. O(n) — Tuyến tính: Duyệt qua từng phần tử
# ============================================================
def linear_search(arr, target):
    """Tìm kiếm tuyến tính — phải kiểm tra từng phần tử."""
    steps = 0
    for i, val in enumerate(arr):
        steps += 1
        if val == target:
            return i, steps
    return -1, steps


# ============================================================
# 4. O(n²) — Bình phương: 2 vòng lặp lồng nhau
# ============================================================
def bubble_sort(arr):
    """Sắp xếp nổi bọt — so sánh từng cặp, lặp lại nhiều lần."""
    arr = arr.copy()
    n = len(arr)
    steps = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            steps += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr, steps


# ============================================================
# 5. O(2^n) — Mũ: Fibonacci đệ quy (KHÔNG tối ưu)
# ============================================================
def fibonacci_recursive(n):
    """Fibonacci đệ quy — cực kỳ chậm vì tính lại nhiều lần."""
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


# ============================================================
# 6. O(n) — Fibonacci tối ưu bằng DP
# ============================================================
def fibonacci_dp(n):
    """Fibonacci với Dynamic Programming — nhanh hơn gấp bội."""
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]


# ============================================================
# DEMO: So sánh thực tế
# ============================================================
def measure_time(func, *args):
    """Đo thời gian chạy của một hàm."""
    start = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - start
    return result, elapsed


def demo_complexity():
    """Demo so sánh các độ phức tạp."""

    print("=" * 60)
    print("  DEMO: SO SÁNH ĐỘ PHỨC TẠP THUẬT TOÁN")
    print("=" * 60)

    # --- Demo 1: O(1) vs O(n) vs O(log n) ---
    sizes = [1000, 10_000, 100_000, 1_000_000]

    print("\n📊 Demo 1: Tìm kiếm — O(1) vs O(log n) vs O(n)")
    print("-" * 60)
    print(f"{'Size':>10} | {'O(1) steps':>12} | {'O(log n) steps':>15} | {'O(n) steps':>12}")
    print("-" * 60)

    for size in sizes:
        arr = list(range(size))
        target = size - 1  # Phần tử cuối (worst case cho linear)

        # O(1) — truy cập trực tiếp
        o1_steps = 1

        # O(log n) — binary search
        _, log_steps = binary_search(arr, target)

        # O(n) — linear search
        _, n_steps = linear_search(arr, target)

        print(f"{size:>10,} | {o1_steps:>12} | {log_steps:>15} | {n_steps:>12,}")

    # --- Demo 2: Sorting — O(n²) vs O(n log n) ---
    print(f"\n📊 Demo 2: Sắp xếp — O(n²) Bubble Sort")
    print("-" * 60)
    print(f"{'Size':>10} | {'Bubble O(n²)':>15} | {'Thời gian':>12}")
    print("-" * 60)

    for size in [100, 500, 1000, 2000]:
        import random
        arr = list(range(size))
        random.shuffle(arr)

        _, elapsed = measure_time(bubble_sort, arr)
        n_sq = size * size
        print(f"{size:>10,} | {n_sq:>15,} | {elapsed:>10.4f}s")

    # --- Demo 3: Fibonacci — O(2^n) vs O(n) ---
    print(f"\n📊 Demo 3: Fibonacci — O(2^n) đệ quy vs O(n) DP")
    print("-" * 60)
    print(f"{'n':>5} | {'Đệ quy O(2^n)':>20} | {'DP O(n)':>20} | {'Tốc độ':>10}")
    print("-" * 60)

    for n in [10, 20, 30, 35]:
        # O(2^n)
        result1, time1 = measure_time(fibonacci_recursive, n)

        # O(n)
        result2, time2 = measure_time(fibonacci_dp, n)

        if time2 > 0:
            speedup = f"{time1 / time2:.0f}x"
        else:
            speedup = "∞"

        print(f"{n:>5} | {time1:>18.6f}s | {time2:>18.6f}s | {speedup:>10}")

    print("\n" + "=" * 60)
    print("  💡 KẾT LUẬN:")
    print("  - O(log n) nhanh hơn O(n) hàng trăm nghìn lần")
    print("  - O(n²) trở nên rất chậm với dữ liệu lớn")
    print("  - O(2^n) gần như không thể chạy với n > 40")
    print("  → Chọn đúng thuật toán = tiết kiệm hàng giờ!")
    print("=" * 60)


if __name__ == "__main__":
    demo_complexity()
