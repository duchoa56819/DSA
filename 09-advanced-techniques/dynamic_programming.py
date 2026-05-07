"""
Chương 9: Kỹ Thuật Nâng Cao — Dynamic Programming
====================================================
DP là kỹ thuật QUAN TRỌNG NHẤT trong phỏng vấn và competitive programming.
"""


# ============================================================
# DP LÀ GÌ?
# ============================================================
# Dynamic Programming = Chia bài toán lớn thành bài toán con,
# LƯU LẠI kết quả để không tính lại.
#
# 2 cách tiếp cận:
# 1. Top-down (Memoization): Đệ quy + cache
# 2. Bottom-up (Tabulation): Xây từ base case lên
#
# Khi nào dùng DP?
# - Bài toán có OPTIMAL SUBSTRUCTURE (cấu trúc con tối ưu)
# - Bài toán có OVERLAPPING SUBPROBLEMS (bài con trùng lặp)
# ============================================================


# ============================================================
# 1. FIBONACCI — Ví dụ nhập môn DP
# ============================================================

def fib_recursive(n):
    """O(2^n) — Cực chậm! Tính lại nhiều lần."""
    if n <= 1:
        return n
    return fib_recursive(n-1) + fib_recursive(n-2)


def fib_memo(n, memo=None):
    """Top-down DP (Memoization) — O(n)."""
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]


def fib_dp(n):
    """Bottom-up DP (Tabulation) — O(n) time, O(n) space."""
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]


def fib_optimized(n):
    """Space-optimized DP — O(n) time, O(1) space."""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


# ============================================================
# 2. CLIMBING STAIRS (LeetCode #70)
# ============================================================

def climb_stairs(n):
    """
    Có bao nhiêu cách leo n bậc thang? Mỗi bước leo 1 hoặc 2 bậc.
    dp[i] = dp[i-1] + dp[i-2]  (giống Fibonacci!)

    n=1: 1 cách (1)
    n=2: 2 cách (1+1, 2)
    n=3: 3 cách (1+1+1, 1+2, 2+1)
    """
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


# ============================================================
# 3. 0/1 KNAPSACK — Bài toán cái túi ⭐
# ============================================================

def knapsack_01(weights, values, capacity):
    """
    Cho n vật, mỗi vật có weight và value.
    Chọn các vật cho vào túi (capacity giới hạn) để tổng value MAX.
    Mỗi vật chỉ được chọn 1 lần!

    dp[i][w] = max value khi xét i vật đầu, capacity = w

    Chuyển tiếp:
    - Không chọn vật i: dp[i][w] = dp[i-1][w]
    - Chọn vật i:       dp[i][w] = dp[i-1][w - weight[i]] + value[i]
    - dp[i][w] = max(không chọn, chọn)
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i-1][w]  # Không chọn
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w],
                               dp[i-1][w - weights[i-1]] + values[i-1])

    return dp[n][capacity]


# ============================================================
# 4. LONGEST COMMON SUBSEQUENCE (LCS) — LeetCode #1143
# ============================================================

def lcs(text1, text2):
    """
    Tìm dãy con chung dài nhất.
    "abcde" và "ace" → "ace" (length 3)

    dp[i][j] = LCS length của text1[:i] và text2[:j]

    Nếu text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1
    Ngược lại: dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]


# ============================================================
# 5. COIN CHANGE (LeetCode #322)
# ============================================================

def coin_change(coins, amount):
    """
    Số đồng xu ÍT NHẤT để tạo thành amount.
    coins = [1, 5, 10], amount = 11 → 2 (10+1)

    dp[i] = số xu ít nhất cho amount i
    dp[i] = min(dp[i - coin] + 1) cho mỗi coin
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


# ============================================================
# 6. LONGEST INCREASING SUBSEQUENCE (LIS) — LeetCode #300
# ============================================================

def lis(nums):
    """
    Dãy con tăng dài nhất.
    [10, 9, 2, 5, 3, 7, 101, 18] → [2, 3, 7, 101] = 4

    dp[i] = LIS kết thúc tại i
    dp[i] = max(dp[j] + 1) cho j < i và nums[j] < nums[i]
    O(n²)
    """
    if not nums:
        return 0
    n = len(nums)
    dp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


# ============================================================
# 7. EDIT DISTANCE (LeetCode #72)
# ============================================================

def edit_distance(word1, word2):
    """
    Số thao tác TỐI THIỂU để biến word1 thành word2.
    Cho phép: Insert, Delete, Replace.

    "horse" → "ros" = 3 (replace h→r, remove r, remove e)

    dp[i][j] = edit distance của word1[:i] và word2[:j]
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],     # Delete
                    dp[i][j-1],     # Insert
                    dp[i-1][j-1]    # Replace
                )

    return dp[m][n]


# ============================================================
# 8. HOUSE ROBBER (LeetCode #198)
# ============================================================

def house_robber(nums):
    """
    Cướp nhà: Không được cướp 2 nhà liền kề. Maximize loot.
    [2, 7, 9, 3, 1] → 12 (2 + 9 + 1)

    dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    """
    if not nums:
        return 0
    if len(nums) <= 2:
        return max(nums)

    prev2, prev1 = nums[0], max(nums[0], nums[1])
    for i in range(2, len(nums)):
        prev2, prev1 = prev1, max(prev1, prev2 + nums[i])
    return prev1


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  DYNAMIC PROGRAMMING DEMO")
    print("=" * 55)

    print(f"\n--- Fibonacci ---")
    for n in [5, 10, 30]:
        print(f"  fib({n}) = {fib_optimized(n)}")

    print(f"\n--- Climbing Stairs ---")
    for n in [3, 5, 10]:
        print(f"  climb({n}) = {climb_stairs(n)} ways")

    print(f"\n--- 0/1 Knapsack ---")
    weights = [2, 3, 4, 5]
    values =  [3, 4, 5, 6]
    cap = 8
    print(f"  Weights: {weights}, Values: {values}, Capacity: {cap}")
    print(f"  Max value: {knapsack_01(weights, values, cap)}")

    print(f"\n--- LCS ---")
    print(f'  LCS("abcde", "ace") = {lcs("abcde", "ace")}')

    print(f"\n--- Coin Change ---")
    print(f"  coins=[1,5,10], amount=11 → {coin_change([1,5,10], 11)} coins")
    print(f"  coins=[2], amount=3 → {coin_change([2], 3)}")

    print(f"\n--- LIS ---")
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    print(f"  LIS({nums}) = {lis(nums)}")

    print(f"\n--- Edit Distance ---")
    print(f'  "horse" → "ros" = {edit_distance("horse", "ros")}')
    print(f'  "intention" → "execution" = {edit_distance("intention", "execution")}')

    print(f"\n--- House Robber ---")
    nums = [2, 7, 9, 3, 1]
    print(f"  Houses: {nums} → Max loot: {house_robber(nums)}")
