from flask import Blueprint, request, jsonify
from models.task_model import Task
from views.task_view import render_tasks_list, render_task_detail
from functools import wraps
from utils.decorators import jwt_required, role_required

task_bp = Blueprint("task", __name__)

@task_bp.route("/taks", methods=["GET"])
@jwt_required
def get_tasks():
    tasks = Task.get_all()
    return jsonify(render_tasks_list(tasks))



@task_bp.route("/taks", methods=["POST"])
@jwt_required
@role_required("admin")
def post_task():
    data = request.json
    title = data.get("title")
    description = data.get("description")
    status = data.get("status")
    created_at = data.get("created_at")
    assigned_to = data.get("assigned_to")
    if not title or not description or not status or not created_at or not assigned_to:
        return jsonify({"error": "Se requieren titulo, status, created_at y assigned_to"}), 400
    task = Task(title=title, description=description, status=status, created_at=created_at, assigned_to=assigned_to)
    task.save()
    return jsonify(render_task_detail(task)), 201




@task_bp.route("/taks/<int:id>", methods=["GET"])
@jwt_required
def get_task(id):
    task = Task.get_by_id(id)
    if task:
        return jsonify(render_task_detail(task))
    return jsonify({"error": "Tarea no encontrado"}), 404


@task_bp.route("/taks/<int:id>", methods=["PUT"])
@jwt_required
@role_required("admin")
def update_task(id):
    task = Task.get_by_id(id)
    if not task:
        return jsonify({"error": "Tarea no encontrado"}), 404
    data = request.json
    title = data.get("title")
    description = data.get("description")
    status = data.get("status")
    created_at = data.get("created_at")
    assigned_to = data.get("assigned_to")
    task.update(title=title, description=description, status=status, created_at=created_at, assigned_to=assigned_to)
    return jsonify(render_task_detail(task))

@task_bp.route("/taks/<int:id>", methods=["DELETE"])
@jwt_required
@role_required("admin")
def delete_task(id):
    task = Task.get_by_id(id)
    if not task:
        return jsonify({"error": "Tarea no encontrado"}), 404
    task.delete()
    return "", 204
