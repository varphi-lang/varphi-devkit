from dataclasses import dataclass, field
from enum import Enum, auto


class ReadWriteTupleElement:
    """Base class for all elements that can appear in the read or write tuple of a Varphi transition."""

    pass


@dataclass(frozen=True, eq=True)
class Character(ReadWriteTupleElement):
    """A concrete unicode character."""

    value: str

    def __post_init__(self):
        if not isinstance(self.value, str) or len(self.value) != 1:
            raise ValueError(
                f"Character must be exactly 1 string character, got {self.value!r}"
            )


class BuiltinSymbol(ReadWriteTupleElement, Enum):
    """A builtin Varphi symbol."""

    BLANK = auto()


@dataclass(frozen=True, eq=True)
class Variable(ReadWriteTupleElement):
    """A variable ID."""

    id: int


class Direction(Enum):
    """A head direction."""

    LEFT = auto()
    RIGHT = auto()
    STAY = auto()


@dataclass(frozen=True)
class VarphiTransition:
    """A transition (logically, a single line) in a Varphi program."""

    current_state: str
    read_symbols: tuple[ReadWriteTupleElement, ...]
    next_state: str
    write_symbols: tuple[ReadWriteTupleElement, ...]
    shift_directions: tuple[Direction, ...]
    line_number: int
    specificity: tuple[int, int] = field(
        init=False
    )  # (unique variables, total variables)

    def __post_init__(self):
        variables = [s for s in self.read_symbols if isinstance(s, Variable)]
        unique_variables = len(set(variables))
        total_variables = len(variables)

        # Because the dataclass is frozen, we must bypass normal assignment
        object.__setattr__(self, "specificity", (unique_variables, total_variables))
