"""
Custom exceptions for ACS ZEEP Client
"""

class ACSZeepException(Exception):
    """Base exception for ACS ZEEP Client"""
    pass

class AuthenticationError(ACSZeepException):
    """Raised when authentication fails"""
    pass

class APIError(ACSZeepException):
    """Raised when API request fails"""
    def __init__(self, message: str, status_code: int = None, response_data=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

class ConnectionError(ACSZeepException):
    """Raised when connection to API fails"""
    pass

class ValidationError(ACSZeepException):
    """Raised when request validation fails"""
    pass

class NotFoundError(APIError):
    """Raised when resource is not found"""
    pass

class UnauthorizedError(APIError):
    """Raised when request is unauthorized"""
    pass

class ForbiddenError(APIError):
    """Raised when request is forbidden"""
    pass
