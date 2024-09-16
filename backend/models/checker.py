#!/usr/bin/env python3

import uuid
import json


class Checker():
    """Base checker class
    """
    def __init__(self, name, type, dir, file_name, weight, clone_dir, **kwargs):
        print(kwargs)
            
        if "_id" in kwargs.keys():
            self._id = kwargs['_id']
        else:
            self._id = str(uuid.uuid4())
            print(f'in else {self._id}')

        self.name = name
        self.type = type
        self.dir = dir
        self.file_name = file_name
        self.weight = weight
        self.clone_dir = clone_dir
        self.score = 0
        self.status = 'INCOMPLETE'

        if kwargs:
            print('\n\n\nin kwargs')
            print(kwargs)
            for key, value in kwargs.items():
                print(f"{key}__{value}\n")
                if key != "__class__":
                    setattr(self, key, value)



    def to_dict(self):
        new_dict = dict()
        dict_copy = self.__dict__.copy()
        for key, value in dict_copy.items():
            new_dict[key] = value
        new_dict["__class__"] = self.__class__.__name__
        return new_dict

if __name__ == "__main__":
    repo_url = 'https://github.com/daveyhmariam/alx-low_level_programming.git'
    file_name = '0x14-bit_manipulation/0-binary_to_uint.c'  # Example file name
    clone_dir = '/home/falcon/alx_2/ByteSchool/e6fedb62-7a84-4ef0-ab43-48aea3b04daf/' + repo_url.split('/')[-1].split('.')[0]
    type = 'file_checker'
    dir = '0x14-bit_manipulation'
    args = {'_id': 'e2901908-957c-4b7d-a332-bc193cf3be76', 'name':'FileChecker', 'type':type, 'dir':dir, 'file_name':file_name, 'weight':2, 'clone_dir':clone_dir}
    checker = Checker(**args)
    print(checker.__dict__)
    #print(f"Final score: {checker.file_name}")
    
    print(f"Final score: {checker.__dict__}")
