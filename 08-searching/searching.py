"""
Chương 8: Thuật Toán Tìm Kiếm (Searching Algorithms)
======================================================
Linear Search, Binary Search và các biến thể.
"""


# ============================================================
# 1. LINEAR SEARCH — O(n)
# ============================================================

def linear_search(arr, target):
    """Tìm tuần tự — kiểm tra từng phần tử."""
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1


# ============================================================
# 2. BINARY SEARCH — O(log n) ⭐ QUAN TRỌNG NHẤT
# ============================================================

def binary_search(arr, target):
    """
    Tìm kiếm nhị phân — mảng phải đã SORTED!
    Mỗi bước loại bỏ NỬA mảng.

    Ví dụ: Tìm 7 trong [1, 3, 5, 7, 9, 11, 13]
    Bước 1: mid=7 → Found! ✅

    Tìm 9:
    Bước 1: mid=7, 9>7 → tìm bên phải [9, 11, 13]
    Bước 2: mid=11, 9<11 → tìm bên trái [9]
    Bước 3: mid=9 → Found! ✅
    """
    lo, hi = 0, len(arr) - 1

    while lo <= hi:
        mid = lo + (hi - lo) // 2  # Tránh overflow (so với (lo+hi)//2)
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1


# ============================================================
# 3. BIẾN THỂ BINARY SEARCH
# ============================================================

def lower_bound(arr, target):
    """
    Tìm index ĐẦU TIÊN mà arr[i] >= target.
    Ví dụ: [1,2,2,2,3,4], target=2 → index 1
    """
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(arr, target):
    """
    Tìm index ĐẦU TIÊN mà arr[i] > target.
    Ví dụ: [1,2,2,2,3,4], target=2 → index 4
    """
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def search_range(arr, target):
    """
    LeetCode #34 — Tìm vị trí đầu và cuối của target.
    Dùng lower_bound + upper_bound.
    """
    left = lower_bound(arr, target)
    right = upper_bound(arr, target) - 1
    if left <= right and left < len(arr) and arr[left] == target:
        return [left, right]
    return [-1, -1]


def search_rotated(nums, target):
    """
    LeetCode #33 — Tìm trong mảng đã xoay.
    [4,5,6,7,0,1,2], target=0 → index 4

    Trick: Một nửa mảng luôn sorted → xác định target ở nửa nào.
    """
    lo, hi = 0, len(nums) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid

        # Nửa trái sorted
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        # Nửa phải sorted
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1

    return -1


def find_peak(nums):
    """
    LeetCode #162 — Tìm đỉnh cực đại.
    Peak: nums[i] > nums[i-1] và nums[i] > nums[i+1]

    Binary Search: Nếu mid tăng → peak ở bên phải, ngược lại.
    """
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1  # Peak ở bên phải
        else:
            hi = mid      # Peak ở bên trái (hoặc mid)
    return lo


def sqrt_binary_search(n):
    """Tính căn bậc 2 (làm tròn xuống) bằng Binary Search."""
    if n < 2:
        return n
    lo, hi = 1, n // 2
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid == n:
            return mid
        elif mid * mid < n:
            lo = mid + 1
        else:
            hi = mid - 1
    return hi


def binary_search_on_answer(weights, days):
    """
    LeetCode #1011 — Capacity To Ship Within D Days.
    Binary search trên đáp án (capacity).
    Tìm capacity nhỏ nhất để ship hết trong days ngày.
    """
    def can_ship(capacity):
        day_count = 1
        current_load = 0
        for w in weights:
            if current_load + w > capacity:
                day_count += 1
                current_load = 0
            current_load += w
        return day_count <= days

    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if can_ship(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("  SEARCHING ALGORITHMS DEMO")
    print("=" * 50)

    arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    print(f"Array: {arr}")

    print(f"\nLinear Search 7:  index {linear_search(arr, 7)}")
    print(f"Binary Search 7:  index {binary_search(arr, 7)}")
    print(f"Binary Search 10: index {binary_search(arr, 10)}")

    print(f"\n--- Binary Search Variants ---")
    arr2 = [1, 2, 2, 2, 3, 4, 5]
    print(f"Array: {arr2}")
    print(f"Lower bound 2: index {lower_bound(arr2, 2)}")
    print(f"Upper bound 2: index {upper_bound(arr2, 2)}")
    print(f"Search range 2: {search_range(arr2, 2)}")

    print(f"\n--- Search Rotated Array ---")
    rotated = [4, 5, 6, 7, 0, 1, 2]
    print(f"Array: {rotated}")
    print(f"Find 0: index {search_rotated(rotated, 0)}")
    print(f"Find 6: index {search_rotated(rotated, 6)}")

    print(f"\n--- Other Applications ---")
    print(f"sqrt(16) = {sqrt_binary_search(16)}")
    print(f"sqrt(27) = {sqrt_binary_search(27)}")

    weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    days = 5
    print(f"\nShip {weights} in {days} days → capacity = {binary_search_on_answer(weights, days)}")
