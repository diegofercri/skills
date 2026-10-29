# Comments that retain information

Judge comments by what a future maintainer would lose if they disappeared. Keep rationale, business constraints, units, concurrency assumptions, security requirements, non-obvious algorithms, compatibility workarounds and public API contracts.

Keep license notices, tool directives, generated-file markers and links or version numbers needed to identify when a workaround can be removed. A docstring may be executable documentation or part of a public interface.

Remove narration that just repeats a declaration or statement. Replace a vague task reminder only when the actual task is known; do not invent a rationale. Preserve project-required documentation even when it seems repetitive.

Prefer concise explanations, but do not enforce a line limit. A complicated invariant can require a paragraph. Do not strip issue references merely to make a comment shorter.

For a comments-only edit, inspect the final diff to verify that behavior and non-comment text remain unchanged. Do not introduce tests solely to prove that punctuation changed.
