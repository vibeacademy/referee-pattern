#!/bin/bash

# Referee Pattern Demonstration Script
# This script automates the workflow of running multiple specialized agents
# in parallel using git worktrees, then comparing their implementations.

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Print colored message
print_msg() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

print_header() {
    echo ""
    print_msg "$BLUE" "=========================================="
    print_msg "$BLUE" "$1"
    print_msg "$BLUE" "=========================================="
    echo ""
}

print_step() {
    print_msg "$GREEN" "✓ $1"
}

print_info() {
    print_msg "$YELLOW" "ℹ $1"
}

print_error() {
    print_msg "$RED" "✗ $1"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"

    if ! command -v uv &> /dev/null; then
        print_error "uv is not installed. Install it from: https://docs.astral.sh/uv/"
        exit 1
    fi
    print_step "uv is installed"

    if ! command -v git &> /dev/null; then
        print_error "git is not installed"
        exit 1
    fi
    print_step "git is installed"

    if [ -z "$ANTHROPIC_API_KEY" ]; then
        print_error "ANTHROPIC_API_KEY environment variable is not set"
        print_info "Set it with: export ANTHROPIC_API_KEY='your-key-here'"
        print_info "Or add to your ~/.zshrc or ~/.bashrc"
        exit 1
    fi
    print_step "ANTHROPIC_API_KEY is set"
}

# Initialize the project
init_project() {
    print_header "Initializing Project"

    if [ ! -d ".venv" ]; then
        print_info "Installing dependencies with uv..."
        uv sync
        print_step "Dependencies installed"
    else
        print_step "Virtual environment already exists"
    fi

    # Verify test infrastructure is working
    print_info "Verifying test infrastructure..."
    if uv run behave --dry-run > /dev/null 2>&1; then
        print_step "Test infrastructure is ready (5 scenarios, 15 steps)"
        print_info "Tests will fail until agents implement the calculator"
    else
        print_error "Test infrastructure has errors. Please check features/calculator.feature"
        exit 1
    fi
}

# Clean up existing worktrees
cleanup_worktrees() {
    print_header "Cleaning Up Old Worktrees"

    # Remove worktrees using git worktree list
    for worktree in maintainability performance robustness; do
        local worktree_path="../referee-pattern-${worktree}"

        # Check if worktree is registered with git
        if git worktree list | grep -q "${worktree_path}"; then
            print_info "Removing git worktree: ${worktree}..."
            git worktree remove "${worktree_path}" --force 2>/dev/null || true
        fi

        # Also remove directory if it still exists (handles orphaned directories)
        if [ -d "${worktree_path}" ]; then
            print_info "Removing orphaned directory: ${worktree_path}..."
            rm -rf "${worktree_path}" 2>/dev/null || true
        fi
    done

    # Delete branches
    for branch in maintainability-calc performance-calc robustness-calc; do
        if git show-ref --verify --quiet refs/heads/${branch}; then
            print_info "Deleting branch: ${branch}..."
            git branch -D ${branch} 2>/dev/null || true
        fi
    done

    # Prune any stale worktree administrative data
    git worktree prune 2>/dev/null || true

    print_step "Cleanup complete"
}

# Create worktrees for parallel development
create_worktrees() {
    print_header "Creating Git Worktrees"

    print_info "Creating worktree for maintainability agent..."
    git worktree add -b maintainability-calc ../referee-pattern-maintainability
    print_step "Maintainability worktree created at ../referee-pattern-maintainability"

    print_info "Creating worktree for performance agent..."
    git worktree add -b performance-calc ../referee-pattern-performance
    print_step "Performance worktree created at ../referee-pattern-performance"

    print_info "Creating worktree for robustness agent..."
    git worktree add -b robustness-calc ../referee-pattern-robustness
    print_step "Robustness worktree created at ../referee-pattern-robustness"

    echo ""
    print_info "All worktrees created successfully!"
    print_info "Each worktree is a separate directory where agents will work independently."
}

# Show next steps
show_next_steps() {
    print_header "Next Steps"

    echo "The worktrees are ready for the agents to implement the calculator feature."
    echo ""
    echo "To proceed, you would typically:"
    echo ""
    print_msg "$YELLOW" "1. Navigate to each worktree and use Claude Code to implement:"
    echo "   cd ../referee-pattern-maintainability"
    echo "   claude-code  # Then ask Claude to implement from maintainability perspective"
    echo ""
    print_msg "$YELLOW" "2. Or use the Task tool to run agents programmatically"
    echo ""
    print_msg "$YELLOW" "3. Once all implementations are complete:"
    echo "   - Compare the implementations in each worktree"
    echo "   - Merge the best approaches back to main"
    echo "   - Run tests to verify: uv run behave"
    echo ""
    print_msg "$GREEN" "Success criteria: All tests pass (5 scenarios, 15 steps)"
    echo ""
    print_info "Read PATTERN.md for detailed explanation of the workflow."
}

# Main execution
main() {
    print_header "Referee Pattern Demo Setup"
    echo "This script will set up the environment for demonstrating the Referee Pattern."
    echo ""

    check_prerequisites
    init_project
    cleanup_worktrees
    create_worktrees
    show_next_steps

    print_header "Setup Complete!"
    print_step "The repository is ready for the Referee Pattern workflow."
}

# Run main function
main
