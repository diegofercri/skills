---
name: architecture
description: Design or assess module boundaries, dependency direction, use cases, ports and component ownership. Use for Clean Architecture or SOLID design decisions; not for local naming cleanup, infrastructure deployment or a general diff review.
---

# Architecture

Start from the actual change pressure: what policy must remain stable, which details vary, who consumes the boundary, and what is difficult to test or evolve? Inspect imports, build modules and a representative execution path; folder names alone do not establish an architecture.

1. Map business rules, application orchestration, adapters and external systems as they currently exist. Do not require four directories, classes for every use case, or a rewrite of a small CRUD application.
2. Trace source dependencies separately from runtime calls. When business policy needs infrastructure, a port owned by the policy can invert that dependency; the outer composition point supplies the adapter.
3. Read [boundary and component decisions](references/decisions.md) for the relevant tradeoff. Propose the smallest useful boundary and explain what coupling it removes and what maintenance it adds.
4. Specify inputs, outputs, errors, ownership and transaction limits for a new boundary. Identify affected callers and compatibility or migration needs before editing it.
5. Verify with existing module/build checks and a test of the policy independently of infrastructure when that is the benefit claimed. Propose an import rule only if a recurring boundary needs enforcement.

An architecture assessment reports evidence and options without editing. A design/implementation request may change the agreed scope. Use the review skill for a change-scoped audit and refactoring for execution of a behavior-preserving migration.
