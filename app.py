from flask import Flask, jsonify, request

app = Flask(__name__)

tasks =[
    {"id":1,"title":"Buy groceries", "done":False},
    {"id":2,"title":"Learn Flask", "done":False}
]

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((t for t in tasks if t["id"]==task_id),None)
    if task is None:
        return jsonify({"error":"Task not found"}),404
    return jsonify(task)

next_id =3

@app.route("/tasks", methods = ["POST"])
def create_task():
    global next_id
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error":"Title is required"}),400
    task = {"id":next_id, "title":data["title"], "done":False}
    tasks.append(task)
    next_id+=1
    return jsonify(task),201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next(( t for t in tasks if t["id"]==task_id),None)
    if task is None:
        return jsonify({"error": "Task not found"}),404
    data = request.get_json()
    task["title"] = data.get("title",task["title"])
    task["done"] = data.get("done",task["done"])
    return jsonify(task)

@app.route("/tasks/<int:task_id>",methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Task deleted"}),200

if __name__ == "__main__":
    app.run(debug=True)