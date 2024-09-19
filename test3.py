#!/usr/bin/env python3

from backend.models.task import Task
import uuid

if __name__ == '__main__':
    example = """
#include <stdio.h>
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
    printf("%u\\n", n);
    n = binary_to_uint("101");
    printf("%u\\n", n);
    n = binary_to_uint("1e01");
    printf("%u\\n", n);
    n = binary_to_uint("1100010");
    printf("%u\\n", n);
    n = binary_to_uint("0000000000000000000110010010");
    printf("%u\\n", n);
    return (0);
}
"""
    description = """
Write a function that converts a binary number to an unsigned int.

Prototype: unsigned int binary_to_uint(const char *b);
where b is pointing to a string of 0 and 1 chars
Return: the converted number, or 0 if
there is one or more chars in the string b that is not 0 or 1
b is NULL
""" 
    user_id = 'f0d3c14b-533e-4f89-a0c4-076dc647e675' #str(uuid.uuid4())
    user_github = 'https://github.com/daveyhmariam/'
    project_id = '1b84a111-013a-44b4-90cc-17cd2da1ea4a' #str(uuid.uuid4())


    repo = 'alx-low_level_programming.git'
    dir = '0x14-bit_manipulation/'
    file_name = '0-binary_to_uint.c'
    repo_url = user_github + repo
    clone_dir = './' + '/'.join([user_id, project_id, repo.split('.')[0]])
    print(repo_url, dir, file_name, clone_dir)
    task1 = Task('0', repo, dir, file_name, description, example)
    import json
    print(json.dumps(task1.__dict__, indent=2))


"""    task1.create_checker('Files are present', 'file_checker', dir, file_name, repo_url, weight=1, clone_dir=clone_dir)
    full_path = f'{clone_dir}/{dir}'
    print(f"in test 3 full path {full_path}")
    command = f'gcc -Wall -pedantic -Werror -Wextra -std=gnu89 {full_path}{file_name} -o {full_path}a'
    output_file = f'{full_path}/{dir}/a'
    expected_output = """"""1
5
0
98
402
"""
"""
    task1.create_checker('Compile program', 'code_checker', dir=dir,
                         file_name=file_name, command=command,
                         clone_dir=clone_dir, checker_file_name = '0-main.c',
                         weight=2, output_file=output_file,
                         expected_output='')"""
    #task1.start_checking()
    #task1.update_checkes_complete()
    #task1.update_task_score()
    #print(f"checkes: {task1.checkes_complete} %")
    #print(f"task score: {task1.task_score} %")
