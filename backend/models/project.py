#!/usr/bin/env python3

from backend.models.task import Task
from backend import models
from bson import ObjectId
import uuid
import json


class Project():
    def __init__(self, name, curriculum, repo, project_weight, release_date, first_deadline, second_deadline, **kwargs):
        self._id = kwargs.get('_id', str(ObjectId()))
        self.name = name
        self.curriculum = curriculum
        self.repo = repo
        self.project_weight = project_weight
        self.release_date = release_date
        self.first_deadline = first_deadline
        self.second_deadline = second_deadline
        self._score_mandatory = 0
        self._score_advanced = 0
        self.project_score = 0
        self.tasks = []
        self.objs = []

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
        models.storage.new(self)

    @property
    def score_mandatory(self):
        return self._score_mandatory

    @score_mandatory.setter
    def score_mandatory(self, value):
        self._score_mandatory = value
        models.storage.save_object(self)

    @property
    def score_advanced(self):
        return self._score_advanced

    @score_advanced.setter
    def score_advanced(self, value):
        self._score_advanced = value
        models.storage.save_object(self)


    """
    def get_task(self, key):
        return self._tasks.get(key, None)

    def add_task(self, key, task):
        self._tasks[key] = task

    def all_task(self):
        return self.tasks.copy()
    """

    def to_dict(self):
        new_dict = {}
        dict_copy = self.__dict__.copy()

        for key, value in dict_copy.items():
            if key == "objs":
                pass
            elif key == '_id':
                new_dict[key] = str(value)
            else:
                new_dict[key] = value

        new_dict["__class__"] = self.__class__.__name__
        return new_dict

    """
    def create_task(self, task_name, task_dir, task_file_name, task_description, task_example, task_type, **kwargs):
        task = Task(task_name, self.repo, task_dir, task_file_name,
                    task_description, task_example, task_type, **kwargs)
        self.tasks.append(f"{task.__class__.__name__}.{task._id}")
        models.storage.save_object(self)
    """

    def get_objs(self):
        if self.objs == []:
            if self.tasks != []:
                for item in self.tasks:
                    idty = item.split(".")
                    print("idty", type(self.tasks))
                    retrieved = models.storage.get(idty[0], idty[1])
                    if retrieved is not None:
                        self.objs.append(retrieved)

    """
    def create_checker(self, task_id, name: str, type, dir,
                       file_name: str, repo_url='',
                       weight=0, branch='main',
                       clone_dir='repo', command='',
                       checker_file_name='',
                       output_file='',
                       expected_output=''):

        new_dict = {}
        if self.objs == []:
            self.get_objs()
        for item in self.objs:
            new_dict[item] = item
        task = new_dict[task_id]
        task.create_checker(name=name, type=type, dir=dir,
                            file_name=file_name, repo_url=repo_url,
                            weight=weight, branch=branch,
                            clone_dir=clone_dir, command=command,
                            checker_file_name=checker_file_name,
                            output_file=output_file,
                            expected_output=expected_output)
        models.storage.save_object(self)
        """

    def create_task(self, task):
        if not isinstance(task, Task):
            raise TypeError("Expected an instance of Task")
        self.tasks.append(f"{task.__class__.__name__}.{task._id}")
        models.storage.save_object(self)

    def update_scores_each(self):
        """Update mandatory and advanced scores based on tasks."""
        pscore_man = 0
        num_man = 0
        pscore_adv = 0
        num_adv = 0
        if not self.objs:
            self.get_objs()

        task_man = [task for task in self.objs if isinstance(
            task, Task) and task.type == 'mandatory']
        task_adv = [task for task in self.objs if isinstance(
            task, Task) and task.type == 'advanced']

        for value in self.objs:
            if isinstance(value, Task):
                value.update_task_score()
                if value.type == 'mandatory':
                    pscore_man += value.task_score
                    num_man += 1
                    models.storage.save_object(value)
                elif value.type == 'advanced':
                    pscore_adv += value.task_score
                    num_adv += 1
                    models.storage.save_object(value)

        try:
            self.score_mandatory = round(
                pscore_man / num_man) if num_man > 0 else 0
        except ZeroDivisionError:
            self.score_mandatory = 0

        try:
            self.score_advanced = round(
                pscore_adv / num_adv) if num_adv > 0 else 0
        except ZeroDivisionError:
            self.score_advanced = 0

        models.storage.save_object(self)

    def update_project_score(self):
        self.update_scores_each()
        pscore_man = self.score_mandatory
        pscore_adv = self.score_advanced
        self.project_score = pscore_man + ((pscore_man / 100) * pscore_adv)
        models.storage.save_object(self)


if __name__ == "__main__":
    project = Project('0x14-bit_manipulation', "SE Foundation",
                      "alx-low_level_programming", 1, '', '', '')

    from backend.models.file_checker import FileChecker
    from backend.models.code_checker import CodeChecker

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
    expected_output = r"""1
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
