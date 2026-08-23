# The Varphi Compiler Development Kit

This is the official frontend parsing and compiler development kit for the Varphi programming language.

The devkit is a target-language-agnostic frontent that handles lexical analysis, syntax parsing, semantic validation, and intermediate representation (IR) generation. It is designed so that downstream developers can write backend compilers (e.g., Varphi-to-Python, Varphi-to-C, ...) without needing to worry about all the "dirty work" of compilers, like lexing and parsing.

---

## 📦 Installation

Assuming you are using a standard Python environment or a modern manager like `uv`:

```
# For pip
pip install varphi-devkit
# For uv
uv pip install varphi-devkit
```

---

## Quick Start: Building a Downstream Compiler

Building a Varphi compiler requires inheriting from the `VarphiCompiler` base class and implementing a single method: `_generate_compiled_program()`.

```python
from varphi_devkit import VarphiCompiler

class VarphiToMyLangCompiler(VarphiCompiler):
    
    def _generate_compiled_program(self) -> str:
        # By the time this method is called, the devkit has already parsed, validated, and sorted the Varphi source code. 
        
        # self.states: A set of all state names (strings) discovered in the code.
        print(f"Total states: {len(self.states)}")
        
        # self.initial_state: The entry state (string).
        print(f"Entry point: {self.initial_state}")
        
        # self._tape_count: The number of tapes in this machine (int).
        print(f"Tape count: {self._tape_count}")

        # self.ir: A dictionary mapping state names to a pre-sorted list of VarphiTransitions.
        # The VarphiTransitions are sorted in non-decreasing order of specificity
        for state_name, transitions in self.ir.items():
            for t in transitions:
                # Code generation logic goes here!
                pass
                
        return "Compilation Complete!"  # You would return your compiled program here

# Usage
compiler = VarphiToMyLangCompiler()
with open("machine.vp", "r") as f:
    compiled_code = compiler.compile(f.read())
```

---

## The Intermediate Representation (IR)

The devkit translates raw `.vp` source text into a strictly typed IR. Every transition rule in the user's source code is mapped to a `VarphiTransition` object.

Because downstream compilers receive this IR *after* the Devkit has validated it, it has already been totally validated, saving you development time/effort.

### `VarphiTransition`

```python
@dataclass(frozen=True)
class VarphiTransition:
    current_state: str 
    read_symbols: tuple[ReadWriteTupleElement, ...]  
    next_state: str
    write_symbols: tuple[ReadWriteTupleElement, ...] 
    shift_directions: tuple[Direction, ...]        
    line_number: int
    specificity: tuple[int, int]  # (unique variables, total variables)
```

---

## The Specificity Engine

Varphi is a nondeterministic language with pattern matching. When multiple rules match a tape state, the machine must choose the "most specific" rule, or stochastically branch if there is a tie.

The Devkit calculates a specificity score for every transition, accessible through the `specificity` of a `VarphiTransition` object. Its type is a two-element tuple, where the first element gives the number of unique variables in the transition rule and the second gives the total number of variables (including dupicates) in the transition rule. 

Thus, a rule containing all literals scores lower (i.e., `(0, 0)`) than one containing variables. 

Before calling your compiler's generation method, the devkit groups all transitions by state and sorts them in non-decreasing order of specificity. Downstream runtimes can simply iterate over a state's transitions, gather the applicable transitions that have the lowest specificity score, then stop once the specificty score increases, which is guaranteed to run in $O(n)$ time, where $n$ is the number of transition rules for a particular state.

---

## Validation and Error Handling

The devkit intercepts and formats all ANTLR4 parser errors, throwing descriptive exceptions. You never have to write validation logic in your downstream compiler.

* `VarphiGlobalTapeCountError`: Thrown if any line uses a different number of tapes than the first transition line. 
* `VarphiTransitionInconsistentTapeCountError`: Thrown if a single rule attempts to read a different number of tape symbols than it writes.
* `VarphiUndefinedVariableError`: Thrown if a variable is used in the write tuple without being bound in the read tuple first.
* `VarphiUnknownSymbolError` & `VarphiUnknownDirectionError`: Lexer fallbacks for unrecognized tokens.

---

## Contributing

When modifying the ANTLR4 grammar (`grammar/Varphi.g4`), ensure you regenerate the parser before running the test suite:

1. Modify `.g4` file.
2. Run `antlr4 -Dlanguage=Python3 grammar/Varphi.g4 -o src/varphi_devkit/parser/`
3. Run the test suite: `pytest tests/`