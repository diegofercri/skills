---
name: code-quality
description: Guide readable implementation, naming, error handling and useful code comments while writing code. Use for focused readability or comment cleanup; use review for a diff audit and refactoring for structural transformations. Not for UI styling or prose editing.
---

# Code quality

Work within the requested change and the project's language conventions. Read nearby implementations and the public contract before choosing names or error semantics.

- Use domain terms consistently. Make units, ownership, effects and absence explicit where confusing them could cause a bug. Preserve public names unless changing their contract is part of the task.
- Keep related logic together. Extract a helper when its name and contract reduce the reader's work; avoid wrappers that merely relocate complexity. Neither line counts nor parameter counts prove a design problem.
- Reuse a rule when it represents the same business decision. Similar syntax for unrelated policies is not necessarily duplication.
- Follow the language's established error model: exceptions, result types and nullable values can all be appropriate. Do not silently turn failure into successful empty data. Preserve causes and clean up resources on failure and cancellation.
- Prefer explicit data contracts over unchecked casts or optional fields that permit impossible states. Validate external data at the boundary rather than scattering defensive checks throughout trusted internal code.

For comment cleanup, read [comment guidance](references/comments.md). A comments-only request permits only comments to change, not identifiers, executable statements or unrelated formatting. Leave formatter/compiler directives intact.

Consult [architecture decisions](../architecture/references/decisions.md) only when responsibility or dependency direction is the actual issue. For a structural change, use the refactoring procedure; do not automatically load its whole catalog for ordinary implementation.

Finish with the concrete change and relevant verification. Do not turn routine coding into a formal quality audit.
