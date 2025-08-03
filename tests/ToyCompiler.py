from varphi_devkit import compile_varphi, VarphiLine, VarphiTapeCharacter, VarphiHeadDirection, VarphiCompiler

class ToyCompiler(VarphiCompiler):
    seen_states: set[str]
    def __init__(self):
        super().__init__()
        self.seen_states = set()

    def handle_line(self, line: VarphiLine) -> None:
        """Handle a single Varphi line (transition rule).
        
        This method must be implemented by subclasses to define how each
        transition rule should be processed and added to the compiled program.
        
        Args:
            line: The VarphiLine object representing a transition rule
        """
        print("Hi!")


import logging
logging.basicConfig(level=logging.DEBUG)

with open(r"C:\Users\Hassan\Downloads\varphi-devkit\tests\example.vp", "r") as f:
    program = f.read()
    print(program)
    print(compile_varphi(program, ToyCompiler()))
        