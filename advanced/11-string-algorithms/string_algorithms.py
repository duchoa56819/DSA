"""
Chương 11: Thuật Toán Xử Lý Chuỗi Nâng Cao
=============================================
KMP, Rabin-Karp, Z-Algorithm, Aho-Corasick.
"""


# ============================================================
# 1. KMP — Knuth-Morris-Pratt — O(n + m)
# ============================================================

def kmp_build_lps(pattern):
    """
    Xây bảng LPS (Longest Proper Prefix which is also Suffix).

    Ví dụ: pattern = "ABCABD"
    LPS = [0, 0, 0, 1, 2, 0]

    Ý nghĩa: khi mismatch tại vị trí i, ta không cần quay lại
    từ đầu mà nhảy đến lps[i-1] — tiết kiệm rất nhiều so sánh.
    """
    m = len(pattern)
    lps = [0] * m
    length = 0  # Độ dài prefix-suffix dài nhất trước đó
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]  # Không tăng i!
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text, pattern):
    """
    KMP — Tìm tất cả vị trí pattern xuất hiện trong text.

    So với brute-force O(n*m), KMP chạy O(n + m) vì:
    - Không bao giờ quay lại pointer trên text
    - Dùng bảng LPS để nhảy thông minh trên pattern

    Ứng dụng: Tìm kiếm văn bản, DNA matching, plagiarism detection.
    """
    n, m = len(text), len(pattern)
    lps = kmp_build_lps(pattern)
    positions = []

    i = j = 0  # i: pointer trên text, j: pointer trên pattern
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return positions


# ============================================================
# 2. RABIN-KARP — Rolling Hash — O(n + m) average
# ============================================================

def rabin_karp(text, pattern):
    """
    Rabin-Karp — Dùng hàm hash để so sánh nhanh.

    Ý tưởng: Hash(window) == Hash(pattern) → có thể match.
    Rolling hash: Hash mới = (Hash cũ - ký tự đi - ký tự đến) × base

    Ưu điểm: Tìm NHIỀU pattern cùng lúc (plagiarism detection).
    Nhược: Worst case O(n*m) khi nhiều hash collision.
    """
    n, m = len(text), len(pattern)
    if m > n:
        return []

    BASE = 256
    MOD = 10**9 + 7
    positions = []

    # Tính hash của pattern và window đầu tiên
    p_hash = 0
    t_hash = 0
    h = pow(BASE, m - 1, MOD)  # BASE^(m-1) mod MOD

    for i in range(m):
        p_hash = (p_hash * BASE + ord(pattern[i])) % MOD
        t_hash = (t_hash * BASE + ord(text[i])) % MOD

    for i in range(n - m + 1):
        if p_hash == t_hash:
            # Hash match → kiểm tra thật (tránh false positive)
            if text[i:i + m] == pattern:
                positions.append(i)

        # Rolling hash: trượt window sang phải 1 ký tự
        if i < n - m:
            t_hash = ((t_hash - ord(text[i]) * h) * BASE + ord(text[i + m])) % MOD
            if t_hash < 0:
                t_hash += MOD

    return positions


# ============================================================
# 3. Z-ALGORITHM — O(n)
# ============================================================

def z_function(s):
    """
    Z-Algorithm — Z[i] = độ dài chuỗi con bắt đầu tại i
    mà trùng với prefix của s.

    Ví dụ: s = "aabxaab"
    Z = [7, 1, 0, 0, 3, 1, 0]
         ^              ^
         |              aab = prefix "aab" → Z[4]=3
         toàn bộ chuỗi

    Ứng dụng: Pattern matching bằng cách tạo s = pattern + "$" + text
    Nếu Z[i] == len(pattern) → match tại vị trí i - len(pattern) - 1
    """
    n = len(s)
    z = [0] * n
    z[0] = n
    l = r = 0

    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]

    return z


def z_search(text, pattern):
    """Tìm pattern trong text bằng Z-Algorithm."""
    combined = pattern + "$" + text
    z = z_function(combined)
    m = len(pattern)
    return [i - m - 1 for i in range(m + 1, len(combined)) if z[i] == m]


# ============================================================
# 4. SUFFIX ARRAY — O(n log² n)
# ============================================================

def build_suffix_array(s):
    """
    Suffix Array — Mảng chứa các suffix đã sắp xếp.

    Ví dụ: s = "banana"
    Suffixes sorted:
    5: "a"
    3: "ana"
    1: "anana"
    0: "banana"
    4: "na"
    2: "nana"
    SA = [5, 3, 1, 0, 4, 2]

    Ứng dụng: Tìm kiếm substring O(m log n), LCP array,
    DNA analysis, data compression (BWT).
    """
    n = len(s)
    suffixes = [(s[i:], i) for i in range(n)]
    suffixes.sort()
    return [idx for _, idx in suffixes]


def suffix_array_search(text, pattern, sa):
    """Tìm pattern trong text dùng Suffix Array + Binary Search — O(m log n)."""
    n, m = len(text), len(pattern)
    lo, hi = 0, n - 1
    result = []

    # Tìm lower bound
    while lo <= hi:
        mid = (lo + hi) // 2
        suffix = text[sa[mid]:sa[mid] + m]
        if suffix < pattern:
            lo = mid + 1
        else:
            hi = mid - 1

    start = lo

    # Tìm upper bound
    hi = n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        suffix = text[sa[mid]:sa[mid] + m]
        if suffix <= pattern:
            lo = mid + 1
        else:
            hi = mid - 1

    for i in range(start, lo):
        result.append(sa[i])

    return sorted(result)


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  KMP SEARCH DEMO")
    print("=" * 55)

    text = "ABABDABACDABABCABAB"
    pattern = "ABABCABAB"
    lps = kmp_build_lps(pattern)
    positions = kmp_search(text, pattern)
    print(f"Text:    {text}")
    print(f"Pattern: {pattern}")
    print(f"LPS:     {lps}")
    print(f"Found at: {positions}")

    print(f"\n{'=' * 55}")
    print("  RABIN-KARP DEMO")
    print("=" * 55)

    text = "the quick brown fox jumps over the lazy dog the end"
    pattern = "the"
    print(f"Text: '{text}'")
    print(f"Pattern: '{pattern}'")
    print(f"Found at: {rabin_karp(text, pattern)}")

    print(f"\n{'=' * 55}")
    print("  Z-ALGORITHM DEMO")
    print("=" * 55)

    s = "aabxaab"
    print(f"Z-function('{s}'): {z_function(s)}")
    print(f"Z-search 'aab' in 'aabxaabxaab': {z_search('aabxaabxaab', 'aab')}")

    print(f"\n{'=' * 55}")
    print("  SUFFIX ARRAY DEMO")
    print("=" * 55)

    text = "banana"
    sa = build_suffix_array(text)
    print(f"Text: '{text}'")
    print(f"Suffix Array: {sa}")
    print(f"Sorted suffixes:")
    for i in sa:
        print(f"  SA[{i}]: '{text[i:]}'")
    print(f"Search 'ana': positions {suffix_array_search(text, 'ana', sa)}")
