#!/bin/bash
# cleanup-worktrees.sh
# Safe cleanup of Referee Pattern worktrees

set -e

echo "🧹 Cleaning up Referee Pattern worktrees..."
echo ""

# Array of worktree names
worktrees=("maintainability" "performance" "robustness" "readability" "security" "testing")

# Remove worktrees
for worktree in "${worktrees[@]}"; do
    worktree_path="../referee-pattern-${worktree}"
    if [ -d "$worktree_path" ]; then
        echo "  📁 Removing ${worktree} worktree..."
        git worktree remove "$worktree_path" --force 2>/dev/null || true
        # Also remove directory if it still exists
        rm -rf "$worktree_path" 2>/dev/null || true
    fi
done

echo ""
echo "🌿 Cleaning up branches..."

# Remove branches
for worktree in "${worktrees[@]}"; do
    branch_name="${worktree}-impl"
    if git show-ref --verify --quiet "refs/heads/${branch_name}"; then
        echo "  🔀 Removing ${branch_name} branch..."
        git branch -D "${branch_name}" 2>/dev/null || true
    fi
done

# Clean up any stale worktree references
git worktree prune 2>/dev/null || true

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📊 Current worktrees:"
git worktree list
echo ""
echo "To recreate worktrees, run: ./run-referee-pattern.sh"
