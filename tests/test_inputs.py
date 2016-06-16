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

    def setUp(self):
        self.configure()
        self.values = [
            self.string, self.seconds,
            self.timedelta, self.tuple_
        ]
        self.converters = {
            'to_iso8601': (
                to_iso8601, self.iso8601,
            ),
            'to_seconds': (
                to_seconds, self.seconds,
            ),
            'to_timedelta': (
                to_timedelta, self.timedelta,
            ),
            'to_tuple': (
                to_tuple, self.tuple_,
            )
        }

    def run_converter(self, name):
        converter, correct_result = self.converters[name]
        for value in self.values:
            result = converter(value)
            self.assertEqual(result, correct_result)

    def test_to_seconds(self):
        self.run_converter('to_seconds')

    def test_to_tuple(self):
        self.run_converter('to_tuple')

    def test_to_timedelta(self):
        self.run_converter('to_timedelta')

    def test_to_iso8601(self):
        self.run_converter('to_iso8601')


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

    def configure(self):
        self.string = "0:25"
        self.seconds = 25
        self.timedelta = timedelta(seconds=25)
        self.tuple_ = (0, 0, 25,)
        self.iso8601 = 'PT25S'


class TestMinutesSeconds(BaseInputsTest, unittest.TestCase):
    """Checks inputs of mm:ss format"""

    def configure(self):
        self.string = "3:47"
        self.seconds = 227
        self.timedelta = timedelta(seconds=227)
        self.tuple_ = (0, 3, 47,)
        self.iso8601 = 'PT03M47S'


class TestHoursMinutesSeconds(BaseInputsTest, unittest.TestCase):
    """Checks inputs of hh:mm:ss format"""

    def configure(self):
        self.string = "1:23:45"
        self.seconds = 5025
        self.timedelta = timedelta(
            hours=1, minutes=23, seconds=45)
        self.tuple_ = (1, 23, 45,)
        self.iso8601 = 'PT01H23M45S'


class TestToSeconds(unittest.TestCase):

    def test_int(self):
        value = 5025  # seconds
        seconds = to_seconds(value)
        self.assertEqual(seconds, value)

    def test_tuple(self):
        value = (1, 23, 45,)
        seconds = to_seconds(value)
        self.assertEqual(seconds, 5025)

    def test_str(self):
        value = "1:23:45"
        seconds = to_seconds(value)
        self.assertEqual(seconds, 5025)

    def test_timedelta(self):
        value = timedelta(hours=1, minutes=23, seconds=45)
        seconds = to_seconds(value)
        self.assertEqual(seconds, 5025)


class TestIsoInputs(unittest.TestCase):

    def test_int(self):
        value = 5025  # seconds
        iso8601 = to_iso8601(value)
        self.assertEqual(iso8601, 'PT01H23M45S')

    def test_tuple(self):
        value = (1, 23, 45,)
        iso8601 = to_iso8601(value)
        self.assertEqual(iso8601, 'PT01H23M45S')

    def test_str(self):
        value = "1:23:45"
        iso8601 = to_iso8601(value)
        self.assertEqual(iso8601, 'PT01H23M45S')

    def test_timedelta(self):
        value = timedelta(hours=1, minutes=23, seconds=45)
        iso8601 = to_iso8601(value)
        self.assertEqual(iso8601, 'PT01H23M45S')
