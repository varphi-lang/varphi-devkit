import pytest
from varphi_devkit import (
    VarphiCompiler,
    VarphiSyntaxError,
    VarphiTransitionInconsistentTapeCountError,
    VarphiGlobalTapeCountError,
    VarphiUndefinedVariableError,
    Variable,
    Direction,
    BuiltinSymbol,
    Character,
)


class MockCompiler(VarphiCompiler):
    """Concrete compiler implementation for inspecting devkit-produced IR."""

    def _generate_compiled_program(self) -> str:
        return "COMPILATION_SUCCESS"


@pytest.fixture
def compiler() -> MockCompiler:
    return MockCompiler()


def test_basic_variable_canonicalization(compiler):
    """Test that arbitrary variables map to 0-indexed integers sequentially."""
    compiler.compile("start ($x, $y) next ($y, $x) (LEFT, RIGHT)")
    t = compiler.ir["start"][0]

    assert t.read_symbols == (Variable(0), Variable(1))
    assert t.write_symbols == (Variable(1), Variable(0))
    assert t.shift_directions == (Direction.LEFT, Direction.RIGHT)


def test_variable_reuse_and_ordering(compiler):
    """Test that reused variables maintain the same ID and ordering is preserved."""
    compiler.compile("s0 ($b, $a, $b) s1 ($a, $b, $b) (STAY, STAY, STAY)")
    t = compiler.ir["s0"][0]

    assert t.read_symbols == (Variable(0), Variable(1), Variable(0))
    assert t.write_symbols == (Variable(1), Variable(0), Variable(0))


def test_variable_scope_resets_per_transition(compiler):
    """Test that variable IDs reset to 0 for each new transition line."""
    code = """
    s0 ($x) s1 ($x) (LEFT)
    s1 ($y) s2 ($y) (RIGHT)
    """
    compiler.compile(code)

    assert compiler.ir["s0"][0].read_symbols == (Variable(0),)
    assert compiler.ir["s1"][0].read_symbols == (Variable(0),)


def test_mixed_symbols_and_directions(compiler):
    """Test quoted CHAR_LITERALs, BLANK_KW, variables, and all shift directions."""
    code = "s0 ('a', BLANK, 'x', $var) s1 ('y', BLANK, 'a', $var) (LEFT, RIGHT, STAY, STAY)"
    compiler.compile(code)

    t = compiler.ir["s0"][0]
    assert t.read_symbols == (
        Character("a"),
        BuiltinSymbol.BLANK,
        Character("x"),
        Variable(0),
    )
    assert t.write_symbols == (
        Character("y"),
        BuiltinSymbol.BLANK,
        Character("a"),
        Variable(0),
    )
    assert t.shift_directions == (
        Direction.LEFT,
        Direction.RIGHT,
        Direction.STAY,
        Direction.STAY,
    )


def test_keywords_as_state_ids(compiler):
    """Test that keywords can be used as state names."""
    code = "LEFT ('a') RIGHT ('b') (STAY)"
    compiler.compile(code)

    t = compiler.ir["LEFT"][0]
    assert t.current_state == "LEFT"
    assert t.next_state == "RIGHT"


def test_keywords_as_variable_names(compiler):
    """Test that variable names can use keyword strings (e.g., $LEFT, $BLANK) when prefixed with '$'."""
    code = "s0 ($LEFT, $BLANK) s1 ($LEFT, $BLANK) (LEFT, RIGHT)"
    compiler.compile(code)

    t = compiler.ir["s0"][0]
    assert t.read_symbols == (Variable(0), Variable(1))
    assert t.write_symbols == (Variable(0), Variable(1))
    assert t.shift_directions == (Direction.LEFT, Direction.RIGHT)


def test_specificity_sorting_order(compiler):
    """Test that the Devkit automatically sorts rules by specificity (literals before variables)."""
    code = """
    s0 ($x) s2 ('b') (RIGHT)
    s0 ('a') s1 ('c') (LEFT)
    """
    compiler.compile(code)

    transitions = compiler.ir["s0"]
    # Literal match ('a') should be sorted before variable match ($x)
    assert transitions[0].read_symbols == (Character("a"),)
    assert transitions[0].specificity == (0, 0)

    assert transitions[1].read_symbols == (Variable(0),)
    assert transitions[1].specificity == (1, 1)


def test_error_local_tape_count_mismatch(compiler):
    """Test mismatch between read/write/shift lengths on a single line."""
    with pytest.raises(VarphiTransitionInconsistentTapeCountError) as exc:
        compiler.compile("s0 ('a', 'b') s1 ('a', 'b', 'c') (LEFT, LEFT)")

    assert "read 2" in exc.value.msg
    assert "wrote 3" in exc.value.msg


def test_error_global_tape_count_mismatch(compiler):
    """Test that tape count must remain consistent across multiple transitions."""
    code = """
    s0 ('a') s1 ('b') (LEFT)
    s1 ('a', 'b') s2 ('b', 'a') (LEFT, LEFT)
    """
    with pytest.raises(VarphiGlobalTapeCountError) as exc:
        compiler.compile(code)

    assert "previous transitions used 1" in exc.value.msg
    assert "this one uses 2" in exc.value.msg


def test_error_undefined_variable(compiler):
    """Test that writing an unread variable raises an error."""
    with pytest.raises(VarphiUndefinedVariableError) as exc:
        compiler.compile("s0 ($x) s1 ($y) (LEFT)")

    assert "Undefined variable: '$y'" in exc.value.msg


def test_comments_and_whitespace(compiler):
    """Test that comments and spaces are safely skipped while newlines delimit transitions."""
    code = """
    // Start of machine
    s0 ('0') s1 ('1') (LEFT)   // Inline comment
    
    /* 
        Multi-line
        Comment 
    */
    s1 ('1') s0 ('0') (RIGHT)
    """
    compiler.compile(code)

    total_transitions = sum(len(transitions) for transitions in compiler.ir.values())
    assert total_transitions == 2


def test_error_empty_program(compiler):
    """Test that an empty program throws a syntax error."""
    with pytest.raises(VarphiSyntaxError):
        compiler.compile("// Just comments \n \n")


def test_syntax_error_rich_formatting(compiler):
    """Test that the custom exception __str__ produces the formatted code snippet."""
    code = "s0 ('a', 'b' s1 ('a', 'b') (LEFT, RIGHT)"

    with pytest.raises(VarphiSyntaxError) as exc:
        compiler.compile(code)

    error_output = str(exc.value)

    assert "error:" in error_output
    assert "line 1" in error_output
    assert "s0 ('a', 'b' s1 ('a', 'b') (LEFT, RIGHT)" in error_output
    assert "^" in error_output
