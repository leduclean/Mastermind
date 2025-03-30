import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from app.mastermind.play import *


# Dummy class to simulate the common module
class DummyCommon:
    LENGTH = 4
    COLORS = ["R", "V", "B", "J"]

    @staticmethod
    def evaluation(combination, human_solution):
        # If the combination is "win", simulate a success, otherwise nothing conclusive.
        if combination == "win":
            return (DummyCommon.LENGTH, 0)
        return (0, 0)


# Dummy modules for codemaker and codebreaker
class DummyCodemaker:
    def __init__(self):
        self.init_called = False

    def init(self):
        self.init_called = True

    def codemaker(self, combination):
        # If the combination is "win", return a winning score.
        if combination == "win":
            return (DummyCommon.LENGTH, 0)
        return (0, 0)


class DummyCodebreaker:
    def __init__(self):
        self.init_called = False
        self.calls = 0

    def init(self):
        self.init_called = True

    def codebreaker(self, ev):
        self.calls += 1
        # On the first call, return a non-winning combination,
        # on the second call, return "win" to end the game.
        if self.calls == 1:
            return "notwin"
        else:
            return "win"


class TestPlayModule(unittest.TestCase):
    # simulate the import_module method with a mock
    @patch("importlib.import_module")
    def test_get_codebreaker_module_success(self, mock_import_module):
        """Test get_codebreaker_module in case the import succeeds

        Args:
            mock_import_module (_type_): import_module mock to simulate the behavior of the function
        """
        # Create a dummy module
        dummy_module = MagicMock()

        # Make importlib.import_module() return this dummy module
        mock_import_module.return_value = dummy_module
        # Call our function with a specific version
        result = get_codebreaker_module(1)
        # Ensure that import_module is called with the correct argument
        mock_import_module.assert_called_with("app.mastermind.codebreaker1")
        # Verify that the function returns the mocked module
        self.assertEqual(result, dummy_module)

    @patch("importlib.import_module", side_effect=ImportError)
    def test_get_codebreaker_module_failure(self, mock_import_module):
        """Test get_codebreaker_module in case the import fails

        Args:
            mock_import_module (_type_): import_module mock to simulate the behavior of the function with an ImportError
        """
        # Store the exception message in cm
        with self.assertRaises(ValueError) as cm:
            get_codebreaker_module(99)

        # Verify that the error message is correct
        self.assertEqual(str(cm.exception), "Module codebreaker99 not found.")

    @patch("importlib.import_module")
    def test_get_codemaker_module_success(self, mock_import_module):
        """Test get_codemaker_module in case the import succeeds

        Args:
            mock_import_module (_type_): import_module mock to simulate an import
        """
        # Similar to the get_codebreaker function
        dummy_module = MagicMock()
        mock_import_module.return_value = dummy_module
        result = get_codemaker_module(2)
        mock_import_module.assert_called_with("app.mastermind.codemaker2")
        self.assertEqual(result, dummy_module)

    @patch("importlib.import_module", side_effect=ImportError)
    def test_get_codemaker_module_failure(self, mock_import_module):
        """Test get_codemaker_module in case the import fails

        Args:
            mock_import_module (_type_): import_module mock to simulate a failed import
        """
        # Same as get_codebreaker_failure
        with self.assertRaises(ValueError) as cm:
            get_codemaker_module(42)
        self.assertEqual(str(cm.exception), "Module codemaker42 not found.")

    def test_check_compatibility_incompatible(self):
        """Test check_compatibility in an incompatible case -> ensure it raises an error"""
        with self.assertRaises(ValueError):
            check_compatibility(0, 2)

    def test_check_compatibility_compatible(self):
        """Test check_compatibility in a compatible case -> ensure no error is raised"""
        try:
            check_compatibility(1, 1)
        except ValueError:
            self.fail("check_compatibility raised an unexpected error for (1,1).")

    @patch("app.mastermind.play.common", new_callable=lambda: DummyCommon)
    @patch("app.mastermind.play.get_codemaker_module")
    @patch("app.mastermind.play.get_codebreaker_module")
    def test_play(self, mock_get_codebreaker, mock_get_codemaker, mock_common):
        """Test the main function play by mocking the behavior of the codebreaker
        and codemaker using DummyCodemaker and DummyCodebreaker"""

        dummy_codemaker = DummyCodemaker()
        dummy_codebreaker = DummyCodebreaker()
        mock_get_codemaker.return_value = dummy_codemaker
        mock_get_codebreaker.return_value = dummy_codebreaker

        # Collect outputs to verify that the function doesn't print anything when quiet=True
        outputs = []

        def fake_output(msg):
            outputs.append(msg)

        # Call the play function: the first combination is non-winning,
        # the second returns "win" to end the game.
        nbr_of_try = play(
            codemaker_version=1,
            codebreaker_version=1,
            reset_solution=True,
            quiet=True,
            output=fake_output,
        )
        self.assertEqual(nbr_of_try, 2)
        self.assertTrue(dummy_codemaker.init_called)
        self.assertTrue(dummy_codebreaker.init_called)

    @patch("app.mastermind.play.common", new_callable=lambda: DummyCommon)
    @patch("app.mastermind.play.get_codemaker_module")
    @patch("app.mastermind.play.get_codebreaker_module")
    def test_play_log(self, mock_get_codebreaker, mock_get_codemaker, mock_common):
        """Test the main function play_log by mocking the behavior of the codebreaker
        and codemaker using DummyCodemaker and DummyCodebreaker to ensure the output log
        """

        dummy_codemaker = DummyCodemaker()
        dummy_codebreaker = DummyCodebreaker()
        mock_get_codemaker.return_value = dummy_codemaker
        mock_get_codebreaker.return_value = dummy_codebreaker

        # Use a custom function to capture the logs
        logs = []

        def fake_output_func(msg):
            logs.append(msg)

        nbr_of_try = play_log(
            codemaker_version=1,
            codebreaker_version=1,
            log_file="dummy",
            reset_solution=True,
            quiet=True,
            output_func=fake_output_func,
            human_solution=False,
        )
        # The game ends in two tries.
        self.assertEqual(nbr_of_try, 2)
        # In each try, two messages are sent (combination and evaluation)
        self.assertEqual(len(logs), 4)

    def test_file_logger(self):
        """Test the FileLogger class by creating a fake log file and verifying the logs format."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = f"{tmpdir}/test_logger.txt"  # Create a temporary log file path
            logger = FileLogger("test_logger")  # Initialize the FileLogger
            logger.log_file = (
                log_path  # Ensure the logger writes to the correct location
            )

            # Write logs
            logger("First log")
            logger("Second log")

            # Read and verify the logs in the file
            with open(log_path, "r") as f:
                self.assertEqual(
                    f.read().splitlines(), ["First log", "Second log"]
                )  # Check if logs match


if __name__ == "__main__":
    unittest.main()
