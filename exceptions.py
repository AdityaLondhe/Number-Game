"""
Custom Exceptions Module
Demonstrates custom exception classes, exception hierarchy, and error handling patterns.
Enhanced with session-specific exceptions.
"""

import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)


class BrainPlayException(Exception):
    """
    Base exception class for all BrainPlay game exceptions.
    Demonstrates exception hierarchy and custom exception design.
    """
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[dict] = None):
        """
        Initialize base exception with enhanced error information.
        
        Args:
            message: Human-readable error message
            error_code: Machine-readable error code for programmatic handling
            details: Additional error context and debugging information
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__.upper()
        self.details = details or {}
        
        # Log the exception when created
        logger.error(f"Exception created: {self.error_code} - {message}")
        if self.details:
            logger.debug(f"Exception details: {self.details}")
    
    def __str__(self) -> str:
        """String representation of the exception."""
        return f"[{self.error_code}] {self.message}"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"{self.__class__.__name__}(message='{self.message}', error_code='{self.error_code}')"
    
    def to_dict(self) -> dict:
        """
        Convert exception to dictionary for JSON serialization.
        Useful for API responses or logging.
        """
        return {
            'exception_type': self.__class__.__name__,
            'message': self.message,
            'error_code': self.error_code,
            'details': self.details
        }


class GameExitException(BrainPlayException):
    """
    Exception raised when player wants to exit the game.
    Demonstrates specific exception for control flow.
    """
    
    def __init__(self, message: str = "Player requested to exit game", exit_reason: str = "user_request"):
        super().__init__(
            message=message,
            error_code="GAME_EXIT",
            details={'exit_reason': exit_reason}
        )
        self.exit_reason = exit_reason


class InvalidInputException(BrainPlayException):
    """
    Exception raised for invalid user input.
    Demonstrates input validation exceptions.
    """
    
    def __init__(self, message: str, input_value: Any = None, expected_format: str = None):
        details = {}
        if input_value is not None:
            details['input_value'] = str(input_value)
        if expected_format:
            details['expected_format'] = expected_format
        
        super().__init__(
            message=message,
            error_code="INVALID_INPUT",
            details=details
        )
        self.input_value = input_value
        self.expected_format = expected_format


class QuestionGenerationException(BrainPlayException):
    """
    Exception raised when question generation fails.
    Demonstrates domain-specific exceptions.
    """
    
    def __init__(self, message: str, question_type: str = None, difficulty: str = None):
        details = {}
        if question_type:
            details['question_type'] = question_type
        if difficulty:
            details['difficulty'] = difficulty
        
        super().__init__(
            message=message,
            error_code="QUESTION_GENERATION_FAILED",
            details=details
        )
        self.question_type = question_type
        self.difficulty = difficulty


class SessionException(BrainPlayException):
    """
    Exception raised for session-related errors.
    Demonstrates session management exceptions.
    """
    
    def __init__(self, message: str, session_id: str = None, player_name: str = None):
        details = {}
        if session_id:
            details['session_id'] = session_id
        if player_name:
            details['player_name'] = player_name
        
        super().__init__(
            message=message,
            error_code="SESSION_ERROR",
            details=details
        )
        self.session_id = session_id
        self.player_name = player_name


class ScoreException(BrainPlayException):
    """
    Exception raised for score-related errors.
    Demonstrates data integrity exceptions.
    """
    
    def __init__(self, message: str, current_score: int = None, attempted_operation: str = None):
        details = {}
        if current_score is not None:
            details['current_score'] = current_score
        if attempted_operation:
            details['attempted_operation'] = attempted_operation
        
        super().__init__(
            message=message,
            error_code="SCORE_ERROR",
            details=details
        )
        self.current_score = current_score
        self.attempted_operation = attempted_operation


# Exception handling utilities and decorators
def handle_exceptions(default_return=None, log_level=logging.ERROR):
    """
    Decorator to handle exceptions gracefully.
    Demonstrates decorator pattern for exception handling.
    
    Args:
        default_return: Value to return if exception occurs
        log_level: Logging level for caught exceptions
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except BrainPlayException as e:
                logger.log(log_level, f"BrainPlay exception in {func.__name__}: {e}")
                return default_return
            except Exception as e:
                logger.log(log_level, f"Unexpected exception in {func.__name__}: {e}")
                return default_return
        return wrapper
    return decorator


def safe_execute(func, *args, **kwargs):
    """
    Safely execute a function and return result or exception.
    Demonstrates functional approach to exception handling.
    
    Returns:
        tuple: (success: bool, result_or_exception: Any)
    """
    try:
        result = func(*args, **kwargs)
        return True, result
    except Exception as e:
        return False, e


# Example usage and testing
if __name__ == "__main__":
    """
    Module testing and demonstration.
    Shows exception hierarchy and handling patterns.
    """
    
    print("Testing Custom Exceptions...")
    
    # Test basic exception creation
    try:
        raise InvalidInputException("Test input error", input_value="abc", expected_format="integer")
    except InvalidInputException as e:
        print(f"Caught exception: {e}")
        print(f"Exception dict: {e.to_dict()}")
    
    # Test session exception
    try:
        raise SessionException("Session expired", session_id="12345", player_name="TestPlayer")
    except SessionException as e:
        print(f"Session exception: {e}")
    
    # Test exception decorator
    @handle_exceptions(default_return="Error occurred")
    def risky_function():
        raise QuestionGenerationException("Test error")
    
    result = risky_function()
    print(f"Decorated function result: {result}")
    
    # Test safe execution
    def another_risky_function():
        raise RuntimeError("Something went wrong")
    
    success, result = safe_execute(another_risky_function)
    print(f"Safe execution - Success: {success}, Result: {result}")