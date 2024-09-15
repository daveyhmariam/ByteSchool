#!/usr/bin/env python3

from backend.models.file_checker import FileChecker
from backend.models.code_checker import CodeChecker
import uuid
import json



class Task():

    def __init__(self, name, repo, dir, file_name, description, example, type='mandatory'):
        self._id = str(uuid.uuid4())
        self.name = name
        self.repo = repo
        self.dir = dir
        self.file_name = file_name
        self.description = description
        self.example = example
        self.type = type
        self._task_score = 0
        self._checkes_complete = 0
        self._checkers_mandatory = {}
        self._checkers = {}

    def get_checker_mandatory(self, key):
        """Retrieve a checker by its key."""
        return self._checkers_mandatory.get(key, None)

    def add_checker_mandatory(self, key, checker):
        """Add a checker to the collection."""
        self._checkers_mandatory[key] = checker

    def get_checker(self, key):
        """Retrieve a checker by its key."""
        return self._checkers.get(key, None)

    def add_checker(self, key, checker):
        """Add a checker to the collection."""
        self._checkers[key] = checker

    def all_checkers(self):
        all_c = self._checkers.copy() | self._checkers_mandatory.copy()
        return all_c

    def to_dict(self):
        new_dict = {}
        dict_copy = self.__dict__.copy()
        for key, value in dict_copy.items():
            if key == "_checkers_mandatory" or key == "_checkers":
                checker = {}
                for k, v in value.items():
                    checker[k] = v.to_dict
                new_dict[key] = checker
            else:
                new_dict[key] = value
        new_dict["__class__"] = self.__class__.__name__
        return new_dict

    def create_checker(self, name: str, type, dir,
                            file_name: str, repo_url='',
                            weight = 0, branch='main',
                            clone_dir= 'repo', command='',
                            checker_file_name='',
                            output_file='', expected_output=''):
        if type == 'file_checker' or type == 'mandatory':
            checker = FileChecker(name, type, dir,
                                file_name, repo_url,
                                weight, branch,
                                clone_dir=clone_dir)
            self.add_checker_mandatory(checker.name, checker)
        else:
            checker = CodeChecker(name, type, dir,
                                file_name, command=command,
                                weight=weight, clone_dir=clone_dir,
                                checker_file_name=checker_file_name,
                                output_file=output_file, expected_output=expected_output)
            self.add_checker(checker.name, checker)

    """
        def create_checker_(self, name, type, dir,
                        file_name, command, weight=0,
                        clone_dir='repo',
                        checker_file_name=''):
            checker = CodeChecker(name, type, dir,
                                file_name, command, weight,
                                clone_dir,
                                checker_file_name)
            self.add_checker(checker.name, checker)
    """
    def start_checking(self):
        for value in self._checkers_mandatory.values():
            value.execute()
            if value.status == "INCOMPLETE":
                print('Previous check failed')
                return
        print('in task start checking')
        for value in self._checkers.values():
            value.execute()
    
    @property
    def checkes_complete(self):
        return self._checkes_complete

    def update_checkes_complete(self):
        total_checkers = len(self._checkers_mandatory) + len(self._checkers)
        if total_checkers == 0:
            self._checkes_complete = 0
            return
        completed = 0
        for value in self._checkers_mandatory.values():
            if value.status == "COMPLETE":
                completed += 1
        for value in self._checkers.values():
            if value.status == "COMPLETE":
                completed += 1
        self._checkes_complete = round((completed / total_checkers) * 100, 2)

    @property
    def task_score(self):
        return self._task_score

    def update_task_score(self):
        total_weight = 0
        task_score = 0
        for value in self._checkers_mandatory.values():
            total_weight += value.weight
            task_score += value.score
        for value in self._checkers.values():
            total_weight += value.weight
            task_score += value.score
        try:
            self._task_score = round((task_score / total_weight) * 100, 2)
        except ZeroDivisionError as e:
            pass


