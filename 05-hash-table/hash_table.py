"""
Chương 5: Hash Table — Bảng Băm
=================================
Triển khai Hash Table và các ứng dụng.
"""


# ============================================================
# 1. HASH TABLE — Cài đặt thủ công
# ============================================================

class HashTable:
    """
    Hash Table dùng Separate Chaining (mỗi bucket là 1 list).

    Hash Function: key → index trong mảng
    Collision: 2 key khác nhau cho cùng index → dùng chaining

    Ví dụ:
    Buckets:
    [0] → []
    [1] → [("cat", 5)]
    [2] → [("dog", 3), ("god", 7)]   ← Collision!
    [3] → []
    [4] → [("bat", 1)]
    """

    def __init__(self, capacity=16, load_factor=0.75):
        self.capacity = capacity
        self.load_factor = load_factor
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def _hash(self, key):
        """Hash function: chuyển key thành index."""
        return hash(key) % self.capacity

    def put(self, key, value):
        """Thêm/cập nhật — O(1) average."""
        idx = self._hash(key)
        bucket = self.buckets[idx]

        # Kiểm tra key đã tồn tại
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Cập nhật
                return

        bucket.append((key, value))  # Thêm mới
        self.size += 1

        # Rehash nếu load factor quá cao
        if self.size / self.capacity > self.load_factor:
            self._rehash()

    def get(self, key, default=None):
        """Lấy giá trị — O(1) average."""
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return default

    def remove(self, key):
        """Xóa — O(1) average."""
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def contains(self, key):
        """Kiểm tra key tồn tại — O(1) average."""
        return self.get(key) is not None

    def _rehash(self):
        """Tăng gấp đôi capacity và hash lại tất cả."""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)

    def __str__(self):
        items = []
        for bucket in self.buckets:
            for k, v in bucket:
                items.append(f"{k}: {v}")
        return "{" + ", ".join(items) + "}"

    def __len__(self):
        return self.size


# ============================================================
# 2. BÀI TOÁN KINH ĐIỂN VỚI HASH MAP
# ============================================================

def two_sum_hash(nums, target):
    """
    Two Sum (LeetCode #1) — O(n) với Hash Map.
    Lưu {giá_trị: index}, tìm complement.
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


def group_anagrams(strs):
    """
    LeetCode #49 — Gom nhóm anagram.
    Key = sorted string, Value = list of anagrams.
    """
    from collections import defaultdict
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))  # "eat" → "aet", "tea" → "aet"
        groups[key].append(s)
    return list(groups.values())


def longest_consecutive(nums):
    """
    LeetCode #128 — Dãy số liên tiếp dài nhất — O(n).
    Dùng HashSet: chỉ bắt đầu đếm từ đầu dãy (num-1 không tồn tại).
    """
    num_set = set(nums)
    max_length = 0

    for num in num_set:
        # Chỉ bắt đầu đếm nếu num là đầu dãy
        if num - 1 not in num_set:
            length = 1
            while num + length in num_set:
                length += 1
            max_length = max(max_length, length)

    return max_length


def first_unique_char(s):
    """
    LeetCode #387 — Ký tự đầu tiên không lặp lại.
    Đếm frequency bằng hash map.
    """
    from collections import Counter
    count = Counter(s)
    for i, char in enumerate(s):
        if count[char] == 1:
            return i
    return -1


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("  HASH TABLE DEMO")
    print("=" * 50)

    ht = HashTable()
    data = {"apple": 5, "banana": 3, "cherry": 8, "date": 2}
    for k, v in data.items():
        ht.put(k, v)

    print(f"Hash Table: {ht}")
    print(f"get('apple'): {ht.get('apple')}")
    print(f"get('grape'): {ht.get('grape', 'Not found')}")
    print(f"contains('banana'): {ht.contains('banana')}")

    ht.remove("banana")
    print(f"After remove('banana'): {ht}")

    print(f"\n{'=' * 50}")
    print("  BÀI TOÁN HASH MAP")
    print("=" * 50)

    # Group Anagrams
    strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    print(f"\nGroup Anagrams {strs}:")
    for group in group_anagrams(strs):
        print(f"  {group}")

    # Longest Consecutive
    nums = [100, 4, 200, 1, 3, 2]
    print(f"\nLongest Consecutive in {nums}: {longest_consecutive(nums)}")

    # First Unique Char
    s = "leetcode"
    print(f"First unique in '{s}': index {first_unique_char(s)}")
