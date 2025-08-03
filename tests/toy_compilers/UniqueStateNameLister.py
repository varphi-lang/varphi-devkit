from varphi_devkit import VarphiCompiler, VarphiLine

class UniqueStateNameLister(VarphiCompiler):
    unique_state_names: set[str]

    def __init__(self):
        self.unique_state_names = set()

    def handle_line(self, line: VarphiLine):
        if line.if_state not in self.unique_state_names:
            self.unique_state_names.add(line.if_state)
        if line.then_state not in self.unique_state_names:
            self.unique_state_names.add(line.then_state)
    
    def generate_compiled_program(self):
        return ", ".join(self.unique_state_names)