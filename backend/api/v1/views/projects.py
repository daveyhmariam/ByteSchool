from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from models.project import Project
from models.util import Util
from backend import models
import bcrypt
from flasgger import swag_from

@app_views.route('/projects', methods=['GET'], strict_slashes=False)
@swag_from({
    'responses': {
        200: {
            'description': 'List of all projects for the user',
            'schema': {
                'type': 'array',
                'items': {
                    '$ref': '#/definitions/Project'
                }
            }
        },
        404: {
            'description': 'No projects found'
        }
    }
})
def all_project():
    user = request.current_user
    user.get_objs()
    projects = user.objs.copy()
    if projects:
        all = [item.to_dict() for item in projects]
        return jsonify(all), 200
    else:
        abort(404, description="Project not found")


@app_views.route('/projects/<project_id>', methods=['GET'], strict_slashes=False)
@swag_from({
    'parameters': [
        {
            'name': 'project_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the project to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'Project retrieved successfully',
            'schema': {
                '$ref': '#/definitions/Project'
            }
        },
        404: {
            'description': 'Project not found'
        }
    }
})
def get_project(project_id):
    user = request.current_user
    project = models.storage.get('Project', project_id)
    if project:
        return jsonify(project.to_dict()), 200
    else:
        abort(404, description="Project not found")


@app_views.route('/projects/<user_id>/<project_name>', methods=['POST'], strict_slashes=False)
@swag_from({
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the user to create the project for'
        },
        {
            'name': 'project_name',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Name of the project to create'
        }
    ],
    'responses': {
        201: {
            'description': 'Project created successfully',
            'schema': {
                '$ref': '#/definitions/Project'
            }
        },
        400: {
            'description': 'User ID is required'
        },
        403: {
            'description': 'User not authorized to create a project'
        },
        404: {
            'description': 'User not found'
        }
    }
})
def create_project(user_id, project_name):
    """Create a new project for a specific user."""
    admin = request.current_user
    util = Util()

    if admin.role != 'admin':
        abort(403, description="User not authorized to create a project")

    user = models.storage.get('User', user_id)
    if user:
        proj = util.create_project(user, project_name)
        return jsonify(proj.to_dict()), 201
    else:
        abort(404, description="User not found")


@app_views.route('/projects/<user_id>/<project_id>', methods=['DELETE'], strict_slashes=False)
@swag_from({
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the user'
        },
        {
            'name': 'project_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the project to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Project deleted successfully'
        },
        403: {
            'description': 'User not authorized to delete a project'
        },
        404: {
            'description': 'User or project not found'
        }
    }
})
def delete_project(user_id, project_id):
    admin = request.current_user

    if admin.role != 'admin':
        abort(403, description="User not authorized to delete a project")

    user = models.storage.get('User', user_id)
    if user:
        success = user.delete_project(project_id)
        if success:
            return jsonify(message='Project deleted successfully'), 200
        else:
            abort(404, description="Project not found or not associated with the user")
    else:
        abort(404, description="User not found")


@app_views.route('/projects/<project_id>', methods=['PUT'], strict_slashes=False)
@swag_from({
    'parameters': [
        {
            'name': 'project_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the project to update'
        }
    ],
    'responses': {
        200: {
            'description': 'Project updated successfully',
            'schema': {
                '$ref': '#/definitions/Project'
            }
        },
        404: {
            'description': 'User or project not found'
        }
    }
})
def update_project(project_id):
    """Update project score for a specific project."""
    user = request.current_user
    project = models.storage.get('Project', project_id)
    if project:
        project.update_project_score()
        models.storage.save_object(project)
        return jsonify(message="Project updated"), 200
    else:
        abort(404, description="Project not found")


@app_views.route('/tasks/<task_id>', methods=['PUT'], strict_slashes=False)
@swag_from({
    'parameters': [
        {
            'name': 'task_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the task to update'
        }
    ],
    'responses': {
        200: {
            'description': 'Task updated successfully',
            'schema': {
                '$ref': '#/definitions/Task'
            }
        },
        404: {
            'description': 'Task not found'
        }
    }
})
def update_task(task_id):
    """Update project score for a specific task."""
    task = models.storage.get("Task", task_id)
    if task:
        task.update_task_score()
        return jsonify(task.to_dict()), 200
    else:
        abort(404, description="Task not found")


@app_views.route('/tasks/<project_id>', methods=['GET'], strict_slashes=False)
def get_task(project_id):
    """Update project score for a specific task."""
    if project_id:
        project = models.storage.get('Project', project_id)
    if not project:
        abort(404, description="Task not found")
    project.get_objs()
    tasks = []
    for item in project.objs:
        tasks.append(item.to_dict())
        return jsonify(tasks), 200
    else:
        abort(404, description="Task not found")