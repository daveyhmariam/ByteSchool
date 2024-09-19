#!/usr/bin/env python3

from backend.models.checker import Checker
from backend.models.code_checker import CodeChecker
from backend.models.file_checker import FileChecker
from backend.models.task import Task
from backend.models.project import Project
from backend.models.user import User
import json
from pymongo import MongoClient
from backend import models


class Util:
    def __init__(self):
        self.users = {}

    def create_user(self, **kwargs):
        user = User(**kwargs)
        self.users[user._id] = user  # Store the instance, not the class
        return user

    def create_project(self, user: User, proj_name):
        args = models.storage.get_catalog("proj_catalog", proj_name)
        if args is None:
            print(f"Project '{proj_name}' not found in catalog.")
            return
        
        tasks = args.pop('tasks', [])  # Remove 'tasks' from args and keep it separately
        project = Project(**args)
        
        for item in tasks:
            checkers = item.pop('checkers', [])  # Remove 'checkers' from item
            task = Task(**item)
            clone_dir = f"/home/falcon/alx_2/ByteSchool/user_data/{user._id}/{project._id}/{project.repo}"
            repo_url = f"{user.user_github}/{project.repo}.git"
            print("util clone dir", clone_dir)
            print('util repo url', repo_url)
            
            for checker in checkers:
                checker.pop("clone_dir", None)
                checker.pop("repo_url", None)
                if checker.get("type") == 'file_checker':
                    ckr = FileChecker(**checker, clone_dir=clone_dir, repo_url=repo_url)
                else:
                    ckr = CodeChecker(**checker, clone_dir=clone_dir)
                print("ckr cln dir", ckr.clone_dir)
                task.create_checker(ckr)
            
            task.update_task_score()
            project.create_task(task)
        
        user.add_project(project)

# Example usage
util = Util()
arg = {
    "username": "Dawit Yilma Habtemariam",
    "email": "daveyhmaariam@gmail.com",
    "password": "daveyhm@12345",
    "user_github": "https://github.com/daveyhmariam",
    "curriculum": "SE Foundation"
}
user = util.create_user(**arg)
util.create_project(user, "0x14. C - Bit manipulation")
user.get_objs()
p = user.objs[0]
print(p.to_dict())
p.get_objs()
#p.objs[0].update_task_score()
#print(p.objs[0].to_dict())
p.objs[0].get_objs()
print(p.objs[0].objs[0].to_dict())

"""
print(user.projects)
print(user.objs)
"""
user.update_score()
print(user.to_dict())
