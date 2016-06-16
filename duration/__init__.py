#!/usr/bin/python3
"""
duration.py module is a collection of fuctions for converting hh:mm:ss
and mm:ss time duration strings to timedeltas, (h, m, s,)-tuples of
integers or seconds (integers)
"""

import re
from datetime import timedelta

from .exceptions import (
    StrictnessError,
    WrongTupleSizeError,
    NegativeDurationError,
)


def safe_int(value):
    """
    Tries to convert a value to int; returns 0 if conversion failed
    """
    try:
        result = int(value)
        if result < 0:
            raise NegativeDurationError(
                'Negative values in duration strings are not allowed!'
            )
    except NegativeDurationError as exc:
        raise exc
    except (TypeError, ValueError):
        result = 0
    return result


def _fix_tuple(tuple_):
    hours, minutes, seconds = tuple_
    seconds = hours*3600 + minutes*60 + seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return (hours, minutes, seconds,)


def _parse(value, strict=True):
    """
    Preliminary duration value parser

    strict=True (by default) raises StrictnessError if either hours,
    minutes or seconds in duration value exceed allowed values
    """
    pattern = r'(?:(?P<hours>\d+):)?(?P<minutes>\d+):(?P<seconds>\d+)'
    match = re.match(pattern, value)
    if not match:
        raise ValueError('Invalid duration value: %s' % value)
    hours = safe_int(match.group('hours'))
    minutes = safe_int(match.group('minutes'))
    seconds = safe_int(match.group('seconds'))

    check_tuple((hours, minutes, seconds,), strict)

    return (hours, minutes, seconds,)


def check_tuple(tuple_, strict=True):
    if len(tuple_) != 3:
        raise WrongTupleSizeError(
            'Duration tuple size must be equal to 3! '
            'Passed tuple has a length of %s' % len(tuple_)
        )

    if not strict:
        return

    hours, minutes, seconds = tuple_

    if hours > 23:
        raise StrictnessError(
            'Hours cannot have a value greater than 23 in strict mode '
            'You passed: %d hours' % hours
        )
    if minutes > 59:
        raise StrictnessError(
            'Minutes cannot have a value greater than 59 in strict mode '
            'You passed: %d minutes' % minutes
        )
    if seconds > 59:
        raise StrictnessError(
            'Seconds cannot have a value greater than 59 in strict mode'
            'You passed: %d seconds' % seconds
        )


def to_iso8601(value, strict=True, force_int=True):
    """
    converts duration value to ISO8601 string
    accepts integers, hh:mm:ss or mm:ss strings, timedelta objects

    strict=True (by default) raises StrictnessError if either hours,
    minutes or seconds in duration string exceed allowed values
    """
    # split seconds to larger units
    # seconds = value.total_seconds()
    seconds = to_seconds(value, strict, force_int)

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    days, hours, minutes = map(int, (days, hours, minutes))
    seconds = round(seconds, 6)

    # build date
    date = ''
    if days:
        date = '%sD' % days

    # build time
    time = 'T'

    # hours
    bigger_exists = date or hours
    if bigger_exists:
        time += '{:02}H'.format(hours)

    # minutes
    bigger_exists = bigger_exists or minutes
    if bigger_exists:
        time += '{:02}M'.format(minutes)

    # seconds
    if isinstance(seconds, int) or force_int:
        seconds = '{:02}'.format(int(seconds))
    else:
        # 9 chars long w/leading 0, 6 digits after decimal
        seconds = '%09.6f' % seconds

    time += '{}S'.format(seconds)
    return 'P' + date + time


def to_seconds(value, strict=True, force_int=True):
    """
    converts duration value to integer seconds

    strict=True (by default) raises StrictnessError if either hours,
    minutes or seconds in duration value exceed allowed values
    """
    if isinstance(value, int):
        return value  # assuming it's seconds
    elif isinstance(value, timedelta):
        seconds = value.total_seconds()
        if force_int:
            seconds = int(round(seconds))
        return seconds
    elif isinstance(value, str):
        hours, minutes, seconds = _parse(value, strict)
    elif isinstance(value, tuple):
        check_tuple(value, strict)
        hours, minutes, seconds = value
    else:
        raise TypeError(
            'Value %s (type %s) not supported' % (
                value, type(value).__name__
            )
        )

    if not (hours or minutes or seconds):
        raise ValueError('No hours, minutes or seconds found')

    result = hours*3600 + minutes*60 + seconds
    return result


def to_timedelta(value, strict=True):
    """
    converts duration string to timedelta

    strict=True (by default) raises StrictnessError if either hours,
    minutes or seconds in duration string exceed allowed values
    """
    if isinstance(value, int):
        return timedelta(seconds=value)  # assuming it's seconds
    elif isinstance(value, timedelta):
        return value
    elif isinstance(value, str):
        hours, minutes, seconds = _parse(value, strict)
    elif isinstance(value, tuple):
        check_tuple(value, strict)
        hours, minutes, seconds = value
    else:
        raise TypeError(
            'Value %s (type %s) not supported' % (
                value, type(value).__name__
            )
        )
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


def to_tuple(value, strict=True, force_int=True):
    """
    converts duration value to tuple of integers

    strict=True (by default) raises StrictnessError if either hours,
    minutes or seconds in duration value exceed allowed values
    """
    if isinstance(value, int):
        seconds = value
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
    elif isinstance(value, str):
        hours, minutes, seconds = _fix_tuple(
            _parse(value, strict)
        )
    elif isinstance(value, tuple):
        check_tuple(value, strict)
        hours, minutes, seconds = _fix_tuple(value)
    elif isinstance(value, timedelta):
        seconds = value.total_seconds()
        if force_int:
            seconds = int(round(seconds))
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

    return (hours, minutes, seconds,)
