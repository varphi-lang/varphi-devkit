"""
The Varphi Development Kit.

A framework for building compilers, interpreters, and analysis tools for the Varphi language.
This package handles the complexity of parsing, validation, and variable canonicalization, providing a
convenient abstraction layer for implementing custom Varphi backends.

**Core API:**
- `VarphiCompiler`: The abstract base class you must subclass. Override `_generate_compiled_program()` to implement custom logic for a compiler.
- `VarphiTransition`: A validated, canonicalized representation of a single transition line.
"""

__version__ = "3.0.0"

from .compiler import (
    VarphiCompiler,
    VarphiTransition,
    Direction,
    BuiltinSymbol,
    Variable,
    Character,
    ReadWriteTupleElement,
)
from .exceptions import (
    VarphiSyntaxError,
    VarphiTransitionInconsistentTapeCountError,
    VarphiGlobalTapeCountError,
    VarphiUndefinedVariableError,
)

__all__ = [
    "VarphiCompiler",
    "VarphiTransition",
    "Direction",
    "BuiltinSymbol",
    "Variable",
    "Character",
    "ReadWriteTupleElement",
    "VarphiSyntaxError",
    "VarphiTransitionInconsistentTapeCountError",
    "VarphiGlobalTapeCountError",
    "VarphiUndefinedVariableError",
]
