# Test design and reliability

## Isolation and data

Keep each test's essential inputs visible. Builders can supply irrelevant defaults; fixtures should not hide the condition being tested. Parameterize meaningful boundaries, including immediately below, at and above a threshold.

A fake is useful for policy tests but cannot establish database constraint, collation, isolation or query behavior. Use a representative real dependency for those risks. A stub can control a failure; a spy can record an externally meaningful effect. Avoid mocking an SDK's internal call chain when a boundary you own is available.

Rollback-based isolation does not exercise commit-time constraints, outbox publication or after-commit hooks. Include committed cases when those are relevant. Ensure application work uses the test transaction before assuming rollback will clean it up. Use unique test resources when parallel tests can collide.

Inject or control time, randomness and scheduling where necessary. Cover cancellation, retry limits and duplicate delivery when the feature relies on them. Avoid arbitrary sleeps as synchronization.

## TDD and regression tests

When TDD is requested, describe one behavior, observe the expected test failure, implement it, then simplify while retaining the passing test. A setup or import error is not proof that a regression test catches the intended bug.

For bug fixes, prefer a test that fails on the original defect. For legacy refactoring, characterize externally observable behavior before altering an uncertain seam. Do not assert accidental private structure merely to raise coverage.

## Flaky suites and confidence

Reproduce and diagnose nondeterminism: shared state, clocks, races, external systems and order dependence. Quarantine only with a recorded owner and resolution date while retaining diagnostic signal; repair or deliberately retire obsolete coverage. Reruns can gather evidence but do not fix the cause.

Use coverage to find unexamined code. Mutation tests can reveal weak assertions, but surviving equivalent or unreachable mutants require judgment. Neither coverage nor mutation score is a universal release threshold.
