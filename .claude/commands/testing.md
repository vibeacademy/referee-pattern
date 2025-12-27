Implement the feature file(s) in `features/` with focus on **testability**: dependency injection, pure functions, and clear interfaces.

## Requirements

1. Read all `.feature` files in `features/` to understand requirements
2. Read step definitions in `features/steps/` to see the expected interface
3. Create test-friendly implementation in `src/`
4. Update step definitions to import and use your implementation
5. Run `uv run behave` to verify all scenarios pass
6. Optionally create `tests/` with pytest unit tests

## Testability Patterns to Apply

- **Dependency injection**: Dependencies injectable via constructor
- **Pure functions where possible**: No side effects
- **Clear interfaces**: Well-defined inputs and outputs
- **Factory methods**: `ClassName.create_for_testing(mocks)`
- **Isolated side effects**: Logging, state changes isolated and mockable
- **Type hints**: Help with test assertions

## Verification

Before reporting done:
- [ ] `src/` directory exists with implementation
- [ ] Dependencies are injectable
- [ ] Clear interface for each method
- [ ] Step definitions import from `src`
- [ ] `uv run behave` shows all scenarios passed
