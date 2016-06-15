========
duration
========

python time duration conversion module

Installation
------------

::

    pip install duration


Usage
-----

Examples below show how to convert timestamps in ``hh:mm:ss`` and ``mm:ss`` format
to iso8601 strings, integer seconds, datetime.timedelta objects and 
(hours, minutes, seconds,) deltas

.. code:: python

    from duration import (
        to_iso8601,
        to_seconds,
        to_timedelta,
        to_tuple,
    )

    time = '1:23:45'

    iso8601 = to_iso8601(time) # 'PT01H23M45S'
    seconds = to_seconds(time) # 5025
    td = to_timedelta(time) # timedelta(hours=1, minutes=23, seconds=45)
    tuple_ = to_tuple(time) # (1, 23, 45,)

Examples above use strict mode by default. In strict mode, conversion 
functions raise ``StrictnessError`` if your duration string meets one of the
following conditions:

1. hh > 23
2. mm > 59
3. ss > 59

To disable strict mode, pass ``strict=False`` to the conversion function

.. code:: python

    from duration import (
        to_iso8601,
        to_seconds,
        to_timedelta,
        to_tuple,
    )

    time = '24:83:25'

    iso8601 = to_iso8601(time, strict=False) # 'P1DT01H23M25S'
    seconds = to_seconds(time) # 91405
    td = to_timedelta(time) # timedelta(seconds=91405)
    tuple_ = to_tuple(time) # (25, 23, 25,)
