# Boundary and component decisions

## Responsibility and contracts

Group behavior that changes for the same business reason. Separate unrelated owners or release cycles when their coupling causes concrete friction. An interface with one implementation is useful if it shields policy from an SDK, storage model or volatile protocol; implementation count is not the deciding criterion.

Keep source dependencies toward policy. Runtime control may flow outward through a policy-owned port. Wire concrete implementations at the application entry point, not inside domain rules. Simple function parameters or native protocols can be enough; a dependency injection framework is optional.

Adapters translate external representations. Do not carry HTTP request objects, lazy ORM state or infrastructure exceptions into a supposedly independent policy. Introduce a DTO when it controls exposure, lifetime or schema coupling; identical data does not need redundant mappings at every conceptual layer. Account for shared mutable objects and who may change them.

## SOLID without ceremony

- Separate responsibilities when different reasons for change collide, not by splitting every method into a class.
- Add an extension point for a real variation or protected boundary. A stable switch with a few cases can remain a switch.
- Substitutes must preserve accepted inputs, outputs, errors and observable side effects. Extra preconditions can break consumers even if signatures match.
- Shape interfaces for their consumers. Empty implementations or unsupported operations often expose a mismatched contract.
- Invert dependencies to isolate policy from mechanisms. A wrapper with no isolation, semantic translation or ownership benefit is optional overhead.

## Components and migration

Look at what is reused, released and changed together before splitting packages. Break dependency cycles by moving responsibility, inverting an edge or extracting a genuinely shared contract. Avoid turning a shared module into an unowned collection of everything.

Fan-in and fan-out help locate costly coupling; they are not pass/fail metrics. Stable concrete value types do not need to become abstract to satisfy a ratio.

For a migration, move one seam at a time, preserving callers with a temporary adapter if needed. State how that adapter is removed. Keep difficult I/O glue thin while testing the decision logic separately. This does not make the glue immune to integration bugs.
