"""
Chương 14: Luồng Trong Mạng (Network Flow)
============================================
Ford-Fulkerson, Edmonds-Karp, Hungarian Algorithm.
"""
from collections import defaultdict, deque


# ============================================================
# 1. FORD-FULKERSON / EDMONDS-KARP — Max Flow
# ============================================================

class MaxFlow:
    """
    Edmonds-Karp = Ford-Fulkerson + BFS tìm augmenting path.

    Bài toán Max Flow:
    - Có đồ thị có hướng, mỗi cạnh có capacity (sức chứa)
    - Tìm luồng LỚN NHẤT từ source (nguồn) đến sink (đích)

    Ứng dụng thực tế:
    1. Mạng giao thông: Lưu lượng xe tối đa
    2. Mạng internet: Bandwidth tối đa
    3. Matching: Ghép đôi tối đa (bipartite matching)
    4. Scheduling: Phân công công việc

    Time: O(V × E²) cho Edmonds-Karp

    Ví dụ:
         s ──10──→ A ──5──→ t
         |              ↑
         └──8──→ B ──7──┘
    Max Flow = 10 + 7 = 12 (nếu edge A-t=12 thay vì 5 thì chỉ 10+7=12 vì bị giới hạn bởi các cạnh khác)
    """

    def __init__(self, n):
        self.n = n
        self.graph = defaultdict(lambda: defaultdict(int))  # capacity

    def add_edge(self, u, v, cap):
        """Thêm cạnh u→v với capacity cap."""
        self.graph[u][v] += cap

    def bfs(self, source, sink, parent):
        """BFS tìm augmenting path (đường tăng luồng)."""
        visited = set([source])
        queue = deque([source])

        while queue:
            u = queue.popleft()
            for v in self.graph[u]:
                if v not in visited and self.graph[u][v] > 0:
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return True
                    queue.append(v)
        return False

    def max_flow(self, source, sink):
        """
        Tìm max flow từ source đến sink.

        Thuật toán:
        1. Tìm đường từ source→sink có capacity > 0 (BFS)
        2. Tìm bottleneck (capacity nhỏ nhất trên đường)
        3. Cập nhật: trừ capacity theo chiều thuận, cộng theo chiều ngược
        4. Lặp lại đến khi không còn đường
        """
        total_flow = 0

        while True:
            parent = {}
            if not self.bfs(source, sink, parent):
                break

            # Tìm bottleneck
            path_flow = float('inf')
            v = sink
            while v != source:
                u = parent[v]
                path_flow = min(path_flow, self.graph[u][v])
                v = u

            # Cập nhật residual graph
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow  # Reverse edge
                v = u

            total_flow += path_flow

        return total_flow


# ============================================================
# 2. BIPARTITE MATCHING — Ghép đôi tối đa
# ============================================================

def max_bipartite_matching(graph, n_left, n_right):
    """
    Ghép đôi tối đa trong đồ thị 2 phía (Bipartite Matching).

    Dùng Hopcroft-Karp hoặc Hungarian.
    Ở đây dùng augmenting path (đơn giản hơn).

    Ví dụ: 3 ứng viên (A,B,C) và 3 công việc (1,2,3).
    A có thể làm 1,2; B làm 1,3; C làm 2.
    Ghép tối đa: A-2, B-1, C-? hoặc A-1, B-3, C-2 → max = 3

    graph[i] = danh sách các đỉnh bên phải mà đỉnh i bên trái nối tới.
    Time: O(V × E)
    """
    match_right = [-1] * n_right  # match_right[j] = i (đỉnh trái ghép với j)

    def dfs(u, visited):
        for v in graph[u]:
            if visited[v]:
                continue
            visited[v] = True
            # Nếu v chưa ghép, hoặc có thể tìm đường khác cho match cũ
            if match_right[v] == -1 or dfs(match_right[v], visited):
                match_right[v] = u
                return True
        return False

    result = 0
    for u in range(n_left):
        visited = [False] * n_right
        if dfs(u, visited):
            result += 1

    return result, match_right


# ============================================================
# 3. MIN-CUT (Định lý Max-Flow Min-Cut)
# ============================================================

def min_cut(n, edges, source, sink):
    """
    Min Cut — Cắt tối thiểu để ngắt source khỏi sink.

    Định lý Max-Flow Min-Cut:
    Max Flow = Min Cut (giá trị luồng cực đại = cắt tối thiểu)

    Sau khi chạy max flow, các đỉnh reachable từ source
    trong residual graph tạo thành 1 phía của min cut.
    """
    mf = MaxFlow(n)
    for u, v, cap in edges:
        mf.add_edge(u, v, cap)

    flow = mf.max_flow(source, sink)

    # Tìm min cut: BFS từ source trong residual graph
    visited = set()
    queue = deque([source])
    visited.add(source)
    while queue:
        u = queue.popleft()
        for v in mf.graph[u]:
            if v not in visited and mf.graph[u][v] > 0:
                visited.add(v)
                queue.append(v)

    # Cut edges: u in visited, v not in visited
    cut_edges = []
    for u, v, cap in edges:
        if u in visited and v not in visited:
            cut_edges.append((u, v, cap))

    return flow, cut_edges


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  MAX FLOW — EDMONDS-KARP DEMO")
    print("=" * 55)

    mf = MaxFlow(6)
    # s=0, t=5
    edges = [(0,1,16),(0,2,13),(1,2,10),(1,3,12),(2,1,4),(2,4,14),(3,2,9),(3,5,20),(4,3,7),(4,5,4)]
    for u, v, c in edges:
        mf.add_edge(u, v, c)

    flow = mf.max_flow(0, 5)
    print(f"Max Flow from 0 to 5: {flow}")  # 23

    print(f"\n{'=' * 55}")
    print("  BIPARTITE MATCHING DEMO")
    print("=" * 55)

    # 3 applicants, 3 jobs
    # A(0) can do jobs 0,1; B(1) can do 0,2; C(2) can do 1
    graph = [[0, 1], [0, 2], [1]]
    matches, match_arr = max_bipartite_matching(graph, 3, 3)
    print(f"Applicant→Job edges: {graph}")
    print(f"Max matching: {matches}")
    print(f"Match (job→applicant): {match_arr}")

    print(f"\n{'=' * 55}")
    print("  MIN CUT DEMO")
    print("=" * 55)

    edges_mc = [(0,1,3),(0,2,2),(1,3,3),(2,3,2),(1,2,1)]
    flow, cuts = min_cut(4, edges_mc, 0, 3)
    print(f"Edges: {edges_mc}")
    print(f"Max Flow = Min Cut = {flow}")
    print(f"Cut edges: {cuts}")
