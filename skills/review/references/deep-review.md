# Two-pass review

Maintain the same diff scope through both passes. Read unchanged dependencies when necessary to trace a changed path.

## Pass 1: correctness, security and compatibility

Trace changed inputs through validation, authorization, state transitions and external effects. Check error and cancellation paths, transaction limits, idempotency and races. Validate exploitability or a concrete failure scenario before assigning severity.

Inspect configuration and build changes that affect how developers start or test the project: renamed environment variables, ports, secret sources, prerequisites and removed defaults. A normal dependency addition is not itself a broken workflow.

Check that feature gating remains effective at the enforcement boundary, including indirect entry points. Examine changed public contracts and migrations for compatibility with existing callers and stored data. Verify performance concerns against the affected path and workload rather than speculative micro-optimizations.

## Pass 2: maintainability

Use the canonical [quality criteria](../../code-quality/SKILL.md) and [boundary decisions](../../architecture/references/decisions.md) only as relevant. Look for a concrete simplification that removes unnecessary concepts, branching or duplicated policy. Suggest the smallest useful remedy; do not implement it during review.

Growth in a file is a cue to inspect cohesion, not a fixed line-count failure. Check whether new types expose impossible states, special cases leak into shared modules, or wrappers conceal the owner of a rule. Consider whether related writes need atomicity and whether concurrency would actually simplify independent work without violating limits or ordering.

## Synthesis

Combine both passes into the findings format in the parent skill. Resolve disagreements against evidence. Separate established bugs from improvements and open questions, and identify anything not checked. Do not inflate a quality preference into a blocker to make the review appear thorough.
