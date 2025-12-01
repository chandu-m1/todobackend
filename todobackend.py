from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tasks = []
task_id = 1

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id
    data = request.json

    new_task = {
        "id": task_id,
        "title": data.get("title"),
        "description": data.get("description", ""),
        "deadline": data.get("deadline", None),
        "completed": False
    }

    tasks.append(new_task)
    task_id += 1
    return jsonify(new_task), 201

@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.json

    for task in tasks:
        if task["id"] == id:
            task["title"] = data.get("title", task["title"])
            task["description"] = data.get("description", task["description"])
            task["deadline"] = data.get("deadline", task["deadline"])
            task["completed"] = data.get("completed", task["completed"])
            return jsonify(task)

    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    global tasks
    tasks = [t for t in tasks if t["id"] != id]
    return jsonify({"message": "Task deleted"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

