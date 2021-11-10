"""
    Exceptions for Pywr parsing and network operations
"""

class HydraPywrException(Exception):
    """  Base class for all package exceptions """
    pass

class PywrParseException(HydraPywrException):
    """  Errors in parsing input prior to building network """
    pass

class PywrNetworkException(HydraPywrException):
    """  Errors in validating network instance """
    pass
