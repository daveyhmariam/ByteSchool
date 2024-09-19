#!/usr/bin/env python3

from backend.models.code_checker import CodeChecker
from backend.models.file_checker import FileChecker

if __name__ == '__main__':
    repo_url = 'https://github.com/daveyhmariam/alx-low_level_programming.git'
    dir = '0x14-bit_manipulation/'
    file_name = '0-binary_to_uint.c'  # Example file name
    clone_dir = '/home/falcon/alx_2/ByteSchool/e6fedb62-7a84-4ef0-ab43-48aea3b04daf/1b84a111-013a-44b4-90cc-17cd2da1ea4a/' + repo_url.split('/')[-1].split('.')[0]
    
    # Initialize FileChecker
    checker = FileChecker('FileChecker', 'file_checker', dir, file_name=file_name, weight=1, repo_url=repo_url, clone_dir=clone_dir)
    checker.execute()
    print(f"Final score: {checker.score}")
    print(checker.status)
    
    # Initialize CodeChecker
    command = f'gcc -Wall -pedantic -Werror -Wextra -std=gnu89 -o {clone_dir}/0x14-bit_manipulation/a'
    #checker2 = CodeChecker(name="code_checker", file_name=clone_dir + '/' + file_name, command=command, type='code_checker', weight=2, checker_file_name=f'{clone_dir}/0x14-bit_manipulation/0-main.c')
    #checker2.execute()
