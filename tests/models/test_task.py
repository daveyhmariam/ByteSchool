import unittest
from unittest.mock import MagicMock, patch
from backend.models.task import Task
from backend.models.file_checker import FileChecker
from backend.models.code_checker import CodeChecker


class TestTask(unittest.TestCase):
    def setUp(self):
        """Set up the Task instance before each test."""
        self.task = Task(
            name='Test Task',
            repo='https://github.com/user/repo.git',
            dir='src',
            file_name='main.c',
            description='Test Task Description',
            example='Test Example',
            type='mandatory'
        )
    
    @patch('file_checker.FileChecker')
    def test_create_file_checker(self, MockFileChecker):
        """Test that a FileChecker is created and added to the task."""
        mock_checker = MockFileChecker.return_value
        self.task.create_checker(
            name='FileChecker1',
            type='file_checker',
            dir='src',
            file_name='main.c',
            repo_url='https://github.com/user/repo.git',
            weight=10
        )
        
        self.assertIn('FileChecker1', self.task._checkers_mandatory)
        MockFileChecker.assert_called_once_with(
            name='FileChecker1', type='file_checker', dir='src',
            file_name='main.c', repo_url='https://github.com/user/repo.git',
            weight=10, branch='main', clone_dir='repo'
        )
    
    @patch('code_checker.CodeChecker')
    def test_create_code_checker(self, MockCodeChecker):
        """Test that a CodeChecker is created and added to the task."""
        mock_checker = MockCodeChecker.return_value
        self.task.create_checker(
            name='CodeChecker1',
            type='code_checker',
            dir='src',
            file_name='main.c',
            command='gcc main.c -o main',
            weight=20,
            checker_file_name='main.c'
        )
        
        self.assertIn('CodeChecker1', self.task._checkers)
        MockCodeChecker.assert_called_once_with(
            name='CodeChecker1', type='code_checker', dir='src',
            file_name='main.c', command='gcc main.c -o main', weight=20, 
            clone_dir='repo', checker_file_name='main.c', 
            output_file='', expected_output=''
        )

    @patch('file_checker.FileChecker')
    @patch('code_checker.CodeChecker')
    def test_start_checking(self, MockCodeChecker, MockFileChecker):
        """Test the start_checking method with both checkers."""
        mock_file_checker = MockFileChecker.return_value
        mock_file_checker.status = "COMPLETE"
        mock_code_checker = MockCodeChecker.return_value
        mock_code_checker.status = "COMPLETE"
        
        self.task.create_checker(
            name='FileChecker1',
            type='file_checker',
            dir='src',
            file_name='main.c',
            repo_url='https://github.com/user/repo.git',
            weight=10
        )
        self.task.create_checker(
            name='CodeChecker1',
            type='code_checker',
            dir='src',
            file_name='main.c',
            command='gcc main.c -o main',
            weight=20,
            checker_file_name='main.c'
        )

        # Execute the start_checking method
        self.task.start_checking()

        # Ensure both checkers were executed
        mock_file_checker.execute.assert_called_once()
        mock_code_checker.execute.assert_called_once()

    @patch('file_checker.FileChecker')
    def test_update_task_score(self, MockFileChecker):
        """Test that the task score is updated based on checker scores."""
        mock_file_checker1 = MockFileChecker.return_value
        mock_file_checker1.weight = 10
        mock_file_checker1.score = 8
        mock_file_checker1.status = "COMPLETE"

        mock_file_checker2 = MockFileChecker.return_value
        mock_file_checker2.weight = 10
        mock_file_checker2.score = 9
        mock_file_checker2.status = "COMPLETE"

        self.task.add_checker_mandatory('FileChecker1', mock_file_checker1)
        self.task.add_checker_mandatory('FileChecker2', mock_file_checker2)

        # Update task score
        self.task.update_task_score()

        # The task score should be based on the total scores of both checkers
        self.assertEqual(self.task.task_score, 85.0)  # (8+9)/(10+10) * 100 = 85%

    @patch('file_checker.FileChecker')
    def test_update_checkes_complete(self, MockFileChecker):
        """Test that the percentage of completed checks is correctly updated."""
        mock_file_checker1 = MockFileChecker.return_value
        mock_file_checker1.status = "COMPLETE"

        mock_file_checker2 = MockFileChecker.return_value
        mock_file_checker2.status = "INCOMPLETE"

        self.task.add_checker_mandatory('FileChecker1', mock_file_checker1)
        self.task.add_checker_mandatory('FileChecker2', mock_file_checker2)

        # Update completed checks percentage
        self.task.update_checkes_complete()

        # Ensure the correct completion percentage is calculated
        self.assertEqual(self.task.checkes_complete, 50.0)

if __name__ == '__main__':
    unittest.main()
