import unittest
from unittest.mock import patch, MagicMock
import os
import subprocess
from backend.models.code_checker import CodeChecker  # Replace with your module name

class TestCodeChecker(unittest.TestCase):
    def setUp(self):
        """Set up the CodeChecker instance before each test."""
        self.command = 'gcc -o output'
        self.file_name = 'main.c'
        self.checker_file_name = 'checker.c'
        self.clone_dir = '/path/to/clone/dir'
        self.output_file = 'output.txt'
        self.expected_output = 'Hello, World!'
        self.code_checker = CodeChecker(name='CodeChecker', type='mandatory', dir='src', file_name=self.file_name, 
                                        command=self.command, clone_dir=self.clone_dir, 
                                        checker_file_name=self.checker_file_name, 
                                        output_file=self.output_file, expected_output=self.expected_output)

    @patch('subprocess.run')
    def test_check_code_successful_execution_with_expected_output(self, mock_run):
        """Test check_code when compilation is successful and output matches expected output."""
        # Mock subprocess.run for command compilation and execution
        mock_result_compile = MagicMock()
        mock_result_compile.stdout = ''
        mock_run.side_effect = [mock_result_compile, MagicMock(stdout=self.expected_output)]

        self.code_checker.check_code()

        # Ensure the command was called for both compilation and output execution
        self.assertEqual(self.code_checker.status, 'COMPLETE')
        self.assertEqual(self.code_checker.score, self.code_checker.weight)
        mock_run.assert_called()

    @patch('subprocess.run')
    def test_check_code_successful_execution_without_expected_output(self, mock_run):
        """Test check_code when expected_output is not provided."""
        self.code_checker.expected_output = ''
        
        mock_result_compile = MagicMock()
        mock_result_compile.stdout = 'Compilation successful'
        mock_run.return_value = mock_result_compile

        self.code_checker.check_code()

        # Ensure the command was called for compilation only
        self.assertEqual(self.code_checker.status, 'COMPLETE')
        self.assertEqual(self.code_checker.score, self.code_checker.weight)
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_check_code_compilation_failure(self, mock_run):
        """Test check_code when compilation fails."""
        mock_run.side_effect = subprocess.CalledProcessError(1, self.command, stderr='Compilation error')

        self.code_checker.check_code()

        # Ensure that the status and score did not change
        self.assertNotEqual(self.code_checker.status, 'COMPLETE')
        self.assertEqual(self.code_checker.score, 0)

    @patch('subprocess.run', side_effect=FileNotFoundError('gcc: command not found'))
    def test_check_code_command_not_found(self, mock_run):
        """Test check_code when the compilation command is not found."""
        self.code_checker.check_code()

        # Ensure that the error was handled correctly
        self.assertNotEqual(self.code_checker.status, 'COMPLETE')
        self.assertEqual(self.code_checker.score, 0)
        mock_run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
