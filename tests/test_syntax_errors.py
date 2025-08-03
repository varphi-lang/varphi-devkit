import pytest
from varphi_devkit import compile_varphi, VarphiSyntaxError
from .toy_compilers import LineCounter


class TestSyntaxErrors:
    """Test suite for verifying that VarphiSyntaxError is raised for invalid syntax."""

    def test_invalid_state_name_no_q_prefix(self):
        """Test that state names without 'q' prefix raise VarphiSyntaxError."""
        compiler = LineCounter()
        program = "state0 0 q1 1 R"
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_invalid_state_name_q_only(self):
        """Test that state name with only 'q' raises VarphiSyntaxError."""
        compiler = LineCounter()
        program = "q 0 q1 1 R"
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_invalid_state_name_special_chars(self):
        """Test that state names with invalid special characters raise VarphiSyntaxError."""
        compiler = LineCounter()
        program = "q-state 0 q1 1 R"
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_invalid_tape_character_letter(self):
        """Test that invalid tape characters (letters) raise VarphiSyntaxError."""
        compiler = LineCounter()
        program = "q0 a q1 1 R"
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_invalid_tape_character_number(self):
        """Test that invalid tape characters (numbers other than 0,1) raise VarphiSyntaxError."""
        compiler = LineCounter()
        program = "q0 2 q1 1 R"
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_invalid_head_direction_up(self):
        """Test that invalid head direction 'U' raises VarphiSyntaxError."""
        compiler = LineCounter()
        program = "q0 0 q1 1 U"
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_invalid_head_direction_word(self):
        """Test that invalid head direction 'LEFT' raises VarphiSyntaxError."""
        compiler = LineCounter()
        program = "q0 0 q1 1 LEFT"
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_too_few_tokens(self):
        """Test that lines with too few tokens raise VarphiSyntaxError."""
        compiler = LineCounter()
        program = "q0 0 q1 1"  # Missing head direction
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_too_many_tokens(self):
        """Test that lines with too many tokens raise VarphiSyntaxError."""
        compiler = LineCounter()
        program = "q0 0 q1 1 R extra"
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_wrong_token_order(self):
        """Test that tokens in wrong order raise VarphiSyntaxError."""
        compiler = LineCounter()
        program = "0 q0 q1 1 R"  # Tape character before state
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_completely_invalid_line(self):
        """Test that completely malformed lines raise VarphiSyntaxError."""
        compiler = LineCounter()
        program = "this is not valid syntax"
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_empty_tokens(self):
        """Test that empty tokens raise VarphiSyntaxError."""
        compiler = LineCounter()
        program = "q0  q1 1 R"  # Double space creating empty token
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_mixed_valid_and_invalid_lines(self):
        """Test that having one invalid line among valid ones raises VarphiSyntaxError."""
        compiler = LineCounter()
        program = """
        q0 0 q1 1 R
        invalid line here
        q2 1 q3 0 L
        """
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_invalid_state_in_second_position(self):
        """Test that invalid state in second state position raises VarphiSyntaxError."""
        compiler = LineCounter()
        program = "q0 0 invalid_state 1 R"
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_invalid_second_tape_character(self):
        """Test that invalid second tape character raises VarphiSyntaxError."""
        compiler = LineCounter()
        program = "q0 0 q1 x R"
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_lowercase_head_direction(self):
        """Test that lowercase head direction raises VarphiSyntaxError."""
        compiler = LineCounter()
        program = "q0 0 q1 1 r"
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_numeric_only_tokens(self):
        """Test that using only numbers raises VarphiSyntaxError."""
        compiler = LineCounter()
        program = "123 0 456 1 789"
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_special_characters_instead_of_tokens(self):
        """Test that special characters instead of tokens raise VarphiSyntaxError."""
        compiler = LineCounter()
        program = "# @ $ % ^"
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_partial_valid_syntax(self):
        """Test that partially valid syntax still raises VarphiSyntaxError."""
        compiler = LineCounter()
        program = "q0 0 q1"  # Valid start but incomplete
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_invalid_multiline_with_one_error(self):
        """Test that multiple lines with one syntax error raises VarphiSyntaxError."""
        compiler = LineCounter()
        program = """
        q0 0 q1 1 R
        q1 1 q2 0 L
        q2 0 INVALID 1 R
        q3 1 q0 0 L
        """
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_tab_separated_invalid_tokens(self):
        """Test that tab-separated invalid tokens raise VarphiSyntaxError."""
        compiler = LineCounter()
        program = "q0\t0\tq1\t1\tX"  # Invalid head direction X
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)

    def test_mixed_separators_invalid(self):
        """Test that mixed separators with invalid tokens raise VarphiSyntaxError."""
        compiler = LineCounter()
        program = "q0 0\tq1 1,R"  # Comma instead of space before R
        with pytest.raises(VarphiSyntaxError):
            compile_varphi(program, compiler)