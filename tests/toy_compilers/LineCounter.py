"""
LineCounter - A toy compiler that counts the number of lines in the input.

This compiler demonstrates basic accumulation during compilation, maintaining
a running count of processed lines and returning the total as the final output.
"""

from varphi_devkit import VarphiCompiler, VarphiLine


class LineCounter(VarphiCompiler):
    """
    A toy compiler that counts the total number of lines in the input.
    
    This compiler maintains a running count of all lines processed and outputs
    the total count as a string. It demonstrates simple accumulation during
    the compilation process.
    
    Attributes:
        num_lines (int): Running count of lines processed. Initialized to 0
                        and incremented for each line encountered.
    
    Examples:
        >>> counter = LineCounter()
        >>> # Initially no lines processed
        >>> counter.generate_compiled_program()
        '0'
        
        >>> # After processing 3 lines
        >>> for line in lines:
        ...     counter.handle_line(line)
        >>> counter.generate_compiled_program()
        '3'
    """
    
    num_lines: int
    
    def __init__(self) -> None:
        """
        Initialize the LineCounter with zero count.
        
        Sets num_lines to 0, representing no lines processed initially.
        """
        self.num_lines = 0

    def handle_line(self, line: VarphiLine) -> None:
        """
        Process a single line of Varphi code and increment the counter.
        
        This method is called for each line in the input. It increments the
        internal counter regardless of the line's content, as only the
        existence of the line matters for counting purposes.
        
        Args:
            line (VarphiLine): A line object representing a line of Varphi code.
                              The content is not examined, only counted.
        """
        self.num_lines += 1
    
    def generate_compiled_program(self) -> str:
        """
        Generate the final compiled output containing the line count.
        
        Returns the total number of lines processed as a string.
        This method should be called after all lines have been processed
        via handle_line().
        
        Returns:
            str: String representation of the total number of lines processed.
                 For example, "0" for empty input, "5" for 5 lines, etc.
        """
        return str(self.num_lines)