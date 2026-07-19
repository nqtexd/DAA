from flask import Flask, jsonify, render_template, request


app = Flask(__name__)


def min_max_divide_conquer(values):
    if not values:
        raise ValueError("Enter at least one number.")

    def solve(low, high):
        if low == high:
            return values[low], values[low], 0
        if high == low + 1:
            if values[low] < values[high]:
                return values[low], values[high], 1
            return values[high], values[low], 1
        length = high - low + 1
        left_size = length // 2
        if length % 2 == 0 and left_size % 2 == 1:
            left_size -= 1
        middle = low + left_size - 1
        left_min, left_max, left_count = solve(low, middle)
        right_min, right_max, right_count = solve(middle + 1, high)
        return min(left_min, right_min), max(left_max, right_max), left_count + right_count + 2

    return solve(0, len(values) - 1)


def min_max_naive(values):
    minimum = maximum = values[0]
    comparisons = 0
    for value in values[1:]:
        comparisons += 1
        if value < minimum:
            minimum = value
        comparisons += 1
        if value > maximum:
            maximum = value
    return minimum, maximum, comparisons


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/analyze")
def analyze():
    try:
        values = [float(value) for value in (request.get_json(silent=True) or {}).get("values", [])]
        if len(values) > 100000:
            raise ValueError("The app accepts at most 100,000 values.")
        dc_min, dc_max, dc_count = min_max_divide_conquer(values)
        naive_min, naive_max, naive_count = min_max_naive(values)
        return jsonify(success=True, minimum=dc_min, maximum=dc_max, divide_conquer_comparisons=dc_count, naive_comparisons=naive_count, verified=dc_min == naive_min and dc_max == naive_max)
    except (ValueError, TypeError) as error:
        return jsonify(success=False, error=str(error)), 400


if __name__ == "__main__":
    app.run(debug=True)
