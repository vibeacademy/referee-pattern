Implement features/calculator.feature with focus on **performance**: speed, memory efficiency, and minimal overhead.

## Requirements

1. Read `features/calculator.feature` to understand requirements
2. Read `features/steps/calculator_steps.py` to see the expected interface
3. Create `src/__init__.py` and `src/calculator.py` with an optimized Calculator
4. Update `features/steps/calculator_steps.py` to import and use your Calculator
5. Run `uv run behave` to verify all 5 scenarios pass

## File Structure

```
src/
├── __init__.py
└── calculator.py     # single file, minimal overhead

features/steps/
└── calculator_steps.py  (update this)
```

## Performance Patterns to Apply

- **`__slots__`**: Use on Calculator class to reduce memory
- **Direct methods**: No strategy pattern indirection, direct `add()`, `subtract()`, etc.
- **Minimal abstraction**: Single file, no unnecessary classes
- **Early returns**: Short-circuit on error conditions
- **Type hints**: Help with optimization
- **No object creation in hot paths**: Reuse where possible

## Verification

Before reporting done:
- [ ] `src/` directory exists with `__init__.py` and `calculator.py`
- [ ] `__slots__` is used on Calculator
- [ ] No unnecessary abstraction layers
- [ ] `features/steps/calculator_steps.py` imports from `src.calculator`
- [ ] `uv run behave` shows 5 scenarios passed
