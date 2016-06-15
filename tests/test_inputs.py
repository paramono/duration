"""
Tests various inputs for (in)validity
"""

import unittest

from datetime import timedelta
from duration import (
    to_seconds,
    to_tuple,
    to_timedelta,
    to_iso8601,
)

from .base import BaseTest


class BaseInputsTest(BaseTest):
    """
    Common test methods for each conversion function
    """

    def test_to_seconds(self):
        seconds = to_seconds(self.string)
        self.assertEqual(seconds, self.expected_seconds)

    def test_to_tuple(self):
        tuple_ = to_tuple(self.string)
        self.assertEqual(tuple_, self.expected_tuple)

    def test_to_timedelta(self):
        td = to_timedelta(self.string)
        self.assertEqual(td, self.expected_timedelta)

    def test_to_iso8601(self):
        iso8601 = to_iso8601(self.string)
        self.assertEqual(iso8601, self.expected_iso8601)


class TestInvalidInputs(BaseTest, unittest.TestCase):
    """Checks that invalid inputs raise exceptions"""

    strings = ['25', ':25', '3:', ':::', '::']

    def test_to_seconds(self):
        for string in self.strings:
            with self.assertRaises(ValueError):
                to_seconds(string)

    def test_to_tuple(self):
        for string in self.strings:
            with self.assertRaises(ValueError):
                to_tuple(string)

    def test_to_timedelta(self):
        for string in self.strings:
            with self.assertRaises(ValueError):
                to_timedelta(string)

    def test_to_iso8601(self):
        for string in self.strings:
            with self.assertRaises(ValueError):
                to_iso8601(string)


class TestNegativeInputs(BaseTest, unittest.TestCase):
    """check that negative inputs raise ValueError"""

    strings = [
        '0:-25', '-2:23', '-5:-55', '-1:12:23',
        '-12:24:-43', '-5:-43:29', '-10:-23:-12',
    ]

    def test_to_seconds(self):
        for string in self.strings:
            with self.assertRaises(ValueError):
                to_seconds(string)

    def test_to_timedelta(self):
        for string in self.strings:
            with self.assertRaises(ValueError):
                to_timedelta(string)

    def test_to_tuple(self):
        for string in self.strings:
            with self.assertRaises(ValueError):
                to_tuple(string)

    def test_to_iso8601(self):
        for string in self.strings:
            with self.assertRaises(ValueError):
                to_iso8601(string)


class TestZeroColonSeconds(BaseInputsTest, unittest.TestCase):
    """Checks inputs of 0:ss format"""

    def setUp(self):
        self.string = "0:25"
        self.expected_seconds = 25
        self.expected_timedelta = timedelta(seconds=25)
        self.expected_tuple = (0, 0, 25,)
        self.expected_iso8601 = 'PT25S'


class TestMinutesSeconds(BaseInputsTest, unittest.TestCase):
    """Checks inputs of mm:ss format"""

    def setUp(self):
        self.string = "3:47"
        self.expected_seconds = 227
        self.expected_timedelta = timedelta(seconds=227)
        self.expected_tuple = (0, 3, 47,)
        self.expected_iso8601 = 'PT03M47S'


class TestHoursMinutesSeconds(BaseInputsTest, unittest.TestCase):
    """Checks inputs of hh:mm:ss format"""

    def setUp(self):
        self.string = "1:23:45"
        self.expected_seconds = 5025
        self.expected_timedelta = timedelta(
            hours=1, minutes=23, seconds=45)
        self.expected_tuple = (1, 23, 45,)
        self.expected_iso8601 = 'PT01H23M45S'
