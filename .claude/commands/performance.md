Implement the feature file(s) in `features/` with focus on **performance**: speed, memory efficiency, and minimal overhead.

## Requirements

1. Read all `.feature` files in `features/` to understand requirements
2. Read step definitions in `features/steps/` to see the expected interface
3. Create optimized implementation in `src/`
4. Update step definitions to import and use your implementation
5. Run `uv run behave` to verify all scenarios pass

## Performance Patterns to Apply

- **`__slots__`**: Use on classes to reduce memory
- **Direct methods**: No unnecessary indirection or dispatch
- **Minimal abstraction**: Fewer files, fewer layers
- **Early returns**: Short-circuit on error conditions
- **Type hints**: Help with optimization
- **No object creation in hot paths**: Reuse where possible

## Verification

Before reporting done:
- [ ] `src/` directory exists with implementation
- [ ] `__slots__` is used on classes
- [ ] No unnecessary abstraction layers
- [ ] Step definitions import from `src`
- [ ] `uv run behave` shows all scenarios passed
