# Referee Pattern with Claude Code

A template project demonstrating the **Referee Pattern** - a powerful workflow for using multiple specialized Claude Code agents to solve problems from different perspectives, then merging the best approaches.

## What is the Referee Pattern?

The Referee Pattern is a code generation workflow where:
1. Multiple specialized agents (like "referees") independently implement the same feature
2. Each agent focuses on a specific quality attribute (maintainability, performance, robustness, etc.)
3. The implementations are evaluated and the best aspects are merged into a final solution

This approach combines diverse perspectives to create code that is:
- ✅ Maintainable (clean architecture, extensible)
- ✅ Performant (optimized, efficient)
- ✅ Robust (error handling, edge cases)

## Quick Start

### Prerequisites

- [uv](https://docs.astral.sh/uv/) - Fast Python package manager
- [Claude Code CLI](https://docs.claude.com/en/docs/claude-code) installed
- Anthropic API key

### Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd referee-pattern
   ```

2. **Set your Anthropic API key:**
   ```bash
   # Option 1: Export environment variable
   export ANTHROPIC_API_KEY="your-api-key-here"

   # Option 2: Add to your shell profile (~/.zshrc or ~/.bashrc)
   echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Run the automated workflow:**
   ```bash
   ./run-referee-pattern.sh
   ```

   This script will:
   - Initialize the project with uv
   - Create git worktrees for each specialized agent
   - Run the maintainability, performance, and robustness agents in parallel
   - Show you the different implementations
   - Guide you through merging the best approaches

### Manual Workflow

If you want to understand each step:

```bash
# 1. Initialize Python environment
uv sync

# 2. Run tests to see the baseline
uv run behave

# 3. Create worktrees for parallel agent development
git worktree add -b maintainability-impl ../referee-pattern-maintainability
git worktree add -b performance-impl ../referee-pattern-performance
git worktree add -b robustness-impl ../referee-pattern-robustness

# 4. In each worktree, use Claude Code to implement from that perspective
# (See PATTERN.md for detailed instructions)
```

## Project Structure

```
referee-pattern/
├── .claude/
│   └── agents/          # Specialized code review agents
│       ├── maintainability.md
│       ├── performance.md
│       ├── robustness.md
│       ├── readability.md
│       ├── security.md
│       └── testing.md
├── calculator/          # Example merged implementation
│   ├── __init__.py
│   ├── calculator.py
│   ├── operations.py
│   └── exceptions.py
├── features/            # BDD specifications
│   ├── calculator.feature
│   └── steps/
│       └── calculator_steps.py
└── PATTERN.md          # Detailed pattern explanation
```

## Example: Calculator Implementation

This repo includes a working example - a simple calculator implemented using the referee pattern.

**The Problem:** Build a calculator that handles basic arithmetic (add, subtract, multiply, divide) and division by zero errors.

**Three Agent Perspectives:**

| Agent | Lines | Approach | Key Features |
|-------|-------|----------|--------------|
| **Maintainability** | 255 | Modular (4 files) | Strategy Pattern, extensible, SOLID |
| **Performance** | 101 | Minimal (1 file) | \`__slots__\`, direct methods, optimized |
| **Robustness** | 534 | Defensive (1 file) | 7 exception types, logging, thread-safe |

**Merged Result:** 302 lines combining:
- Maintainability's modular Strategy Pattern architecture
- Performance's \`__slots__\` memory optimization
- Robustness's exception hierarchy and error handling

All tests pass: 5 scenarios, 15 steps ✅

## The Specialized Agents

The \`.claude/agents/\` directory contains 6 specialized code review agents:

1. **maintainability** - Clean architecture, SOLID principles, extensibility
2. **performance** - Speed, memory efficiency, algorithmic optimization
3. **robustness** - Error handling, edge cases, defensive programming
4. **readability** - Code clarity, documentation, naming
5. **security** - Vulnerabilities, input validation, secure practices
6. **testing** - Test coverage, test quality, testability

These agents can be used with Claude Code's \`/agents\` command or the Task tool.

## When to Use This Pattern

The Referee Pattern is ideal for:
- ✅ Features with competing quality attributes (performance vs. maintainability)
- ✅ Complex problems that benefit from multiple perspectives
- ✅ Learning opportunities - see different approaches to the same problem
- ✅ Code review - generate implementations optimized for different concerns
- ✅ Architecture decisions - evaluate tradeoffs empirically

Not recommended for:
- ❌ Simple, trivial tasks
- ❌ Time-critical situations (requires more upfront work)
- ❌ Problems with one obvious solution

## Learn More

- [PATTERN.md](./PATTERN.md) - Detailed explanation of the referee pattern
- [.claude/agents/README.md](./.claude/agents/README.md) - Agent descriptions
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)

## License

This is a template project - use it however you like!

## Contributing

This project uses [Conventional Commits](https://www.conventionalcommits.org/) for automated versioning and changelog generation.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: A new feature (triggers minor version bump)
- `fix`: A bug fix (triggers patch version bump)
- `docs`: Documentation changes only
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring without feature changes
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `build`: Build system changes
- `ci`: CI configuration changes
- `chore`: Other changes that don't modify src or test files

**Examples:**
```bash
feat: add division by zero handling
fix: correct calculator memory leak
docs: update installation instructions
```

The project uses:
- **Husky** - Git hooks for commit message validation
- **Commitlint** - Enforces conventional commit format
- **Semantic Release** - Automated versioning and releases on GitHub

This is a demonstration/template project. Feel free to fork and adapt for your needs!

---

**Built with [Claude Code](https://claude.com/claude-code) 🤖**
