import heapq

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)


class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, first, second):
        first_root, second_root = self.find(first), self.find(second)
        if first_root == second_root:
            return False
        if self.rank[first_root] < self.rank[second_root]:
            first_root, second_root = second_root, first_root
        self.parent[second_root] = first_root
        if self.rank[first_root] == self.rank[second_root]:
            self.rank[first_root] += 1
        return True


def validate_graph(vertex_count, edges):
    if vertex_count < 2:
        raise ValueError("Enter at least two vertices.")
    for first, second, _ in edges:
        if not (0 <= first < vertex_count and 0 <= second < vertex_count):
            raise ValueError(f"Vertices must be in the range 0 to {vertex_count - 1}.")


def kruskal(vertex_count, edges):
    validate_graph(vertex_count, edges)
    union_find, tree, cost = UnionFind(vertex_count), [], 0
    for weight, first, second in sorted((weight, first, second) for first, second, weight in edges):
        if first != second and union_find.union(first, second):
            tree.append([first, second, weight])
            cost += weight
            if len(tree) == vertex_count - 1:
                break
    if len(tree) != vertex_count - 1:
        raise ValueError("The graph is disconnected; an MST does not exist.")
    return tree, cost


def prim(vertex_count, edges, start=0):
    validate_graph(vertex_count, edges)
    if not 0 <= start < vertex_count:
        raise ValueError("The start vertex is outside the graph.")
    adjacency = [[] for _ in range(vertex_count)]
    for first, second, weight in edges:
        if first != second:
            adjacency[first].append((second, weight))
            adjacency[second].append((first, weight))
    queue, visited, tree, cost = [(0, start, -1)], set(), [], 0
    while queue and len(tree) < vertex_count - 1:
        weight, node, parent = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        if parent != -1:
            tree.append([parent, node, weight])
            cost += weight
        for neighbor, edge_weight in adjacency[node]:
            if neighbor not in visited:
                heapq.heappush(queue, (edge_weight, neighbor, node))
    if len(tree) != vertex_count - 1:
        raise ValueError("The graph is disconnected; an MST does not exist.")
    return tree, cost


def parse_edges(raw_edges):
    edges = []
    for raw in raw_edges:
        if len(raw) != 3:
            raise ValueError("Each edge must contain from, to, and weight.")
        edges.append((int(raw[0]), int(raw[1]), float(raw[2])))
    if not edges:
        raise ValueError("Enter at least one edge.")
    return edges


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/mst")
def build_mst():
    try:
        data = request.get_json(silent=True) or {}
        vertex_count = int(data.get("vertex_count", 0))
        edges = parse_edges(data.get("edges", []))
        start = int(data.get("start", 0))
        kruskal_edges, kruskal_cost = kruskal(vertex_count, edges)
        prim_edges, prim_cost = prim(vertex_count, edges, start)
        return jsonify(success=True, kruskal={"edges": kruskal_edges, "cost": kruskal_cost}, prim={"edges": prim_edges, "cost": prim_cost})
    except (ValueError, TypeError) as error:
        return jsonify(success=False, error=str(error)), 400


if __name__ == "__main__":
    app.run(debug=True)
