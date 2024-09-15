#!/usr/bin/env python3

from backend.models.task import Task
import uuid
import json



class Project():
    def __init__(self, name, curriculum, repo, project_weight, release_date='', first_deadline='', second_deadline=''):
        self._id = str(uuid.uuid4())
        self.name = name
        self.curriculum = curriculum
        self.repo = repo
        self.project_weight = project_weight
        self.release_date = release_date
        self.first_deadline = first_deadline
        self.second_deadline = second_deadline
        self._score_mandatory = 0
        self._score_advanced = 0
        self._project_score = 0
        self._tasks = {}

    @property
    def score_mandatory(self):
        return self._score_mandatory

    @score_mandatory.setter
    def score_mandatory(self, value):
        self._score_mandatory = value

    @property
    def score_advanced(self):
        return self._score_advanced

    @score_advanced.setter
    def score_advanced(self, value):
        self._score_advanced = value

    @property
    def project_score(self):
        return self._project_score

    @project_score.setter
    def project_score(self, value):
        self._project_score = value

    def get_task(self, key):
        return self._tasks.get(key, None)

    def add_task(self, key, task):
        self._tasks[key] = task

    def all_task(self):
        return self._tasks.copy()

    def to_dict(self):
        new_dict = {}
        dict_copy = self.__dict__.copy()
        for key, value in dict_copy.items():
            if key == "_tasks":
                checker = {}
                for k, v in value.items():
                    checker[k] = v.to_dict()
                new_dict[key] = checker
            else:
                new_dict[key] = value
        new_dict["__class__"] = self.__class__.__name__
        return new_dict


    def create_task(self, task_name, task_dir, task_file_name, task_description, task_example, task_type):
        task = Task(task_name, self.repo, task_dir, task_file_name, task_description, task_example, task_type)
        self.add_task(task.name, task)

    def create_checker(self, task_name, name: str, type, dir,
                            file_name: str, repo_url='',
                            weight = 0, branch='main',
                            clone_dir= 'repo', command='',
                            checker_file_name='',
                            output_file='',
                            expected_output=''):
        
        task = self.get_task(task_name)
        task.create_checker(name=name, type=type, dir=dir,
                            file_name=file_name, repo_url=repo_url,
                            weight=weight, branch=branch,
                            clone_dir=clone_dir, command=command,
                            checker_file_name=checker_file_name,
                            output_file=output_file,
                            expected_output=expected_output)
    
    def update_scores_each(self):
        pscore_man = 0
        num_man = 0
        pscore_adv = 0
        num_adv = 0
        tasks = self.all_task()
        for value in tasks.values():
            value.update_task_score()
            if value.type == 'mandatory':
                pscore_man += value.task_score
                num_man += 1
            elif value.type == 'advanced':
                pscore_adv += value.task_score
                num_adv += 1
        try:
            self.score_mandatory = round(pscore_man / num_man)
        except ZeroDivisionError as e:
            pass
        try:
            self.score_advanced = round(pscore_adv / num_adv)
        except ZeroDivisionError as e:
            pass

    def update_project_score(self):
        self.update_scores_each()
        pscore_man = self.score_mandatory
        pscore_adv = self.score_advanced
        self.project_score = pscore_man + (pscore_man * pscore_adv)
