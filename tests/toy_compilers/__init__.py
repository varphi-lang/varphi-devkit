"""
Toy Compilers Package - Example implementations of VarphiCompiler.

This package contains simple example compilers that demonstrate different
aspects of the VarphiCompiler interface. These compilers serve as educational
examples and test cases for the varphi-devkit framework.

Available Compilers:
    EmptyChecker: Determines if input contains any lines
    LineCounter: Counts the total number of lines in input  
    UniqueStateNameLister: Extracts and lists unique state names

Each compiler demonstrates different compilation patterns:
- EmptyChecker: Simple boolean state tracking
- LineCounter: Accumulation and counting
- UniqueStateNameLister: Data extraction and collection
"""

from .EmptyChecker import EmptyChecker
from .LineCounter import LineCounter
from .UniqueStateNameLister import UniqueStateNameLister

# Make all compilers available at package level
__all__ = [
    'EmptyChecker',
    'LineCounter', 
    'UniqueStateNameLister'
]