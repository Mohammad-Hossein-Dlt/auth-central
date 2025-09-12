class AppBaseException(Exception):
    """Base class for other custom exceptions."""
    
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        
        super().__init__(message)

class Error(AppBaseException):
    """Raised for general errors"""

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code, message)

class InvalidRequestException(AppBaseException):
    """Raised for general errors (mostly for 400)"""

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code, message)

class AuthenticationException(AppBaseException):
    """This exception is raised when an authentication error occurs"""

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code, message)

class InvalidTokenException(AppBaseException):
    """This exception is raised when a token is invalid"""

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code, message)

class TokenExpiredException(AppBaseException):
    """This exception is raised when a token expired"""

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code, message)

class OperationFailureException(AppBaseException):
    """Raised for unknown errors in database operations"""

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code, message)

class EntityNotFoundError(AppBaseException):
    """This exception is raised when an entity is not exists"""

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code, message)
