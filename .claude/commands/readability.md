Implement the feature file(s) in `features/` with focus on **readability**: clarity, self-documentation, and clean code.

## Requirements

1. Read all `.feature` files in `features/` to understand requirements
2. Read step definitions in `features/steps/` to see the expected interface
3. Create crystal-clear implementation in `src/`
4. Update step definitions to import and use your implementation
5. Run `uv run behave` to verify all scenarios pass

## Readability Patterns to Apply

- **Descriptive names**: Full words, not abbreviations
- **Comprehensive docstrings**: Class docstrings with examples, method docstrings with Args/Returns
- **Meaningful error messages**: Context-rich, actionable
- **Logical organization**: Group related methods, public API first
- **Type hints**: As documentation
- **PEP 8**: Consistent formatting

## Verification

Before reporting done:
- [ ] `src/` directory exists with implementation
- [ ] All public methods have docstrings
- [ ] Classes have docstrings with usage examples
- [ ] Names are descriptive (no single letters)
- [ ] Step definitions import from `src`
- [ ] `uv run behave` shows all scenarios passed
