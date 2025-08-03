"""
EmptyChecker - A simple toy compiler that checks if input contains any lines.

This compiler serves as a basic example of the VarphiCompiler interface,
demonstrating how to track state across line processing and generate output.
"""

from varphi_devkit import VarphiCompiler, VarphiLine


class EmptyChecker(VarphiCompiler):
    """
    A toy compiler that determines whether the input contains any lines.
    
    This compiler tracks whether it has encountered at least one line during
    processing. It serves as a minimal example of stateful compilation where
    the presence or absence of input affects the output.
    
    Attributes:
        seen_line (bool): Flag indicating whether any line has been processed.
                         Initialized to False and set to True upon encountering
                         the first line.
    
    Examples:
        >>> checker = EmptyChecker()
        >>> # For empty input
        >>> checker.generate_compiled_program()
        'EMPTY'
        
        >>> # After processing at least one line
        >>> checker.handle_line(some_line)
        >>> checker.generate_compiled_program()
        'NOT EMPTY'
    """
    
    seen_line: bool
    
    def __init__(self) -> None:
        """
        Initialize the EmptyChecker with default state.
        
        Sets seen_line to False, indicating no lines have been processed yet.
        """
        self.seen_line = False

    def handle_line(self, line: VarphiLine) -> None:
        """
        Process a single line of Varphi code.
        
        This method is called for each line in the input. It sets the seen_line
        flag to True, indicating that at least one line has been encountered.
        The actual content of the line is irrelevant for this compiler.
        
        Args:
            line (VarphiLine): A line object representing a line of Varphi code.
                              The content is not used, only the fact that a line
                              exists is significant.
        """
        self.seen_line = True
    
    def generate_compiled_program(self) -> str:
        """
        Generate the final compiled output.
        
        Returns a string indicating whether the input contained any lines.
        This method should be called after all lines have been processed
        via handle_line().
        
        Returns:
            str: "NOT EMPTY" if at least one line was processed,
                 "EMPTY" if no lines were encountered.
        """
        return "NOT EMPTY" if self.seen_line else "EMPTY"