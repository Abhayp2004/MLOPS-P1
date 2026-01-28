import sys
from typing import Optional


class CustomException(Exception):
    def __init__(self, error_message: str, error_detail=None):
        """
        error_message: custom error message
        error_detail: sys module or exception object (to fetch traceback info)
        """
        self.error_message = self.get_detailed_error_message(
            error_message, error_detail or sys
        )
        super().__init__(self.error_message)

    @staticmethod
    def get_detailed_error_message(
        error_message: str, error_detail=None
    ) -> str:
        try:
            # Check if error_detail is sys module (has exc_info method)
            if error_detail is sys or (hasattr(error_detail, 'exc_info') and callable(getattr(error_detail, 'exc_info', None))):
                _, _, exc_tb = error_detail.exc_info()
            else:
                # If it's an exception object or something else, get traceback from current exception
                _, _, exc_tb = sys.exc_info()
        except (AttributeError, TypeError):
            # Fallback: try to get traceback from sys
            _, _, exc_tb = sys.exc_info()
        
        if exc_tb is None:
            return error_message

        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        return (
            f"Error occurred in script: [{file_name}] "
            f"at line number: [{line_number}] "
            f"error message: [{error_message}]"
        )