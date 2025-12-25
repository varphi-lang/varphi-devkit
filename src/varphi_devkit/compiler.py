from abc import ABC, abstractmethod
from dataclasses import dataclass
from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker

from .antlr import VarphiLexer
from .antlr import VarphiParser
from .antlr import VarphiListener

from .exceptions import (
    VarphiErrorListener,
    VarphiTransitionInconsistentTapeCountError,
    VarphiGlobalTapeCountError,
)

BLANK = "_"
WILDCARD = "*"


@dataclass(frozen=True)
class VarphiTransition:
    current_state: str
    read_symbols: tuple[str, ...]
    next_state: str
    write_symbols: tuple[str, ...]
    shift_directions: tuple[str, ...]
    line_number: int


class VarphiCompiler(VarphiListener, ABC):
    def __init__(self):
        self._expected_tape_count = None

    @abstractmethod
    def handle_transition(self, transition: VarphiTransition) -> None:
        pass

    @abstractmethod
    def generate_compiled_program(self) -> str:
        pass

    def compile(self, program: str) -> str:
        # Reset state (subclasses must do so for their own state too)
        self._expected_tape_count = None

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

        return self.generate_compiled_program()

    def enterTransition(self, ctx: VarphiParser.TransitionContext) -> None:
        current_state = ctx.current_state.getText()
        next_state = ctx.next_state.getText()

        def extract(symbol_ctx) -> str:
            if symbol_ctx.STAR():
                return WILDCARD
            if symbol_ctx.BLANK_KW():
                return BLANK
            if symbol_ctx.ALPHANUM():
                return symbol_ctx.ALPHANUM().getText()
            raise ValueError(f"Unknown symbol type: {symbol_ctx.getText()}")

        read_ctx = ctx.read_symbols()
        reads = tuple(extract(s) for s in read_ctx.symbol()) if read_ctx else ()

        write_ctx = ctx.write_symbols()
        writes = tuple(extract(s) for s in write_ctx.symbol()) if write_ctx else ()

        shift_ctx = ctx.shift_directions()
        shifts = tuple(d.getText() for d in shift_ctx.direction()) if shift_ctx else ()

        # Check that intra-line tuples have the same length
        if len(writes) != len(reads) or len(shifts) != len(reads):
            raise VarphiTransitionInconsistentTapeCountError(
                ctx, len(reads), len(writes), len(shifts)
            )

        # Check that intra-line tuples have the same length
        current_tape_count = len(reads)

        if self._expected_tape_count is None:
            # First valid transition sets the rule for the rest of the file
            self._expected_tape_count = current_tape_count
        elif current_tape_count != self._expected_tape_count:
            # New transition does not match the established tape count
            raise VarphiGlobalTapeCountError(
                ctx, self._expected_tape_count, current_tape_count
            )

        transition = VarphiTransition(
            current_state=current_state,
            read_symbols=reads,
            next_state=next_state,
            write_symbols=writes,
            shift_directions=shifts,
            line_number=ctx.start.line,
        )
        self.handle_transition(transition)
