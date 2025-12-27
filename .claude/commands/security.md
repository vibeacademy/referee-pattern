Implement the feature file(s) in `features/` with focus on **security**: input validation, type safety, and secure defaults.

## Requirements

1. Read all `.feature` files in `features/` to understand requirements
2. Read step definitions in `features/steps/` to see the expected interface
3. Create security-first implementation in `src/`
4. Update step definitions to import and use your implementation
5. Run `uv run behave` to verify all scenarios pass

## Security Patterns to Apply

- **Strict input validation**: Check type, None, NaN, Infinity before any operation
- **`__slots__`**: Prevent attribute injection
- **Safe error messages**: No internal details leaked
- **Type checking**: `isinstance()` checks on all inputs
- **Bounds checking**: Check for overflow conditions
- **No implicit coercion**: Explicit type conversion only

## Verification

Before reporting done:
- [ ] `src/` directory exists with implementation
- [ ] All inputs validated before use
- [ ] `__slots__` used on classes
- [ ] Error messages don't leak internals
- [ ] Step definitions import from `src`
- [ ] `uv run behave` shows all scenarios passed
