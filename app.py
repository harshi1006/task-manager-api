from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3306/tasks"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    done = db.Column(db.Boolean,default=False)

    def __repr__(self) -> str:
        return f"<Task {self.id}-{self.title}>"

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks= Task.query.all()
    tasks = [
        {
            "id": task.id,
            "title": task.title,
            "done": task.done
        } for task in tasks
    ]
    return tasks

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    return jsonify({
        "id": task.id,
        "title": task.title,
        "done": task.done
    })

@app.route("/tasks", methods = ["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error":"Title is required"}),400
    task = Task(title = data['title'])
    db.session.add(task)
    db.session.commit()
    return jsonify({
        "id": task.id,
        "title": task.title,
        "done": task.done
    }),201

@app.route("/tasks/<int:task_id>", methods=["PUT","POST"])
def complete_task(task_id):
    task= Task.query.filter_by(id=task_id).first()
    data = request.get_json()
    task.title = data.get("title",task.title)
    task.done = data.get("done", task.done)
    db.session.add(task)
    db.session.commit()
    return jsonify({
        "id": task.id,
        "title": task.title,
        "done": task.done
    })
@app.route("/tasks/<int:task_id>",methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
    else:
        return jsonify({"error":"Task not found"}),404
    return jsonify({"message": "Task deleted"}),200

if __name__ == "__main__":
    app.run(debug=True)