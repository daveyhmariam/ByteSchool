#!/usr/bin/env python3

from backend.models.checker import Checker
import os
import subprocess
from git import Repo

class FileChecker(Checker):
    def __init__(self, name: str, type, dir,  file_name: str, weight, clone_dir, repo_url, branch: str = 'main', **kwargs):


        super().__init__(name=name, type=type, dir=dir, file_name=file_name, weight=weight, clone_dir=clone_dir)
        self.repo_url = repo_url
        self.branch = branch

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)


    def clone_repo(self):
        """ Clone the repository into the specified directory. """
        if os.path.exists(self.clone_dir):
            print(f"Directory '{self.clone_dir}' already exists. Updating it.")
            try:
                #subprocess.run(['rm', '-rf', self.clone_dir], check=True)
                print("updating")
                repo = Repo(self.clone_dir)
                #repo.remotes.origin.fetch()
                #repo.remotes.origin.pull(self.branch)
                pass
            except subprocess.CalledProcessError as e:
                print(f"Error removing directory: {e}")
                return
        
        else:
            print(f"Cloning repository from {self.repo_url}...")
            try:
                print(f"clone_dir: {self.clone_dir}")
                #Repo.clone_from(self.repo_url, self.clone_dir, branch=self.branch)
                print("cloning done")
                pass
            except Exception as e:
                print(f"File Doens't exsist {e}")

    def check_exist(self):
        """ Check if the specified file exists in the cloned repository and update score accordingly. """
        print("checking file")
        full_path = os.path.join(self.clone_dir, self.dir, self.file_name)
        print(f"fill path {full_path}")
        if os.path.isfile(full_path):
            self.score = self.weight
            print(f"File '{self.file_name}' exists. Score: {self.score}")
            self.status = "COMPLETE"
            return full_path
        else:
            self.score = 0
            print(f"File '{self.file_name}' does not exist. Score: {self.score}")

    def execute(self):
        """ Full execution pipeline. """
        print(self.name)
        self.clone_repo()
        full_path = self.check_exist()
        return full_path

if __name__ == '__main__':
    repo_url = 'https://github.com/daveyhmariam/alx-low_level_programming.git'
    file_name = '0-binary_to_uint.c'  # Example file name
    clone_dir = '/home/falcon/alx_2/ByteSchool/e6fedb62-7a84-4ef0-ab43-48aea3b04daf/' + repo_url.split('/')[-1].split('.')[0]
    type = 'file_checker'
    dir = '0x14-bit_manipulation'
    args = {'name':'FileChecker', 'type':type, 'dir':dir, 'file_name':file_name, 'weight':1, 'clone_dir':clone_dir, 'repo_url':repo_url}
    checker = FileChecker('FileChecker', type, dir, file_name, 1, clone_dir, repo_url, "main")
    print(checker.__dict__)
    print(checker.execute())
    print(f"Final score: {checker.score}")
    checker.execute()
    import json
    print(json.dumps(checker.__dict__, indent=2))
    print(clone_dir)
