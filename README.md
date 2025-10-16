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

3. **Choose your workflow:** See "Two Ways to Use This Template" below

---

## Two Ways to Use This Template

You can complete the Referee Pattern using either an automated script or manual steps. **Both approaches achieve the same result** - choose based on your learning style and comfort with git.

### Option 1: Automated Script (Recommended for First-Time Users)

The script automates worktree creation and provides a guided experience.

```bash
./run-referee-pattern.sh
```

**What the script does:**
- Initializes the project with uv
- Creates git worktrees for each specialized agent
- Runs the maintainability, performance, and robustness agents in parallel
- Shows you the different implementations
- Guides you through merging the best approaches

**Pros:**
- ✅ Automated setup - less manual work
- ✅ Guided workflow - script prompts you through each step
- ✅ Handles common errors gracefully
- ✅ Good for learning the pattern quickly

**Cons:**
- ❌ Less hands-on - you don't see every command
- ❌ Hides underlying git operations
- ❌ May not work if you have custom git setup

**When to use:** First time through the pattern, want to focus on the concepts rather than git mechanics.

---

### Option 2: Manual Workflow (Recommended for Deep Learning)

Follow manual steps to understand each component of the pattern.

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
# (See AGENT_USAGE_GUIDE.md for detailed instructions and template prompts)

# 5. After implementations complete, merge using MERGE_GUIDE.md
# (See SUCCESS_CRITERIA.md to know when you're done)
```

**Pros:**
- ✅ Deep understanding - you execute every step
- ✅ Full control and flexibility
- ✅ Learn git worktrees directly
- ✅ Easy to customize for your needs

**Cons:**
- ❌ More commands to manage
- ❌ Need to understand worktrees
- ❌ More opportunities for errors

**When to use:** Want to understand the mechanics, comfortable with git, need to customize the workflow.

---

**Note:** The script is a **convenience wrapper**, not a requirement. Both workflows are fully supported and documented. If the script doesn't work for your setup, the manual workflow will always work.

**Cleanup:** Both workflows use the same cleanup process - see [Understanding Git Worktrees](#understanding-git-worktrees) below for cleanup instructions.

---

## Understanding Git Worktrees

**New to git worktrees?** This section explains what they are and why we use them.

### What's a Git Worktree?

A worktree lets you check out multiple branches simultaneously in different directories. Instead of switching branches with `git checkout`, you have multiple copies of your repo, each on a different branch, all sharing the same git history.

**Normal Git:**
```
my-repo/  (on main branch)
# To work on feature: git checkout feature-branch
# Can't work on multiple branches simultaneously
```

**With Worktrees:**
```
my-repo/                           (main branch)
my-repo-maintainability/           (maintainability-impl branch)
my-repo-performance/               (performance-impl branch)
my-repo-robustness/                (robustness-impl branch)
# Work on all branches simultaneously!
```

### Why Worktrees for Referee Pattern?

The Referee Pattern needs three agents working in parallel. Worktrees provide:

✅ **Isolation** - Each agent has its own workspace, no conflicts
✅ **Parallel Work** - All agents can work simultaneously
✅ **Easy Comparison** - Open all implementations side-by-side
✅ **Git Integration** - All changes tracked in branches
✅ **Clean Merging** - Compare and merge systematically

**Alternative: Why not just branches?**
You could use branches, but you'd need to:
- Constantly switch between branches (`git checkout`)
- Can't compare implementations side-by-side easily
- Risk mixing up which branch you're on
- Can't work in parallel (agents would conflict)

### Common Worktree Errors

**Error: `fatal: '../referee-pattern-maintainability' already exists`**

This means a previous worktree wasn't cleaned up.

```bash
# Solution: Remove the directory and try again
rm -rf ../referee-pattern-maintainability
git worktree add -b maintainability-impl ../referee-pattern-maintainability

# Or use the cleanup script (see below)
./cleanup-worktrees.sh
```

**Error: `fatal: 'maintainability-impl' is already checked out`**

The branch exists in another worktree.

```bash
# Solution 1: List all worktrees to find where it's checked out
git worktree list

# Solution 2: Remove that worktree first
git worktree remove ../referee-pattern-maintainability

# Solution 3: Delete the branch if you want to start fresh
git branch -D maintainability-impl
```

**Error: `fatal: invalid reference: maintainability-impl`**

The branch doesn't exist yet but you're trying to check it out.

```bash
# Solution: Use -b flag to create the branch
git worktree add -b maintainability-impl ../referee-pattern-maintainability
```

### Worktree Cheat Sheet

```bash
# Create worktree with new branch
git worktree add -b <branch-name> <path>

# Create worktree from existing branch
git worktree add <path> <existing-branch>

# List all worktrees
git worktree list

# Remove worktree
git worktree remove <path>

# Remove worktree forcefully (if it has uncommitted changes)
git worktree remove <path> --force

# Clean up stale worktrees
git worktree prune

# Move a worktree
git worktree move <old-path> <new-path>
```

### Cleanup Script

To clean up all worktrees created by this pattern, use the cleanup script:

```bash
./cleanup-worktrees.sh
```

Or manually:

```bash
# Remove worktrees
git worktree remove ../referee-pattern-maintainability --force
git worktree remove ../referee-pattern-performance --force
git worktree remove ../referee-pattern-robustness --force

# Remove branches (optional - only if you want to start fresh)
git branch -D maintainability-impl
git branch -D performance-impl
git branch -D robustness-impl
```

### FAQ

**Q: Do worktrees use more disk space?**
A: Slightly. They share the `.git` directory, so only working files are duplicated. For this project, that's minimal (~few KB per worktree).

**Q: Can I commit from worktrees?**
A: Yes! Each worktree is a full git repository. Commits go to that worktree's branch.

**Q: What happens if I delete a worktree directory manually?**
A: Git still thinks it exists. Run `git worktree prune` to clean up git's references.

**Q: Can worktrees be on different branches of the same repo?**
A: Yes! That's exactly what we do in the Referee Pattern.

**Q: Do I need to create worktrees, or can I use branches?**
A: Worktrees are recommended but not required. You could use branches with `git checkout`, but:
- You'd need to switch constantly
- Can't compare implementations easily
- Agents can't work in parallel
- More prone to mistakes (forgetting which branch you're on)

**Q: Where should I create worktrees?**
A: The convention is to create them as sibling directories:
```
projects/
├── referee-pattern/                    (main repo)
├── referee-pattern-maintainability/    (worktree)
├── referee-pattern-performance/        (worktree)
└── referee-pattern-robustness/         (worktree)
```

This keeps them close but separate.

---

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
├── features/            # BDD specifications
│   ├── calculator.feature
│   └── steps/
│       └── calculator_steps.py  # TODO: Implement these!
└── PATTERN.md          # Detailed pattern explanation
```

## The Challenge: Calculator Implementation

This template includes a feature spec for a simple calculator - your agents will implement it using the referee pattern.

**The Problem:** Build a calculator that handles basic arithmetic (add, subtract, multiply, divide) and division by zero errors.

**Your Task:**
1. Run the workflow script: `./run-referee-pattern.sh`
2. Three specialized agents will independently implement the calculator:
   - **Maintainability agent** - Clean architecture, SOLID principles
   - **Performance agent** - Speed and memory efficiency
   - **Robustness agent** - Error handling and edge cases
3. Review the different implementations
4. Merge the best approaches into your main branch (see [MERGE_GUIDE.md](./MERGE_GUIDE.md))

**Success Criteria:** All tests pass: 5 scenarios, 15 steps ✅

**See [SUCCESS_CRITERIA.md](./SUCCESS_CRITERIA.md) for complete checklist and verification steps.**

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

### Core Documentation
- [PATTERN.md](./PATTERN.md) - Detailed explanation of the referee pattern
- [MERGE_GUIDE.md](./MERGE_GUIDE.md) - **Step-by-step guide for merging implementations**
- [AGENT_USAGE_GUIDE.md](./AGENT_USAGE_GUIDE.md) - **How to use specialized agents with template prompts**
- [SUCCESS_CRITERIA.md](./SUCCESS_CRITERIA.md) - **Completion checklist and verification steps**
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - **Common issues and solutions**

### Example Implementations
- [examples/](./examples/) - **Reference merge implementations with rationale**
  - [Strategy A: Architectural Base](./examples/merge-strategies/strategy-a/) - Maintainability-first with performance features
  - [Strategy B: Performance Core](./examples/merge-strategies/strategy-b/) - Speed-first with essential safety
  - [Strategy C: Balanced Synthesis](./examples/merge-strategies/strategy-c/) - Pragmatic middle ground
  - [STRATEGY_COMPARISON.md](./examples/STRATEGY_COMPARISON.md) - **Choose the right strategy for your context**

### Additional Resources
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
