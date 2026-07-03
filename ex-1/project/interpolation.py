from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def interpolation_search(stack, key):
    l = 0
    r = len(stack) - 1

    while l <= r and key >= stack[l] and key <= stack[r]:

        if stack[l] == stack[r]:
            if stack[l] == key:
                return l
            break

        pos = l + ((key - stack[l])*(r - l)// (stack[r] - stack[l]))

        if stack[pos] == key:
            return pos

        elif stack[pos] < key:
            l = pos + 1

        else:
            r = pos - 1

    return -1


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/interpolate', methods=['POST'])
def interpolate():

    data = request.get_json()

    array = data["array"]
    key = int(data["key"])

    array.sort()

    index = interpolation_search(array, key)

    if index != -1:
        return jsonify({
            "success": True,
            "array": array,
            "index": index,
            "message": f"{key} found at index {index}"
        })

    return jsonify({
        "success": False,
        "array": array,
        "message": f"{key} not found."
    })


if __name__ == "__main__":
    app.run(debug=True)