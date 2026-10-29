# Moves and hazards

| Evidence | Candidate move | Check before applying |
|---|---|---|
| A cohesive block has a useful name | Extract function | Captured mutable state, evaluation order, early returns, exception scopes |
| A helper obscures an already simple expression | Inline | Side-effect count, dispatch overrides and public callers |
| A rule is duplicated and must evolve together | Extract shared policy | Similar-looking rules may have different owners or future behavior |
| Several changes scatter across unrelated modules | Move behavior to its owner | Dependency direction and exposed mutable state |
| A class mixes distinct change reasons | Extract responsibility | Whether callers now need more coordination than before |
| Data travels together and has shared invariants | Parameter/value object | Public serialization shape, validation timing and allocation costs |
| Repeated branching varies by behavior | Strategy or explicit state model | A stable local switch may be simpler; preserve exhaustiveness |
| Nested guards obscure the normal path | Early returns | Finally/defer behavior, locks and cleanup still execute correctly |
| A subtype rejects valid base operations | Composition or narrower contract | Existing substitution assumptions and consumers |
| Temporary fields allow invalid combinations | Explicit state type | Valid transitions, persisted values and compatibility |
| A wrapper forwards everything without purpose | Inline/remove wrapper | It may still be a compatibility, authorization or instrumentation boundary |
| Code appears unused | Remove dead code | Reflection, generated callers, feature flags and external API usage |
| A temporary computation could become a query | Extract query if useful | Do not multiply expensive I/O, read time twice or change a snapshot into a live value |

Use simple design as a decision order: preserve correctness, reveal intent, remove shared-rule duplication, then remove unnecessary parts. Do not pursue fewer lines at the expense of clarity or move presentation logic into domain objects just because it reads their fields.
