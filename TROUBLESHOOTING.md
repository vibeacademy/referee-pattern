# Troubleshooting Guide

This guide helps you resolve common issues when using the Referee Pattern.

---

## Table of Contents

1. [Git Worktree Issues](#git-worktree-issues)
2. [Test Failures](#test-failures)
3. [Agent Issues](#agent-issues)
4. [Merge Problems](#merge-problems)
5. [Environment Setup](#environment-setup)
6. [Getting Help](#getting-help)

---

## Git Worktree Issues

### Issue: "fatal: '../referee-pattern-maintainability' already exists"

**Symptom:** When trying to create a worktree, git reports the directory already exists.

**Cause:** A previous worktree wasn't cleaned up properly, or the directory exists from a failed attempt.

**Solution:**

```bash
# Remove the directory and try again
rm -rf ../referee-pattern-maintainability
git worktree add -b maintainability-impl ../referee-pattern-maintainability

# Or clean up stale worktree references first
git worktree prune
```

**Prevention:** Use `git worktree prune` to clean up stale references before creating new worktrees.

---

### Issue: "fatal: 'maintainability-impl' is already checked out"

**Symptom:** Git won't create a worktree because the branch is already in use.

**Cause:** The branch is checked out in another worktree.

**Solution:**

```bash
# Step 1: Find where it's checked out
git worktree list

# Step 2: Remove the existing worktree
git worktree remove ../referee-pattern-maintainability

# Step 3: If that fails, force remove
git worktree remove ../referee-pattern-maintainability --force

# Step 4: Clean up the branch if needed
git branch -D maintainability-impl

# Step 5: Recreate
git worktree add -b maintainability-impl ../referee-pattern-maintainability
```

**Prevention:** Use `git worktree list` before creating worktrees to check current state.

---

### Issue: "fatal: invalid reference: maintainability-impl"

**Symptom:** Git can't find the branch you're trying to check out.

**Cause:** The branch doesn't exist yet, but you didn't use the `-b` flag to create it.

**Solution:**

```bash
# Use -b flag to create the branch
git worktree add -b maintainability-impl ../referee-pattern-maintainability
```

**Prevention:** Always use `-b` flag when creating new worktrees for the Referee Pattern.

---

### Issue: Can't remove worktree - "worktree contains modified or untracked files"

**Symptom:** `git worktree remove` fails because of uncommitted changes.

**Cause:** The worktree has modifications that haven't been committed.

**Solution:**

```bash
# Option 1: Force remove (loses changes)
git worktree remove ../referee-pattern-maintainability --force

# Option 2: Commit changes first
cd ../referee-pattern-maintainability
git add .
git commit -m "Save work before removing worktree"
cd ../referee-pattern
git worktree remove ../referee-pattern-maintainability

# Option 3: Save changes to stash
cd ../referee-pattern-maintainability
git stash
cd ../referee-pattern
git worktree remove ../referee-pattern-maintainability
```

**When to use each:**
- Force remove if you don't need the changes
- Commit if you want to keep the work
- Stash if you might need it later

---

### Issue: Worktree directory deleted manually but git still thinks it exists

**Symptom:** `git worktree list` shows a worktree that doesn't exist on disk.

**Cause:** Directory was deleted without telling git.

**Solution:**

```bash
# Clean up stale worktree references
git worktree prune

# Verify it's gone
git worktree list
```

**Prevention:** Always use `git worktree remove` instead of manually deleting directories.

---

## Test Failures

### Issue: "ImportError: No module named 'behave'"

**Symptom:** Tests fail with module not found error.

**Cause:** Python environment not set up or dependencies not installed.

**Solution:**

```bash
# Ensure you're in the project directory
cd /path/to/referee-pattern

# Initialize Python environment
uv sync

# Try tests again
uv run behave
```

**Prevention:** Always run `uv sync` after cloning or switching worktrees.

---

### Issue: "No steps directory found"

**Symptom:** Behave can't find step definitions.

**Cause:** Running tests from wrong directory or step files missing.

**Solution:**

```bash
# Check you're in the correct directory
pwd
# Should be: /path/to/referee-pattern (or a worktree)

# Check if steps directory exists
ls features/steps/

# If missing, you need to implement them
# See AGENT_USAGE_GUIDE.md for how to have agents implement them
```

**Prevention:** Always run tests from the project root directory.

---

### Issue: Tests pass in one worktree but fail in another

**Symptom:** Same test suite gives different results in different worktrees.

**Cause:** Different implementations, possibly with bugs.

**Solution:**

```bash
# In the failing worktree
cd ../referee-pattern-[name]

# Check what the actual error is
uv run behave --verbose

# Debug the specific failure
# Review the implementation vs the BDD specification
# Fix the code to match the specification

# Re-run tests
uv run behave
```

**This is expected!** Different implementations might have bugs. The point is all three should pass when complete.

---

### Issue: "AssertionError" in step definitions

**Symptom:** Tests fail with assertion errors.

**Cause:** Implementation doesn't match expected behavior.

**Solution:**

```bash
# Read the failure message carefully
uv run behave

# Example failure:
# AssertionError: expected 8, got 7

# This means your implementation has a logic bug
# Review the code and fix the calculation/logic

# Common issues:
# - Off-by-one errors
# - Wrong operation used
# - Missing edge case handling
```

**Debugging tips:**
1. Add print statements to see actual values
2. Review the step definition to understand what's being tested
3. Check the implementation logic carefully
4. Test the operation manually in Python REPL

---

### Issue: "ZeroDivisionError: division by zero"

**Symptom:** Test fails with division by zero error.

**Cause:** Your implementation doesn't handle division by zero properly.

**Solution:**

```python
# Your code should raise a custom exception, not let Python's default error through

# Bad:
def divide(self, a, b):
    return a / b  # Will raise ZeroDivisionError

# Good:
def divide(self, a, b):
    if b == 0:
        raise DivisionByZeroError(f"Cannot divide {a} by zero")
    return a / b
```

**Prevention:** Always validate inputs for edge cases like division by zero.

---

## Agent Issues

### Issue: Agent doesn't focus on assigned quality attribute

**Symptom:** Maintainability agent creates performance-focused code, or vice versa.

**Cause:** Prompt is too generic or agent misunderstood focus.

**Solution:**

```
# Be very explicit in your prompt:
Implement the calculator feature focusing ONLY on maintainability.

DO focus on:
- Modular design with multiple files
- SOLID principles
- Strategy pattern for operations
- Comprehensive documentation

DO NOT focus on:
- Performance optimizations
- Memory efficiency
- Speed

Your goal is clean, maintainable, extensible code.
Run 'uv run behave' when done.
```

**Key:** Use "DO focus on" and "DO NOT focus on" lists.

---

### Issue: Agent modifies files in wrong directory

**Symptom:** Agent edits main branch instead of worktree, or wrong worktree.

**Cause:** Not in the correct worktree directory when starting.

**Solution:**

```bash
# Always verify before starting agent:
pwd
# Should show: /path/to/../referee-pattern-maintainability (or similar)

git branch
# Should show: * maintainability-impl (or similar)

# If wrong directory:
cd ../referee-pattern-maintainability
claude code  # Start fresh session in correct directory
```

**Prevention:**
- Check `pwd` before starting Claude Code
- Check `git branch` to confirm you're on the right branch
- Close and reopen Claude Code in the correct directory if needed

---

### Issue: Agent implementation fails all tests

**Symptom:** Agent creates code but none of the tests pass.

**Cause:** Agent misunderstood the specifications or made logic errors.

**Solution:**

1. **Review with agent:**
   ```
   The tests are failing. Let's debug this together.

   Run: uv run behave --verbose

   Read the feature file: features/calculator.feature

   Compare your implementation to the specifications.
   What did you implement differently?
   ```

2. **If agent still struggles:**
   ```
   Let's start over with a simpler approach:

   1. Implement just the Calculator class with add() method
   2. Run tests - verify add() works
   3. Then implement subtract()
   4. Run tests again
   5. Continue one operation at a time
   ```

3. **Last resort:**
   - Review the BDD feature file yourself
   - Understand what's required
   - Give agent very specific implementation instructions
   - Or start fresh with a different agent approach

**Prevention:** Ask agent to run tests after each method implementation, not just at the end.

---

### Issue: Agent code is too simple/generic

**Symptom:** Agent creates basic code that doesn't showcase their specialty.

**Cause:** Prompt didn't specify desired complexity or patterns.

**Solution:**

```
# For maintainability agent:
I need a more sophisticated implementation showing maintainability best practices.

Please use:
- Strategy Pattern for operations (separate Operation classes)
- Multiple modules (exceptions.py, operations.py, calculator.py)
- Comprehensive type hints
- Detailed docstrings
- Clear separation of concerns

Show me maintainability-focused architecture, not just working code.
```

**For each agent type:**
- **Maintainability:** Request specific patterns (Strategy, Factory, etc.)
- **Performance:** Request specific optimizations (__slots__, caching, etc.)
- **Robustness:** Request specific defensive features (validation, logging, etc.)

---

### Issue: Agent creates overly complex code

**Symptom:** Agent adds unnecessary abstraction or features.

**Cause:** Agent over-interpreted the focus area.

**Solution:**

```
The implementation is too complex. Let's simplify.

For a calculator with 4 operations, we don't need:
- Abstract factories
- Complex inheritance hierarchies
- Multiple layers of indirection

Please simplify while keeping the [quality attribute] focus.
Keep it proportional to the problem size.
```

**Balance:** The pattern is about different approaches, not maximum complexity.

---

## Merge Problems

### Issue: Can't decide which implementation to use as base

**Symptom:** All three implementations seem equally good or equally flawed.

**Cause:** Unclear evaluation criteria.

**Solution:**

1. **Use the merge-critic agent:**
   ```bash
   claude code
   # "Analyze the three implementations in my worktrees and recommend a merge strategy"
   ```

2. **Use decision framework:**
   - **Default:** Start with maintainability as base (easiest to extend)
   - **If simple project:** Use performance as base (minimal abstraction)
   - **If critical system:** Use robustness as base (maximum safety)

3. **Create comparison table:**
   | Aspect | Maint. | Perf. | Robust. |
   |--------|--------|-------|---------|
   | LOC    | 250    | 100   | 500     |
   | Files  | 4      | 1     | 1       |
   | Tests  | ✅     | ✅    | ✅      |

   Pick the one that best fits your project needs.

**When in doubt:** Choose maintainability. You can always optimize later.

---

### Issue: Tests fail after merging

**Symptom:** Individual implementations pass tests, but merged code fails.

**Cause:** Merge introduced bugs or incompatibilities.

**Solution:**

```bash
# Step 1: Identify what broke
uv run behave --verbose
# Note which specific test fails

# Step 2: Compare to working implementation
# Open the original implementation that worked
code ../referee-pattern-maintainability/src/

# Step 3: Find the difference
# What did you change in the merge that broke it?

# Step 4: Fix incrementally
# Revert the problematic change
# Test again
# Try a different merge approach

# Step 5: Use git
git diff HEAD~1  # See what changed
git checkout -- <file>  # Revert specific file if needed
```

**Prevention:**
- Merge incrementally (one file/feature at a time)
- Test after each merge step
- Commit frequently so you can revert easily

---

### Issue: Merged code is worse than any single implementation

**Symptom:** Final code is more complex, slower, or harder to read than the originals.

**Cause:** Trying to merge everything instead of being selective.

**Solution:**

**Stop and reassess:**

1. **Is merging adding value?**
   - If one implementation is clearly best, use it as-is
   - The pattern's goal is to create something BETTER, not just different

2. **Are you being selective enough?**
   - You don't have to merge everything
   - Skip features that add complexity without benefit
   - Example: Skip thread locks if single-threaded, skip extensive logging if not production

3. **Start over with clearer strategy:**
   - Review MERGE_GUIDE.md decision frameworks
   - Pick ONE base implementation
   - Add only 2-3 specific features from others
   - Keep it simple

**Remember:** Simpler is often better. Don't over-engineer the merge.

---

### Issue: Can't integrate different architectures

**Symptom:** One uses classes, another uses functions; structures are incompatible.

**Cause:** Implementations took very different approaches.

**Solution:**

**Option 1: Choose one architecture**
- Pick the architecture you prefer
- Rebuild the other features within that architecture
- Don't try to force incompatible structures together

**Option 2: Take techniques, not code**
- From performance: Use \_\_slots\_\_ and type hints (technique)
- From robustness: Use exception hierarchy (technique)
- Don't copy-paste code, apply techniques to your chosen architecture

**Option 3: Use one implementation**
- If architectures are too different, just pick the best one
- Document what you learned from the others
- That's still valuable!

**The pattern is about learning, not forcing a merge.**

---

## Environment Setup

### Issue: "uv: command not found"

**Symptom:** The `uv` command doesn't work.

**Cause:** UV not installed.

**Solution:**

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv

# Or with homebrew (Mac)
brew install uv

# Verify installation
uv --version
```

---

### Issue: "ANTHROPIC_API_KEY not set"

**Symptom:** Claude Code can't connect because API key is missing.

**Cause:** Environment variable not configured.

**Solution:**

```bash
# Option 1: Set for current session
export ANTHROPIC_API_KEY="your-api-key-here"

# Option 2: Add to shell profile (permanent)
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc

# Verify it's set
echo $ANTHROPIC_API_KEY
```

**Prevention:** Add to shell profile so it persists across sessions.

---

### Issue: Python version incompatibility

**Symptom:** UV or tests fail due to Python version.

**Cause:** Project requires specific Python version.

**Solution:**

```bash
# Check current Python version
python --version

# Check project requirements
cat pyproject.toml | grep "python"

# Use UV to manage Python version
uv python install 3.11  # Or whatever version is required
uv venv --python 3.11

# Verify
uv run python --version
```

---

## Getting Help

### Before Asking for Help

Collect this information:

1. **What you were trying to do:**
   - Step in the workflow
   - Command you ran
   - Expected result

2. **What actually happened:**
   - Error message (full text)
   - Unexpected behavior
   - Screenshot if relevant

3. **Your environment:**
   ```bash
   # Run these and include output:
   pwd
   git status
   git worktree list
   uv --version
   python --version
   ```

4. **What you've tried:**
   - Solutions you attempted
   - Results of those attempts

### Where to Get Help

1. **Check this guide first** - Most issues are covered here

2. **Review documentation:**
   - [README.md](./README.md)
   - [MERGE_GUIDE.md](./MERGE_GUIDE.md)
   - [AGENT_USAGE_GUIDE.md](./AGENT_USAGE_GUIDE.md)
   - [SUCCESS_CRITERIA.md](./SUCCESS_CRITERIA.md)

3. **Use Claude Code itself:**
   ```
   "I'm having trouble with [specific issue].
   Here's what I tried: [attempts]
   Here's the error: [error message]
   Can you help me debug this?"
   ```

4. **GitHub Issues:**
   - https://github.com/vibeacademy/referee-pattern/issues
   - Search existing issues first
   - Create new issue with all info above

### How to Ask Good Questions

**Bad question:**
> "It doesn't work. Help!"

**Good question:**
> "I'm trying to create the maintainability worktree (step 3 of manual workflow). When I run `git worktree add -b maintainability-impl ../referee-pattern-maintainability`, I get error: 'fatal: '../referee-pattern-maintainability' already exists'.
>
> I tried removing the directory with `rm -rf` and running again, but got the same error.
>
> Environment:
> - macOS 14.2
> - git version 2.39.0
> - Currently on main branch
> - `git worktree list` shows only main worktree
>
> What am I missing?"

**What makes it good:**
- Specific step being attempted
- Exact command run
- Exact error message
- What was tried already
- Environment details
- Clear question

---

## Quick Troubleshooting Checklist

When something goes wrong, check these first:

- [ ] Am I in the correct directory? (`pwd`)
- [ ] Am I on the correct branch? (`git branch`)
- [ ] Did I run `uv sync` after cloning/switching?
- [ ] Are all dependencies installed?
- [ ] Did I read the error message completely?
- [ ] Have I checked this troubleshooting guide?
- [ ] Did I try the obvious solution first?

**Most issues are solved by:**
1. Being in the wrong directory
2. Not running `uv sync`
3. Not reading the error message carefully

---

## Preventing Issues

### Best Practices

1. **Always check your location:**
   ```bash
   pwd && git branch
   ```

2. **Test incrementally:**
   - Don't write all code then test
   - Test after each small change

3. **Clean up worktrees:**
   ```bash
   git worktree prune
   ```

4. **Commit often:**
   ```bash
   git add .
   git commit -m "Checkpoint: working state"
   ```

5. **Read error messages:**
   - They usually tell you exactly what's wrong
   - Don't just skip to searching for solutions

6. **Follow the guides:**
   - [MERGE_GUIDE.md](./MERGE_GUIDE.md) for merging
   - [AGENT_USAGE_GUIDE.md](./AGENT_USAGE_GUIDE.md) for agents
   - [SUCCESS_CRITERIA.md](./SUCCESS_CRITERIA.md) for completion

### When to Start Over

Sometimes the best solution is to start fresh:

**Signs you should start over:**
- Worktrees are in a tangled state you can't understand
- Multiple failed merge attempts
- Unsure what changes you've made
- Spent more than 30 min debugging without progress

**How to start fresh:**
```bash
# 1. Clean up worktrees
git worktree remove ../referee-pattern-maintainability --force
git worktree remove ../referee-pattern-performance --force
git worktree remove ../referee-pattern-robustness --force
git worktree prune

# 2. Remove any partial work
git checkout main
git reset --hard origin/main  # WARNING: Loses uncommitted changes

# 3. Start from beginning
# Follow README.md Quick Start

# 4. This time, commit more frequently!
```

**Don't be afraid to start over.** Often it's faster than debugging a mess.

---

## Still Stuck?

If you've:
- ✅ Checked this entire guide
- ✅ Reviewed all relevant documentation
- ✅ Tried the suggested solutions
- ✅ Collected all the information listed above

Then create a GitHub issue with all details:
https://github.com/vibeacademy/referee-pattern/issues/new

Someone will help you figure it out!

---

**Remember:** The Referee Pattern is a learning tool. Getting stuck is part of learning. Every issue you solve teaches you something about git, Python, testing, or software design.

**Keep going!** You've got this. 💪
