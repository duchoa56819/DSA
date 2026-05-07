"""
Chương 2: Array — Mảng
======================
Các thao tác cơ bản và bài toán kinh điển trên mảng.
"""


# ============================================================
# 1. CÁC THAO TÁC CƠ BẢN
# ============================================================

def demo_array_basics():
    """Demo các thao tác cơ bản trên mảng (Python list)."""
    print("=" * 50)
    print("  ARRAY — CÁC THAO TÁC CƠ BẢN")
    print("=" * 50)

    # Tạo mảng
    arr = [10, 20, 30, 40, 50]
    print(f"\nMảng ban đầu: {arr}")

    # Truy cập O(1)
    print(f"arr[0] = {arr[0]}")  # 10
    print(f"arr[-1] = {arr[-1]}")  # 50 (phần tử cuối)

    # Chèn cuối O(1) amortized
    arr.append(60)
    print(f"Sau append(60): {arr}")

    # Chèn vào vị trí O(n) — phải dịch các phần tử
    arr.insert(2, 25)
    print(f"Sau insert(2, 25): {arr}")

    # Xóa O(n)
    arr.remove(25)
    print(f"Sau remove(25): {arr}")

    # Xóa cuối O(1)
    arr.pop()
    print(f"Sau pop(): {arr}")

    # Slicing
    print(f"arr[1:3] = {arr[1:3]}")  # [20, 30]

    # List comprehension — cách Pythonic tạo mảng
    squares = [x**2 for x in range(1, 6)]
    print(f"Bình phương 1-5: {squares}")


# ============================================================
# 2. BÀI TOÁN KINH ĐIỂN TRÊN MẢNG
# ============================================================

def two_sum(nums, target):
    """
    Two Sum (LeetCode #1) — O(n) với Hash Map
    Tìm 2 số trong mảng có tổng = target.
    """
    seen = {}  # {giá_trị: index}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


def max_subarray(nums):
    """
    Maximum Subarray (LeetCode #53) — Kadane's Algorithm O(n)
    Tìm subarray có tổng lớn nhất.
    """
    max_sum = current_sum = nums[0]
    for num in nums[1:]:
        # Tại mỗi vị trí: tiếp tục subarray cũ hoặc bắt đầu mới?
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum


def rotate_array(nums, k):
    """
    Rotate Array (LeetCode #189) — O(n) time, O(1) space
    Xoay mảng k bước sang phải.
    Trick: Đảo ngược 3 lần!
    """
    n = len(nums)
    k = k % n  # Xử lý k > n

    def reverse(lo, hi):
        while lo < hi:
            nums[lo], nums[hi] = nums[hi], nums[lo]
            lo += 1
            hi -= 1

    # [1,2,3,4,5] k=2
    reverse(0, n - 1)   # [5,4,3,2,1]
    reverse(0, k - 1)   # [4,5,3,2,1]
    reverse(k, n - 1)   # [4,5,1,2,3] ✓
    return nums


def merge_sorted_arrays(arr1, arr2):
    """
    Merge Two Sorted Arrays — O(n + m) Two Pointers
    Trộn 2 mảng đã sắp xếp thành 1 mảng sắp xếp.
    """
    result = []
    i = j = 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    # Thêm phần còn lại
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result


# ============================================================
# 3. KỸ THUẬT TWO POINTERS TRÊN MẢNG
# ============================================================

def remove_duplicates_sorted(nums):
    """
    Remove Duplicates from Sorted Array (LeetCode #26) — O(n)
    Dùng 2 con trỏ: slow (vị trí ghi) và fast (vị trí đọc).
    """
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1  # Số phần tử unique


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    demo_array_basics()

    print("\n" + "=" * 50)
    print("  BÀI TOÁN KINH ĐIỂN")
    print("=" * 50)

    # Two Sum
    nums = [2, 7, 11, 15]
    target = 9
    result = two_sum(nums, target)
    print(f"\nTwo Sum: {nums}, target={target} → indices {result}")

    # Max Subarray
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    result = max_subarray(nums)
    print(f"Max Subarray: {nums} → {result}")  # 6

    # Rotate Array
    nums = [1, 2, 3, 4, 5]
    result = rotate_array(nums.copy(), 2)
    print(f"Rotate [1,2,3,4,5] by 2 → {result}")

    # Merge Sorted
    result = merge_sorted_arrays([1, 3, 5], [2, 4, 6])
    print(f"Merge [1,3,5] + [2,4,6] → {result}")

    # Remove Duplicates
    nums = [1, 1, 2, 2, 3, 4, 4, 5]
    k = remove_duplicates_sorted(nums)
    print(f"Remove Duplicates [1,1,2,2,3,4,4,5] → {nums[:k]}")
