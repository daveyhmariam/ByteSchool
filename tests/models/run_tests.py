#!/usr/bin/env python3

import unittest
import sys
import os

# Define a function to run all test cases in the current environment
def run_all_tests():
    # Discover and run all tests in the current directory
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(start_dir='/home/falcon/alx_2/ByteSchool/tests/models', pattern='test_*.py')  # Assumes test files are named test_*.py

    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)                                                                                                                                                                                                         

# Trigger the test runner to execute all test cases
run_all_tests()
