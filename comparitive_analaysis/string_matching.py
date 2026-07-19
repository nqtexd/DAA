from flask import Flask, jsonify, render_template, request


app = Flask(__name__)


def naive_search(text, pattern):
    matches, comparisons = [], 0
    for start in range(len(text) - len(pattern) + 1):
        for offset in range(len(pattern)):
            comparisons += 1
            if text[start + offset] != pattern[offset]:
                break
        else:
            matches.append(start)
    return matches, comparisons


def compute_lps(pattern):
    lps = [0] * len(pattern)
    length, index = 0, 1
    while index < len(pattern):
        if pattern[index] == pattern[length]:
            length += 1
            lps[index] = length
            index += 1
        elif length:
            length = lps[length - 1]
        else:
            index += 1
    return lps


def kmp_search(text, pattern):
    lps = compute_lps(pattern)
    matches, comparisons = [], 0
    text_index = pattern_index = 0
    while text_index < len(text):
        comparisons += 1
        if text[text_index] == pattern[pattern_index]:
            text_index += 1
            pattern_index += 1
            if pattern_index == len(pattern):
                matches.append(text_index - pattern_index)
                pattern_index = lps[pattern_index - 1]
        elif pattern_index:
            pattern_index = lps[pattern_index - 1]
        else:
            text_index += 1
    return matches, comparisons


def rabin_karp(text, pattern, modulus=101):
    if len(pattern) > len(text):
        return [], 0
    base, pattern_hash, window_hash = 256, 0, 0
    high_place = pow(base, len(pattern) - 1, modulus)
    matches, comparisons = [], 0
    for index in range(len(pattern)):
        pattern_hash = (base * pattern_hash + ord(pattern[index])) % modulus
        window_hash = (base * window_hash + ord(text[index])) % modulus
    for start in range(len(text) - len(pattern) + 1):
        if pattern_hash == window_hash:
            for offset in range(len(pattern)):
                comparisons += 1
                if text[start + offset] != pattern[offset]:
                    break
            else:
                matches.append(start)
        if start < len(text) - len(pattern):
            window_hash = (
                base * (window_hash - ord(text[start]) * high_place)
                + ord(text[start + len(pattern)])
            ) % modulus
    return matches, comparisons


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/compare")
def compare():
    data = request.get_json(silent=True) or {}
    text = str(data.get("text", ""))
    pattern = str(data.get("pattern", ""))
    if not text or not pattern:
        return jsonify(success=False, error="Text and pattern are required."), 400
    if len(pattern) > len(text):
        return jsonify(success=False, error="Pattern cannot be longer than the text."), 400
    if len(text) > 100000:
        return jsonify(success=False, error="Text is limited to 100,000 characters."), 400
    naive_matches, naive_comparisons = naive_search(text, pattern)
    kmp_matches, kmp_comparisons = kmp_search(text, pattern)
    rk_matches, rk_comparisons = rabin_karp(text, pattern)
    return jsonify(
        success=True,
        lps=compute_lps(pattern),
        results=[
            {"name": "Naive", "matches": naive_matches, "comparisons": naive_comparisons},
            {"name": "KMP", "matches": kmp_matches, "comparisons": kmp_comparisons},
            {"name": "Rabin-Karp", "matches": rk_matches, "comparisons": rk_comparisons},
        ],
    )


if __name__ == "__main__":
    app.run(debug=True)
