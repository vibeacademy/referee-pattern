Implement features/calculator.feature with focus on **testability**: dependency injection, pure functions, and clear interfaces.

## Requirements

1. Read `features/calculator.feature` to understand requirements
2. Read `features/steps/calculator_steps.py` to see the expected interface
3. Create `src/__init__.py` and `src/calculator.py` designed for easy testing
4. Update `features/steps/calculator_steps.py` to import and use your Calculator
5. Run `uv run behave` to verify all 5 scenarios pass
6. Optionally create `tests/test_calculator.py` with pytest unit tests

## File Structure

```
src/
├── __init__.py
└── calculator.py

features/steps/
└── calculator_steps.py  (update this)

tests/                   # optional
├── __init__.py
└── test_calculator.py
```

## Testability Patterns to Apply

- **Dependency injection**: Logger, operation provider injectable via constructor
- **Pure functions where possible**: `add(a, b)` with no side effects
- **Clear interfaces**: Well-defined inputs and outputs
- **Factory methods**: `Calculator.create_for_testing(mock_ops)`
- **Isolated side effects**: Logging, state changes isolated and mockable
- **Type hints**: Help with test assertions

Example:
```python
class Calculator:
    def __init__(self, logger=None):
        self._logger = logger or NullLogger()

    @classmethod
    def create_for_testing(cls, mock_logger=None):
        return cls(logger=mock_logger)
```

## Verification

Before reporting done:
- [ ] `src/` directory exists with `__init__.py` and `calculator.py`
- [ ] Dependencies are injectable
- [ ] Clear interface for each method
- [ ] `features/steps/calculator_steps.py` imports from `src.calculator`
- [ ] `uv run behave` shows 5 scenarios passed
