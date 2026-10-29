---
name: testing
description: Choose meaningful test coverage and test levels, design regression tests, use TDD when requested, and diagnose flaky suites. Use for testing decisions; use framework documentation for syntax. Not a mandatory checklist for every edit.
---

# Testing

Identify the behavior at risk and the failure a test should catch. Use the lowest level that exercises that risk faithfully, with the project's existing tools and CI budget.

- Pure decisions, transformations and domain invariants usually suit unit tests.
- Persistence, adapters and interactions need integration tests when a fake would conceal the relevant behavior.
- Cross-service compatibility benefits from consumer/provider contract tests; these do not prove end-to-end business behavior.
- Reserve end-to-end tests for journeys whose risk cannot be covered adequately below that level. Run them where appropriate to the project's feedback budget, not only at a universally mandated CI stage.

Assert observable outcomes and failure contracts. Include meaningful boundaries and error paths, not just the happy path. Mock an interaction when that interaction is itself the contract; avoid asserting every internal call.

Read [test design and reliability](references/design.md) for doubles, database isolation, time, flakiness, mutation testing or TDD. Do not prescribe coverage percentages or unit/integration ratios independently of the application.

For a proposed suite, map risks to tests and say what remains uncovered. For implementation, run the relevant checks and report the exact result and any environment limitation. Never turn a failure into a claimed pass by retrying until green.
