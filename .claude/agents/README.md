# Referee Pattern Agents

This directory contains two types of specialized agents:

1. **Review Agents** (`*.md`) - Code reviewers that evaluate existing code
2. **Implementation Agents** (`*-impl.md`) - Code implementers that write code with specific quality focus

## Implementation Agents (Use These for the Referee Pattern)

These agents **implement features** by writing code to disk. Use these when you want agents to create different implementations of the same feature, each optimized for a specific quality attribute.

### 1. Robustness Implementation (`robustness-impl.md`)
Implements features with focus on reliability, error handling, and edge cases.

**Implementation Focus:**
- Custom exception hierarchies
- Comprehensive input validation
- Defensive programming
- Graceful error handling

### 2. Maintainability Implementation (`maintainability-impl.md`)
Implements features with focus on clean architecture and SOLID principles.

**Implementation Focus:**
- Strategy pattern for extensibility
- Separation of concerns (multiple files)
- Dependency injection
- Type hints and documentation

### 3. Performance Implementation (`performance-impl.md`)
Implements features with focus on speed and efficiency.

**Implementation Focus:**
- `__slots__` for memory efficiency
- Direct operations (minimal abstraction)
- Single-file design
- Optimized algorithms

### 4. Readability Implementation (`readability-impl.md`)
Implements features with focus on clarity and self-documentation.

**Implementation Focus:**
- Descriptive naming
- Comprehensive docstrings
- Clear code organization
- Consistent style

### 5. Security Implementation (`security-impl.md`)
Implements features with focus on security best practices.

**Implementation Focus:**
- Strict input validation
- Type safety
- Secure error handling
- Bounds checking

### 6. Testing Implementation (`testing-impl.md`)
Implements features with focus on testability.

**Implementation Focus:**
- Dependency injection
- Pure functions
- Clear interfaces
- Optional pytest unit tests

## Review Agents (For Code Review Only)

These agents **review existing code** and provide scores/recommendations. They do NOT write code.

### 1. Readability Referee (`readability.md`)
Reviews code for clarity, naming, documentation, and clean code principles.

### 2. Robustness Referee (`robustness.md`)
Reviews code for reliability, error handling, and edge case coverage.

### 3. Performance Referee (`performance.md`)
Reviews code for efficiency and optimization opportunities.

### 4. Security Referee (`security.md`)
Reviews code for security vulnerabilities and attack vectors.

### 5. Maintainability Referee (`maintainability.md`)
Reviews code for long-term sustainability and ease of modification.

### 6. Testing Referee (`testing.md`)
Reviews code for testability, test coverage, and test quality.

## Usage

### For the Referee Pattern (Parallel Implementations)

Use the `-impl` agents to create competing implementations:

```
# In each worktree, invoke the corresponding implementation agent:

# Worktree: referee-pattern-robustness
"Use the robustness-impl agent to implement features/calculator.feature"

# Worktree: referee-pattern-maintainability
"Use the maintainability-impl agent to implement features/calculator.feature"

# Worktree: referee-pattern-performance
"Use the performance-impl agent to implement features/calculator.feature"
```

Each agent will:
1. Read the feature specification
2. Create `src/calculator.py` with their focused implementation
3. Update `features/steps/calculator_steps.py` to use the Calculator
4. Run `uv run behave` to verify all tests pass
5. Report what files were created

### For Code Review

Use the review agents (without `-impl`) to evaluate existing code:

```
"Use the robustness agent to review src/calculator.py"
```

## Key Differences

| Aspect | Review Agents | Implementation Agents |
|--------|---------------|----------------------|
| Purpose | Evaluate code | Write code |
| Tools | Read, Grep, Glob, Bash | + Edit, Write |
| Output | Score + recommendations | Working code on disk |
| Verification | N/A | Tests must pass |

## Customization

Adjust the agent markdown files to match your team's standards. Implementation agents can be modified to:
- Change file locations
- Add/remove patterns to apply
- Adjust verification checklists
