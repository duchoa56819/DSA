"""
Chương 9: Backtracking & Greedy
=================================
Hai kỹ thuật giải thuật quan trọng.
"""


# ============================================================
# BACKTRACKING — Quay lui
# ============================================================
# Template:
# def backtrack(candidate):
#     if is_solution(candidate):
#         output(candidate)
#         return
#     for next_candidate in get_candidates():
#         if is_valid(next_candidate):
#             place(next_candidate)
#             backtrack(next_candidate)
#             remove(next_candidate)  ← QUAY LUI!


# 1. Subsets (LeetCode #78) — Liệt kê tất cả tập con
def subsets(nums):
    """
    Input: [1,2,3]
    Output: [[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]]
    """
    result = []

    def backtrack(start, current):
        result.append(current[:])  # Thêm bản sao
        for i in range(start, len(nums)):
            current.append(nums[i])       # Chọn
            backtrack(i + 1, current)      # Đệ quy
            current.pop()                  # Quay lui!

    backtrack(0, [])
    return result


# 2. Permutations (LeetCode #46) — Liệt kê hoán vị
def permutations(nums):
    """
    Input: [1,2,3]
    Output: [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
    """
    result = []

    def backtrack(current, remaining):
        if not remaining:
            result.append(current[:])
            return
        for i in range(len(remaining)):
            current.append(remaining[i])
            backtrack(current, remaining[:i] + remaining[i+1:])
            current.pop()

    backtrack([], nums)
    return result


# 3. N-Queens (LeetCode #51) — Đặt N quân hậu
def n_queens(n):
    """
    Đặt n quân hậu trên bàn cờ n×n sao cho không quân nào tấn công nhau.
    Kinh điển nhất của Backtracking!
    """
    result = []
    board = [['.' ] * n for _ in range(n)]
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col

    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            # Đặt quân hậu
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            backtrack(row + 1)

            # Quay lui
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return result


# 4. Combination Sum (LeetCode #39)
def combination_sum(candidates, target):
    """
    Tìm tổ hợp có tổng = target. Mỗi số dùng nhiều lần.
    candidates=[2,3,6,7], target=7 → [[2,2,3], [7]]
    """
    result = []

    def backtrack(start, current, remaining):
        if remaining == 0:
            result.append(current[:])
            return
        if remaining < 0:
            return
        for i in range(start, len(candidates)):
            current.append(candidates[i])
            backtrack(i, current, remaining - candidates[i])
            current.pop()

    backtrack(0, [], target)
    return result


# ============================================================
# GREEDY — Tham lam
# ============================================================
# Tại mỗi bước, chọn phương án TỐT NHẤT tại thời điểm đó.
# Không quay lui! Nhanh hơn DP nhưng không phải lúc nào cũng đúng.
# Chỉ đúng khi bài toán có GREEDY CHOICE PROPERTY.


# 1. Activity Selection — Chọn hoạt động
def activity_selection(start, finish):
    """
    Chọn NHIỀU hoạt động nhất không trùng thời gian.
    Greedy: Luôn chọn hoạt động KẾT THÚC SỚM NHẤT.
    """
    activities = sorted(zip(start, finish), key=lambda x: x[1])
    selected = [activities[0]]

    for s, f in activities[1:]:
        if s >= selected[-1][1]:  # Không trùng
            selected.append((s, f))

    return selected


# 2. Jump Game (LeetCode #55)
def can_jump(nums):
    """
    Kiểm tra có thể nhảy từ đầu đến cuối mảng.
    nums[i] = bước nhảy tối đa tại i.
    Greedy: Track farthest reach.
    """
    max_reach = 0
    for i in range(len(nums)):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + nums[i])
    return True


# 3. Fractional Knapsack (khác 0/1 Knapsack — có thể lấy 1 phần)
def fractional_knapsack(weights, values, capacity):
    """
    Greedy: Sắp xếp theo value/weight giảm dần, lấy nhiều nhất.
    """
    items = sorted(zip(weights, values),
                   key=lambda x: x[1]/x[0], reverse=True)
    total = 0
    for w, v in items:
        if capacity >= w:
            total += v
            capacity -= w
        else:
            total += v * (capacity / w)  # Lấy 1 phần
            break
    return total


# ============================================================
# TWO POINTERS & SLIDING WINDOW
# ============================================================

def two_sum_sorted(nums, target):
    """
    Two Sum II — mảng đã sorted. O(n) với 2 con trỏ.
    """
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return [lo, hi]
        elif s < target:
            lo += 1
        else:
            hi -= 1
    return []


def max_subarray_sum_k(nums, k):
    """
    Sliding Window: Tổng lớn nhất của subarray kích thước k.
    O(n) — window trượt qua mảng.
    """
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]  # Thêm phải, bỏ trái
        max_sum = max(max_sum, window_sum)
    return max_sum


def longest_substring_no_repeat(s):
    """
    LeetCode #3 — Longest Substring Without Repeating Characters.
    Sliding Window với HashSet. O(n).
    """
    char_set = set()
    left = max_len = 0
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)
    return max_len


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  BACKTRACKING DEMO")
    print("=" * 55)

    print(f"\nSubsets [1,2,3]:")
    for s in subsets([1, 2, 3]):
        print(f"  {s}")

    print(f"\nPermutations [1,2,3]:")
    for p in permutations([1, 2, 3]):
        print(f"  {p}")

    print(f"\nN-Queens (4×4): {len(n_queens(4))} solutions")
    for sol in n_queens(4):
        for row in sol:
            print(f"  {row}")
        print()

    print(f"Combination Sum [2,3,6,7], target=7:")
    print(f"  {combination_sum([2,3,6,7], 7)}")

    print(f"\n{'=' * 55}")
    print("  GREEDY DEMO")
    print("=" * 55)

    start =  [1, 3, 0, 5, 8, 5]
    finish = [2, 4, 6, 7, 9, 9]
    print(f"\nActivity Selection:")
    print(f"  Selected: {activity_selection(start, finish)}")

    print(f"\nJump Game [2,3,1,1,4]: {can_jump([2,3,1,1,4])}")
    print(f"Jump Game [3,2,1,0,4]: {can_jump([3,2,1,0,4])}")

    print(f"\n{'=' * 55}")
    print("  TWO POINTERS & SLIDING WINDOW")
    print("=" * 55)

    print(f"\nTwo Sum Sorted [1,2,3,4,6] target=6: {two_sum_sorted([1,2,3,4,6], 6)}")
    print(f"Max subarray sum k=3 [2,1,5,1,3,2]: {max_subarray_sum_k([2,1,5,1,3,2], 3)}")
    print(f'Longest no repeat "abcabcbb": {longest_substring_no_repeat("abcabcbb")}')
