from varphi_devkit import VarphiCompiler, VarphiLine

class LineCounter(VarphiCompiler):
    num_lines: int
    def __init__(self) -> None:
        self.num_lines = 0

    def handle_line(self, line: VarphiLine) -> None:
        self.num_lines += 1
    
    def generate_compiled_program(self) -> str:
        return str(self.num_lines)