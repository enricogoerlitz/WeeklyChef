"""
API exceptions
"""


class FieldRequiredException(Exception):
    """Exception for not passed fields in request"""
    pass


class MethodNotImplementedException(Exception):
    """Exception for not implemented methods"""
    pass
