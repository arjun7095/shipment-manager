class CoreException(Exception):
    """Base exception class"""


class InvalidIdFormat(CoreException):
    """Invalid ID format"""


class InvalidContentData(CoreException):
    """Invalid content data exception"""


class ContentNotSet(CoreException):
    """Content not set exception"""


class NoDataFound(CoreException):
    """No data found"""
