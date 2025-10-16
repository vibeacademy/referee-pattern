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
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
WORKTREES=("maintainability" "performance" "robustness")
BRANCH_SUFFIX="-impl"

# Flags
CLEAN_MODE=false
HELP_MODE=false
VERBOSE_MODE=false

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

print_verbose() {
    if [ "$VERBOSE_MODE" = true ]; then
        print_msg "$CYAN" "  → $1"
    fi
}

# Show help message
show_help() {
    cat << EOF
$(print_msg "$BLUE" "Referee Pattern Setup Script")

This script automates the setup of git worktrees for the Referee Pattern workflow.

$(print_msg "$YELLOW" "USAGE:")
    ./run-referee-pattern.sh [OPTIONS]

$(print_msg "$YELLOW" "OPTIONS:")
    -h, --help      Show this help message and exit
    -c, --clean     Clean up all worktrees and branches, then exit
    -v, --verbose   Show detailed output during execution
    --skip-tests    Skip test infrastructure verification

$(print_msg "$YELLOW" "EXAMPLES:")
    # Standard setup (creates worktrees if they don't exist)
    ./run-referee-pattern.sh

    # Clean up everything and start fresh
    ./run-referee-pattern.sh --clean

    # Run with detailed output
    ./run-referee-pattern.sh --verbose

    # Clean up, then set up fresh
    ./run-referee-pattern.sh --clean && ./run-referee-pattern.sh

$(print_msg "$YELLOW" "WORKTREES CREATED:")
    ../referee-pattern-maintainability  (maintainability-impl branch)
    ../referee-pattern-performance      (performance-impl branch)
    ../referee-pattern-robustness       (robustness-impl branch)

$(print_msg "$YELLOW" "IDEMPOTENCY:")
    This script is idempotent - safe to run multiple times.
    - Existing worktrees are detected and skipped
    - Existing branches are reused
    - No data loss from repeated runs

$(print_msg "$YELLOW" "PREREQUISITES:")
    - uv (Python package manager): https://docs.astral.sh/uv/
    - git
    - ANTHROPIC_API_KEY environment variable

$(print_msg "$YELLOW" "DOCUMENTATION:")
    - README.md: Overview and quick start
    - PATTERN.md: Detailed pattern explanation
    - AGENT_USAGE_GUIDE.md: How to use agents
    - MERGE_GUIDE.md: How to merge implementations
    - SUCCESS_CRITERIA.md: Completion checklist
    - TROUBLESHOOTING.md: Common issues and solutions

$(print_msg "$YELLOW" "GETTING HELP:")
    - GitHub Issues: https://github.com/vibeacademy/referee-pattern/issues
    - Documentation: See files above

EOF
}

# Parse command line arguments
parse_args() {
    SKIP_TESTS=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                HELP_MODE=true
                shift
                ;;
            -c|--clean)
                CLEAN_MODE=true
                shift
                ;;
            -v|--verbose)
                VERBOSE_MODE=true
                shift
                ;;
            --skip-tests)
                SKIP_TESTS=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"

    local all_good=true

    # Check uv
    if ! command -v uv &> /dev/null; then
        print_error "uv is not installed"
        print_info "Install from: https://docs.astral.sh/uv/"
        all_good=false
    else
        print_step "uv is installed ($(uv --version))"
    fi

    # Check git
    if ! command -v git &> /dev/null; then
        print_error "git is not installed"
        all_good=false
    else
        print_step "git is installed ($(git --version | head -1))"
    fi

    # Check API key
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        print_error "ANTHROPIC_API_KEY environment variable is not set"
        print_info "Set it with: export ANTHROPIC_API_KEY='your-key-here'"
        print_info "Or add to your ~/.zshrc or ~/.bashrc"
        all_good=false
    else
        print_step "ANTHROPIC_API_KEY is set"
    fi

    # Check we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "Not in a git repository"
        all_good=false
    else
        print_step "Git repository detected"
    fi

    if [ "$all_good" = false ]; then
        print_error "Prerequisites not met. Please fix the issues above."
        exit 1
    fi
}

# Initialize the project
init_project() {
    print_header "Initializing Project"

    # Check if already initialized
    if [ -d ".venv" ] && [ -f "pyproject.toml" ]; then
        print_step "Virtual environment already exists"
        print_verbose "Skipping dependency installation"
    else
        print_info "Installing dependencies with uv..."
        uv sync
        print_step "Dependencies installed"
    fi

    # Verify test infrastructure is working (unless skipped)
    if [ "$SKIP_TESTS" = false ]; then
        print_info "Verifying test infrastructure..."
        if uv run behave --dry-run > /dev/null 2>&1; then
            print_step "Test infrastructure is ready (5 scenarios, 15 steps)"
            print_verbose "Tests will fail until agents implement the calculator"
        else
            print_error "Test infrastructure has errors"
            print_info "Check features/calculator.feature"
            print_info "Or use --skip-tests to bypass this check"
            exit 1
        fi
    else
        print_verbose "Skipping test verification (--skip-tests flag)"
    fi
}

# Clean up existing worktrees
cleanup_worktrees() {
    print_header "Cleaning Up Worktrees and Branches"

    local removed_count=0

    # Remove worktrees
    for worktree in "${WORKTREES[@]}"; do
        local worktree_path="../referee-pattern-${worktree}"
        local branch_name="${worktree}${BRANCH_SUFFIX}"

        # Check if worktree is registered with git
        if git worktree list | grep -q "${worktree_path}"; then
            print_info "Removing git worktree: ${worktree}..."
            git worktree remove "${worktree_path}" --force 2>/dev/null || true
            ((removed_count++))
            print_verbose "Worktree removed: ${worktree_path}"
        fi

        # Also remove directory if it still exists (handles orphaned directories)
        if [ -d "${worktree_path}" ]; then
            print_verbose "Removing orphaned directory: ${worktree_path}..."
            rm -rf "${worktree_path}" 2>/dev/null || true
            ((removed_count++))
        fi

        # Delete branch
        if git show-ref --verify --quiet "refs/heads/${branch_name}"; then
            print_info "Deleting branch: ${branch_name}..."
            git branch -D "${branch_name}" 2>/dev/null || true
            print_verbose "Branch deleted: ${branch_name}"
        fi
    done

    # Prune any stale worktree administrative data
    git worktree prune 2>/dev/null || true

    if [ $removed_count -eq 0 ]; then
        print_step "No worktrees to clean up"
    else
        print_step "Cleanup complete (removed $removed_count items)"
    fi
}

# Create worktrees for parallel development
create_worktrees() {
    print_header "Creating Git Worktrees"

    local created_count=0
    local skipped_count=0

    for worktree in "${WORKTREES[@]}"; do
        local worktree_path="../referee-pattern-${worktree}"
        local branch_name="${worktree}${BRANCH_SUFFIX}"

        # Check if worktree already exists
        if git worktree list | grep -q "${worktree_path}"; then
            print_info "Worktree already exists: ${worktree}"
            print_verbose "Skipping creation: ${worktree_path}"
            ((skipped_count++))
            continue
        fi

        # Check if directory exists but not tracked by git (orphaned)
        if [ -d "${worktree_path}" ]; then
            print_verbose "Removing orphaned directory before creating worktree..."
            rm -rf "${worktree_path}"
        fi

        # Create worktree
        print_info "Creating worktree for ${worktree} agent..."

        # If branch exists, use it; otherwise create new
        if git show-ref --verify --quiet "refs/heads/${branch_name}"; then
            print_verbose "Branch ${branch_name} exists, checking it out..."
            git worktree add "${worktree_path}" "${branch_name}"
        else
            print_verbose "Creating new branch: ${branch_name}..."
            git worktree add -b "${branch_name}" "${worktree_path}"
        fi

        print_step "${worktree} worktree created at ${worktree_path}"
        ((created_count++))
    done

    echo ""
    if [ $created_count -eq 0 ]; then
        print_step "All worktrees already exist (idempotent - no changes made)"
        print_info "Use --clean to remove and recreate them"
    else
        print_step "Created $created_count new worktree(s)"
        if [ $skipped_count -gt 0 ]; then
            print_info "Skipped $skipped_count existing worktree(s)"
        fi
        print_info "Each worktree is a separate directory for independent agent work"
    fi
}

# Show current worktree status
show_worktree_status() {
    print_header "Worktree Status"

    echo "Current worktrees:"
    git worktree list | while read -r line; do
        print_msg "$CYAN" "  $line"
    done
    echo ""
}

# Show next steps
show_next_steps() {
    print_header "Next Steps"

    cat << EOF
The worktrees are ready for agents to implement the calculator feature.

$(print_msg "$YELLOW" "📚 Review the documentation:")
   - AGENT_USAGE_GUIDE.md: Template prompts and invocation methods
   - MERGE_GUIDE.md: How to merge implementations
   - SUCCESS_CRITERIA.md: How to know when you're done

$(print_msg "$YELLOW" "🤖 Method 1: Use Claude Code with Task Tool (Recommended)")
   cd /path/to/referee-pattern
   claude code
   # Then ask Claude to launch agents in parallel

$(print_msg "$YELLOW" "🔧 Method 2: Work with each agent sequentially")
   # Maintainability
   cd ../referee-pattern-maintainability
   claude code
   # Use template prompt from AGENT_USAGE_GUIDE.md

   # Repeat for performance and robustness

$(print_msg "$YELLOW" "✅ Verification:")
   # After each implementation
   cd ../referee-pattern-[agent-name]
   uv run behave
   # Expected: 5 scenarios passed, 0 failed

$(print_msg "$YELLOW" "🔀 Merging:")
   # Once all three pass tests
   - Review MERGE_GUIDE.md
   - Use merge-critic agent for recommendations
   - Merge best aspects to main branch
   - Document decisions in MERGE_DECISIONS.md

$(print_msg "$GREEN" "🎯 Success Criteria:")
   All tests pass on all implementations: 5 scenarios, 15 steps ✓

$(print_msg "$YELLOW" "🧹 Cleanup when done:")
   ./cleanup-worktrees.sh
   # Or: ./run-referee-pattern.sh --clean

EOF
}

# Main execution
main() {
    parse_args "$@"

    # Show help and exit
    if [ "$HELP_MODE" = true ]; then
        show_help
        exit 0
    fi

    # Clean mode: cleanup and exit
    if [ "$CLEAN_MODE" = true ]; then
        print_header "Clean Mode: Removing All Worktrees"
        check_prerequisites
        cleanup_worktrees
        print_header "Cleanup Complete!"
        print_info "Run without --clean to set up worktrees again"
        exit 0
    fi

    # Normal mode: setup
    print_header "Referee Pattern Setup"
    echo "Setting up the environment for the Referee Pattern workflow."
    echo ""
    print_info "This script is idempotent - safe to run multiple times"
    echo ""

    check_prerequisites
    init_project
    create_worktrees
    show_worktree_status
    show_next_steps

    print_header "Setup Complete!"
    print_step "The repository is ready for the Referee Pattern workflow"
    print_info "See documentation links above for next steps"
}

# Run main function
main "$@"
