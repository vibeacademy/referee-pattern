# Working with Specialized Agents

This guide shows you how to use specialized Claude Code agents to implement features in the Referee Pattern.

---

## The Specialized Agents

The `.claude/agents/` directory contains 6 specialized code review agents:

1. **maintainability** - Clean architecture, SOLID principles, extensibility
2. **performance** - Speed, memory efficiency, algorithmic optimization
3. **robustness** - Error handling, edge cases, defensive programming
4. **readability** - Code clarity, documentation, naming
5. **security** - Vulnerabilities, input validation, secure practices
6. **testing** - Test coverage, test quality, testability

**For the Referee Pattern, use the first three** (maintainability, performance, robustness).

---

## Method 1: Using Claude Code with Task Tool (Recommended)

From your main directory, ask Claude Code to launch agents in parallel:

```bash
cd /path/to/referee-pattern
claude code
```

Then describe what you want:

> "I need you to use the Task tool to launch three agents in parallel:
>
> 1. Maintainability agent in ../referee-pattern-maintainability worktree
> 2. Performance agent in ../referee-pattern-performance worktree
> 3. Robustness agent in ../referee-pattern-robustness worktree
>
> Each should implement the calculator feature from features/calculator.feature
> and run 'uv run behave' to verify tests pass."

---

## Method 2: Sequential per-worktree

Work with each agent one at a time:

```bash
# Terminal 1: Maintainability
cd ../referee-pattern-maintainability
claude code
```

**Prompt to use:**
```
Implement the calculator feature following the BDD specifications in
features/calculator.feature.

Focus on MAINTAINABILITY:
- Clean architecture with separation of concerns
- SOLID principles (especially Open/Closed for future operations)
- Strategy Pattern for extensibility
- Well-documented with type hints
- Multiple small, focused modules

After implementing, run 'uv run behave' to verify all tests pass.

Create an IMPLEMENTATION_SUMMARY.md documenting your architectural
decisions and why they promote maintainability.
```

Repeat for Performance and Robustness agents in their respective worktrees.

---

## Template Prompts

Copy and customize these prompts for each agent:

### For Maintainability Agent

```
Implement the calculator feature focusing on long-term maintainability:
- Modular design with clear separation of concerns
- SOLID principles (especially Open/Closed for extensions)
- Strategy pattern for operations
- Comprehensive documentation and type hints
- Multiple small files over one large file

Run 'uv run behave' when done and document your design decisions.
```

---

### For Performance Agent

```
Implement the calculator feature focusing on performance optimization:
- Memory efficiency (use __slots__, avoid unnecessary objects)
- Algorithmic efficiency (O(1) operations where possible)
- Minimal abstraction overhead
- Type hints for speed
- Direct operations without indirection

Run 'uv run behave' when done and document your optimizations.
```

---

### For Robustness Agent

```
Implement the calculator feature focusing on production robustness:
- Comprehensive error handling with custom exceptions
- Input validation and type checking
- Defensive programming (guards, assertions)
- Edge case handling
- Clear, actionable error messages

Run 'uv run behave' when done and document your defensive strategies.
```

---

## What to Expect

Each agent will:
1. ✅ Read the BDD specifications
2. ✅ Design an architecture aligned with their focus
3. ✅ Implement the feature in their style
4. ✅ Run tests to verify correctness (**all should pass!**)
5. ✅ Document their approach and key decisions

**All implementations should pass the same tests** - they're functionally equivalent but architecturally different.

---

## Troubleshooting Agent Issues

### Agent doesn't follow the focus

**Problem:** Agent implements generic code instead of focusing on their specialty.

**Solution:**
- Be more explicit in your prompt about the single focus area
- Reference the agent configuration in `.claude/agents/`
- Give examples of what you want (e.g., "Use Strategy pattern for operations")
- Emphasize the quality attribute: "ONLY focus on maintainability, not performance"

---

### Agent modifies wrong files

**Problem:** Agent edits files in the wrong worktree or main branch.

**Solution:**
- Ensure you're in the correct worktree directory
- Check with `pwd` and `git branch` before starting
- Re-navigate to the correct worktree
- Start a fresh Claude Code session in the right directory

---

### Tests fail

**Problem:** Agent's implementation doesn't pass the BDD tests.

**Solution:**
- Agent may have misunderstood specifications
- Review the BDD feature file together with the agent
- Ask agent to debug why tests are failing
- Request agent to fix failing tests before completing
- If stuck, try a different approach or reset and start over

---

### Agent produces too simple/complex code

**Problem:** Code doesn't match expected complexity for the focus area.

**Solution:**
- Adjust your prompt to specify desired complexity level
- Show examples of the complexity you want
- Ask for specific patterns or architectures
- For maintainability: "Use multiple modules, Strategy pattern"
- For performance: "Single file, minimize abstractions"
- For robustness: "Comprehensive error handling, extensive validation"

---

## Tips for Success

1. **Be specific in prompts** - Generic prompts get generic results
2. **Verify worktree before starting** - Run `pwd` and `git branch`
3. **Let agents complete fully** - Don't interrupt mid-implementation
4. **Review before moving on** - Check tests pass, review code quality
5. **Document as you go** - Have agents create summary files
6. **Compare implementations** - Open all three side-by-side to see differences

---

## Next Steps

After all three agents complete their implementations:

1. **Verify all pass tests** - All three should show 100% pass rate
2. **Review implementations** - Understand what each agent did differently
3. **Use merge-critic agent** - Get automated analysis and recommendations
4. **Follow MERGE_GUIDE.md** - Systematically merge the best aspects
5. **Document decisions** - Create MERGE_DECISIONS.md

See [MERGE_GUIDE.md](./MERGE_GUIDE.md) for detailed merge instructions.

---

**Ready to start?** Choose your method (parallel or sequential) and begin implementing!
