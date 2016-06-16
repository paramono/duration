class StrictnessError(ValueError):
    """
    raised when hours, minutes or seconds in duration string exceed
    allowed values
    """


class WrongTupleSizeError(ValueError):
    """
    raised when tuple size is not equal to 3
    (hours, minutes, seconds,)
    """


class NegativeDurationError(ValueError):
    """
    Raised when either hours, minutes or seconds in duration string
    are negative. Used internally only, in safe_int, as a safeguard,
    since regular expression pattern does not take negative values
    into consideration
    """
