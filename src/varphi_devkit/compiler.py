from abc import ABC, abstractmethod
from typing import Optional
from collections import defaultdict
from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

from .parser import VarphiLexer, VarphiParser, VarphiListener
from .models import (
    ReadWriteTupleElement,
    Character,
    BuiltinSymbol,
    Variable,
    Direction,
    VarphiTransition,
)
from .exceptions import (
    VarphiErrorListener,
    VarphiTransitionInconsistentTapeCountError,
    VarphiGlobalTapeCountError,
    VarphiUndefinedVariableError,
    VarphiInvalidUnicodeError,
    VarphiUnknownSymbolError,
    VarphiUnknownDirectionError,
)


class VarphiCompiler(VarphiListener, ABC):
    """
    An abstract Varphi compiler and IR generator.

    Concrete subclasses must implement `_generate_compiled_program()`.
    When called, the subclass can safely access:
        - self.states (set[str]): The names of all states in the user's source Varphi program
        - self.initial_state (str): The name of the first state encountered.
        - self.ir (dict[str, list[VarphiTransition]]): A map of states to their transitions, sorted by specificity score.
    """

    _tape_count: Optional[int]
    _raw_transitions: list[VarphiTransition]

    states: set[str]
    initial_state: Optional[str]
    ir: dict[str, list[VarphiTransition]]

    def __init__(self):
        """Initialize this compiler."""
        self._tape_count = None
        self._raw_transitions = []
        self.states = set()
        self.initial_state = None
        self.ir = {}

    @abstractmethod
    def _generate_compiled_program(self) -> str:
        """Generate the compiled program."""
        pass

    def compile(self, program: str) -> str:
        """Compile a Varphi program."""
        self._tape_count = None
        self._raw_transitions = []
        self.states = set()
        self.initial_state = None
        self.ir = {}

        input_stream = InputStream(program)
        error_listener = VarphiErrorListener()

        lexer = VarphiLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)

        token_stream = CommonTokenStream(lexer)
        parser = VarphiParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)

        tree = parser.program()
        walker = ParseTreeWalker()
        walker.walk(self, tree)

        self._build_ir()

        return self._generate_compiled_program()

    def _build_ir(self) -> None:
        """Groups parsed transitions by state and sorts them by specificity."""
        grouped_transitions: defaultdict[str, list[VarphiTransition]] = defaultdict(
            list
        )
        for transition in self._raw_transitions:
            grouped_transitions[transition.current_state].append(transition)

        for state, transitions in grouped_transitions.items():
            transitions.sort(key=lambda transition: transition.specificity)
            self.ir[state] = transitions

    def enterTransition(self, ctx: VarphiParser.TransitionContext) -> None:
        """Process and add a transition to the raw IR."""
        current_state = ctx.current_state.getText()
        next_state = ctx.next_state.getText()
        self.states.add(current_state)
        self.states.add(next_state)

        if self.initial_state is None:
            self.initial_state = current_state

        next_variable_number = 0
        variable_name_to_variable_object = {}

        def extract_symbol(
            symbol_ctx, variable_undefined_ok: bool = True
        ) -> ReadWriteTupleElement:
            nonlocal next_variable_number, variable_name_to_variable_object

            if symbol_ctx.VARIABLE():
                variable_name = symbol_ctx.VARIABLE().getText()
                if variable_name in variable_name_to_variable_object:
                    return variable_name_to_variable_object[variable_name]
                if not variable_undefined_ok:
                    raise VarphiUndefinedVariableError(symbol_ctx, variable_name)
                variable_name_to_variable_object[variable_name] = Variable(
                    next_variable_number
                )
                next_variable_number += 1
                return variable_name_to_variable_object[variable_name]

            if symbol_ctx.BLANK_KW():
                return BuiltinSymbol.BLANK

            if symbol_ctx.INT():
                unicode_val = int(symbol_ctx.INT().getText())
                if not (0 <= unicode_val <= 0x10FFFF):
                    raise VarphiInvalidUnicodeError(symbol_ctx, unicode_val)
                return Character(chr(unicode_val))

            if symbol_ctx.CHAR_LITERAL():
                # Strip the outer single quotes (e.g., "'a'" becomes "a")
                text = symbol_ctx.CHAR_LITERAL().getText()[1:-1]
                return Character(text)

            raise VarphiUnknownSymbolError(symbol_ctx, symbol_ctx.getText())

        def extract_direction(direction_ctx) -> Direction:
            if direction_ctx.LEFT_KW():
                return Direction.LEFT
            if direction_ctx.RIGHT_KW():
                return Direction.RIGHT
            if direction_ctx.STAY_KW():
                return Direction.STAY
            raise VarphiUnknownDirectionError(direction_ctx, direction_ctx.getText())

        read_ctx = ctx.read_symbols()
        reads = tuple(extract_symbol(s) for s in read_ctx.symbol()) if read_ctx else ()

        write_ctx = ctx.write_symbols()
        writes = (
            tuple(
                extract_symbol(s, variable_undefined_ok=False)
                for s in write_ctx.symbol()
            )
            if write_ctx
            else ()
        )

        shift_ctx = ctx.shift_directions()
        shifts = (
            tuple(extract_direction(d) for d in shift_ctx.direction())
            if shift_ctx
            else ()
        )

        if len(writes) != len(reads) or len(shifts) != len(reads):
            raise VarphiTransitionInconsistentTapeCountError(
                ctx, len(reads), len(writes), len(shifts)
            )

        current_tape_count = len(reads)
        if self._tape_count is None:
            self._tape_count = current_tape_count
        elif current_tape_count != self._tape_count:
            raise VarphiGlobalTapeCountError(ctx, self._tape_count, current_tape_count)

        transition = VarphiTransition(
            current_state=current_state,
            read_symbols=reads,
            next_state=next_state,
            write_symbols=writes,
            shift_directions=shifts,
            line_number=ctx.start.line,
        )
        self._raw_transitions.append(transition)
