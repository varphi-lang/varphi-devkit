from varphi_devkit import compile_varphi
from .toy_compilers import UniqueStateNameLister

def test_empty_program():
    """Test UniqueStateNameLister with an empty program."""
    compiler = UniqueStateNameLister()
    program = ""
    result = compile_varphi(program, compiler)
    assert result == ""

def test_whitespace_only():
    """Test UniqueStateNameLister with whitespace-only program."""
    compiler = UniqueStateNameLister()
    program = "   \t  \n  \r\n  "
    result = compile_varphi(program, compiler)
    assert result == ""

def test_comments_only():
    """Test UniqueStateNameLister with only comments."""
    compiler = UniqueStateNameLister()
    program = """
    // This is a comment
    /* This is a 
       multi-line comment */
    // Another comment
    """
    result = compile_varphi(program, compiler)
    assert result == ""

def test_single_line_different_states():
    """Test UniqueStateNameLister with one line having different if/then states."""
    compiler = UniqueStateNameLister()
    program = "q0 0 q1 1 R"
    result = compile_varphi(program, compiler)
    states = set(result.split(", "))
    expected = {"q0", "q1"}
    assert states == expected

def test_single_line_same_states():
    """Test UniqueStateNameLister with one line having same if/then state."""
    compiler = UniqueStateNameLister()
    program = "q0 0 q0 1 R"
    result = compile_varphi(program, compiler)
    assert result == "q0"

def test_two_lines_all_different_states():
    """Test UniqueStateNameLister with two lines having all different states."""
    compiler = UniqueStateNameLister()
    program = """
    q0 0 q1 1 R
    q2 1 q3 0 L
    """
    result = compile_varphi(program, compiler)
    states = set(result.split(", "))
    expected = {"q0", "q1", "q2", "q3"}
    assert states == expected

def test_two_lines_shared_states():
    """Test UniqueStateNameLister with two lines sharing some states."""
    compiler = UniqueStateNameLister()
    program = """
    q0 0 q1 1 R
    q1 1 q0 0 L
    """
    result = compile_varphi(program, compiler)
    states = set(result.split(", "))
    expected = {"q0", "q1"}
    assert states == expected

def test_multiple_lines_duplicate_states():
    """Test UniqueStateNameLister with multiple lines containing duplicate states."""
    compiler = UniqueStateNameLister()
    program = """
    q0 0 q1 1 R
    q1 0 q2 0 R
    q1 1 q0 0 L
    q2 0 q0 1 L
    q2 1 q1 1 R
    """
    result = compile_varphi(program, compiler)
    states = set(result.split(", "))
    expected = {"q0", "q1", "q2"}
    assert states == expected

def test_lines_with_comments():
    """Test UniqueStateNameLister with both lines and comments."""
    compiler = UniqueStateNameLister()
    program = """
    // Start state transitions
    q0 0 q1 1 R  // Move right after writing 1
    /* Multi-line comment
       explaining the next transition */
    q1 1 q_halt 0 L
    """
    result = compile_varphi(program, compiler)
    states = set(result.split(", "))
    expected = {"q0", "q1", "q_halt"}
    assert states == expected

def test_complex_state_names():
    """Test UniqueStateNameLister with complex state names."""
    compiler = UniqueStateNameLister()
    program = """
    qstart 0 q_processing 1 R
    q_processing 1 qEnd123 0 L
    qEnd123 0 q_final_state 1 R
    """
    result = compile_varphi(program, compiler)
    states = set(result.split(", "))
    expected = {"qstart", "q_processing", "qEnd123", "q_final_state"}
    assert states == expected

def test_self_loops():
    """Test UniqueStateNameLister with self-looping transitions."""
    compiler = UniqueStateNameLister()
    program = """
    q0 0 q0 1 R
    q1 1 q1 0 L
    q0 1 q1 0 R
    """
    result = compile_varphi(program, compiler)
    states = set(result.split(", "))
    expected = {"q0", "q1"}
    assert states == expected

def test_mixed_scenarios():
    """Test UniqueStateNameLister with a mix of self-loops and different states."""
    compiler = UniqueStateNameLister()
    program = """
    q0 0 q0 1 R
    q0 1 q1 0 L
    q1 0 q2 1 R
    q1 1 q1 0 L
    q2 0 q_halt 0 R
    q2 1 q0 1 L
    """
    result = compile_varphi(program, compiler)
    states = set(result.split(", "))
    expected = {"q0", "q1", "q2", "q_halt"}
    assert states == expected

def test_single_state_program():
    """Test UniqueStateNameLister with a program that only uses one state."""
    compiler = UniqueStateNameLister()
    program = """
    qloop 0 qloop 1 R
    qloop 1 qloop 0 L
    """
    result = compile_varphi(program, compiler)
    assert result == "qloop"

def test_alphabetical_ordering_consistency():
    """Test that the result contains all expected states (order may vary due to set behavior)."""
    compiler = UniqueStateNameLister()
    program = """
    qz 0 qa 1 R
    qb 1 qy 0 L
    qc 0 qx 1 R
    """
    result = compile_varphi(program, compiler)
    states = set(result.split(", "))
    expected = {"qa", "qb", "qc", "qx", "qy", "qz"}
    assert states == expected