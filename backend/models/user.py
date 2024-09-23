#!/usr/bin/env python3

import uuid
import bcrypt
from backend.models.project import Project
from backend import models
from bson import ObjectId
import json


class User:
    def __init__(self, username, email, curriculum, user_github, role, password='', password_hash='', **kwargs):
        self._id = kwargs.get('_id', str(ObjectId()))

        self.username = username
        self.email = email

        self.password_hash = password_hash if password_hash != '' else self._hash_password(
            password)

        self.curriculum = curriculum if isinstance(
            curriculum, list) else [curriculum]
        self.user_github = user_github
        self.role = role
        self.projects = []
        self.objs = []
        self.average = {}

        for key, value in kwargs.items():
            if key != "__class__":
                if key == "password_hash":
                    hash = value.encode(
                        'utf-8') if isinstance(value, str) else value
                    setattr(self, key, hash)
                else:
                    setattr(self, key, value)

        models.storage.new(self)

    def get_objs(self):
        """Return the project ID if it exists, else None"""
        self.objs == []
        for item in self.projects:
            idty = item.split(".")
            self.objs.append(models.storage.get(idty[0], idty[1]))

    def add_project(self, project):
        """Add a project ID to the list of projects"""
        if not isinstance(project, Project):
            raise TypeError("Expected an instance of Project")
        self.projects.append(f"{project.__class__.__name__}.{project._id}")
        models.storage.save_object(self)

    def all_projects(self):
        """Return a copy of the list of project IDs"""
        return self.projects.copy()

    def _hash_password(self, password):
        """Hashes the password using bcrypt"""

        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        """Checks if the provided password matches the stored hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        new_dict = {}
        dict_copy = self.__dict__.copy()

        for key, value in dict_copy.items():
            if key == "objs":
                pass
            else:
                new_dict[key] = value

        new_dict["__class__"] = self.__class__.__name__
        return new_dict

    def update_score(self):
        self.get_objs()
        if isinstance(self.curriculum, list):
            for curriculum in self.curriculum:
                score = 0
                weight = 0
                for proj in self.objs:
                    if proj.curriculum == curriculum:
                        proj.update_project_score()
                        score += (proj.project_score * proj.project_weight)
                        weight += proj.project_weight
                try:
                    print("user score", score, weight)
                    self.average[curriculum] = score / weight
                    models.storage.save_object(self)
                except ZeroDivisionError as e:
                    pass
        else:
            for proj in self.objs:
                proj.update_project_score()
                score += (proj.project_score * proj.project_weight)
                weight += proj.project_weight

            try:
                self.average[curriculum] = score / weight
                models.storage.save_object(self)

            except ZeroDivisionError as e:
                pass


if __name__ == "__main__":
    name = 'dave'
    email = 'dave@'
    passw = "dave@!@#"
    curri = 'found'
    arg = {'username': name, 'email': email, 'password': passw, 'curriculum': curri,
           'user_github': "https://github.com/daveyhmariam", "role": "user"}
    user = User(**arg)
    project = Project('0x14-bit_manipulation', "SE Foundation",
                      "alx-low_level_programming", 1, '', '', '')

    from backend.models.file_checker import FileChecker
    from backend.models.code_checker import CodeChecker
    from backend.models.task import Task

    task = Task("0", "alx-low_level_programming",
                "0-binary_to_uint.c", "", "", 'mandatory')
    repo_url = 'https://github.com/daveyhmariam/alx-low_level_programming.git'
    file_name = '0-binary_to_uint.c'  # Example file name
    clone_dir = '/home/falcon/alx_2/ByteSchool/e6fedb62-7a84-4ef0-ab43-48aea3b04daf/' + \
        repo_url.split('/')[-1].split('.')[0]
    type = 'file_checker'
    dir = '0x14-bit_manipulation'
    args = {'name': 'FileChecker', 'type': type, 'dir': dir,
            'file_name': file_name, 'weight': 1, 'clone_dir': clone_dir, 'repo_url': repo_url, 'branch': "main"}
    checker1 = FileChecker(**args)
    task.create_checker(checker1)
    repo_url = 'https://github.com/daveyhmariam/alx-low_level_programming.git'
    dir = '0x14-bit_manipulation'
    file_name = '0-binary_to_uint.c'
    clone_dir = '/home/falcon/alx_2/ByteSchool/e6fedb62-7a84-4ef0-ab43-48aea3b04daf/' + \
        repo_url.split('/')[-1].split('.')[0]
    type = 'code_checker'
    checker_file_name = '0-main.c'
    output_file = 'a'
    expected_output = """1
5
0
98
402
"""

    command = f'gcc -Wall -pedantic -Werror -Wextra -std=gnu89 -o '
    correction_code = r"""#include <stdio.h>
#include "main.h"

/**
 * main - check the code
 *
 * Return: Always 0.
 */
int main(void)
{
    unsigned int n;

    n = binary_to_uint("1");
    printf("%u\n", n);
    n = binary_to_uint("101");
    printf("%u\n", n);
    n = binary_to_uint("1e01");
    printf("%u\n", n);
    n = binary_to_uint("1100010");
    printf("%u\n", n);
    n = binary_to_uint("0000000000000000000110010010");
    printf("%u\n", n);
    return (0);
}
"""

    checker2 = CodeChecker('Code_checker', type, dir, file_name, 2, clone_dir,
                           checker_file_name, command, output_file, expected_output, correction_code)
    task.create_checker(checker2)
    project.create_task(task)
    print(project.tasks)
    project.update_project_score()
    project.get_objs()
    print(project.objs)
    print(project.to_dict())
