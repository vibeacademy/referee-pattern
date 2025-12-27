Implement features/calculator.feature with focus on **maintainability**: clean architecture, SOLID principles, and long-term sustainability.

## Requirements

1. Read `features/calculator.feature` to understand requirements
2. Read `features/steps/calculator_steps.py` to see the expected interface
3. Create `src/` with modular Calculator implementation (multiple files)
4. Update `features/steps/calculator_steps.py` to import and use your Calculator
5. Run `uv run behave` to verify all 5 scenarios pass

## File Structure

```
src/
├── __init__.py       # exports Calculator
├── calculator.py     # main Calculator class
├── operations.py     # Strategy pattern for operations
└── exceptions.py     # custom exceptions

features/steps/
└── calculator_steps.py  (update this)
```

## Maintainability Patterns to Apply

- **Strategy pattern**: Abstract `Operation` base class, concrete `Addition`, `Subtraction`, etc.
- **Separation of concerns**: Calculator orchestrates, operations compute, exceptions handle errors
- **Open/Closed principle**: Easy to add new operations without modifying Calculator
- **Dependency injection**: Operations passed to Calculator
- **Type hints**: Throughout all modules
- **Docstrings**: Module, class, and method level

## Verification

Before reporting done:
- [ ] `src/` has `__init__.py`, `calculator.py`, `operations.py`, `exceptions.py`
- [ ] Strategy pattern is implemented
- [ ] `features/steps/calculator_steps.py` imports from `src`
- [ ] `uv run behave` shows 5 scenarios passed
