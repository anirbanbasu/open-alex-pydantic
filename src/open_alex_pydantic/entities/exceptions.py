from pydantic import ValidationError


class WorkParsingError(ValueError):
    """Domain exception for public Work parsing failures."""

    def __init__(self, message: str, cause: ValidationError):
        super().__init__(message)
        self.cause = cause


class AuthorParsingError(ValueError):
    """Domain exception for public Author parsing failures."""

    def __init__(self, message: str, cause: ValidationError):
        super().__init__(message)
        self.cause = cause
