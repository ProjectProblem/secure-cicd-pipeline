"""
Secure Flask API - Sample Application
A simple REST API demonstrating security best practices
"""

from flask import Flask, jsonify, request
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Sample data store (in-memory)
tasks = [
    {"id": 1, "title": "Learn DevSecOps", "completed": False},
    {"id": 2, "title": "Implement CI/CD", "completed": False},
]


@app.route("/")
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Secure CI/CD Pipeline API",
        "version": "1.0.0"
    })


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Get all tasks"""
    logger.info("Fetching all tasks")
    return jsonify({"tasks": tasks})


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    """Get a specific task by ID"""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        return jsonify({"task": task})
    return jsonify({"error": "Task not found"}), 404


@app.route("/api/tasks", methods=["POST"])
def create_task():
    """Create a new task"""
    if not request.json or "title" not in request.json:
        return jsonify({"error": "Title is required"}), 400
    
    new_task = {
        "id": tasks[-1]["id"] + 1 if tasks else 1,
        "title": request.json["title"],
        "completed": request.json.get("completed", False)
    }
    tasks.append(new_task)
    logger.info(f"Created new task: {new_task['id']}")
    return jsonify({"task": new_task}), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Update an existing task"""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    if "title" in request.json:
        task["title"] = request.json["title"]
    if "completed" in request.json:
        task["completed"] = request.json["completed"]
    
    logger.info(f"Updated task: {task_id}")
    return jsonify({"task": task})


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task"""
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    tasks = [t for t in tasks if t["id"] != task_id]
    logger.info(f"Deleted task: {task_id}")
    return jsonify({"message": "Task deleted successfully"})


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {error}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
