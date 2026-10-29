---
name: refactoring
description: Simplify existing code through small behavior-preserving transformations, including extraction, inlining, moving responsibilities and removing duplication. Use when asked to refactor; not merely to review a diff or implement new behavior.
---

# Refactoring

Define the intended simplification and the observable behavior to preserve: returned values, exceptions, ordering, side effects, persistence, timing contracts and public names. Separate a requested behavior change from the structural change so each can be reviewed.

1. Inspect callers and existing tests. Establish the relevant baseline; distinguish pre-existing failures from regressions.
2. Select one transformation from [moves and hazards](references/moves.md). Explain its benefit when the tradeoff is non-obvious.
3. Make a small step and verify the affected behavior. Add a characterization test when risky behavior is unprotected; use existing checks for safe mechanical edits rather than manufacturing tests that mirror the implementation. See [testing guidance](../testing/SKILL.md) if choosing the safety net requires more thought.
4. Inspect the resulting diff for unintended API, serialization or side-effect changes. If a step regresses behavior, repair or undo only your own step, preserving the user's work.
5. Stop when the requested simplification is achieved. Report any unresolved behavior uncertainty; do not claim equivalence solely because the build passes.

Use symbol-aware rename tools when available; otherwise search code, configuration, reflection and external consumers before a targeted rename. Do not require an unavailable IDE. Do not commit or publish as an automatic part of the refactoring rhythm.

For naming and comments, consult the relevant [code-quality guidance](../code-quality/SKILL.md); for a cross-module seam, consult [architecture decisions](../architecture/references/decisions.md). Read only what the transformation needs.
