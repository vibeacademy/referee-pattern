#!/usr/bin/env bash
#
# run-referee-pattern.sh - Automates the Referee Pattern workflow
#
# This script creates git worktrees, runs specialized agents in parallel,
# and orchestrates the merge process.
#
# Usage:
#   ./run-referee-pattern.sh [OPTIONS]
#
# Options:
#   --help     Show this help message
#   --clean    Remove all worktrees and branches, then restart
#   --dry-run  Show what would be done without making changes
#

set -euo pipefail

# =============================================================================
# Configuration
# =============================================================================

SCRIPT_NAME="$(basename "$0")"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_NAME="$(basename "$SCRIPT_DIR")"

# Agent configurations
AGENTS=("maintainability" "performance" "robustness")
WORKTREE_PREFIX="${REPO_NAME}"

# Colors for output (disabled if not a terminal)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    MAGENTA='\033[0;35m'
    CYAN='\033[0;36m'
    BOLD='\033[1m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    MAGENTA=''
    CYAN=''
    BOLD=''
    NC=''
fi

# =============================================================================
# Helper Functions
# =============================================================================

print_header() {
    echo -e "\n${BOLD}${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${BLUE}  $1${NC}"
    echo -e "${BOLD}${BLUE}════════════════════════════════════════════════════════════════${NC}\n"
}

print_step() {
    local step_num="$1"
    local total="$2"
    local message="$3"
    echo -e "${CYAN}[${step_num}/${total}]${NC} ${BOLD}${message}${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_progress() {
    echo -e "  ${MAGENTA}→${NC} $1"
}

confirm() {
    local prompt="$1"
    local default="${2:-n}"

    if [[ "$default" == "y" ]]; then
        prompt="$prompt [Y/n] "
    else
        prompt="$prompt [y/N] "
    fi

    read -r -p "$prompt" response
    response="${response:-$default}"
    [[ "$response" =~ ^[Yy]$ ]]
}

# =============================================================================
# Validation Functions
# =============================================================================

check_prerequisites() {
    local missing=()
    local warnings=()

    if ! command -v git &> /dev/null; then
        missing+=("git")
    fi

    # Check for claude - it may be an alias or in a non-standard location
    if ! command -v claude &> /dev/null && ! type claude &> /dev/null && [[ ! -x "$HOME/.claude/local/claude" ]]; then
        warnings+=("claude (Claude Code CLI) - may be installed but not in PATH")
    fi

    if ! command -v uv &> /dev/null; then
        missing+=("uv (Python package manager)")
    fi

    if [[ ${#missing[@]} -gt 0 ]]; then
        print_error "Missing required tools:"
        for tool in "${missing[@]}"; do
            echo "  - $tool"
        done
        echo ""
        echo "Please install the missing tools and try again."
        exit 1
    fi

    if [[ ${#warnings[@]} -gt 0 ]]; then
        for tool in "${warnings[@]}"; do
            print_warning "Could not detect: $tool"
        done
    fi

    print_success "All prerequisites are installed"
}

check_git_repo() {
    if ! git rev-parse --git-dir &> /dev/null; then
        print_error "Not a git repository: $SCRIPT_DIR"
        echo "Please run this script from within the referee-pattern repository."
        exit 1
    fi
    print_success "Git repository detected"
}

check_clean_working_tree() {
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        print_warning "Working tree has uncommitted changes"
        if ! confirm "Continue anyway?"; then
            echo "Please commit or stash your changes first."
            exit 1
        fi
    else
        print_success "Working tree is clean"
    fi
}

# =============================================================================
# Worktree Functions
# =============================================================================

get_worktree_path() {
    local agent="$1"
    echo "../${WORKTREE_PREFIX}-${agent}"
}

get_branch_name() {
    local agent="$1"
    echo "${agent}-impl"
}

worktree_exists() {
    local agent="$1"
    local worktree_path
    worktree_path="$(get_worktree_path "$agent")"

    # Check if worktree is registered with git
    git worktree list 2>/dev/null | grep -q "$(cd "$SCRIPT_DIR" && cd "$worktree_path" 2>/dev/null && pwd)" 2>/dev/null
}

branch_exists() {
    local branch="$1"
    git show-ref --verify --quiet "refs/heads/$branch" 2>/dev/null
}

create_worktree() {
    local agent="$1"
    local worktree_path branch_name
    worktree_path="$(get_worktree_path "$agent")"
    branch_name="$(get_branch_name "$agent")"

    print_progress "Creating worktree for ${BOLD}${agent}${NC} agent..."

    # Check if worktree directory already exists
    if [[ -d "$worktree_path" ]]; then
        # Check if it's a valid worktree
        if worktree_exists "$agent"; then
            print_success "Worktree already exists: $worktree_path"
            return 0
        else
            # Directory exists but not a valid worktree - clean it up
            print_warning "Found orphaned directory: $worktree_path"
            rm -rf "$worktree_path"
        fi
    fi

    # Check if branch already exists
    if branch_exists "$branch_name"; then
        print_info "Branch '$branch_name' already exists, using existing branch"
        git worktree add "$worktree_path" "$branch_name"
    else
        git worktree add -b "$branch_name" "$worktree_path"
    fi

    print_success "Created worktree: $worktree_path (branch: $branch_name)"
}

remove_worktree() {
    local agent="$1"
    local worktree_path branch_name
    worktree_path="$(get_worktree_path "$agent")"
    branch_name="$(get_branch_name "$agent")"

    print_progress "Removing worktree for ${BOLD}${agent}${NC} agent..."

    # Remove worktree if it exists
    if [[ -d "$worktree_path" ]]; then
        git worktree remove --force "$worktree_path" 2>/dev/null || rm -rf "$worktree_path"
        print_success "Removed worktree: $worktree_path"
    else
        print_info "Worktree not found: $worktree_path"
    fi

    # Remove branch if it exists
    if branch_exists "$branch_name"; then
        git branch -D "$branch_name" 2>/dev/null || true
        print_success "Removed branch: $branch_name"
    fi
}

# =============================================================================
# Cleanup Function
# =============================================================================

cleanup_all() {
    print_header "Cleaning Up Referee Pattern Resources"

    echo "This will remove:"
    for agent in "${AGENTS[@]}"; do
        echo "  - Worktree: $(get_worktree_path "$agent")"
        echo "  - Branch: $(get_branch_name "$agent")"
    done
    echo ""

    if ! confirm "Are you sure you want to remove all worktrees and branches?"; then
        echo "Cleanup cancelled."
        exit 0
    fi

    echo ""
    for agent in "${AGENTS[@]}"; do
        remove_worktree "$agent"
    done

    # Prune any stale worktrees
    git worktree prune 2>/dev/null || true

    echo ""
    print_success "Cleanup complete!"
    echo ""
    echo "You can now run '$SCRIPT_NAME' to start fresh."
}

# =============================================================================
# Help Function
# =============================================================================

show_help() {
    cat << EOF
${BOLD}${CYAN}Referee Pattern Runner${NC}
${BOLD}═══════════════════════${NC}

${BOLD}DESCRIPTION${NC}
    This script automates the Referee Pattern workflow for Claude Code.
    It creates git worktrees for parallel development, allowing multiple
    specialized agents to implement the same feature independently.

${BOLD}USAGE${NC}
    $SCRIPT_NAME [OPTIONS]

${BOLD}OPTIONS${NC}
    --help      Show this help message and exit
    --clean     Remove all worktrees and branches created by this script
    --dry-run   Show what would be done without making any changes

${BOLD}WORKFLOW${NC}
    The script performs the following steps:

    1. ${CYAN}Prerequisites Check${NC}
       Verifies git, claude, and uv are installed

    2. ${CYAN}Create Worktrees${NC}
       Creates isolated git worktrees for each agent:
       - ../referee-pattern-maintainability (maintainability-impl branch)
       - ../referee-pattern-performance (performance-impl branch)
       - ../referee-pattern-robustness (robustness-impl branch)

    3. ${CYAN}Agent Implementation${NC}
       Each agent implements the feature in its worktree.
       Claude Code can run these in parallel using the Task tool.

    4. ${CYAN}Merge & Evaluate${NC}
       The merge-critic agent analyzes implementations and creates
       the final merged solution.

${BOLD}AGENTS${NC}
    ${GREEN}maintainability${NC}  Clean architecture, SOLID principles, extensibility
    ${BLUE}performance${NC}       Speed, memory efficiency, optimization
    ${YELLOW}robustness${NC}        Error handling, edge cases, production-readiness

${BOLD}IDEMPOTENCY${NC}
    This script is safe to run multiple times:
    - Existing worktrees are detected and reused
    - Existing branches are checked out instead of recreated
    - Use --clean to reset everything and start fresh

${BOLD}EXAMPLES${NC}
    # Run the referee pattern workflow
    $SCRIPT_NAME

    # Clean up and start fresh
    $SCRIPT_NAME --clean
    $SCRIPT_NAME

    # See what would happen without making changes
    $SCRIPT_NAME --dry-run

${BOLD}RECOVERY${NC}
    If something goes wrong:

    1. ${YELLOW}Worktree already locked${NC}
       git worktree prune
       rm -rf ../referee-pattern-<agent>

    2. ${YELLOW}Branch already exists${NC}
       git branch -D <agent>-impl

    3. ${YELLOW}Full reset${NC}
       $SCRIPT_NAME --clean

${BOLD}FILES${NC}
    features/calculator.feature    BDD specification to implement
    .claude/agents/                 Specialized agent definitions

${BOLD}SEE ALSO${NC}
    README.md           Project overview
    PATTERN.md          Detailed pattern explanation
    WORKTREES.md        Git worktrees guide
    MERGE_GUIDE.md      Merging implementations guide

EOF
}

# =============================================================================
# Dry Run Mode
# =============================================================================

dry_run() {
    print_header "Dry Run - Referee Pattern Workflow"

    echo "The following actions would be performed:"
    echo ""

    echo "${BOLD}1. Prerequisites Check${NC}"
    echo "   - Verify git, claude, and uv are installed"
    echo ""

    echo "${BOLD}2. Repository Validation${NC}"
    echo "   - Confirm this is a git repository"
    echo "   - Check for uncommitted changes"
    echo ""

    echo "${BOLD}3. Create Worktrees${NC}"
    for agent in "${AGENTS[@]}"; do
        local worktree_path branch_name
        worktree_path="$(get_worktree_path "$agent")"
        branch_name="$(get_branch_name "$agent")"

        if [[ -d "$worktree_path" ]]; then
            echo "   ${YELLOW}[EXISTS]${NC} $worktree_path ($branch_name)"
        else
            echo "   ${GREEN}[CREATE]${NC} $worktree_path ($branch_name)"
        fi
    done
    echo ""

    echo "${BOLD}4. Next Steps${NC}"
    echo "   - Open each worktree in separate terminals"
    echo "   - Run Claude Code with specialized agents"
    echo "   - Merge the best implementations"
    echo ""

    print_info "No changes were made (dry run mode)"
}

# =============================================================================
# Main Workflow
# =============================================================================

run_workflow() {
    local total_steps=5
    local current_step=0

    print_header "Referee Pattern Workflow"

    # Step 1: Prerequisites
    ((current_step++))
    print_step "$current_step" "$total_steps" "Checking prerequisites..."
    check_prerequisites
    echo ""

    # Step 2: Git repository
    ((current_step++))
    print_step "$current_step" "$total_steps" "Validating repository..."
    check_git_repo
    check_clean_working_tree
    echo ""

    # Step 3: Create worktrees
    ((current_step++))
    print_step "$current_step" "$total_steps" "Creating worktrees for specialized agents..."
    for agent in "${AGENTS[@]}"; do
        create_worktree "$agent"
    done
    echo ""

    # Step 4: Summary
    ((current_step++))
    print_step "$current_step" "$total_steps" "Worktree Summary"
    echo ""
    echo "  ${BOLD}Worktrees created:${NC}"
    for agent in "${AGENTS[@]}"; do
        local worktree_path branch_name abs_path
        worktree_path="$(get_worktree_path "$agent")"
        branch_name="$(get_branch_name "$agent")"
        abs_path="$(cd "$SCRIPT_DIR" && cd "$worktree_path" && pwd)"
        echo "    ${GREEN}${agent}${NC}: $abs_path"
        echo "           Branch: $branch_name"
    done
    echo ""

    # Step 5: Next steps
    ((current_step++))
    print_step "$current_step" "$total_steps" "Ready for Implementation"
    echo ""
    echo "  ${BOLD}Option A: Automated (Recommended)${NC}"
    echo "  Run Claude Code in this directory and paste:"
    echo ""
    echo "    ${CYAN}Use the maintainability, performance, and robustness coding agents${NC}"
    echo "    ${CYAN}to solve the spec, then use the merge-critic agent to put the${NC}"
    echo "    ${CYAN}best bits into a final solution. Make sure the specs pass.${NC}"
    echo ""
    echo "  ${BOLD}Option B: Manual${NC}"
    echo "  Open separate terminals for each worktree and run Claude Code:"
    echo ""
    for agent in "${AGENTS[@]}"; do
        local worktree_path
        worktree_path="$(get_worktree_path "$agent")"
        echo "    cd $worktree_path && claude"
    done
    echo ""

    print_header "Setup Complete!"

    echo "The referee pattern worktrees are ready."
    echo ""
    echo "  ${BOLD}To start:${NC} Run 'claude' in this directory"
    echo "  ${BOLD}To clean up:${NC} Run '$SCRIPT_NAME --clean'"
    echo "  ${BOLD}For help:${NC} Run '$SCRIPT_NAME --help'"
    echo ""
}

# =============================================================================
# Main Entry Point
# =============================================================================

main() {
    cd "$SCRIPT_DIR"

    # Parse arguments
    case "${1:-}" in
        --help|-h)
            show_help
            exit 0
            ;;
        --clean)
            cleanup_all
            exit 0
            ;;
        --dry-run)
            dry_run
            exit 0
            ;;
        "")
            run_workflow
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Run '$SCRIPT_NAME --help' for usage information."
            exit 1
            ;;
    esac
}

main "$@"
