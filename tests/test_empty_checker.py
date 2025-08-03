from varphi_devkit import compile_varphi
from .toy_compilers import EmptyChecker

def test_with_empty_program():
    """Test EmptyChecker with an empty program."""
    compiler = EmptyChecker()
    program = ""
    assert compile_varphi(program, compiler) == "EMPTY"

def test_with_whitespace_only():
    """Test EmptyChecker with whitespace-only program."""
    compiler = EmptyChecker()
    program = "   \t  \n  \r\n  "
    assert compile_varphi(program, compiler) == "EMPTY"

def test_with_comments_only():
    """Test EmptyChecker with only comments."""
    compiler = EmptyChecker()
    program = """
    // This is a comment
    /* This is a 
       multi-line comment */
    // Another comment
    """
    assert compile_varphi(program, compiler) == "EMPTY"

def test_with_single_line():
    """Test EmptyChecker with a single transition line."""
    compiler = EmptyChecker()
    program = "q0 0 q1 1 R"
    assert compile_varphi(program, compiler) == "NOT EMPTY"

def test_with_multiple_lines():
    """Test EmptyChecker with multiple transition lines."""
    compiler = EmptyChecker()
    program = """
    q0 0 q1 1 R
    q1 1 q0 0 L
    """
    assert compile_varphi(program, compiler) == "NOT EMPTY"

def test_with_lines_and_comments():
    """Test EmptyChecker with both lines and comments."""
    compiler = EmptyChecker()
    program = """
    // Start state transitions
    q0 0 q1 1 R  // Move right after writing 1
    /* Multi-line comment
       explaining the next transition */
    q1 1 q_halt 0 L
    """
    assert compile_varphi(program, compiler) == "NOT EMPTY"

def test_with_complex_state_names():
    """Test EmptyChecker with complex state names."""
    compiler = EmptyChecker()
    program = """
    qstart 0 q_processing 1 R
    q_processing 1 qEnd123 0 L
    """
    assert compile_varphi(program, compiler) == "NOT EMPTY"
