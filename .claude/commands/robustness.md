Implement features/calculator.feature with focus on **robustness**: reliability, error handling, edge cases, and resilience.

## Requirements

1. Read `features/calculator.feature` to understand requirements
2. Read `features/steps/calculator_steps.py` to see the expected interface
3. Create `src/__init__.py` and `src/calculator.py` with a robust Calculator implementation
4. Update `features/steps/calculator_steps.py` to import and use your Calculator
5. Run `uv run behave` to verify all 5 scenarios pass

## File Structure

```
src/
├── __init__.py
└── calculator.py

features/steps/
└── calculator_steps.py  (update this)
```

## Robustness Patterns to Apply

- **Custom exceptions**: Create `DivisionByZeroError` extending a base `CalculatorError`
- **Input validation**: Validate types, check for None, validate ranges
- **Defensive programming**: Fail fast on invalid states, use assertions
- **Clear error messages**: Actionable, no internal details leaked
- **Edge cases**: Division by zero (required), overflow, underflow, floats

## Verification

Before reporting done:
- [ ] `src/` directory exists with `__init__.py` and `calculator.py`
- [ ] `features/steps/calculator_steps.py` imports from `src.calculator`
- [ ] `uv run behave` shows 5 scenarios passed
