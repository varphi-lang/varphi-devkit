import pytest
import textwrap
from varphi_devkit import VarphiCompiler, VarphiTransition, BLANK, WILDCARD
from varphi_devkit import (
    VarphiSyntaxError,
    VarphiTransitionInconsistentTapeCountError,
    VarphiGlobalTapeCountError,
)


class CapturingCompiler(VarphiCompiler):
    """A concrete compiler implementation which captures transitions."""

    def __init__(self):
        super().__init__()
        self.captured_transitions = []

    def handle_transition(self, transition: VarphiTransition) -> None:
        self.captured_transitions.append(transition)

    def generate_compiled_program(self) -> str:
        return "Done"


@pytest.fixture
def compiler() -> CapturingCompiler:
    return CapturingCompiler()


def test_compile_single_tape_basic(compiler):
    """Verify a simple 1-tape transition is parsed into the correct object attributes."""
    source = "start (0) end (1) (RIGHT)"
    compiler.compile(source)

    assert len(compiler.captured_transitions) == 1
    t = compiler.captured_transitions[0]

    assert t.current_state == "start"
    assert t.read_symbols == ("0",)
    assert t.next_state == "end"
    assert t.write_symbols == ("1",)
    assert t.shift_directions == ("RIGHT",)
    assert t.line_number == 1


def test_compile_multi_tape_and_constants(compiler):
    """Verify multi-tape tuple ordering and correct mapping of keywords (BLANK) and symbols (*) to internal constants."""
    source = "q0 (0, 1, BLANK) q1 (1, 0, *) (LEFT, RIGHT, STAY)"
    compiler.compile(source)

    t = compiler.captured_transitions[0]

    assert t.read_symbols == ("0", "1", BLANK)
    assert t.write_symbols == ("1", "0", WILDCARD)
    assert t.shift_directions == ("LEFT", "RIGHT", "STAY")


def test_compile_keywords_as_state_names(compiler):
    """Verify that using reserved keywords (LEFT, RIGHT, STAY, BLANK) as State Identifiers is allowed and handled correctly."""
    source = "LEFT (0) RIGHT (1) (LEFT)"
    compiler.compile(source)

    t = compiler.captured_transitions[0]

    assert t.current_state == "LEFT"  # As Identifier
    assert t.next_state == "RIGHT"  # As Identifier
    assert t.shift_directions == ("LEFT",)  # As Direction Keyword


def test_compile_alphanumeric_states(compiler):
    """Verify states with numbers and underscores are valid."""
    source = "state_1 (0) state_2 (1) (STAY)"
    compiler.compile(source)

    t = compiler.captured_transitions[0]
    assert t.current_state == "state_1"
    assert t.next_state == "state_2"


def test_formatting_comments_and_line_numbers(compiler):
    """
    Verify that:
    1. Comments (// and /* ... */) are ignored.
    2. Blank lines are ignored.
    3. Line numbers reported in the Transition object match the source file.
    """
    # We use 'dedent' with a leading backslash to ensure accurate line counting
    source = textwrap.dedent(
        """\
    // Line 1: Setup
    
    start (0) middle (0) (RIGHT)
    
    /* Block comment on 
       lines 5-6 */
       
    middle (1) end (1) (LEFT)
    """
    )

    compiler.compile(source)
    assert len(compiler.captured_transitions) == 2

    # "start" is on line 3 (Line 1 is comment, Line 2 is empty)
    t1 = compiler.captured_transitions[0]
    assert t1.current_state == "start"
    assert t1.line_number == 3

    # "middle" is on line 8
    t2 = compiler.captured_transitions[1]
    assert t2.current_state == "middle"
    assert t2.line_number == 8


def test_syntax_garbage_input(compiler):
    with pytest.raises(VarphiSyntaxError):
        compiler.compile("invalid blah blah")


def test_syntax_bad_direction_shorthand(compiler):
    """The grammar requires LEFT/RIGHT/STAY, not L/R/S."""
    source = "s (0) q (1) (R)"
    with pytest.raises(VarphiSyntaxError) as exc:
        compiler.compile(source)
    assert "mismatched input" in str(exc.value) or "viable alternative" in str(
        exc.value
    )


def test_syntax_bad_symbol_underscore(compiler):
    """Underscore '_' is a valid ID but invalid Symbol (must use BLANK)."""
    source = "s (_) q (1) (RIGHT)"
    with pytest.raises(VarphiSyntaxError):
        compiler.compile(source)


def test_syntax_bad_symbol_multichar(compiler):
    """Symbols must be single characters (0-9, a-z, A-Z)."""
    source = "s (10) q (1) (RIGHT)"
    with pytest.raises(VarphiSyntaxError):
        compiler.compile(source)


def test_error_local_mismatch_counts(compiler):
    """Reading 2 symbols but writing 1 is invalid."""
    source = "s (0, 0) s (1) (LEFT, LEFT)"
    with pytest.raises(VarphiTransitionInconsistentTapeCountError) as exc:
        compiler.compile(source)
    assert "read 2 symbols, but wrote 1" in str(exc.value)


def test_error_global_mismatch_tape_count(compiler):
    """
    Defining a 2-tape transition followed by a 3-tape transition
    should raise a Global Consistency error.
    """
    source = """
    stateA (0, 0) stateA (1, 1) (LEFT, LEFT)
    stateB (0, 0, 0) stateB (1, 1, 1) (LEFT, LEFT, LEFT)
    """
    with pytest.raises(VarphiGlobalTapeCountError) as exc:
        compiler.compile(source)
    assert "previous transitions used 2 tapes, but this one uses 3" in str(exc.value)


def test_compiler_state_reset_between_runs(compiler):
    """
    Ensure the compiler clears its internal state (tape count memory)
    between calls to compile().
    """
    # Run 1: 1-tape machine (Valid)
    compiler.compile("s (0) q (1) (RIGHT)")

    # Run 2: 2-tape machine (Valid).
    # If state wasn't cleared, this would raise GlobalTapeCountError (1 vs 2).
    compiler.compile("s (0, 0) q (1, 1) (RIGHT, RIGHT)")
