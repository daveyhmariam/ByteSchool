import unittest
import uuid
from backend.models.checker import Checker  # Assuming your Checker class is in a module named checker_module


class TestChecker(unittest.TestCase):
    def setUp(self):
        # This method runs before every test. It sets up the Checker instance.
        self.checker = Checker(name="TestChecker", type="mandatory", dir="/test_dir", file_name="test_file.c")

    def test_uuid_generation(self):
        # Ensure that the UUID is generated as a valid string
        try:
            uuid.UUID(self.checker.uuid)
            valid_uuid = True
        except ValueError:
            valid_uuid = False
        self.assertTrue(valid_uuid, "UUID should be a valid UUID string")

    def test_initial_status(self):
        # Test the initial status is set correctly
        self.assertEqual(self.checker.status, 'INCOMPLETE', "Initial status should be 'INCOMPLETE'")

    def test_set_status(self):
        # Test the status setter
        self.checker.status = 'COMPLETE'
        self.assertEqual(self.checker.status, 'COMPLETE', "Status should be set to 'COMPLETE'")

    def test_initial_score(self):
        # Test the initial score is set to 0
        self.assertEqual(self.checker.score, 0, "Initial score should be 0")

    def test_set_score(self):
        # Test the score setter
        self.checker.score = 85
        self.assertEqual(self.checker.score, 85, "Score should be set to 85")

    def test_weight_property(self):
        # Ensure the weight is set correctly
        self.assertEqual(self.checker.weight, 0, "Initial weight should be 0")
        # Change the weight and verify
        self.checker.weight = 5
        self.assertEqual(self.checker.weight, 5, "Weight should be set to 5")

    def test_file_name_property(self):
        # Ensure the file name is set correctly
        self.assertEqual(self.checker.file_name, 'test_file.c', "File name should be 'test_file.c'")

    def test_clone_dir_property(self):
        # Test if the clone directory is correctly initialized and updated
        self.assertEqual(self.checker.clone_dir, '', "Initial clone_dir should be an empty string")
        self.checker.clone_dir = '/new_clone_dir'
        self.assertEqual(self.checker.clone_dir, '/new_clone_dir', "Clone_dir should be updated to '/new_clone_dir'")

if __name__ == '__main__':
    unittest.main()
