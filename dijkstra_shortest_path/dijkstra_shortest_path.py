import heapq
import math

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)


def dijkstra(vertex_count, edges, source):
    if vertex_count < 2 or not 0 <= source < vertex_count:
        raise ValueError("Check the vertex count and source vertex.")
    graph = [[] for _ in range(vertex_count)]
    for first, second, weight in edges:
        if not (0 <= first < vertex_count and 0 <= second < vertex_count):
            raise ValueError(f"Vertices must be in the range 0 to {vertex_count - 1}.")
        if weight < 0:
            raise ValueError("Dijkstra's algorithm cannot use negative weights.")
        graph[first].append((second, weight))
    distances, previous = [math.inf] * vertex_count, [None] * vertex_count
    distances[source] = 0
    queue = [(0, source)]
    while queue:
        distance, node = heapq.heappop(queue)
        if distance != distances[node]:
            continue
        for neighbor, weight in graph[node]:
            candidate = distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor], previous[neighbor] = candidate, node
                heapq.heappush(queue, (candidate, neighbor))
    return distances, previous


def reconstruct_path(previous, source, target):
    path, node = [], target
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()
    return path if path and path[0] == source else []


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/shortest-paths")
def shortest_paths():
    try:
        data = request.get_json(silent=True) or {}
        vertex_count, source = int(data.get("vertex_count", 0)), int(data.get("source", 0))
        edges = [(int(edge[0]), int(edge[1]), float(edge[2])) for edge in data.get("edges", [])]
        distances, previous = dijkstra(vertex_count, edges, source)
        paths = []
        for vertex, distance in enumerate(distances):
            paths.append({
                "vertex": vertex,
                "distance": None if math.isinf(distance) else distance,
                "path": reconstruct_path(previous, source, vertex),
            })
        return jsonify(success=True, source=source, paths=paths)
    except (ValueError, TypeError, IndexError) as error:
        return jsonify(success=False, error=str(error)), 400


if __name__ == "__main__":
    app.run(debug=True)
