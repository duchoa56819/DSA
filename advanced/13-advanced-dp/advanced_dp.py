"""
Chương 13: Quy Hoạch Động Nâng Cao
=====================================
DP Bitmask, DP trên cây, DP Digit, Longest Palindromic Subsequence.
"""


# ============================================================
# 1. DP BITMASK — Dùng bitmask để biểu diễn tập con
# ============================================================

def tsp(dist):
    """
    Travelling Salesman Problem (TSP) — Bài toán người bán hàng.

    Tìm đường đi ngắn nhất thăm TẤT CẢ thành phố đúng 1 lần rồi quay lại.

    Brute-force: O(n!) — thử mọi hoán vị
    DP Bitmask:  O(n² × 2^n) — tốt hơn nhiều khi n ≤ 20

    State: dp[mask][i] = chi phí nhỏ nhất để thăm tập thành phố
           biểu diễn bởi mask, kết thúc tại thành phố i.

    mask: bitmask, bit thứ j = 1 nghĩa là đã thăm thành phố j.
    Ví dụ: mask = 0b1011 = đã thăm thành phố 0, 1, 3.

    dist: ma trận khoảng cách dist[i][j]
    """
    n = len(dist)
    INF = float('inf')
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Bắt đầu từ thành phố 0

    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == INF:
                continue
            if not (mask & (1 << u)):
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue  # Đã thăm v
                new_mask = mask | (1 << v)
                cost = dp[mask][u] + dist[u][v]
                if cost < dp[new_mask][v]:
                    dp[new_mask][v] = cost

    # Quay lại thành phố 0
    full = (1 << n) - 1
    return min(dp[full][i] + dist[i][0] for i in range(n))


# ============================================================
# 2. DP TRÊN CÂY (Tree DP)
# ============================================================

def tree_dp_max_independent_set(adj, n):
    """
    Maximum Independent Set trên cây.

    Chọn tập đỉnh lớn nhất sao cho không có 2 đỉnh nào kề nhau.

    dp[u][0] = max set khi KHÔNG chọn u
    dp[u][1] = max set khi CÓ chọn u

    dp[u][0] = sum(max(dp[v][0], dp[v][1])) cho mỗi con v
    dp[u][1] = 1 + sum(dp[v][0]) cho mỗi con v
    (Nếu chọn u thì KHÔNG được chọn con v)
    """
    dp = [[0, 0] for _ in range(n)]
    visited = [False] * n

    def dfs(u):
        visited[u] = True
        dp[u][1] = 1  # Chọn u

        for v in adj[u]:
            if not visited[v]:
                dfs(v)
                dp[u][0] += max(dp[v][0], dp[v][1])
                dp[u][1] += dp[v][0]

    dfs(0)  # Root = 0
    return max(dp[0][0], dp[0][1])


def tree_diameter_dp(adj, n):
    """
    Đường kính cây — Đường đi dài nhất trong cây.

    dp[u] = đường đi dài nhất bắt đầu từ u đi xuống.
    Đường kính = max(top1 + top2) qua mỗi node u,
    với top1, top2 là 2 nhánh dài nhất từ u.
    """
    result = [0]
    visited = [False] * n

    def dfs(u):
        visited[u] = True
        top1 = top2 = 0  # 2 nhánh dài nhất

        for v in adj[u]:
            if not visited[v]:
                depth = dfs(v) + 1
                if depth > top1:
                    top2 = top1
                    top1 = depth
                elif depth > top2:
                    top2 = depth

        result[0] = max(result[0], top1 + top2)
        return top1

    dfs(0)
    return result[0]


# ============================================================
# 3. DP DIGIT — Đếm trên các chữ số
# ============================================================

def count_numbers_with_digit(n, d):
    """
    Digit DP — Đếm số lượng số từ 0 đến n chứa chữ số d.

    Ví dụ: n=100, d=1 → các số chứa 1: 1,10-19,21,31,...,91,100 = 21 số

    Kỹ thuật: Xử lý từng chữ số từ trái sang phải.
    State: (position, tight, found) — vị trí, có bị giới hạn không, đã tìm thấy d chưa
    """
    digits = [int(x) for x in str(n)]
    length = len(digits)
    memo = {}

    def dp(pos, tight, found):
        """pos: vị trí hiện tại, tight: còn bị ràng buộc bởi n, found: đã có digit d"""
        if pos == length:
            return 1 if found else 0

        state = (pos, tight, found)
        if state in memo:
            return memo[state]

        limit = digits[pos] if tight else 9
        count = 0

        for digit in range(0, limit + 1):
            count += dp(
                pos + 1,
                tight and (digit == limit),
                found or (digit == d)
            )

        memo[state] = count
        return count

    return dp(0, True, False)


# ============================================================
# 4. LONGEST PALINDROMIC SUBSEQUENCE
# ============================================================

def longest_palindromic_subseq(s):
    """
    LeetCode #516 — Dãy con đối xứng dài nhất.
    "bbbab" → "bbbb" (length 4)

    Trick: LPS(s) = LCS(s, reverse(s))!
    Hoặc dùng DP 2D:
    dp[i][j] = LPS length của s[i..j]
    """
    n = len(s)
    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = 1

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    return dp[0][n - 1]


# ============================================================
# 5. MATRIX CHAIN MULTIPLICATION
# ============================================================

def matrix_chain_order(dims):
    """
    Tìm cách đặt ngoặc tối ưu khi nhân dãy ma trận.
    dims = [10, 30, 5, 60] → 3 ma trận: 10×30, 30×5, 5×60

    dp[i][j] = chi phí nhân tối thiểu cho ma trận i..j
    dp[i][j] = min(dp[i][k] + dp[k+1][j] + dims[i]*dims[k+1]*dims[j+1])
    """
    n = len(dims) - 1
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n - 1]


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  TSP — DP BITMASK DEMO")
    print("=" * 55)

    dist = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    print(f"Distance matrix: {dist}")
    print(f"TSP min cost: {tsp(dist)}")  # 80

    print(f"\n{'=' * 55}")
    print("  TREE DP DEMO")
    print("=" * 55)

    # Tree:  0 - 1 - 3
    #        |   |
    #        2   4
    adj = [[1, 2], [0, 3, 4], [0], [1], [1]]
    print(f"Tree adj: {adj}")
    print(f"Max Independent Set: {tree_dp_max_independent_set(adj, 5)}")
    print(f"Tree Diameter: {tree_diameter_dp(adj, 5)}")

    print(f"\n{'=' * 55}")
    print("  DIGIT DP DEMO")
    print("=" * 55)

    print(f"Numbers 0..100 containing digit 1: {count_numbers_with_digit(100, 1)}")
    print(f"Numbers 0..1000 containing digit 7: {count_numbers_with_digit(1000, 7)}")

    print(f"\n{'=' * 55}")
    print("  PALINDROMIC SUBSEQUENCE")
    print("=" * 55)

    s = "bbbab"
    print(f"LPS('{s}'): {longest_palindromic_subseq(s)}")

    print(f"\n--- Matrix Chain Multiplication ---")
    dims = [10, 30, 5, 60]
    print(f"Dims: {dims}")
    print(f"Min multiplications: {matrix_chain_order(dims)}")
