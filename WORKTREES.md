# Understanding Git Worktrees

This guide explains git worktrees and how they enable the Referee Pattern workflow.

---

## What's a Git Worktree?

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

---

## Why Worktrees for Referee Pattern?

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

---

## Common Worktree Errors

### Error: `fatal: '../referee-pattern-maintainability' already exists`

This means a previous worktree wasn't cleaned up.

```bash
# Solution: Remove the directory and try again
rm -rf ../referee-pattern-maintainability
git worktree add -b maintainability-impl ../referee-pattern-maintainability
```

### Error: `fatal: 'maintainability-impl' is already checked out`

The branch exists in another worktree.

```bash
# Solution 1: List all worktrees to find where it's checked out
git worktree list

# Solution 2: Remove that worktree first
git worktree remove ../referee-pattern-maintainability

# Solution 3: Delete the branch if you want to start fresh
git branch -D maintainability-impl
```

### Error: `fatal: invalid reference: maintainability-impl`

The branch doesn't exist yet but you're trying to check it out.

```bash
# Solution: Use -b flag to create the branch
git worktree add -b maintainability-impl ../referee-pattern-maintainability
```

---

## Worktree Cheat Sheet

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

---

## Cleanup After Completion

To clean up worktrees created during the Referee Pattern:

```bash
# Remove worktrees
git worktree remove ../referee-pattern-maintainability --force
git worktree remove ../referee-pattern-performance --force
git worktree remove ../referee-pattern-robustness --force

# Remove branches (optional - only if you want to start fresh)
git branch -D maintainability-impl
git branch -D performance-impl
git branch -D robustness-impl

# Clean up any stale references
git worktree prune
```

---

## FAQ

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

## Visual Guide

For visual diagrams of worktree operations, see:
- [VISUAL_GUIDE.md](./VISUAL_GUIDE.md#git-worktree-operations) - Git Worktree Operations flowchart

---

## Learn More

- [Git Worktrees Official Documentation](https://git-scm.com/docs/git-worktree)
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md#git-worktree-issues) - Solutions to worktree problems

---

**Note:** Claude Code handles worktree creation automatically when you use the Referee Pattern workflow. This guide is for understanding what's happening behind the scenes and for manual troubleshooting.
