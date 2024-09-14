#!/usr/bin/env python3

import uuid
import bcrypt
from backend.models.project import Project
import json


class User():
    def __init__(self, username, email, password):

        self._id = str(uuid.uuid4())
        self.username = username
        self.email = email

        self.password_hash = self._hash_password(password)
        self.projects = {}
    
    def get_project(self, project_id):
        return self.projects.get(project_id, None)

    def add_project(self, project):
        if not isinstance(project, Project):
            raise TypeError
        self.projects[project.project_id] = project

    def all_projects(self):
        return self.projects.copy()

    def _hash_password(self, password):
        """Hashes the password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

    def to_dict(self):
        dict_copy = self.__dict__.copy()
        new_dict = {}
        for key, value in dict_copy.items():
            if key == "projects":
                projects = {}
                for k, v in value.items():
                    projects[k] = v.to_dict()
                new_dict[key] = projects
            else:
                if key == "password_hash":
                    print(type(value))
                    new_dict[key] = value.decode('utf-8')     
                new_dict[key] = value
        new_dict["__class__"] = self.__class__.__name__
        return new_dict

if __name__ == "__main__":

    user = User("dave", "daveyhmariam@", "dave!@#")
    print(user.to_dict())

