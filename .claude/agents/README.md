# Review Agents

This directory contains specialized **code review** agents. These agents evaluate existing code and provide scores/recommendations. They do NOT write code.

For **implementation prompts** that guide Claude to write code, see `.claude/prompts/`.

## Available Review Agents

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

### 7. Merge Critic (`merge-critic.md`)
Analyzes multiple implementations and recommends merge strategies.

## Usage

These agents are invoked via the Task tool for code review:

```
"Use the robustness agent to review src/calculator.py"
```

Each agent provides:
- **Numerical Score** (1-10) for their area of focus
- **Strengths** - What the code does well
- **Issues** - Specific problems with severity and recommendations
- **Overall Assessment** - Summary and priorities
