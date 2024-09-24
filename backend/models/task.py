#!/usr/bin/env python3

from backend.models.file_checker import FileChecker
from backend.models.code_checker import CodeChecker
from backend import models
import uuid
from bson import ObjectId
import json


class Task():

    def __init__(self, name, repo, dir, file_name, description, example, type='mandatory', **kwargs):

        self._id = kwargs.get('_id', str(ObjectId()))

        self.name = name
        self.repo = repo
        self.dir = dir
        self.file_name = file_name
        self.description = description
        self.example = example
        self.type = type
        self._task_score = 0
        self._checkes_complete = 0
        # self._checkers_mandatory = {}
        self.checkers = []
        self.objs = []

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
        models.storage.new(self)

        """
            def get_checker_mandatory(self, key):
                Retrieve a checker by its key
                #return self._checkers_mandatory.get(key, None)

            def add_checker_mandatory(self, key, checker):
                Add a checker to the collection
                self._checkers_mandatory[key] = checker
        """

    """
    def get_checker(self, key):
        ###"""  # Retrieve a checker by its key."""
    # return self._checkers.get(key, None)
    """

    def add_checker(self, key, checker):
        """  # Add a checker to the collection."""
    # self._checkers[key] = checker

    def all_checkers(self):
        all_c = self.checkers.copy()
        return all_c

    def to_dict(self):
        """Converts the task object to a dictionary"""
        new_dict = {}
        dict_copy = self.__dict__.copy()

        # Ensure objs is populated

        for key, value in dict_copy.items():
            if key == "objs":
                pass
            if key == "_id":
                new_dict[key] = str(value)
            else:
                new_dict[key] = value

        new_dict["__class__"] = self.__class__.__name__

        # Remove old checkers key if it exists

        return new_dict

    def get_objs(self):
        self.objs = []
        if self.checkers:
            for item in self.checkers:
                idty = item.split(".")
                if len(idty) == 2:
                    retrieved = models.storage.get(idty[0], idty[1])
                    if retrieved is not None:
                        self.objs.append(retrieved)
                    else:
                        print(f"Checker not found: {item}")

    """
    def create_checker(self, name: str, type, dir,
                       file_name: str, repo_url='',
                       weight=0, branch='main',
                       clone_dir='', command='',
                       checker_file_name='',
                       output_file='', expected_output='',correction_code='',
                       **kwargs):
        if type == 'file_checker' or type == 'mandatory':
            checker = FileChecker(name, type, dir,
                                  file_name, weight, clone_dir,
                                  branch='main', **kwargs)

            # self.add_checker_mandatory(checker.name, checker)
            self.checkers.append(f"{checker.__class__.__name__}.{checker._id}")
        else:
            checker = CodeChecker(name, type, dir,
                                  file_name, weight=weight, clone_dir=clone_dir,
                                  checker_file_name=checker_file_name,
                                  command=command, output_file=output_file,
                                  expected_output=expected_output,
                                  correction_code=correction_code,
                                  **kwargs)
            self.checkers.append(f"{checker.__class__.__name__}.{checker._id}")
        models.storage.save_object(self) """

    def create_checker(self, checker):
        if not isinstance(checker, (FileChecker, CodeChecker)):
            raise TypeError(
                "Expected an instance of FileChecker or CodeChecker")
        self.checkers.append(f"{checker.__class__.__name__}.{checker._id}")
        models.storage.save_object(self)

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
        if not self.objs:
            self.get_objs()

        # Filter out None values and ensure all objects have 'type' attribute
        valid_checkers = [
            checker for checker in self.objs if checker is not None and hasattr(checker, 'type')]

        # Separate mandatory and file checkers
        mandatory = [checker for checker in valid_checkers if checker.type in [
            "file_checker", "mandatory"]]
        others = [checker for checker in valid_checkers if checker.type not in [
            "file_checker", "mandatory"]]

        for value in mandatory:
            value.execute()
            if value.status == "INCOMPLETE":
                print('Previous check failed')
                return
            models.storage.save_object(value)

        print('In task start checking')
        for value in others:
            value.execute()
            models.storage.save_object(value)

    def update_checkes_complete(self):
        if self.objs == []:
            self.get_objs()
        total_checkers = len(self.checkers)
        if total_checkers == 0:
            self._checkes_complete = 0
            return
        completed = 0
        for value in self.objs:
            if value.status == "COMPLETE":
                completed += 1

        self._checkes_complete = round((completed / total_checkers) * 100, 2)
        models.storage.save_object(self)

    @property
    def task_score(self):
        return self._task_score

    def update_task_score(self):
        total_weight = 0
        task_score = 0
        self.start_checking()
        for value in self.objs:
            total_weight += value.weight
            task_score += value.score

        try:
            self._task_score = round((task_score / total_weight) * 100, 2)
            self.update_checkes_complete()
            models.storage.save_object(self)
        except ZeroDivisionError as e:
            pass


if __name__ == "__main__":

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
    print(task.checkers)
    task.get_objs()
    task.update_task_score()
    print(task.objs)
    print(task.to_dict())
