Implement the feature file(s) in `features/` with focus on **maintainability**: clean architecture, SOLID principles, and long-term sustainability.

## Requirements

1. Read all `.feature` files in `features/` to understand requirements
2. Read step definitions in `features/steps/` to see the expected interface
3. Create modular implementation in `src/` (multiple files preferred)
4. Update step definitions to import and use your implementation
5. Run `uv run behave` to verify all scenarios pass

## Maintainability Patterns to Apply

- **Strategy pattern**: Abstract base classes for extensible operations
- **Separation of concerns**: Separate files for different responsibilities
- **Open/Closed principle**: Easy to add features without modifying existing code
- **Dependency injection**: Dependencies passed in, not created internally
- **Type hints**: Throughout all modules
- **Docstrings**: Module, class, and method level

## Verification

Before reporting done:
- [ ] `src/` has modular structure with multiple files
- [ ] Strategy or similar pattern is implemented
- [ ] Step definitions import from `src`
- [ ] `uv run behave` shows all scenarios passed
- [ ] Type hints present throughout
