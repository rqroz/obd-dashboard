"""
Generic exception classes
"""

class DictException(Exception):
    """
    Exception class.

    Attributes:
        - errors (dict): Map of errors raised.
    """
    def __init__(self, errors: dict):
        self.errors = errors
