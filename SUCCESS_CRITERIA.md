# Success Criteria

Know when you've successfully completed the Referee Pattern workflow.

---

## ✅ Three Implementations Complete

- [ ] **Maintainability implementation** exists in worktree
- [ ] **Performance implementation** exists in worktree
- [ ] **Robustness implementation** exists in worktree
- [ ] **All three pass 100%** of behave tests

### Verify

Run tests in each worktree:

```bash
cd ../referee-pattern-maintainability && uv run behave
cd ../referee-pattern-performance && uv run behave
cd ../referee-pattern-robustness && uv run behave
```

**Expected output for each:**
```
5 scenarios passed, 0 failed, 0 skipped
15 steps passed, 0 failed, 0 skipped
```

If any tests fail, that implementation needs fixing before proceeding.

---

## ✅ Comparison Complete

- [ ] You've reviewed all three implementations
- [ ] You understand the trade-offs between approaches
- [ ] You've identified strengths of each implementation
- [ ] You've created a comparison matrix (see [MERGE_GUIDE.md](./MERGE_GUIDE.md))

### How to Compare

1. **Open implementations side-by-side:**
   ```bash
   code ../referee-pattern-maintainability \
        ../referee-pattern-performance \
        ../referee-pattern-robustness
   ```

2. **Note differences:**
   - File structure (single file vs multiple modules)
   - Design patterns used
   - Performance optimizations
   - Error handling approaches
   - Documentation level

3. **Create comparison notes:**
   - What makes each implementation special?
   - What did each agent prioritize?
   - Which approach resonates with you?

---

## ✅ Merge Complete

- [ ] Final implementation merged to main branch
- [ ] All tests pass on main branch (100%)
- [ ] `MERGE_DECISIONS.md` documents what was taken from each
- [ ] Code combines best aspects of all implementations

### Verify Merge

```bash
cd /path/to/referee-pattern
uv run behave
```

**Expected:**
```
5 scenarios passed, 0 failed, 0 skipped
15 steps passed, 0 failed, 0 skipped
```

### Check Merge Quality

Your merged code should:
- Be **better** than any single implementation
- Not be **worse** than the best implementation
- Combine strengths from multiple approaches
- Balance competing quality attributes

**If your merge is worse than one implementation, consider using that implementation as-is.**

---

## ✅ Learning Objectives Met

- [ ] You can explain the trade-offs between approaches
- [ ] You understand why different priorities lead to different designs
- [ ] You can articulate what you chose to merge and why
- [ ] You see the value of multiple perspectives

### Reflection Questions

**Trade-offs:**
- What did the maintainability implementation sacrifice for clean architecture?
- What did the performance implementation give up for speed?
- What did the robustness implementation add that increased complexity?

**Design Impact:**
- How did prioritizing maintainability change the code structure?
- How did optimizing for performance affect readability?
- How did adding robustness features change the implementation size?

**Merge Decisions:**
- Why did you choose the features you merged?
- What did you leave out and why?
- Would you make different choices for a different project?

**Pattern Value:**
- Did seeing multiple approaches change your perspective?
- Which implementation surprised you?
- What did you learn about software design trade-offs?

---

## Example Final Structure

Your merged solution should look something like:

```
referee-pattern/
├── src/
│   └── calculator/
│       ├── __init__.py           # Public API (from maintainability)
│       ├── exceptions.py         # Custom exceptions (from robustness)
│       ├── operations.py         # Strategy pattern (from maintainability)
│       └── calculator.py         # Main class (merged: structure from
│                                 # maintainability, __slots__ from performance)
├── features/
│   ├── calculator.feature        # BDD specifications (unchanged)
│   └── steps/
│       └── calculator_steps.py   # Your implementation
├── MERGE_DECISIONS.md            # Your merge rationale
├── MERGE_GUIDE.md                # Merge guide (reference)
├── AGENT_USAGE_GUIDE.md          # Agent usage (reference)
├── SUCCESS_CRITERIA.md           # This file
└── README.md                     # Main documentation
```

**Lines of Code Range:** Expect ~250-400 lines total for your merge (between minimal and verbose implementations).

---

## What Good Looks Like

A successful merge typically combines:

### From Maintainability
- ✅ Clean module structure (multiple files)
- ✅ Strategy pattern for operations
- ✅ Clear separation of concerns
- ✅ Extensibility for new operations
- ✅ Good documentation with docstrings

### From Performance
- ✅ `__slots__` for memory efficiency (~40% reduction)
- ✅ Type hints throughout for speed
- ✅ Direct operations where sensible
- ✅ Minimal unnecessary object creation
- ✅ O(1) operations for common cases

### From Robustness
- ✅ Custom exception hierarchy (DivisionByZeroError, etc.)
- ✅ Input validation for critical operations
- ✅ Defensive checks for edge cases
- ✅ Clear, actionable error messages
- ❌ Skip excessive logging (unless production system)
- ❌ Skip thread locks (unless multi-threaded)

### Result
Code that is:
- **Maintainable** - Easy to extend and modify
- **Performant** - Fast and memory-efficient
- **Robust** - Handles errors gracefully
- **Balanced** - No quality attribute dominates

---

## Common Pitfalls

### Pitfall 1: Merging Everything

**Problem:** Trying to include every feature from all three implementations.

**Result:** Overly complex code that's worse than any single implementation.

**Solution:** Be selective. Skip features that add complexity without value (extensive logging, thread locks for single-threaded code, etc.).

---

### Pitfall 2: Picking One Implementation

**Problem:** Just using one implementation without merging.

**Result:** Miss the point of the pattern - synthesizing multiple perspectives.

**Solution:** Even if one is great, look for at least 2-3 features to adopt from others. The value is in the synthesis.

---

### Pitfall 3: Rushed Merge

**Problem:** Merging without understanding what each implementation does.

**Result:** Inconsistent code with mixed paradigms that don't work together.

**Solution:** Take time to review all three. Use the merge-critic agent. Follow MERGE_GUIDE.md systematically.

---

### Pitfall 4: Tests Fail After Merge

**Problem:** Merge breaks functionality.

**Result:** Non-working code, wasted time.

**Solution:** Merge incrementally. Test after each change. Use git to revert if something breaks.

---

## Completion Checklist

Use this final checklist before considering the pattern complete:

### Implementation Phase
- [ ] Three worktrees created successfully
- [ ] Maintainability agent completed implementation
- [ ] Performance agent completed implementation
- [ ] Robustness agent completed implementation
- [ ] All three implementations pass 100% of tests

### Analysis Phase
- [ ] Reviewed all three implementations thoroughly
- [ ] Created comparison matrix of strengths/weaknesses
- [ ] Identified specific features to merge from each
- [ ] Used merge-critic agent for recommendations (optional but helpful)

### Merge Phase
- [ ] Followed MERGE_GUIDE.md merge strategy
- [ ] Merged incrementally with testing after each step
- [ ] All tests pass on merged code (100%)
- [ ] Code quality is better than any single implementation

### Documentation Phase
- [ ] Created MERGE_DECISIONS.md with rationale
- [ ] Documented trade-offs and choices
- [ ] Included code examples showing before/after
- [ ] Reflected on lessons learned

### Cleanup Phase
- [ ] Worktrees removed (./cleanup-worktrees.sh)
- [ ] Implementation branches cleaned up (optional)
- [ ] Final code committed to main branch
- [ ] Repository is clean and organized

---

## What If You Get Stuck?

### Stuck on Implementations

If agents aren't producing good implementations:
- Review [AGENT_USAGE_GUIDE.md](./AGENT_USAGE_GUIDE.md) for better prompts
- Check you're in the correct worktree
- Verify the BDD specifications are clear
- Try starting fresh with a clearer prompt

### Stuck on Merge

If you can't decide how to merge:
- Use the merge-critic agent for guidance
- Review [MERGE_GUIDE.md](./MERGE_GUIDE.md) decision frameworks
- Start with Strategy A (Architectural Base + Feature Adoption)
- When in doubt, favor maintainability

### Stuck on Understanding

If you don't understand the trade-offs:
- Re-read PATTERN.md for context
- Compare implementations side-by-side
- Ask yourself: "Why did this agent make this choice?"
- Focus on learning over perfection

---

## Measuring Success

### Quantitative Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Test pass rate | 100% | `uv run behave` |
| Lines of code | 250-400 | `cloc src/` |
| Implementations | 3 | Check worktrees |
| Time to complete | 1-2 hours | Track your time |

### Qualitative Metrics

| Metric | Good | Great |
|--------|------|-------|
| **Understanding** | Can explain one approach | Can explain all three + trade-offs |
| **Merge Quality** | Works, passes tests | Better than any single implementation |
| **Learning** | Completed the exercise | Changed how you think about design |
| **Documentation** | Basic MERGE_DECISIONS.md | Comprehensive rationale with examples |

---

## Next Steps After Completion

Once you've successfully completed the pattern:

1. **Apply to Real Projects**
   - Use the pattern for non-trivial features
   - Adapt to your tech stack and team

2. **Teach Others**
   - Share your MERGE_DECISIONS.md
   - Explain trade-offs you discovered
   - Help others through the pattern

3. **Expand the Pattern**
   - Try additional agents (readability, security, testing)
   - Use for architecture decisions
   - Apply to refactoring exercises

4. **Contribute Back**
   - Share interesting merge decisions
   - Suggest improvements to the template
   - Create examples for other domains

---

## Congratulations!

If you've checked all the boxes above, you've successfully completed the Referee Pattern. You now have:

✅ Three different implementations of the same feature
✅ Deep understanding of quality attribute trade-offs
✅ A merged solution combining the best aspects
✅ Documentation of your decisions and learnings
✅ Experience with a powerful code generation workflow

**Well done!** The Referee Pattern is now in your toolkit for tackling complex software design decisions.

---

**Questions or feedback?** See [README.md](./README.md) for resources and next steps.
