"""
API exceptions
"""


class FieldRequiredError(Exception):
    """Exception for not passed fields in request"""
    pass


class MethodNotImplementedError(Exception):
    """Exception for not implemented methods"""
    pass


class NotEqualError(Exception):
    """Exception for objects not equal"""
    pass
