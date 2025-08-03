"""Custom error handling for Varphi language syntax errors.

This module provides error handling components for the Varphi language parser.

Classes:
    VarphiSyntaxError: Custom exception for Varphi syntax errors with line/column info.
    VarphiSyntaxErrorListener: ANTLR4 error listener that formats and raises syntax errors.
"""

from antlr4.error.ErrorListener import ErrorListener


class VarphiSyntaxError(Exception):
    """Exception raised for general syntax errors."""

    line: int
    column: int

    def __init__(self, message: str, line: int, column: int) -> None:
        """Initializes a VarphiSyntaxError with a message, line, and column.

        Args:
            message (str): The error message.
            line (int): The line where the error occurred.
            column (int): The column where the error occurred.
        """
        super().__init__(message)
        self.line = line
        self.column = column


class VarphiSyntaxErrorListener(ErrorListener):
    """Custom error listener for Varphi syntax errors.

    This listener processes syntax errors and raises an exception with a detailed
    error message, including the specific line and column where the error occurred.
    """

    input_text: list[str]

    def __init__(self, input_text: str) -> None:
        """Initializes the VarphiSyntaxErrorListener with the input text.

        Args:
            input_text (str): The input text to be processed.
        """
        super().__init__()
        self.input_text = input_text.splitlines()

    def syntaxError(self,  # pylint: disable=too-many-arguments, too-many-positional-arguments
                    recognizer,
                    offendingSymbol,
                    line,
                    column,
                    msg,
                    e
    ) -> None:
        """Handles syntax errors encountered by the parser.

        Raises a VarphiSyntaxError with detailed information about the error.

        Args:
            recognizer: The recognizer that encountered the error.
            offending_symbol: The symbol that caused the error.
            line (int): The line number where the error occurred.
            column (int): The column number where the error occurred.
            msg (str): The error message.
            e: The exception that caused the error.
        """
        error_line = self.input_text[line - 1]
        # Create a line with ^ pointing to the offending symbol
        pointer_line = " " * column + "^"

        # Format the error message
        error = f"Syntax error at line {line}:{column} - {msg}\n"
        error += f"    {error_line}\n"
        error += f"    {pointer_line}\n"

        raise VarphiSyntaxError(error, line, column)
