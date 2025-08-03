from varphi_devkit import compile_varphi
from .toy_compilers import LineCounter

def test_empty_program():
    """Test LineCounter with an empty program."""
    compiler = LineCounter()
    program = ""
    assert compile_varphi(program, compiler) == "0"

def test_whitespace_only():
    """Test LineCounter with whitespace-only program."""
    compiler = LineCounter()
    program = "   \t  \n  \r\n  "
    assert compile_varphi(program, compiler) == "0"

def test_comments_only():
    """Test LineCounter with only comments."""
    compiler = LineCounter()
    program = """
    // This is a comment
    /* This is a 
       multi-line comment */
    // Another comment
    """
    assert compile_varphi(program, compiler) == "0"

def test_single_line():
    """Test LineCounter with a single transition line."""
    compiler = LineCounter()
    program = "q0 0 q1 1 R"
    assert compile_varphi(program, compiler) == "1"

def test_two_lines():
    """Test LineCounter with two transition lines."""
    compiler = LineCounter()
    program = """
    q0 0 q1 1 R
    q1 1 q0 0 L
    """
    assert compile_varphi(program, compiler) == "2"

def test_multiple_lines():
    """Test LineCounter with multiple transition lines."""
    compiler = LineCounter()
    program = """
    q0 0 q1 1 R
    q1 0 q2 0 R
    q1 1 q0 0 L
    q2 0 q_halt 1 L
    q2 1 q1 1 R
    """
    assert compile_varphi(program, compiler) == "5"

def test_lines_with_comments():
    """Test LineCounter with both lines and comments (comments shouldn't be counted)."""
    compiler = LineCounter()
    program = """
    // Start state transitions
    q0 0 q1 1 R  // Move right after writing 1
    /* Multi-line comment
       explaining the next transition */
    q1 1 q_halt 0 L
    // End of program
    """
    assert compile_varphi(program, compiler) == "2"

def test_mixed_tape_characters():
    """Test LineCounter with different tape character combinations."""
    compiler = LineCounter()
    program = """
    q0 0 q1 0 L
    q0 1 q1 1 R
    q1 0 q2 1 L
    q1 1 q2 0 R
    """
    assert compile_varphi(program, compiler) == "4"

def test_complex_state_names():
    """Test LineCounter with complex state names."""
    compiler = LineCounter()
    program = """
    qstart 0 q_processing 1 R
    q_processing 1 qEnd123 0 L
    qEnd123 0 q_final_state 1 R
    """
    assert compile_varphi(program, compiler) == "3"

def test_single_line_with_comments():
    """Test LineCounter with one line surrounded by comments."""
    compiler = LineCounter()
    program = """
    /* Beginning comment */
    // Another comment
    q0 0 q1 1 R  // Inline comment
    /* Ending comment */
    """
    assert compile_varphi(program, compiler) == "1"

def test_large_program():
    """Test LineCounter with a larger program (10 lines)."""
    compiler = LineCounter()
    program = """
    q0 0 q1 1 R
    q0 1 q2 0 L
    q1 0 q3 1 R
    q1 1 q4 0 L
    q2 0 q5 1 R
    q2 1 q6 0 L
    q3 0 q7 1 R
    q3 1 q8 0 L
    q4 0 q9 1 R
    q4 1 q0 0 L
    """
    assert compile_varphi(program, compiler) == "10"