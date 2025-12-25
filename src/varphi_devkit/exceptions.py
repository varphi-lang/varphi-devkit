from antlr4.error.ErrorListener import ErrorListener
from antlr4 import Token

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
BLUE = "\033[34m"
CYAN = "\033[96m"
WHITE = "\033[97m"


class VarphiSyntaxError(Exception):
    def __init__(self, recognizer, offendingSymbol, line, column, msg):
        self.recognizer = recognizer
        self.offendingSymbol = offendingSymbol
        self.line = line
        self.column = column
        self.msg = msg
        super().__init__(msg)

    def __str__(self):
        result = [f"\n{BOLD}{RED}error:{RESET} {BOLD}{WHITE}{self.msg}{RESET}"]
        result.append(f"{BLUE}   -->{RESET} line {self.line}:{self.column + 1}")

        stream = None
        try:
            if self.recognizer:
                temp_stream = self.recognizer.getInputStream()
                if hasattr(temp_stream, "tokenSource"):
                    stream = temp_stream.tokenSource.inputStream
                else:
                    stream = temp_stream

            elif self.offendingSymbol:
                if hasattr(self.offendingSymbol, "getInputStream"):
                    stream = self.offendingSymbol.getInputStream()
                elif hasattr(self.offendingSymbol, "tokenSource"):
                    stream = self.offendingSymbol.tokenSource.inputStream

            if stream:
                lines = str(stream).splitlines()
                if 0 <= self.line - 1 < len(lines):
                    code_line = lines[self.line - 1]

                    gutter_width = 4
                    line_num_str = str(self.line)

                    result.append(f"{BLUE}{' ' * gutter_width} |{RESET}")

                    result.append(
                        f"{BLUE}{line_num_str:>{gutter_width}} |{RESET} {code_line}"
                    )

                    token_len = 1
                    if self.offendingSymbol and isinstance(self.offendingSymbol, Token):
                        start = self.offendingSymbol.start
                        stop = self.offendingSymbol.stop
                        if start is not None and stop is not None:
                            token_len = stop - start + 1

                    padding = " " * self.column
                    pointer = f"{BOLD}{RED}^{'~' * (token_len - 1)}{RESET}"
                    result.append(
                        f"{BLUE}{' ' * gutter_width} |{RESET} {padding}{pointer}"
                    )

        except Exception:
            pass

        return "\n".join(result)


class VarphiTransitionInconsistentTapeCountError(VarphiSyntaxError):
    def __init__(self, ctx, r_len, w_len, s_len):
        msg = (
            f"local tape count mismatch: read {r_len} symbols, "
            f"but wrote {w_len} and shifted {s_len}"
        )
        super().__init__(None, ctx.start, ctx.start.line, ctx.start.column, msg)


class VarphiGlobalTapeCountError(VarphiSyntaxError):
    def __init__(self, ctx, expected, actual):
        msg = (
            f"global tape count mismatch: previous transitions used {expected} tapes, "
            f"but this one uses {actual}"
        )
        super().__init__(None, ctx.start, ctx.start.line, ctx.start.column, msg)


class VarphiErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise VarphiSyntaxError(recognizer, offendingSymbol, line, column, msg)
