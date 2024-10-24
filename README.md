# ByteSchool API

## Description

ByteSchool is an online platform designed to facilitate coding education. The API provides endpoints for user management, project management, and task management. This project aims to create a seamless learning experience for users by enabling them to register, create projects, manage tasks, and track their progress.

## Features
- User registration and authentication
- Project creation and management
- Task management within projects
- API documentation using Swagger

## Getting Started

### Prerequisites
- Python 3.7 or higher
- Flask
- Flask-CORS
- Flasgger
- bcrypt
- MongoDB

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/daveyhmariam/ByteSchool
   cd ByteSchool
Create a virtual environment:

bash
python3 -m venv venv
source venv/bin/activate

bash
pip install -r requirenents.txt

env
Copy code
API_HOST=0.0.0.0
API_PORT=5000
FLASK_APP=/backend/app/views/app.py
Run the application:

bash
flask run




API Endpoints
User Endpoints
POST /api/users/register - Register a new user.
POST /api/users/login - Login to the application.
GET /api/users/me - Get the current user profile.
PUT /api/users/me - Update the current user's profile.
Project Endpoints
POST /api/projects - Create a new project.
GET /api/projects - Get all projects for the current user.
GET /api/projects/{id} - Get a specific project by ID.
PUT /api/projects/{id} - Update a project by ID.
DELETE /api/projects/{id} - Delete a project by ID.
Task Endpoints
POST /api/projects/{id}/tasks - Create a new task in a project.
POST /api/projects/{id}/tasks/{taskId}/check - Check the code for a task.
GET /api/projects/{id}/tasks - Get all tasks for a specific project.
GET /api/projects/{id}/progress - Get the progress of a project.
Miscellaneous
POST /api/projects/{id}/clone - Clone the project's GitHub repository.
Documentation
API documentation is available at /apidocs/.


Acknowledgments
Flask
Flasgger
MongoDB