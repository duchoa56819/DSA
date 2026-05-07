"""
Chương 10: Thuật Toán Đồ Thị Nâng Cao
========================================
Dijkstra, Bellman-Ford, Floyd-Warshall, MST, Union-Find.
"""
import heapq
from collections import defaultdict


# ============================================================
# 1. DIJKSTRA — Đường đi ngắn nhất (weighted, non-negative)
# ============================================================

def dijkstra(graph, start):
    """
    Dijkstra — Tìm đường đi ngắn nhất từ start đến MỌI đỉnh.

    Yêu cầu: Trọng số KHÔNG ÂM!
    Time: O((V + E) log V) với priority queue

    Ý tưởng:
    1. Bắt đầu: dist[start] = 0, dist[others] = ∞
    2. Luôn xử lý đỉnh có dist NHỎ NHẤT (dùng min-heap)
    3. Relax: nếu dist[u] + w(u,v) < dist[v] → cập nhật

    graph: {node: [(neighbor, weight), ...]}
    """
    dist = {start: 0}
    prev = {start: None}
    heap = [(0, start)]  # (distance, node)
    visited = set()

    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)

        for v, weight in graph.get(u, []):
            if v not in visited:
                new_dist = d + weight
                if new_dist < dist.get(v, float('inf')):
                    dist[v] = new_dist
                    prev[v] = u
                    heapq.heappush(heap, (new_dist, v))

    return dist, prev


def reconstruct_path(prev, target):
    """Truy vết đường đi từ prev dictionary."""
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = prev.get(current)
    return path[::-1]


# ============================================================
# 2. BELLMAN-FORD — Cho phép trọng số ÂM
# ============================================================

def bellman_ford(n, edges, start):
    """
    Bellman-Ford — Xử lý được trọng số âm!
    Phát hiện negative cycle.

    Time: O(V * E) — chậm hơn Dijkstra
    edges: [(u, v, weight), ...]
    """
    dist = [float('inf')] * n
    dist[start] = 0

    # Relax V-1 lần
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Kiểm tra negative cycle (lần thứ V)
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None  # Có negative cycle!

    return dist


# ============================================================
# 3. FLOYD-WARSHALL — All-pairs shortest path
# ============================================================

def floyd_warshall(n, edges):
    """
    Floyd-Warshall — Đường đi ngắn nhất giữa MỌI CẶP đỉnh.

    Time: O(V³)  Space: O(V²)
    Đơn giản: 3 vòng lặp lồng nhau!

    dp[i][j] = min distance from i to j
    dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j]) cho mọi k
    """
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0

    for u, v, w in edges:
        dist[u][v] = w

    for k in range(n):          # Đỉnh trung gian
        for i in range(n):      # Nguồn
            for j in range(n):  # Đích
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist


# ============================================================
# 4. UNION-FIND (Disjoint Set Union — DSU)
# ============================================================

class UnionFind:
    """
    Union-Find — Quản lý tập hợp không giao nhau.

    Ứng dụng:
    1. Kruskal MST
    2. Detect cycle trong undirected graph
    3. Connected components
    4. Network connectivity

    Tối ưu:
    - Path compression: Nén đường đi → find gần O(1)
    - Union by rank: Gắn cây nhỏ vào cây lớn

    Amortized: O(α(n)) ≈ O(1) cho mỗi thao tác!
    """

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        """Tìm đại diện (root) của tập chứa x — Path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Nén!
        return self.parent[x]

    def union(self, x, y):
        """Hợp nhất 2 tập — Union by rank."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # Đã cùng tập

        # Gắn cây nhỏ vào cây lớn
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

        self.components -= 1
        return True

    def connected(self, x, y):
        """Kiểm tra 2 phần tử cùng tập."""
        return self.find(x) == self.find(y)


# ============================================================
# 5. KRUSKAL — Minimum Spanning Tree (MST)
# ============================================================

def kruskal(n, edges):
    """
    Kruskal — Cây khung nhỏ nhất.

    Greedy: Sắp xếp cạnh theo trọng số tăng dần.
    Lần lượt thêm cạnh nếu không tạo cycle (dùng Union-Find).

    Time: O(E log E)

    Ví dụ:
        0 ---2--- 1
        |         |
        3    1    4
        |         |
        2 ---5--- 3

    MST: 0-1(2), 1-3(4), 2-0(3) → tổng = 9
    (không lấy 2-3(5) vì tạo cycle)
    """
    edges.sort(key=lambda x: x[2])  # Sort by weight
    uf = UnionFind(n)
    mst = []
    total_weight = 0

    for u, v, w in edges:
        if uf.union(u, v):  # Không tạo cycle
            mst.append((u, v, w))
            total_weight += w
            if len(mst) == n - 1:
                break

    return mst, total_weight


# ============================================================
# 6. PRIM — MST (alternative)
# ============================================================

def prim(graph, start=0):
    """
    Prim — MST bằng cách mở rộng cây từ 1 đỉnh.
    Dùng priority queue, tương tự Dijkstra.

    Time: O((V + E) log V)
    graph: {node: [(neighbor, weight), ...]}
    """
    visited = set([start])
    heap = [(w, start, v) for v, w in graph.get(start, [])]
    heapq.heapify(heap)
    mst = []
    total_weight = 0

    while heap and len(visited) < len(graph):
        w, u, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        mst.append((u, v, w))
        total_weight += w

        for neighbor, weight in graph.get(v, []):
            if neighbor not in visited:
                heapq.heappush(heap, (weight, v, neighbor))

    return mst, total_weight


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  DIJKSTRA DEMO")
    print("=" * 55)

    graph = {
        'A': [('B', 4), ('C', 1)],
        'B': [('A', 4), ('C', 2), ('D', 5)],
        'C': [('A', 1), ('B', 2), ('D', 8)],
        'D': [('B', 5), ('C', 8)],
    }

    dist, prev = dijkstra(graph, 'A')
    print(f"Shortest distances from A: {dist}")
    print(f"Path A → D: {reconstruct_path(prev, 'D')}")

    print(f"\n{'=' * 55}")
    print("  BELLMAN-FORD DEMO")
    print("=" * 55)

    edges_bf = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 5), (2, 3, 8)]
    dist_bf = bellman_ford(4, edges_bf, 0)
    print(f"Edges: {edges_bf}")
    print(f"Distances from 0: {dist_bf}")

    print(f"\n{'=' * 55}")
    print("  FLOYD-WARSHALL DEMO")
    print("=" * 55)

    edges_fw = [(0, 1, 4), (0, 2, 1), (1, 3, 5), (2, 1, 2), (2, 3, 8)]
    dist_fw = floyd_warshall(4, edges_fw)
    print("All-pairs shortest paths:")
    for i, row in enumerate(dist_fw):
        print(f"  From {i}: {row}")

    print(f"\n{'=' * 55}")
    print("  KRUSKAL MST DEMO")
    print("=" * 55)

    edges_mst = [(0, 1, 2), (0, 2, 3), (1, 3, 4), (2, 3, 5), (1, 2, 1)]
    mst, weight = kruskal(4, edges_mst)
    print(f"Edges: {edges_mst}")
    print(f"MST: {mst}")
    print(f"Total weight: {weight}")

    print(f"\n{'=' * 55}")
    print("  UNION-FIND DEMO")
    print("=" * 55)

    uf = UnionFind(6)
    unions = [(0, 1), (2, 3), (4, 5), (0, 2), (1, 5)]
    for u, v in unions:
        uf.union(u, v)
        print(f"  Union({u}, {v}) → components = {uf.components}")
    print(f"  Connected(0, 5): {uf.connected(0, 5)}")
    print(f"  Connected(0, 4): {uf.connected(0, 4)}")
