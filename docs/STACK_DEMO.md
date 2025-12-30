# Stack Demo Documentation

This document demonstrates a Graphite stack workflow with multiple dependent pull requests.

## Overview

A stack is a series of 2 or more pull requests where each PR builds upon the previous one. This allows for incremental, reviewable changes.

## Stack Structure

This demo stack consists of 3 pull requests:

1. **PR 1: Foundation** - Adds basic documentation structure
2. **PR 2: Enhancements** - Adds detailed content (depends on PR 1)
3. **PR 3: Validation** - Adds examples and validation (depends on PR 2)

## Benefits of Stacking

- **Incremental Review**: Reviewers can approve changes step by step
- **Early Merges**: Lower PRs can be merged independently
- **Clear Dependencies**: Each PR has a clear, focused purpose
- **Better CI/CD**: Each PR can be tested independently

## Detailed Workflow

### Creating a Stack

1. Start from your base branch (usually `main`)
2. Create the first branch: `gt branch create stack/pr1-name`
3. Make changes and commit
4. Create the next branch: `gt branch create stack/pr2-name --insert`
5. Continue for each PR in the stack

### Graphite Commands

- `gt branch create <name>` - Create a new branch
- `gt branch create <name> --insert` - Create a branch that inserts into the stack
- `gt stack submit` - Submit all branches in the stack as PRs
- `gt stack restack` - Restack branches after changes

### Best Practices

- Keep each PR focused on a single concern
- Write clear commit messages
- Update PR descriptions to explain dependencies
- Test each PR independently before submitting the next

## Examples

### Example Stack: Feature Implementation

```
main
  └── stack/feat/add-api-endpoint (PR #1)
       └── stack/feat/add-validation (PR #2)
            └── stack/feat/add-tests (PR #3)
```

### Example Stack: Bug Fix

```
main
  └── stack/fix/identify-issue (PR #1)
       └── stack/fix/implement-fix (PR #2)
            └── stack/fix/add-regression-test (PR #3)
```

## Validation Checklist

Before submitting a stack, ensure:

- [ ] Each PR has a clear, focused purpose
- [ ] Dependencies are clearly documented
- [ ] Each PR can be reviewed independently
- [ ] Tests pass for each PR in isolation
- [ ] Commit messages follow conventional commits format
- [ ] PR descriptions explain what and why

## Summary

This stack demonstrates how Graphite enables efficient code review through incremental, dependent pull requests. Each PR builds upon the previous one, allowing for early merges and clear dependency tracking.

