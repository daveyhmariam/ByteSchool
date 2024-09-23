#!/usr/bin/env python3

from backend.models.checker import Checker
import os
import subprocess
from backend import models
import stat


class CodeChecker(Checker):
    def __init__(self, name, type, dir,
                 file_name, weight, clone_dir,
                 checker_file_name, command,
                 output_file, expected_output,
                 correction_code, **kwargs):
        super().__init__(name=name, type=type, dir=dir,
                         file_name=file_name, weight=weight,
                         clone_dir=clone_dir)
        self.checker_file_name = checker_file_name
        self.command = command
        self.output_file = output_file
        self.expected_output = expected_output
        self.correction_code = correction_code

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
        models.storage.new(self)

    def prepare_code(self):
        """Prepare the code by creating or writing to the checker file."""
        checker_file_path = os.path.join(
            self.clone_dir, self.dir, self.checker_file_name)
        directory = os.path.dirname(checker_file_path)

        # Ensure the directory exists
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Check if the file exists and write to it if it doesn't
        if not os.path.isfile(checker_file_path):
            try:
                with open(checker_file_path, 'w') as file:
                    file.write(self.correction_code)
            except IOError as e:
                print(f"Error writing to file: {e}")
                return  # Exit if file creation fails

            # Set file permissions
            try:
                permissions = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
                os.chmod(checker_file_path, permissions)
            except OSError as e:
                print(f"Error setting file permissions: {e}")

    def check_code(self):
        """Compile the code using the specified command."""
        try:
            checker_file_path = os.path.join(
                self.clone_dir, self.dir, self.checker_file_name)
            file_path = os.path.join(self.clone_dir, self.dir, self.file_name)
            output_path = os.path.join(
                self.clone_dir, self.dir, self.output_file)

            # Construct the command arguments
            arg = self.command.split()
            if self.output_file:
                arg.append(output_path)
            if self.file_name:
                arg.append(file_path)
            arg.append(checker_file_path)

            print(f"Running command: {' '.join(arg)}")
            result = subprocess.run(
                arg, capture_output=True, text=True, check=True)
            print(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed: {e.stderr}")
        except FileNotFoundError as e:
            print(f"Command not found: {e}")

    def check_output(self, result: subprocess.CompletedProcess):
        """Check the output of the compiled code."""
        output_path = os.path.join(self.clone_dir, self.dir, self.output_file)
        if self.expected_output:
            try:
                if self.output_file:
                    output = subprocess.run(
                        [output_path], capture_output=True, text=True, check=True)
                    if self.expected_output.strip() == output.stdout.strip():
                        print('YES IT IS CHECKED')
                        self.status = "COMPLETE"
                        self.score = self.weight

                    else:
                        print('Output does not match expected output')
                        print(f"Expected {self.expected_output}")
                        print(f"Got {output.stdout}", output.stdout.strip(
                        ) == self.expected_output.strip())
                elif result.stdout == self.expected_output:
                    print('YES IT IS CHECKED')
                    self.status = "COMPLETE"
                    self.score = self.weight
                    print("Compilation output:")
                    print(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"Error checking output: {e}")
        else:
            print('No expected output provided')
            self.status = "COMPLETE"
            self.score = self.weight

        models.storage.save_object(self)

    def execute(self):
        """Execute the code checking process."""
        print(f"Starting code checker: {self.name}")
        self.prepare_code()
        result = self.check_code()
        if result:
            self.check_output(result)
        print('----------')


if __name__ == '__main__':
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
    import json
    print(json.dumps(checker2.__dict__, indent=2))
    checker2.execute()
