# Referee Pattern Agents

This directory contains specialized code review agents, each focusing on a specific quality attribute. These agents work together in a referee pattern to provide comprehensive code reviews.

## Available Agents

### 1. Readability Referee (`readability.md`)
Reviews code for clarity, naming, documentation, and clean code principles.

**Focus Areas:**
- Naming conventions
- Code organization
- Documentation quality
- Code clarity
- Formatting and style

### 2. Robustness Referee (`robustness.md`)
Reviews code for reliability, error handling, and edge case coverage.

**Focus Areas:**
- Error handling
- Input validation
- Edge case coverage
- Resource management
- Defensive programming

### 3. Performance Referee (`performance.md`)
Reviews code for efficiency and optimization opportunities.

**Focus Areas:**
- Algorithmic efficiency
- Resource usage
- I/O operations
- Database optimization
- Concurrency

### 4. Security Referee (`security.md`)
Reviews code for security vulnerabilities and attack vectors.

**Focus Areas:**
- Input validation and sanitization
- Authentication and authorization
- Data protection
- Cryptography
- Common vulnerabilities (OWASP)

### 5. Maintainability Referee (`maintainability.md`)
Reviews code for long-term sustainability and ease of modification.

**Focus Areas:**
- Code structure
- Coupling and cohesion
- Extensibility
- Technical debt
- Documentation

### 6. Testing Referee (`testing.md`)
Reviews code for testability, test coverage, and test quality.

**Focus Areas:**
- Test coverage
- Test quality
- Test organization
- Testability of code
- Testing strategy

## Usage

Each agent can be invoked independently to review code from their specialized perspective. The agents provide:

1. **Numerical Score** (1-10) for their area of focus
2. **Strengths** - What the code does well
3. **Issues** - Specific problems with severity and recommendations
4. **Overall Assessment** - Summary and priorities

## Referee Pattern

The referee pattern allows multiple specialized agents to evaluate the same code independently, then aggregate their findings for a comprehensive review. This ensures no aspect of code quality is overlooked.

### Workflow

1. Submit code for review
2. Each referee evaluates independently
3. Collect scores and findings from all referees
4. Aggregate results into comprehensive report
5. Prioritize issues based on severity and impact
6. Generate actionable recommendations

## Customization

You can adjust the evaluation criteria in each agent's markdown file to match your team's standards and priorities. The agents are designed to be flexible and adaptable to different projects and coding standards.
