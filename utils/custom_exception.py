"""
Custom Exception Handling

This module defines a custom exception class that enriches error messages
with contextual information such as file name and line number.
"""

import sys


class CustomException(Exception):
    """
    Custom exception class that provides detailed error information.

    The exception captures:
    - Custom error message
    - Original exception details (if any)
    - Source file name
    - Line number where the exception occurred
    """

    def __init__(self, message: str, error_detail: Exception = None):
        """
        Initialize the CustomException.

        Args:
            message (str): Custom error message describing the failure.
            error_detail (Exception, optional): Original exception instance.
        """
        # Build a detailed error message including traceback info
        self.error_message = self.get_detailed_error_message(
            message,
            error_detail
        )

        # Initialize the base Exception class
        super().__init__(self.error_message)

    @staticmethod
    def get_detailed_error_message(
        message: str,
        error_detail: Exception = None
    ) -> str:
        """
        Generate a detailed error message with traceback information.

        Args:
            message (str): Custom error message.
            error_detail (Exception, optional): Original exception.

        Returns:
            str: Formatted error message including file and line number.
        """

        # Retrieve the current exception traceback
        _, _, exc_tb = sys.exc_info()

        # Extract file name and line number if traceback exists
        file_name = (
            exc_tb.tb_frame.f_code.co_filename
            if exc_tb else "Unknown File"
        )
        line_number = (
            exc_tb.tb_lineno
            if exc_tb else "Unknown Line"
        )

        return (
            f"{message} | "
            f"Error: {str(error_detail)} | "
            f"File: {file_name} | "
            f"Line: {line_number}"
        )

    def __str__(self) -> str:
        """
        Return the formatted error message when the exception is printed.

        Returns:
            str: Detailed error message.
        """
        return self.error_message