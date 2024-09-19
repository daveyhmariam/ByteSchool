import unittest
from unittest.mock import MagicMock, patch
from backend.models.project import Project
from backend.models.task import Task

class TestProject(unittest.TestCase):
    
    def setUp(self):
        """Set up a Project instance before each test."""
        self.project = Project(
            name='Test Project',
            curriculum='Test Curriculum',
            repo='https://github.com/user/repo.git',
            project_weight=100
        )

    @patch('backend.models.task.Task')
    def test_create_task(self, MockTask):
        """Test the creation of a task in the project."""
        mock_task = MockTask.return_value
        self.project.create_task(
            task_name='Task 1',
            task_dir='src',
            task_file_name='main.c',
            task_description='Test task description',
            task_example='Example usage',
            task_type='mandatory'
        )
        
        # Check if the task was created and added to the project
        self.assertIn('Task 1', self.project._tasks)
        mock_task.assert_called_once_with(
            'Task 1', 'https://github.com/user/repo.git', 'src', 'main.c', 
            'Test task description', 'Example usage', 'mandatory'
        )

    @patch('backend.models.task.Task')
    def test_create_checker_for_task(self, MockTask):
        """Test adding a checker to an existing task."""
        mock_task = MockTask.return_value
        
        # Create a task first
        self.project.create_task(
            task_name='Task 1',
            task_dir='src',
            task_file_name='main.c',
            task_description='Test task description',
            task_example='Example usage',
            task_type='mandatory'
        )

        # Create a checker for the task
        self.project.create_checker(
            task_name='Task 1',
            name='FileChecker1',
            type='file_checker',
            dir='src',
            file_name='main.c',
            repo_url='https://github.com/user/repo.git',
            weight=10
        )
        
        # Check if the checker was created for the task
        mock_task.create_checker.assert_called_once_with(
            name='FileChecker1',
            type='file_checker',
            dir='src',
            file_name='main.c',
            repo_url='https://github.com/user/repo.git',
            weight=10,
            branch='main',
            clone_dir='repo',
            command='',
            checker_file_name='',
            output_file='',
            expected_output=''
        )

    @patch('backend.models.task.Task')
    def test_update_scores_each(self, MockTask):
        """Test updating the scores for mandatory and advanced tasks."""
        # Mock tasks with different types and scores
        mock_task1 = MagicMock()
        mock_task1.type = 'mandatory'
        mock_task1.task_score = 85
        mock_task1.update_task_score = MagicMock()

        mock_task2 = MagicMock()
        mock_task2.type = 'mandatory'
        mock_task2.task_score = 90
        mock_task2.update_task_score = MagicMock()

        mock_task3 = MagicMock()
        mock_task3.type = 'advanced'
        mock_task3.task_score = 95
        mock_task3.update_task_score = MagicMock()

        # Add tasks to the project
        self.project.add_task('Task 1', mock_task1)
        self.project.add_task('Task 2', mock_task2)
        self.project.add_task('Task 3', mock_task3)

        # Update scores for each task type
        self.project.update_scores_each()

        # Check that task scores were updated
        mock_task1.update_task_score.assert_called_once()
        mock_task2.update_task_score.assert_called_once()
        mock_task3.update_task_score.assert_called_once()

        # Verify the mandatory and advanced scores
        self.assertEqual(self.project.score_mandatory, 88)  # (85+90)/2 = 87.5 rounded to 88
        self.assertEqual(self.project.score_advanced, 95)   # Only one advanced task

    @patch('backend.models.task.Task')
    def test_update_project_score(self, MockTask):
        """Test updating the overall project score."""
        # Mock task scores
        mock_task1 = MagicMock()
        mock_task1.type = 'mandatory'
        mock_task1.task_score = 85
        mock_task1.update_task_score = MagicMock()

        mock_task2 = MagicMock()
        mock_task2.type = 'advanced'
        mock_task2.task_score = 90
        mock_task2.update_task_score = MagicMock()

        # Add tasks to the project
        self.project.add_task('Task 1', mock_task1)
        self.project.add_task('Task 2', mock_task2)

        # Update the project score
        self.project.update_project_score()

        # Verify that mandatory and advanced scores were calculated correctly
        self.assertEqual(self.project.score_mandatory, 85)
        self.assertEqual(self.project.score_advanced, 90)

        # Verify the final project score
        # Formula: pscore_man + (pscore_man * pscore_adv)
        expected_project_score = 85 + (85 * 90 / 100)
        self.assertEqual(self.project.project_score, expected_project_score)

if __name__ == '__main__':
    unittest.main()
