# Contributing to Varphi Development Kit

Thank you for your interest in contributing to the Varphi Development Kit! This guide will help you get started with development and understand the project structure.

## Prerequisites

- **Python 3.10+**
- **Poetry** (Python dependency management and packaging tool)

If you don't have Poetry installed, you can install it following the instructions at [python-poetry.org](https://python-poetry.org/docs/#installation).

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/varphi-lang/varphi-devkit.git
   cd varphi-devkit
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

   This will create a virtual environment and install all project dependencies including development tools.

3. **Activate the virtual environment**
   ```bash
   poetry shell
   ```

## Project Structure

The project is organized as follows:

```
varphi-devkit/
├── src/varphi_devkit/          # Main package
│   ├── __init__.py             # Package exports
│   ├── model.py                # Data model (VarphiLine, enums)
│   ├── compilation.py          # Compiler framework
│   └── syntax/                 # Language parsing
│       ├── __init__.py
│       ├── Varphi.g4           # ANTLR grammar definition
│       ├── error_listener.py   # Syntax error handling
│       └── antlr/              # Generated ANTLR files
├── tests/                      # Test suite
│   ├── toy_compilers/          # Example compiler implementations
│   └── test_*.py               # Test files
└── pyproject.toml              # Project configuration
```

For detailed information about each component, refer to the [README.md](README.md).

## Development Workflow

### Making Changes

1. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the existing code style and patterns.

3. Add or update tests as needed in the `tests/` directory.

4. Run the test suite (from the project root directory) to ensure everything works:
   ```bash
   poetry run pytest tests/
   ```

5. Run linting to check code quality:
   ```bash
   poetry run pylint src/varphi_devkit/
   ```

### Modifying the Varphi Language Syntax

If you need to modify the Varphi language grammar (in `src/varphi_devkit/syntax/Varphi.g4`), you must regenerate the ANTLR parser files:

1. **Regenerate parser files** (run from the project root directory):
   ```bash
   antlr4 -o src/varphi_devkit/syntax/antlr -Dlanguage=Python3 src/varphi_devkit/syntax/Varphi.g4
   ```

   This command will regenerate:
   - `VarphiLexer.py` - Tokenizer
   - `VarphiParser.py` - Parser
   - `VarphiListener.py` - Parse tree listener interface

2. **Test the changes**: Run the test suite to ensure the grammar changes work correctly:
   ```bash
   poetry run pytest tests/
   ```

### Testing

The project uses pytest for testing. Test files are organized by functionality:

- `test_syntax_errors.py` - Tests for syntax error handling
- `test_line_counter.py` - Tests for the LineCounter example compiler
- `test_empty_checker.py` - Tests for the EmptyChecker example compiler
- `test_unique_state_name_lister.py` - Tests for the UniqueStateNameLister example compiler

Run specific test files:
```bash
poetry run pytest tests/test_syntax_errors.py
```

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Add docstrings for public functions and classes
- Keep line length under 88 characters (Black formatter default)

The project uses pylint for code quality checking. Run it before submitting:
```bash
poetry run pylint src/varphi_devkit/
```
