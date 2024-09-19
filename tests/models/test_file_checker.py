import unittest
from unittest.mock import patch, MagicMock
import os
from backend.models.file_checker import FileChecker  # Assume the FileChecker class is in file_checker_module.py

class TestFileChecker(unittest.TestCase):
    def setUp(self):
        """Setup a FileChecker instance for testing"""
        self.repo_url = 'https://github.com/daveyhmariam/alx-low_level_programming.git'
        self.file_name = '0x14-bit_manipulation/0-binary_to_uint.c'
        self.clone_dir = '/home/falcon/alx_2/ByteSchool/test_repo'
        self.file_checker = FileChecker(name='FileChecker', file_name=self.file_name, repo_url=self.repo_url, clone_dir=self.clone_dir)

    @patch('file_checker_module.Repo')  # Mock the Repo object from GitPython
    def test_clone_repo_when_directory_exists(self, mock_repo):
        """Test clone_repo method when the directory already exists"""
        # Mock os.path.exists to return True to simulate directory existence
        with patch('os.path.exists', return_value=True):
            mock_repo.return_value.remotes.origin.pull = MagicMock()  # Mock the pull function
            self.file_checker.clone_repo()
            mock_repo.return_value.remotes.origin.pull.assert_called_once_with('main')

    @patch('file_checker_module.Repo')  # Mock the Repo object from GitPython
    @patch('os.path.exists', return_value=False)  # Mock os.path.exists to simulate directory doesn't exist
    def test_clone_repo_when_directory_does_not_exist(self, mock_exists, mock_repo):
        """Test clone_repo method when the directory does not exist"""
        self.file_checker.clone_repo()
        mock_repo.clone_from.assert_called_once_with(self.repo_url, self.clone_dir, branch='main')

    @patch('os.path.isfile', return_value=True)  # Mock os.path.isfile to simulate file existence
    def test_check_exist_when_file_exists(self, mock_isfile):
        """Test check_exist method when the file exists"""
        full_path = os.path.join(self.clone_dir, self.file_checker.dir, self.file_checker.file_name)
        result = self.file_checker.check_exist()
        self.assertEqual(result, full_path)
        self.assertEqual(self.file_checker.score, self.file_checker.weight)
        self.assertEqual(self.file_checker.status, 'COMPLETE')

    @patch('os.path.isfile', return_value=False)  # Mock os.path.isfile to simulate file does not exist
    def test_check_exist_when_file_does_not_exist(self, mock_isfile):
        """Test check_exist method when the file does not exist"""
        result = self.file_checker.check_exist()
        self.assertIsNone(result)
        self.assertEqual(self.file_checker.score, 0)
        self.assertNotEqual(self.file_checker.status, 'COMPLETE')

    @patch.object(FileChecker, 'clone_repo', return_value=None)  # Mock clone_repo method
    @patch.object(FileChecker, 'check_exist', return_value='/path/to/file')  # Mock check_exist method
    def test_execute(self, mock_clone_repo, mock_check_exist):
        """Test execute method to ensure it runs the pipeline correctly"""
        result = self.file_checker.execute()
        self.assertEqual(result, '/path/to/file')
        mock_clone_repo.assert_called_once()
        mock_check_exist.assert_called_once()

if __name__ == '__main__':
    unittest.main()
