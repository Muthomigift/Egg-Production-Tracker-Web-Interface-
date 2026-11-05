from datetime import datetime

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# In-memory storage: all records are lost when the server restarts
eggs = []


def validate_record(data):
    """Check the incoming JSON. Return an error message, or None if it is valid."""
    if not data:
        return "Request body must be JSON with shed, date and count"

    for field in ("shed", "date", "count"):
        if field not in data:
            return f"'{field}' is required"

    shed = data["shed"]
    if not isinstance(shed, str) or not shed.strip():
        return "'shed' must be a non-empty text, e.g. \"Shed A\""

    try:
        datetime.strptime(str(data["date"]), "%Y-%m-%d")
    except ValueError:
        return "'date' must be a real date in YYYY-MM-DD format, e.g. 2026-11-04"

    count = data["count"]
    # bool is a subtype of int in Python, so reject it explicitly
    if isinstance(count, bool) or not isinstance(count, int):
        return "'count' must be a whole number"
    if count < 0:
        return "'count' cannot be negative"

    return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/eggs", methods=["POST"])
def log_eggs():
    data = request.get_json(silent=True)
    error = validate_record(data)
    if error:
        return jsonify({"error": error}), 400

    record = {
        "id": len(eggs) + 1,
        "shed": data["shed"].strip(),
        "date": data["date"],
        "count": data["count"],
    }
    eggs.append(record)
    return jsonify(record), 201


@app.route("/api/eggs", methods=["GET"])
def get_eggs():
    records = []
    running_total = 0
    totals_by_shed = {}

    for record in eggs:
        running_total += record["count"]
        totals_by_shed[record["shed"]] = (
            totals_by_shed.get(record["shed"], 0) + record["count"]
        )
        records.append({**record, "running_total": running_total})

    return jsonify(
        {
            "records": records,
            "total_eggs": running_total,
            "totals_by_shed": totals_by_shed,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)