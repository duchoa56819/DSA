"""
Chương 15: Hình Học Tính Toán (Computational Geometry)
=======================================================
Convex Hull, Line Intersection, Closest Pair of Points.
"""
import math


# ============================================================
# 1. CÁC PHÉP TOÁN CƠ BẢN
# ============================================================

def cross_product(O, A, B):
    """
    Tích có hướng OA × OB.
    > 0: B nằm bên TRÁI OA (ngược chiều kim đồng hồ)
    = 0: Thẳng hàng
    < 0: B nằm bên PHẢI OA (theo chiều kim đồng hồ)
    """
    return (A[0] - O[0]) * (B[1] - O[1]) - (A[1] - O[1]) * (B[0] - O[0])


def distance(A, B):
    """Khoảng cách Euclidean giữa 2 điểm."""
    return math.sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2)


def on_segment(p, q, r):
    """Kiểm tra q nằm trên đoạn pr."""
    return (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
            min(p[1], r[1]) <= q[1] <= max(p[1], r[1]))


# ============================================================
# 2. CONVEX HULL — Bao lồi (Andrew's Monotone Chain)
# ============================================================

def convex_hull(points):
    """
    Convex Hull — Tìm bao lồi của tập điểm.

    Bao lồi = đa giác lồi nhỏ nhất chứa tất cả các điểm.
    Hình dung: Đóng đinh vào các điểm, dùng dây thun bao quanh.

    Andrew's Monotone Chain — O(n log n):
    1. Sort theo x (rồi y)
    2. Xây lower hull (đi từ trái sang phải)
    3. Xây upper hull (đi từ phải sang trái)

    Ứng dụng: Collision detection, Image processing, GIS.
    """
    points = sorted(set(points))
    if len(points) <= 1:
        return points

    # Lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]


# ============================================================
# 3. LINE SEGMENT INTERSECTION
# ============================================================

def segments_intersect(p1, p2, p3, p4):
    """
    Kiểm tra 2 đoạn thẳng (p1,p2) và (p3,p4) có cắt nhau không.

    Dùng cross product:
    - d1 = cross(p3,p4, p1): p1 nằm bên nào của p3p4?
    - d2 = cross(p3,p4, p2): p2 nằm bên nào?
    - Nếu d1 và d2 khác dấu → p1,p2 nằm 2 bên p3p4
    - Tương tự kiểm tra ngược lại
    """
    d1 = cross_product(p3, p4, p1)
    d2 = cross_product(p3, p4, p2)
    d3 = cross_product(p1, p2, p3)
    d4 = cross_product(p1, p2, p4)

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True

    # Collinear cases
    if d1 == 0 and on_segment(p3, p1, p4): return True
    if d2 == 0 and on_segment(p3, p2, p4): return True
    if d3 == 0 and on_segment(p1, p3, p2): return True
    if d4 == 0 and on_segment(p1, p4, p2): return True

    return False


# ============================================================
# 4. CLOSEST PAIR OF POINTS — O(n log n)
# ============================================================

def closest_pair(points):
    """
    Tìm cặp điểm gần nhất — Divide & Conquer O(n log n).

    Brute-force: O(n²) — so sánh mọi cặp
    D&C: Chia điểm thành 2 nửa, tìm min mỗi nửa,
         rồi kiểm tra các điểm gần đường chia.

    Ứng dụng: Clustering, nearest neighbor, GIS.
    """
    def _closest_rec(pts_x, pts_y):
        n = len(pts_x)
        if n <= 3:
            return _brute_force(pts_x)

        mid = n // 2
        mid_point = pts_x[mid]

        # Chia thành 2 nửa
        yl = [p for p in pts_y if p[0] <= mid_point[0]]
        yr = [p for p in pts_y if p[0] > mid_point[0]]

        dl = _closest_rec(pts_x[:mid], yl)
        dr = _closest_rec(pts_x[mid:], yr)
        d = min(dl, dr)

        # Kiểm tra strip (vùng gần đường chia)
        strip = [p for p in pts_y if abs(p[0] - mid_point[0]) < d]
        return min(d, _strip_closest(strip, d))

    def _brute_force(pts):
        min_d = float('inf')
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                min_d = min(min_d, distance(pts[i], pts[j]))
        return min_d

    def _strip_closest(strip, d):
        min_d = d
        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and (strip[j][1] - strip[i][1]) < min_d:
                min_d = min(min_d, distance(strip[i], strip[j]))
                j += 1
        return min_d

    pts_x = sorted(points, key=lambda p: p[0])
    pts_y = sorted(points, key=lambda p: p[1])
    return _closest_rec(pts_x, pts_y)


# ============================================================
# 5. POLYGON AREA — Diện tích đa giác (Shoelace formula)
# ============================================================

def polygon_area(vertices):
    """
    Diện tích đa giác dùng công thức Shoelace.
    vertices = [(x1,y1), (x2,y2), ...] theo thứ tự.
    """
    n = len(vertices)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    return abs(area) / 2


def point_in_polygon(point, polygon):
    """
    Kiểm tra điểm nằm trong đa giác (Ray Casting algorithm).
    Bắn tia từ point sang phải, đếm số lần cắt cạnh.
    Lẻ → trong, Chẵn → ngoài.
    """
    x, y = point
    n = len(polygon)
    inside = False

    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i

    return inside


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  CONVEX HULL DEMO")
    print("=" * 55)

    points = [(0,0),(1,1),(2,2),(0,2),(2,0),(1,0),(0,1),(2,1),(1,2)]
    hull = convex_hull(points)
    print(f"Points: {points}")
    print(f"Convex Hull: {hull}")

    print(f"\n{'=' * 55}")
    print("  LINE INTERSECTION DEMO")
    print("=" * 55)

    print(f"(0,0)-(2,2) x (0,2)-(2,0): {segments_intersect((0,0),(2,2),(0,2),(2,0))}")
    print(f"(0,0)-(1,1) x (2,2)-(3,3): {segments_intersect((0,0),(1,1),(2,2),(3,3))}")

    print(f"\n{'=' * 55}")
    print("  CLOSEST PAIR DEMO")
    print("=" * 55)

    points = [(2,3),(12,30),(40,50),(5,1),(12,10),(3,4)]
    print(f"Points: {points}")
    print(f"Closest pair distance: {closest_pair(points):.4f}")

    print(f"\n{'=' * 55}")
    print("  POLYGON DEMO")
    print("=" * 55)

    square = [(0,0),(4,0),(4,4),(0,4)]
    print(f"Square {square}")
    print(f"Area: {polygon_area(square)}")
    print(f"(2,2) inside: {point_in_polygon((2,2), square)}")
    print(f"(5,5) inside: {point_in_polygon((5,5), square)}")
