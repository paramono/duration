#!/usr/bin/python3
"""
duration.py module is a collection of fuctions for converting hh:mm:ss
and mm:ss time duration strings to timedeltas, (h, m, s,)-tuples of
integers or seconds (integers)
"""

import re
from datetime import timedelta


class StrictnessError(ValueError):
    """
    raised when hours, minutes or seconds in duration string exceed
    allowed values
    """


class NegativeDurationError(ValueError):
    """
    Raised when either hours, minutes or seconds in duration string
    are negative. Used internally only, in safe_int as a safeguard,
    since regular expression pattern does not take negative values
    into consideration
    """


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


def _parse(string, strict=True):
    """
    Preliminary duration string parser

    strict=True (by default) raises StrictnessError if either hours,
    minutes or seconds in duration string exceed allowed values
    """
    pattern = r'(?:(?P<hours>\d+):)?(?P<minutes>\d+):(?P<seconds>\d+)'
    match = re.match(pattern, string)
    if not match:
        raise ValueError('Invalid duration string: %s' % string)
    hours = safe_int(match.group('hours'))
    minutes = safe_int(match.group('minutes'))
    seconds = safe_int(match.group('seconds'))

    if strict:
        if hours > 23:
            raise StrictnessError(
                'Hours cannot have a value greater than 23 in strict mode'
            )
        if minutes > 59:
            raise StrictnessError(
                'Minutes cannot have a value greater than 59 in strict mode'
            )
        if seconds > 59:
            raise StrictnessError(
                'Seconds cannot have a value greater than 59 in strict mode'
            )
    return (hours, minutes, seconds,)


def to_iso8601(string, strict=True):
    """
    converts duration string to ISO8601 string

    strict=True (by default) raises StrictnessError if either hours,
    minutes or seconds in duration string exceed allowed values
    """
    # split seconds to larger units
    # seconds = value.total_seconds()
    seconds = to_seconds(string, strict)
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
    if isinstance(seconds, int):
        seconds = '{:02}'.format(int(seconds))
    else:
        # 9 chars long w/leading 0, 6 digits after decimal
        seconds = '%09.6f' % seconds

    # remove trailing zeros
    seconds = seconds.rstrip('0')
    time += '{}S'.format(seconds)
    return 'P' + date + time


def to_seconds(string, strict=True):
    """
    converts duration string to integer seconds

    strict=True (by default) raises StrictnessError if either hours,
    minutes or seconds in duration string exceed allowed values
    """
    hours, minutes, seconds = _parse(string, strict)
    if not (hours or minutes or seconds):
        raise ValueError('No hours, minutes or seconds found in string')
    result = hours*3600 + minutes*60 + seconds
    return result


def to_timedelta(string, strict=True):
    """
    converts duration string to timedelta

    strict=True (by default) raises StrictnessError if either hours,
    minutes or seconds in duration string exceed allowed values
    """
    hours, minutes, seconds = _parse(string, strict)
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


def to_tuple(string, strict=True):
    """
    converts duration string to tuple of integers

    strict=True (by default) raises StrictnessError if either hours,
    minutes or seconds in duration string exceed allowed values
    """
    hours, minutes, seconds = _parse(string, strict)
    seconds = hours*3600 + minutes*60 + seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return (hours, minutes, seconds,)
