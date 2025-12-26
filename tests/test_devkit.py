import pytest
from typing import List
from varphi_devkit import (
    VarphiCompiler,
    VarphiTransition,
    VarphiSyntaxError,
    VarphiTransitionInconsistentTapeCountError,
    VarphiGlobalTapeCountError,
    VarphiUndefinedVariableError,
    BLANK,
    LEFT,
    RIGHT,
)


class MockCompiler(VarphiCompiler):
    """
    A concrete implementation of VarphiCompiler for testing.
    It simply captures the transitions it processes.
    """

    def __init__(self):
        super().__init__()
        self.captured_transitions: List[VarphiTransition] = []

    def handle_transition(self, transition: VarphiTransition) -> None:
        self.captured_transitions.append(transition)

    def generate_compiled_program(self) -> str:
        return "COMPILATION_SUCCESS"


@pytest.fixture
def compiler() -> MockCompiler:
    return MockCompiler()


def test_basic_canonicalization(compiler):
    """Test that arbitrary variable names are mapped to $1, $2, etc."""
    code = """
    start ($x, $y) next ($y, $x) (LEFT, RIGHT)
    """
    compiler.compile(code)

    assert len(compiler.captured_transitions) == 1
    t = compiler.captured_transitions[0]

    # Verify State
    assert t.current_state == "start"
    assert t.next_state == "next"

    # Verify Canonicalization ($x -> $1, $y -> $2)
    assert t.read_symbols == ("$1", "$2")
    assert t.write_symbols == ("$2", "$1")

    # Verify Directions
    assert t.shift_directions == (LEFT, RIGHT)


def test_variable_reuse_constraint(compiler):
    """
    Test the new feature: reusing variables in read tuple.
    read($x, $x) should become read($1, $1).
    """
    code = "scan ($val, $val) match ($val, $val) (RIGHT, RIGHT)"
    compiler.compile(code)

    t = compiler.captured_transitions[0]
    assert t.read_symbols == ("$1", "$1")
    assert t.write_symbols == ("$1", "$1")


def test_variable_ordering_consistency(compiler):
    """
    Test that variable IDs are assigned based on order of appearance in READ.
    read($b, $a) -> read($1, $2).
    """
    code = "s0 ($b, $a) s1 ($b, $a) (STAY, STAY)"
    compiler.compile(code)

    t = compiler.captured_transitions[0]
    # $b appears first -> $1
    # $a appears second -> $2
    assert t.read_symbols == ("$1", "$2")
    assert t.write_symbols == ("$1", "$2")


def test_literals_and_blanks(compiler):
    """Test that literals and keywords are preserved and not treated as variables."""
    code = "s0 (0, BLANK, 1) s1 (1, BLANK, 0) (LEFT, STAY, RIGHT)"
    compiler.compile(code)

    t = compiler.captured_transitions[0]
    assert t.read_symbols == ("0", BLANK, "1")
    assert t.write_symbols == ("1", BLANK, "0")


def test_error_local_tape_count_mismatch(compiler):
    """Test mismatch within a single line (read 2, write 3)."""
    code = "s0 (a, b) s1 (a, b, c) (LEFT, LEFT)"

    with pytest.raises(VarphiTransitionInconsistentTapeCountError) as exc:
        compiler.compile(code)

    assert "local tape count mismatch" in exc.value.msg
    assert "read 2" in exc.value.msg
    assert "wrote 3" in exc.value.msg


def test_error_global_tape_count_mismatch(compiler):
    """Test mismatch between two different lines."""
    code = """
    s0 (a) s1 (b) (LEFT)
    s1 (a, b) s2 (b, a) (LEFT, LEFT)  // Error: Changed from 1 tape to 2 tapes
    """

    with pytest.raises(VarphiGlobalTapeCountError) as exc:
        compiler.compile(code)

    assert "global tape count mismatch" in exc.value.msg
    assert "previous transitions used 1" in exc.value.msg
    assert "this one uses 2" in exc.value.msg


def test_error_undefined_variable(compiler):
    """Test using a variable in WRITE that wasn't in READ."""
    code = "s0 ($x) s1 ($y) (LEFT)"

    with pytest.raises(VarphiUndefinedVariableError) as exc:
        compiler.compile(code)

    assert "Undefined variable: '$y'" in exc.value.msg


def test_syntax_error_garbage_input(compiler):
    """Test that general parsing errors raise VarphiSyntaxError."""
    code = "This is not valid varphi code"

    with pytest.raises(VarphiSyntaxError):
        compiler.compile(code)


def test_comments_and_whitespace(compiler):
    """Test that comments and whitespace are ignored."""
    code = """
    // This is a comment
    start (0) end (1) (LEFT)
    
    /* Multi-line
       comment */
       
    end (1) start (0) (RIGHT)
    """
    compiler.compile(code)
    assert len(compiler.captured_transitions) == 2
