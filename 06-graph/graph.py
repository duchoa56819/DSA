"""
Chương 6: Đồ Thị (Graph) — Cơ bản
====================================
Biểu diễn đồ thị, BFS, DFS, Topological Sort.
"""
from collections import deque, defaultdict


# ============================================================
# 1. BIỂU DIỄN ĐỒ THỊ
# ============================================================

class Graph:
    """
    Đồ thị dùng Adjacency List.

    Ví dụ đồ thị vô hướng:
        0 --- 1
        |     |
        3 --- 2

    Adjacency List:
    0: [1, 3]
    1: [0, 2]
    2: [1, 3]
    3: [0, 2]

    So sánh với Adjacency Matrix (ma trận kề):
        0  1  2  3
    0 [ 0, 1, 0, 1 ]
    1 [ 1, 0, 1, 0 ]
    2 [ 0, 1, 0, 1 ]
    3 [ 1, 0, 1, 0 ]

    Adjacency List tốt hơn khi đồ thị thưa (sparse).
    Adjacency Matrix tốt hơn khi đồ thị dày (dense).
    """

    def __init__(self, directed=False):
        self.adj = defaultdict(list)
        self.directed = directed

    def add_edge(self, u, v, weight=1):
        """Thêm cạnh."""
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def get_neighbors(self, u):
        """Lấy các đỉnh kề."""
        return self.adj[u]

    def get_vertices(self):
        """Lấy tất cả đỉnh."""
        return list(self.adj.keys())


# ============================================================
# 2. BFS — Breadth-First Search (Duyệt theo chiều rộng)
# ============================================================

def bfs(graph, start):
    """
    BFS — Duyệt đồ thị theo tầng dùng Queue.

    Ứng dụng:
    1. Tìm đường đi ngắn nhất (unweighted)
    2. Level-order traversal
    3. Kiểm tra đồ thị 2 phía (bipartite)
    4. Tìm connected components

    Time: O(V + E), Space: O(V)

    Ví dụ: BFS từ 0
        0 --- 1 --- 4
        |     |
        3 --- 2

    Thứ tự: 0 → 1, 3 → 2, 4 (theo tầng)
    """
    visited = set([start])
    queue = deque([start])
    order = []

    while queue:
        vertex = queue.popleft()
        order.append(vertex)

        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


def bfs_shortest_path(graph, start, end):
    """Tìm đường đi ngắn nhất (unweighted) bằng BFS."""
    visited = set([start])
    queue = deque([(start, [start])])  # (node, path)

    while queue:
        vertex, path = queue.popleft()
        if vertex == end:
            return path

        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None  # Không tìm thấy


# ============================================================
# 3. DFS — Depth-First Search (Duyệt theo chiều sâu)
# ============================================================

def dfs_recursive(graph, start, visited=None):
    """
    DFS đệ quy — đi sâu nhất có thể trước khi quay lui.

    Ứng dụng:
    1. Detect cycle
    2. Topological sort
    3. Connected components
    4. Maze solving
    5. Backtracking problems

    Time: O(V + E), Space: O(V)
    """
    if visited is None:
        visited = set()

    visited.add(start)
    order = [start]

    for neighbor, _ in graph.get_neighbors(start):
        if neighbor not in visited:
            order.extend(dfs_recursive(graph, neighbor, visited))

    return order


def dfs_iterative(graph, start):
    """DFS dùng Stack (không đệ quy)."""
    visited = set()
    stack = [start]
    order = []

    while stack:
        vertex = stack.pop()
        if vertex in visited:
            continue
        visited.add(vertex)
        order.append(vertex)

        for neighbor, _ in graph.get_neighbors(vertex):
            if neighbor not in visited:
                stack.append(neighbor)

    return order


# ============================================================
# 4. DETECT CYCLE
# ============================================================

def has_cycle_undirected(graph):
    """Phát hiện chu trình trong đồ thị vô hướng."""
    visited = set()

    def dfs(node, parent):
        visited.add(node)
        for neighbor, _ in graph.get_neighbors(node):
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True  # Cycle!
        return False

    for vertex in graph.get_vertices():
        if vertex not in visited:
            if dfs(vertex, -1):
                return True
    return False


def has_cycle_directed(graph):
    """Phát hiện chu trình trong đồ thị có hướng (3 màu)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(int)  # Default WHITE

    def dfs(node):
        color[node] = GRAY  # Đang xử lý
        for neighbor, _ in graph.get_neighbors(node):
            if color[neighbor] == GRAY:
                return True  # Back edge = cycle!
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        color[node] = BLACK  # Xong
        return False

    for vertex in graph.get_vertices():
        if color[vertex] == WHITE:
            if dfs(vertex):
                return True
    return False


# ============================================================
# 5. TOPOLOGICAL SORT
# ============================================================

def topological_sort(graph):
    """
    Topological Sort — Sắp xếp topo cho DAG (Directed Acyclic Graph).

    Ví dụ: Thứ tự học môn học
    Math → Physics → Engineering
    Math → CS
    CS → AI

    Topo sort: Math, CS, Physics, AI, Engineering
    (Mỗi môn phải học SAU các môn prerequisite)
    """
    visited = set()
    stack = []

    def dfs(node):
        visited.add(node)
        for neighbor, _ in graph.get_neighbors(node):
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)  # Thêm SAU khi xử lý hết con

    for vertex in graph.get_vertices():
        if vertex not in visited:
            dfs(vertex)

    return stack[::-1]  # Đảo ngược


def topological_sort_kahn(graph):
    """Topological Sort bằng BFS (Kahn's Algorithm) — dùng in-degree."""
    in_degree = defaultdict(int)
    for u in graph.get_vertices():
        for v, _ in graph.get_neighbors(u):
            in_degree[v] += 1

    queue = deque([v for v in graph.get_vertices() if in_degree[v] == 0])
    order = []

    while queue:
        vertex = queue.popleft()
        order.append(vertex)
        for neighbor, _ in graph.get_neighbors(vertex):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == len(graph.get_vertices()) else []  # [] = có cycle


# ============================================================
# 6. CONNECTED COMPONENTS
# ============================================================

def count_connected_components(graph):
    """Đếm số thành phần liên thông."""
    visited = set()
    count = 0

    for vertex in graph.get_vertices():
        if vertex not in visited:
            # BFS/DFS để đánh dấu toàn bộ component
            queue = deque([vertex])
            while queue:
                node = queue.popleft()
                if node in visited:
                    continue
                visited.add(node)
                for neighbor, _ in graph.get_neighbors(node):
                    if neighbor not in visited:
                        queue.append(neighbor)
            count += 1

    return count


# ============================================================
# DEMO
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("  GRAPH — BFS & DFS DEMO")
    print("=" * 50)

    # Đồ thị vô hướng
    g = Graph(directed=False)
    edges = [(0, 1), (0, 3), (1, 2), (1, 4), (2, 3)]
    for u, v in edges:
        g.add_edge(u, v)

    print(f"Edges: {edges}")
    print(f"BFS from 0: {bfs(g, 0)}")
    print(f"DFS from 0: {dfs_recursive(g, 0)}")
    print(f"Shortest 0→4: {bfs_shortest_path(g, 0, 4)}")
    print(f"Has cycle: {has_cycle_undirected(g)}")
    print(f"Components: {count_connected_components(g)}")

    # Topological Sort (DAG)
    print(f"\n{'=' * 50}")
    print("  TOPOLOGICAL SORT DEMO")
    print("=" * 50)

    dag = Graph(directed=True)
    # Course prerequisites
    courses = [("Math", "Physics"), ("Math", "CS"),
               ("Physics", "Engineering"), ("CS", "AI")]
    for u, v in courses:
        dag.add_edge(u, v)

    print(f"Prerequisites: {courses}")
    print(f"Topological order (DFS): {topological_sort(dag)}")
    print(f"Topological order (BFS): {topological_sort_kahn(dag)}")
    print(f"Has cycle: {has_cycle_directed(dag)}")
