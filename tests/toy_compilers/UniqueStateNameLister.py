"""
UniqueStateNameLister - A toy compiler that extracts unique state names from Varphi code.

This compiler analyzes Varphi lines to collect all unique state names that appear
in both if_state and then_state positions, demonstrating more complex data extraction
and analysis during compilation.
"""

from varphi_devkit import VarphiCompiler, VarphiLine


class UniqueStateNameLister(VarphiCompiler):
    """
    A toy compiler that collects and lists all unique state names from input lines.
    
    This compiler examines each VarphiLine to extract state names from both the
    if_state (condition) and then_state (result) fields. It maintains a set of
    unique state names encountered and outputs them as a comma-separated list.
    
    This demonstrates more sophisticated analysis during compilation, where the
    compiler needs to examine the structure and content of each line rather than
    just counting or checking for presence.
    
    Attributes:
        unique_state_names (set[str]): Set containing all unique state names
                                      encountered during processing. Using a set
                                      ensures automatic deduplication.
    
    Examples:
        >>> lister = UniqueStateNameLister()
        >>> # Process lines with states "idle", "running", "stopped"
        >>> # Line 1: if_state="idle", then_state="running"
        >>> # Line 2: if_state="running", then_state="stopped"
        >>> # Line 3: if_state="stopped", then_state="idle"
        >>> lister.generate_compiled_program()
        'idle, running, stopped'  # Order may vary due to set nature
    """
    
    unique_state_names: set[str]

    def __init__(self) -> None:
        """
        Initialize the UniqueStateNameLister with an empty state set.
        
        Creates an empty set to store unique state names encountered
        during line processing.
        """
        self.unique_state_names = set()

    def handle_line(self, line: VarphiLine) -> None:
        """
        Process a single line of Varphi code and extract state names.
        
        Examines both the if_state and then_state attributes of the line,
        adding any new state names to the unique_state_names set. The set
        automatically handles deduplication, so states that appear multiple
        times across different lines are only stored once.
        
        Args:
            line (VarphiLine): A line object representing a line of Varphi code.
                              Must have if_state and then_state attributes
                              containing state name strings.
        """
        # Add if_state to our collection of unique state names
        if line.if_state not in self.unique_state_names:
            self.unique_state_names.add(line.if_state)
        
        # Add then_state to our collection of unique state names    
        if line.then_state not in self.unique_state_names:
            self.unique_state_names.add(line.then_state)
    
    def generate_compiled_program(self) -> str:
        """
        Generate the final compiled output listing all unique state names.
        
        Converts the set of unique state names into a comma-separated string.
        The order of states in the output is not guaranteed due to the unordered
        nature of sets.
        
        Returns:
            str: Comma-separated list of unique state names encountered.
                 Returns empty string if no states were found.
                 Example: "idle, running, stopped"
        """
        return ", ".join(self.unique_state_names)