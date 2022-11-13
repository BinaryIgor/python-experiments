from unittest import TestCase
from src import field_validator


class TestFieldValidator(TestCase):

    def test_should_validate_integer(self):
        test_cases = [
            ("2", True),
            ("2456", True),
            ("0", True),
            ("-2", True),
            ("-224", True),
            ("", False),
            (None, False),
            ("ada90=-+", False),
            ("56 adada", False),
            ("Ad dx09", False),
            ("Ad 877", False)
        ]

        for string, valid in test_cases:
            with self.subTest(string=string, valid=valid):
                self.assertEqual(valid, field_validator.is_valid_integer(string))

    def test_should_validate_double(self):
        test_cases = [
            ("22", True),
            ("0", True),
            ("-2", True),
            ("-224", True),
            ("2.2", True),
            ("222.298", True),
            ("12,2", True),
            ("4,898", True),
            ("-8.898", True),
            ("-823.8", True),
            ("122.8", True),
            ("", False),
            (" ", False),
            (None, False),
            ("aX9X=-@", False),
            ("56 adadadd", False),
            ("56.9 adadadd", False),
            ("Ad dx09", False),
            ("Ad 877.88", False),
            ("X 8,88", False)
        ]

        for string, valid in test_cases:
            with self.subTest(string=string, valid=valid):
                self.assertEqual(valid, field_validator.is_valid_double(string))

    def test_should_validate_name(self):
        too_long_name = ''.join(['c' for _ in range(21)])

        test_cases = [
            ("Ada", True),
            ("ax123", True),
            ("a12", True),
            ("z12_-", True),
            ("1dada", False),
            ("some name", False),
            ("some\name233", False),
            ("2344", False),
            (" ", False),
            (None, False),
            ("so", False),
            (too_long_name, False)
        ]

        for string, valid in test_cases:
            with self.subTest(string=string, valid=valid):
                self.assertEqual(valid, field_validator.is_valid_name(string))
