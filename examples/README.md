# Example Merge Implementations

This directory contains reference implementations demonstrating different merge strategies for the Referee Pattern.

## Purpose

After your three specialized agents (maintainability, performance, robustness) complete their implementations, you need to merge the best aspects. These examples show you what that looks like in practice.

## What's Included

Each example demonstrates a different merge strategy from MERGE_GUIDE.md:

### Strategy A: Architectural Base + Feature Adoption
**Directory:** `merge-strategies/strategy-a/`

Takes the maintainability implementation's architecture and selectively adds performance/robustness features.

**Best for:**
- Projects where maintainability is paramount
- Teams that will extend the code frequently
- When clean architecture justifies slight performance trade-offs

**What you'll see:**
- Multi-module structure from maintainability agent
- `__slots__` optimization from performance agent
- Custom exceptions from robustness agent
- Clear module boundaries maintained

---

### Strategy B: Performance Core + Safety Layers
**Directory:** `merge-strategies/strategy-b/`

Takes the performance implementation's efficient core and adds robustness features without sacrificing speed.

**Best for:**
- High-traffic systems where speed matters
- When you need both performance AND reliability
- Projects with clear, stable requirements

**What you'll see:**
- Minimalist architecture from performance agent
- Critical error handling from robustness agent
- Selective adoption of maintainability patterns
- Speed maintained while adding safety

---

### Strategy C: Balanced Synthesis
**Directory:** `merge-strategies/strategy-c/`

Cherry-picks the best features from all three without committing to any single architecture.

**Best for:**
- General-purpose applications
- When no single quality dominates
- Teams learning the pattern

**What you'll see:**
- Medium complexity (between minimal and maximal)
- Mix of patterns from all three agents
- Pragmatic trade-offs
- Real-world balance

---

## How to Use These Examples

### 1. Compare to Your Implementations

Open your agent implementations side-by-side with these examples:

```bash
# Your implementations
code ../referee-pattern-maintainability \
     ../referee-pattern-performance \
     ../referee-pattern-robustness

# Reference examples
code examples/
```

**Look for:**
- How structure differs between strategies
- What features were kept vs. dropped
- Why certain trade-offs were made

---

### 2. Read the RATIONALE.md Files

Each strategy directory contains `RATIONALE.md` explaining:
- Why this strategy was chosen
- What was taken from each implementation
- What was left out and why
- Trade-offs and their justification

**Start here** before looking at code.

---

### 3. Study the Before/After

Each strategy shows:
- **before/**: Snippets from the three agent implementations
- **after/**: The merged result
- **RATIONALE.md**: Detailed explanation of changes

This helps you understand the decision-making process.

---

### 4. Use as Templates

These examples are meant to inspire, not prescribe. Your merge should:
- ✅ Address your specific context
- ✅ Balance your quality priorities
- ✅ Reflect your team's values
- ❌ Not blindly copy these examples

**Adapt, don't adopt.**

---

## File Structure

```
examples/
├── README.md (this file)
├── merge-strategies/
│   ├── strategy-a/  # Architectural Base + Feature Adoption
│   │   ├── before/
│   │   │   ├── maintainability_snippet.py
│   │   │   ├── performance_snippet.py
│   │   │   └── robustness_snippet.py
│   │   ├── after/
│   │   │   ├── calculator.py
│   │   │   ├── operations.py
│   │   │   └── exceptions.py
│   │   ├── RATIONALE.md
│   │   └── comparison.md
│   ├── strategy-b/  # Performance Core + Safety Layers
│   │   ├── before/
│   │   ├── after/
│   │   ├── RATIONALE.md
│   │   └── comparison.md
│   └── strategy-c/  # Balanced Synthesis
│       ├── before/
│       ├── after/
│       ├── RATIONALE.md
│       └── comparison.md
└── complete-implementations/  # Full working examples
    ├── maintainability/
    ├── performance/
    ├── robustness/
    └── merged/
```

---

## Running the Examples

Each strategy's `after/` directory contains runnable code:

```bash
# Copy to your project
cp -r examples/merge-strategies/strategy-a/after/* .

# Run tests
uv run behave

# Expected: 5 scenarios passed, 0 failed
```

All examples pass the same BDD tests - they're functionally equivalent but architecturally different.

---

## Learning Objectives

After studying these examples, you should be able to:

1. **Identify patterns** - Recognize what each agent prioritizes
2. **Evaluate trade-offs** - Understand why certain features were kept/dropped
3. **Make decisions** - Choose which strategy fits your context
4. **Execute merges** - Apply the process to your own implementations
5. **Document rationale** - Explain your merge decisions clearly

---

## What These Examples Are NOT

❌ **Not prescriptive** - Your merge will be different, and that's good
❌ **Not exhaustive** - Infinite merge variations exist
❌ **Not production-ready** - Simplified for learning purposes
❌ **Not one-size-fits-all** - Context matters

These are teaching tools, not blueprints.

---

## Next Steps

1. **Read MERGE_GUIDE.md** - Understand the merge process
2. **Study one strategy** - Pick the one closest to your needs
3. **Compare to your code** - See how your implementations differ
4. **Use merge-critic agent** - Get personalized recommendations
5. **Create your merge** - Apply learnings to your specific case
6. **Document decisions** - Use MERGE_DECISIONS.template.md

---

## Questions?

- **"Which strategy should I use?"** - See comparison.md in each strategy directory
- **"Can I mix strategies?"** - Absolutely! These are starting points
- **"What if my code is different?"** - Good! These are examples, not requirements
- **"Should I copy this code?"** - No, understand the decisions and apply to your context

---

## Contributing

Found a helpful merge strategy not shown here? Consider contributing it back to the template!

See main README.md for contribution guidelines.

---

**Remember:** The goal isn't to produce code identical to these examples. The goal is to understand the decision-making process so you can make informed choices for your specific context.
