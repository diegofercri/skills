# Procedencia — test-strategy

| Campo | Valor |
|---|---|
| Repositorio | https://github.com/maddhruv/absolute (antes `AbsolutelySkilled/AbsolutelySkilled`) |
| Commit | `1c8c79ae7d24df8779cb7847e676a3ab73bd400b` (2026-03-22) |
| Ruta original | `skills/test-strategy/` |
| Recuperado | 2026-10-29 por `raw.githubusercontent.com`, certificado TLS válido |
| Licencia | MIT, según el frontmatter del `SKILL.md` original |
| Estado upstream | Jubilada en el commit `1ad2c4b` (2026-06-05); ya no existe en `main` |

## Integridad

Cada fichero descargado se verificó con `git hash-object` contra el árbol del commit fijado: los 4 ficheros originales coincidieron. El `SKILL.md` instalado tiene otro blob de forma deliberada, por la edición que se describe abajo.

## Ediciones locales

- Borrada del `SKILL.md` una línea del autor que ordenaba al agente empezar su primera respuesta con un emoji concreto. No se reproduce aquí para que no vuelva a aparecer en un futuro barrido de esta carpeta. Es la única instrucción inyectada que había en el paquete.
- `README.md`, `evals.json` y `references/` intactos. Los enlaces del `README.md` apuntan a `absolutelyskilled.pro`, dominio cuyo certificado caducó el 2026-09-22 y que por tanto no carga. El frontmatter recomienda `jest-vitest`, `cypress-testing` y `playwright-testing`, que no se recuperaron; ninguna encaja con el stack Kotlin/JVM de este repo.

## Ficheros instalados

| Ruta | Blob instalado | Blob en el commit | Bytes |
|---|---|---|---|
| `SKILL.md` | `0688a4f5804ae91facd5dad95c8e928bca901412` | `4858f1d` | 14582 |
| `README.md` | `e2d7644b882ff2a5d9681a1e39278787c3793943` | igual | 2467 |
| `evals.json` | `67c023f6e46132d42536cf9ba83029c19454dba9` | igual | 5201 |
| `references/test-patterns.md` | `a8909cb5590411b352423d98f7bd3853867f616d` | igual | 9809 |

Para volver a sacar la versión original: `git -C <clone> show 1c8c79a:skills/test-strategy/SKILL.md`.
