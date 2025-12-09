# Basic test file for sample project
# Note: This file intentionally has minimal coverage to demonstrate SonarQube

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import calculate_average, add_numbers, is_even

class TestMain(unittest.TestCase):
    
    def test_calculate_average_basic(self):
        # Test with normal numbers
        result = calculate_average([1, 2, 3, 4, 5])
        self.assertEqual(result, 3.0)
    
    def test_add_numbers(self):
        # Test addition
        result = add_numbers(5, 3)
        self.assertEqual(result, 8)
    
    # Note: Missing tests for:
    # - calculate_average with empty list (bug case)
    # - is_even function (has logic bug)
    # - authenticate_user (security issue)
    # - read_file (error handling)
    # - And many other functions

if __name__ == '__main__':
    unittest.main()

