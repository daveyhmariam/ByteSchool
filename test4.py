#!/usr/bin/env python3


from backend.models.project import Project
from backend.models.task import Task
from backend.models.file_checker import FileChecker
from backend.models.code_checker import CodeChecker



if __name__ == '__main__':
    project_name = '0x14. C - Bit manipulation'
    curriculum = 'Foundation'
    repo = 'alx-low_level_programming'
    project_weight = 1
    project = Project(project_name, curriculum, repo, project_weight)
    task1_name = '0'
    task1_repo = repo
    task1_dir = '0x14-bit_manipulation'
    task1_file_name = '0-binary_to_uint.c'
    task1_description = """Write a function that converts a binary number to an unsigned int.

    Prototype: unsigned int binary_to_uint(const char *b);
    where b is pointing to a string of 0 and 1 chars
    Return: the converted number, or 0 if
    there is one or more chars in the string b that is not 0 or 1
    b is NULL
    """
    task1_example = """#include <stdio.h>
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
    julien@ubuntu:~/0x14. Binary$ gcc -Wall -pedantic -Werror -Wextra -std=gnu89 0-main.c 0-binary_to_uint.c -o a
    julien@ubuntu:~/0x14. Binary$ ./a 
    1
    5
    0
    98
    402
"""
    user_id = 'f0d3c14b-533e-4f89-a0c4-076dc647e675'
    user_github = 'https://github.com/daveyhmariam/'
    project_id = '1b84a111-013a-44b4-90cc-17cd2da1ea4a'
    task1_type = 'mandatory'
    project.create_task(task1_name, task1_dir, task1_file_name, task1_description, task1_example, task1_type)
    t1c1_name = 'File Exists'
    t1c1_type = 'file_checker'
    t1c1_dir = task1_dir
    t1c1_file_name = task1_file_name
    t1c1_repo_url = user_github + repo + '.git'
    t1c1_weight = 1
    t1c1_clone_dir = './' + '/'.join([user_id, project_id, repo])
    project.create_checker(task_name=task1_name, name=t1c1_name, type=t1c1_type, dir=t1c1_dir,
                           file_name=t1c1_file_name,
                           repo_url=t1c1_repo_url, weight=t1c1_weight,
                           clone_dir=t1c1_clone_dir)
    t1c2_name = 'Correct output - case: 1'
    t1c2_type = 'code_checker'
    t1c2_dir = task1_dir
    t1c2_file_name = task1_file_name
    full_path = f'{t1c1_clone_dir}/{task1_dir}'
    t1c2_command = f'gcc -Wall -pedantic -Werror -Wextra -std=gnu89 {full_path}/0-binary_to_uint.c -o {full_path}/a'
    t1c2_weight = 2
    t1c2_clone_dir = t1c1_clone_dir
    t1c2_checker_file_name = '0-main.c'
    t1c2_output_file = f'{full_path}/{t1c2_dir}/a'
    t1c2_expected_output = """1
5
0
98
402
"""
    project.create_checker(task_name=task1_name, name=t1c2_name, type=t1c2_type,
                           dir=t1c2_dir, file_name=t1c2_file_name, command=t1c2_command,
                           weight=t1c2_weight, clone_dir=t1c2_clone_dir,
                           checker_file_name=t1c2_checker_file_name,
                           output_file=t1c2_output_file,
                           expected_output=t1c2_expected_output)
    project.get_task('0').start_checking()
    project.update_project_score()
    #print(f'project score {project.project_score}, man: {project.score_mandatory}, adv: {project.score_advanced} checker1: {project.get_task(task1_name).name}')
    """
    tasks = project.all_task()
    checkers = []
   for task in project.all_task().values():
        print(type(task))
        for c in task.all_checkers().values():
            checkers.append(c)
            print(c.name, c.score, c.weight)
    """
    print(f'project score: {project.project_score}%')
    print(f'project dict\n{project.to_dict()}')
    print(f'task dict\n{project.get_task(task1_name).to_dict()}')
    print(f'checker dict t1c1 {project.get_task(task1_name).get_checker_mandatory(t1c1_name).to_dict()}')
    print(f'checker dict t1c2{project.get_task(task1_name).get_checker(t1c2_name).to_dict()}')