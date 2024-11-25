#!/usr/bin/env python3
""" Module of Users views
This module provides the user-related API endpoints for user management, 
including registration, retrieval, updating, and deletion of users.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from backend import models
import bcrypt
from flasgger import swag_from

def hash_password(password):
    """Hash a password for storing.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(stored_hash, password):
    """Verify a stored password against a provided password.

    Args:
        stored_hash (str): The hashed password stored in the database.
        password (str): The password provided by the user for verification.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)


@app_views.route('/users/register', methods=['POST'], strict_slashes=False)
@swag_from({
    'tags': ['Users'],
    'responses': {
        201: {
            'description': 'User created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'curriculum': {'type': 'string'},
                    'user_github': {'type': 'string'},
                    'role': {'type': 'string'},
                }
            }
        },
        400: {
            'description': 'Bad Request: Missing required fields or email already exists'
        }
    },
    'parameters': [
        {
            'name': 'body',
            'description': 'User registration details',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'curriculum': {'type': 'string'},
                    'user_github': {'type': 'string'},
                    'password': {'type': 'string'},
                    'role': {'type': 'string'}
                }
            }
        }
    ]
})
def create_user():
    """Register a new user.

    This endpoint allows for the creation of a new user by providing
    the required user information.

    Returns:
        Response object with the created user's data and status code 201
        if successful, or a 400 status code if the request is malformed.
    """
    data = request.json
    required_fields = ['username', 'email', 'curriculum', 'user_github', 'password', 'role']
    if not all(field in data for field in required_fields):
        abort(400, description="Missing required fields")

    existing_user = models.storage.get_email(data['email'])
    if existing_user:
        abort(400, description="Email already exists")

    user_data = {
        'username': data['username'],
        'email': data['email'],
        'curriculum': data['curriculum'],
        'user_github': data['user_github'],
        'password': data["password"],
        'role': data['role']
    }

    user = User(**user_data)
    models.storage.new(user)

    return jsonify(user.to_dict()), 201


@app_views.route('/users/me', methods=['GET'], strict_slashes=False)
@swag_from({
    'tags': ['Users'],
    'responses': {
        200: {
            'description': 'Current user profile retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'curriculum': {'type': 'string'},
                    'user_github': {'type': 'string'},
                    'role': {'type': 'string'},
                }
            }
        }
    }
})
def get_user():
    """Get the current user's profile.

    Returns:
        Response object with the current user's data.
    """
    return jsonify(request.current_user.to_dict())


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from({
    'tags': ['Users'],
    'responses': {
        200: {
            'description': 'User updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'curriculum': {'type': 'string'},
                    'user_github': {'type': 'string'},
                    'role': {'type': 'string'},
                }
            }
        },
        400: {
            'description': 'Bad Request: No fields to update'
        },
        404: {
            'description': 'User not found'
        },
        403: {
            'description': 'User not authorized to update'
        }
    },
    'parameters': [
        {
            'name': 'user_id',
            'description': 'ID of the user to update',
            'in': 'path',
            'type': 'string',
            'required': True
        },
        {
            'name': 'body',
            'description': 'Updated user information',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'curriculum': {'type': 'string'},
                    'user_github': {'type': 'string'},
                    'password': {'type': 'string'},
                    'role': {'type': 'string'}
                }
            }
        }
    ]
})
def update_user(user_id):
    """Update a user's information.

    This endpoint allows an admin user to update the specified user's information.

    Args:
        user_id (str): The ID of the user to update.

    Returns:
        Response object with the updated user's data and status code 200
        if successful, or a 404 status code if the user is not found.
    """
    data = request.json
    update_fields = {}

    if 'password' in data:
        update_fields['password_hash'] = hash_password(data['password'])
    if 'username' in data:
        update_fields['username'] = data['username']
    if 'curriculum' in data:
        update_fields['curriculum'] = data['curriculum']
    if 'user_github' in data:
        update_fields['user_github'] = data['user_github']
    if 'role' in data:
        update_fields['role'] = data['role']

    if not update_fields:
        abort(400, description="No fields to update")

    admin = request.current_user
    user = models.storage.get("User", user_id)

    if not user:
        abort(404, description="User not found")

    if admin and admin.role == "admin":
        for key, value in update_fields.items():
            setattr(user, key, value)
        models.storage.save_object(user)
        return jsonify(user.to_dict())
    else:
        abort(403, description="User not authorized to update")


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@swag_from({
    'tags': ['Users'],
    'responses': {
        200: {
            'description': 'User deleted successfully'
        },
        404: {
            'description': 'User not found'
        }
    },
    'parameters': [
        {
            'name': 'user_id',
            'description': 'ID of the user to delete',
            'in': 'path',
            'type': 'string',
            'required': True
        }
    ]
})
def delete_user(user_id):
    """Delete a user.

    This endpoint allows an admin user to delete the specified user.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        Response object with a success message and status code 200
        if successful, or a 404 status code if the user is not found.
    """
    admin = request.current_user
    user = models.storage.get("User", user_id)
    if admin and admin.role == 'admin':
        models.storage.delete("User", user._id)
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        abort(404, description="User not found")



@app_views.route('/users/update', methods=['PUT'], strict_slashes=False)
def update_user_score():
    user = request.current_user
    if user:
        user.update_score()
        return jsonify(message="updated successfully"), 201
    else:
        abort(404, description="not found")

