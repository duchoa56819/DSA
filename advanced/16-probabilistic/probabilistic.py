"""
Chương 16: Cấu Trúc Xác Suất & Nâng Cao Khác
================================================
Bloom Filter, Reservoir Sampling, Bit Manipulation nâng cao.
"""
import hashlib
import random
import math


# ============================================================
# 1. BLOOM FILTER — Kiểm tra phần tử "có thể có" trong tập
# ============================================================

class BloomFilter:
    """
    Bloom Filter — Cấu trúc dữ liệu xác suất.

    Trả lời: "Phần tử có trong tập không?"
    - "Chắc chắn KHÔNG" → 100% chính xác
    - "Có thể CÓ"       → có xác suất sai (false positive)

    Ưu điểm: Cực kỳ tiết kiệm bộ nhớ! 1 tỷ phần tử chỉ cần ~1.2 GB.
    So với HashSet: 1 tỷ phần tử cần hàng chục GB.

    Ứng dụng:
    1. Web crawler: URL đã crawl chưa?
    2. Database: Tránh đọc disk nếu key chắc chắn không tồn tại
    3. Spam filter: Email này có phải spam?
    4. Blockchain: Bitcoin SPV nodes

    Cách hoạt động:
    - Bit array kích thước m
    - k hàm hash khác nhau
    - Insert: Set k bits = 1
    - Query: Kiểm tra k bits, nếu tất cả = 1 → "có thể có"
    """

    def __init__(self, expected_items, false_positive_rate=0.01):
        # Tính kích thước tối ưu
        self.m = self._optimal_size(expected_items, false_positive_rate)
        self.k = self._optimal_hash_count(self.m, expected_items)
        self.bit_array = [False] * self.m
        self.count = 0

    def _optimal_size(self, n, p):
        """m = -(n * ln(p)) / (ln(2))²"""
        return int(-n * math.log(p) / (math.log(2) ** 2))

    def _optimal_hash_count(self, m, n):
        """k = (m/n) * ln(2)"""
        return max(1, int((m / n) * math.log(2)))

    def _hashes(self, item):
        """Tạo k hash values từ item."""
        hashes = []
        for i in range(self.k):
            h = hashlib.md5(f"{item}_{i}".encode()).hexdigest()
            hashes.append(int(h, 16) % self.m)
        return hashes

    def add(self, item):
        """Thêm phần tử — O(k)."""
        for pos in self._hashes(item):
            self.bit_array[pos] = True
        self.count += 1

    def might_contain(self, item):
        """Kiểm tra — O(k). True = "có thể có", False = "chắc chắn không"."""
        return all(self.bit_array[pos] for pos in self._hashes(item))

    def false_positive_rate(self):
        """Tỷ lệ false positive thực tế."""
        ones = sum(self.bit_array)
        return (ones / self.m) ** self.k


# ============================================================
# 2. RESERVOIR SAMPLING — Lấy mẫu ngẫu nhiên từ stream
# ============================================================

def reservoir_sampling(stream, k):
    """
    Reservoir Sampling — Chọn k phần tử ngẫu nhiên đều từ stream.

    Bài toán: Dữ liệu đến liên tục (stream), không biết trước
    kích thước n. Chọn k phần tử sao cho mỗi phần tử có
    xác suất k/n được chọn.

    Thuật toán (Vitter's Algorithm R):
    1. Lấy k phần tử đầu tiên vào reservoir
    2. Với phần tử thứ i (i > k):
       - Random j trong [0, i]
       - Nếu j < k: thay reservoir[j] = stream[i]

    Chứng minh: P(phần tử i được chọn) = k/n cho mọi i.

    Ứng dụng: Big data sampling, A/B testing, random playlist.
    """
    reservoir = []

    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        else:
            j = random.randint(0, i)
            if j < k:
                reservoir[j] = item

    return reservoir


# ============================================================
# 3. BIT MANIPULATION NÂNG CAO
# ============================================================

def count_set_bits(n):
    """Đếm số bit 1 — Brian Kernighan's algorithm O(number of 1s)."""
    count = 0
    while n:
        n &= n - 1  # Xóa bit 1 thấp nhất
        count += 1
    return count


def is_power_of_two(n):
    """Kiểm tra n là lũy thừa của 2 — O(1)."""
    return n > 0 and (n & (n - 1)) == 0


def find_single_number(nums):
    """
    LeetCode #136 — Tìm số xuất hiện 1 lần (các số khác xuất hiện 2 lần).
    XOR tất cả: a ^ a = 0, a ^ 0 = a → chỉ còn lại số lẻ.
    """
    result = 0
    for num in nums:
        result ^= num
    return result


def find_two_single_numbers(nums):
    """
    LeetCode #260 — 2 số xuất hiện 1 lần, còn lại 2 lần.

    1. XOR tất cả → xor = a ^ b (a, b là 2 số cần tìm)
    2. Tìm bit khác nhau giữa a và b (rightmost set bit)
    3. Chia nums thành 2 nhóm dựa trên bit đó
    4. XOR mỗi nhóm → ra a và b
    """
    xor = 0
    for num in nums:
        xor ^= num

    # Tìm rightmost set bit
    diff_bit = xor & (-xor)

    a = b = 0
    for num in nums:
        if num & diff_bit:
            a ^= num
        else:
            b ^= num

    return [a, b]


def subsets_bitmask(nums):
    """
    Liệt kê tất cả tập con dùng bitmask.
    n phần tử → 2^n tập con.
    mask = 0b101 → chọn phần tử index 0 và 2.
    """
    n = len(nums)
    result = []
    for mask in range(1 << n):
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result


# ============================================================
# 4. MONOTONIC STACK — Stack đơn điệu
# ============================================================

def next_greater_element(nums):
    """
    Tìm phần tử lớn hơn tiếp theo cho mỗi phần tử.
    [2, 1, 2, 4, 3] → [4, 2, 4, -1, -1]

    Dùng Monotonic Stack (stack giảm dần):
    - Duyệt từ phải sang trái
    - Pop các phần tử nhỏ hơn current ra khỏi stack
    - Top of stack = next greater element

    O(n) — mỗi phần tử push/pop tối đa 1 lần!
    """
    n = len(nums)
    result = [-1] * n
    stack = []  # Stack chứa index, duy trì giảm dần

    for i in range(n - 1, -1, -1):
        while stack and nums[stack[-1]] <= nums[i]:
            stack.pop()
        if stack:
            result[i] = nums[stack[-1]]
        stack.append(i)

    return result


def largest_rectangle_histogram(heights):
    """
    LeetCode #84 — Hình chữ nhật lớn nhất trong histogram.
    Dùng Monotonic Stack — O(n).

    Ý tưởng: Với mỗi cột, tìm cột nhỏ hơn gần nhất bên trái và phải.
    Width = right_smaller - left_smaller - 1
    Area = height * width
    """
    stack = []  # Stack tăng dần
    max_area = 0
    heights = heights + [0]  # Sentinel

    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i - stack[-1] - 1 if stack else i
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  BLOOM FILTER DEMO")
    print("=" * 55)

    bf = BloomFilter(1000, 0.01)
    words = ["apple", "banana", "cherry", "date", "elderberry"]
    for w in words:
        bf.add(w)

    print(f"Added: {words}")
    print(f"Bits: {bf.m}, Hash functions: {bf.k}")
    print(f"'apple' might exist:  {bf.might_contain('apple')}")    # True
    print(f"'grape' might exist:  {bf.might_contain('grape')}")    # False (probably)
    print(f"'banana' might exist: {bf.might_contain('banana')}")   # True

    print(f"\n{'=' * 55}")
    print("  RESERVOIR SAMPLING DEMO")
    print("=" * 55)

    stream = range(1, 101)  # 1 to 100
    sample = reservoir_sampling(stream, 5)
    print(f"Stream: 1..100")
    print(f"Random sample of 5: {sample}")

    print(f"\n{'=' * 55}")
    print("  BIT MANIPULATION DEMO")
    print("=" * 55)

    print(f"Count bits in 13 (1101): {count_set_bits(13)}")
    print(f"Is 16 power of 2: {is_power_of_two(16)}")
    print(f"Is 15 power of 2: {is_power_of_two(15)}")
    print(f"Single number in [2,3,2,4,4]: {find_single_number([2,3,2,4,4])}")
    print(f"Two singles in [1,2,1,3,2,5]: {find_two_single_numbers([1,2,1,3,2,5])}")
    print(f"Subsets of [1,2,3]: {subsets_bitmask([1,2,3])}")

    print(f"\n{'=' * 55}")
    print("  MONOTONIC STACK DEMO")
    print("=" * 55)

    nums = [2, 1, 2, 4, 3]
    print(f"Next greater of {nums}: {next_greater_element(nums)}")

    heights = [2, 1, 5, 6, 2, 3]
    print(f"Largest rectangle in {heights}: {largest_rectangle_histogram(heights)}")
