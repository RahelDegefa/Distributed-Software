from flask import Flask, request, jsonify

app = Flask(__name__)
items = []
next_id = 1

@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(items), 200

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    for item in items:
        if item["id"] == item_id:
            return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route("/items", methods=["POST"])
def create_item():
    global next_id
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Invalid input"}), 400
    item = {"id": next_id, "name": data["name"]}
    items.append(item)
    next_id += 1
    return jsonify(item), 201

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    for item in items:
        if item["id"] == item_id:
            item["name"] = data.get("name", item["name"])
            return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"message": "Item deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
