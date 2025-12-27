Implement features/calculator.feature with focus on **readability**: clarity, self-documentation, and clean code.

## Requirements

1. Read `features/calculator.feature` to understand requirements
2. Read `features/steps/calculator_steps.py` to see the expected interface
3. Create `src/__init__.py` and `src/calculator.py` with crystal-clear code
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

## Readability Patterns to Apply

- **Descriptive names**: `dividend`, `divisor` not `a`, `b`
- **Comprehensive docstrings**: Class docstring with examples, method docstrings with Args/Returns
- **Meaningful error messages**: `f"Cannot divide {dividend} by zero"`
- **Logical organization**: Group related methods, public API first
- **Type hints**: As documentation
- **PEP 8**: Consistent formatting

## Verification

Before reporting done:
- [ ] `src/` directory exists with `__init__.py` and `calculator.py`
- [ ] All public methods have docstrings
- [ ] Class has docstring with usage example
- [ ] Names are descriptive (no single letters)
- [ ] `features/steps/calculator_steps.py` imports from `src.calculator`
- [ ] `uv run behave` shows 5 scenarios passed
