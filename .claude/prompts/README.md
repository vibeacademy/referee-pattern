# Implementation Prompts

This directory contains **implementation guides** for the Referee Pattern. Each guide instructs Claude to implement the same feature with a different quality focus.

## Usage

In your worktree, tell Claude to follow a specific implementation guide:

```
Follow .claude/prompts/robustness.md to implement features/calculator.feature
```

Or more explicitly:

```
Read .claude/prompts/maintainability.md and follow those instructions to implement the calculator feature. Create the src/ directory and files as specified.
```

**Important**: Do NOT say "use the X agent" - that triggers subagent spawning which can hallucinate. Instead, ask Claude to "follow" or "read and implement according to" the prompt file.

## Available Implementation Guides

| Guide | Focus | Typical Output |
|-------|-------|----------------|
| `robustness.md` | Error handling, validation, edge cases | Custom exceptions, defensive code |
| `maintainability.md` | Clean architecture, SOLID principles | Multiple files, Strategy pattern |
| `performance.md` | Speed, memory efficiency | `__slots__`, minimal abstraction |
| `readability.md` | Clarity, self-documentation | Comprehensive docstrings |
| `security.md` | Input validation, type safety | Strict validation, bounds checking |
| `testing.md` | Testability, dependency injection | Injectable dependencies, pure functions |

## Workflow

1. Create worktrees for each implementation:
   ```bash
   git worktree add -b robustness-impl ../referee-pattern-robustness
   git worktree add -b maintainability-impl ../referee-pattern-maintainability
   git worktree add -b performance-impl ../referee-pattern-performance
   ```

2. In each worktree, start Claude and give it the corresponding prompt:
   ```
   # In referee-pattern-robustness/
   Follow .claude/prompts/robustness.md to implement features/calculator.feature
   ```

3. Verify tests pass:
   ```bash
   uv run behave
   ```

4. Compare implementations across worktrees and merge the best aspects.

## What Each Guide Produces

All guides instruct Claude to:
1. Read `features/calculator.feature` for requirements
2. Create `src/` directory with Calculator implementation
3. Update `features/steps/calculator_steps.py` to use the Calculator
4. Run `uv run behave` to verify all 5 scenarios pass

The difference is in **how** they implement - what patterns, tradeoffs, and priorities they apply.
