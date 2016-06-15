import unittest
from datetime import timedelta

from duration import (
    to_seconds,
    to_tuple,
    to_timedelta,
    to_iso8601,
    StrictnessError,
)

from .base import BaseTest


class BaseStrictnessTest(BaseTest):

    def test_to_seconds(self):
        with self.assertRaises(StrictnessError):
            seconds = to_seconds(self.string, strict=True)
        seconds = to_seconds(self.string, strict=False)
        self.assertEqual(seconds, self.expected_seconds)

    def test_to_tuple(self):
        with self.assertRaises(StrictnessError):
            tuple_ = to_tuple(self.string, strict=True)
        tuple_ = to_tuple(self.string, strict=False)
        self.assertEqual(tuple_, self.expected_tuple)

    def test_to_timedelta(self):
        with self.assertRaises(StrictnessError):
            timedelta_ = to_timedelta(self.string, strict=True)
        timedelta_ = to_timedelta(self.string, strict=False)
        self.assertEqual(timedelta_, self.expected_timedelta)

    def test_to_iso8601(self):
        with self.assertRaises(StrictnessError):
            iso8601 = to_iso8601(self.string, strict=True)
        iso8601 = to_iso8601(self.string, strict=False)
        self.assertEqual(iso8601, self.expected_iso8601)


class TestStrictnessZeroColonBigSeconds(BaseStrictnessTest, unittest.TestCase):

    def setUp(self):
        self.string = "0:72"
        self.expected_seconds = 72
        self.expected_timedelta = timedelta(seconds=72)
        self.expected_tuple = (0, 1, 12,)
        self.expected_iso8601 = 'PT01M12S'


class TestStrictnessBigSeconds(BaseStrictnessTest, unittest.TestCase):

    def setUp(self):
        self.string = "2:65"
        self.expected_seconds = 185
        self.expected_timedelta = timedelta(seconds=185)
        self.expected_tuple = (0, 3, 5,)
        self.expected_iso8601 = 'PT03M05S'


class TestStrictnessBigMinutes(BaseStrictnessTest, unittest.TestCase):

    def setUp(self):
        self.string = "61:29"
        self.expected_seconds = 3689
        self.expected_timedelta = timedelta(seconds=3689)
        self.expected_tuple = (1, 1, 29,)
        self.expected_iso8601 = 'PT01H01M29S'


class TestStrictnessBigHours(BaseStrictnessTest, unittest.TestCase):

    def setUp(self):
        self.string = "24:59:21"
        self.expected_seconds = 89961
        self.expected_timedelta = timedelta(seconds=89961)
        self.expected_tuple = (24, 59, 21,)
        self.expected_iso8601 = 'P1DT00H59M21S'


class TestStrictnessBigHoursMinutes(BaseStrictnessTest, unittest.TestCase):

    def setUp(self):
        self.string = "24:83:25"
        self.expected_seconds = 91405
        self.expected_timedelta = timedelta(seconds=91405)
        self.expected_tuple = (25, 23, 25,)
        self.expected_iso8601 = 'P1DT01H23M25S'


class TestStrictnessBigHoursMinutesSeconds(
    BaseStrictnessTest,
    unittest.TestCase
):

    def setUp(self):
        self.string = "24:83:61"
        self.expected_seconds = 91441
        self.expected_timedelta = timedelta(seconds=91441)
        self.expected_tuple = (25, 24, 1,)
        self.expected_iso8601 = 'P1DT01H24M01S'
