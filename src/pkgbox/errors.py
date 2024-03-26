"""
Errors module which contains all error handling source code.
"""
import errno


class PBError(Exception):
    """
    Base error class to be inherited from by other specialized
    error classes.
    """
    def __init__(self, message: str, errno: int = 1) -> None:
        """
        Create a new PBError object instance.
        """
        super(PBError, self).__init__(message)

        self.message = message
        self.errno = errno

    def __str__(self) -> str:
        """
        Return the user friendly string representation
        of the error.
        """
        return f'ERR: {self.message}'
    
    def __eq__(self, other) -> bool:
        """
        Method implementation when comparing two error objects.

        It checks if both `message` and `errno` properties are the same.
        """
        if other is None:
            return False

        if self.message != other.message:
            return False

        if self.errno != other.errno:
            return False

        return True


class PBNotImplementedError(PBError):
    """
    This error should be raised when a feature or
    API ha not been implemented yet.
    """
    def __init__(self) -> None:
        """
        Create a new object instance of this error.
        """
        super(PBNotImplementedError, self).__init__('Not Implemented', errno.ENOSYS)
