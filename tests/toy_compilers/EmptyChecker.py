from varphi_devkit import VarphiCompiler, VarphiLine

class EmptyChecker(VarphiCompiler):
    seen_line: bool
    def __init__(self) -> None:
        self.seen_line = False

    def handle_line(self, line: VarphiLine) -> None:
        self.seen_line = True
    
    def generate_compiled_program(self) -> str:
        return "NOT EMPTY" if self.seen_line else "EMPTY"