Implement the feature file(s) in `features/` with focus on **robustness**: reliability, error handling, edge cases, and resilience.

## Requirements

1. Read all `.feature` files in `features/` to understand requirements
2. Read step definitions in `features/steps/` to see the expected interface
3. Create implementation in `src/` with robust design
4. Update step definitions to import and use your implementation
5. Run `uv run behave` to verify all scenarios pass

## Robustness Patterns to Apply

- **Custom exceptions**: Create exception hierarchy for domain errors
- **Input validation**: Validate types, check for None, validate ranges
- **Defensive programming**: Fail fast on invalid states, use assertions
- **Clear error messages**: Actionable, no internal details leaked
- **Edge cases**: Handle boundaries, nulls, overflow, underflow

## Verification

Before reporting done:
- [ ] `src/` directory exists with implementation
- [ ] Step definitions import from `src`
- [ ] `uv run behave` shows all scenarios passed
- [ ] Custom exceptions implemented
- [ ] Input validation present
