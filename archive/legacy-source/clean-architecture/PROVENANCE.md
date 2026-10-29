# Procedencia — clean-architecture

| Campo | Valor |
|---|---|
| Repositorio | https://github.com/maddhruv/absolute (antes `AbsolutelySkilled/AbsolutelySkilled`) |
| Commit | `1c8c79ae7d24df8779cb7847e676a3ab73bd400b` (2026-03-22) |
| Ruta original | `skills/clean-architecture/` |
| Recuperado | 2026-10-29 por `raw.githubusercontent.com`, certificado TLS válido |
| Licencia | MIT, según el frontmatter del `SKILL.md` original |
| Estado upstream | Jubilada en el commit `1ad2c4b` (2026-06-05); ya no existe en `main` |

## Integridad

Cada fichero descargado se verificó con `git hash-object` contra el árbol del commit fijado: los 7 ficheros originales coincidieron. El `SKILL.md` instalado tiene otro blob de forma deliberada, por la edición que se describe abajo.

## Ediciones locales

- Borrada del `SKILL.md` una línea del autor que ordenaba al agente empezar su primera respuesta con un emoji concreto. No se reproduce aquí para que no vuelva a aparecer en un futuro barrido de esta carpeta. Es la única instrucción inyectada que había en el paquete.
- `README.md`, `evals.json` y `references/` intactos. Los enlaces del `README.md` apuntan a `absolutelyskilled.pro`, dominio cuyo certificado caducó el 2026-09-22 y que por tanto no carga. El frontmatter recomienda `system-design`, `microservices` y `backend-engineering`, que no se recuperaron.

## Ficheros instalados

| Ruta | Blob instalado | Blob en el commit | Bytes |
|---|---|---|---|
| `SKILL.md` | `6c95cbade1c0e74b6e481ddec19c63dbe7da4bc4` | `4b86195` | 14667 |
| `README.md` | `0a20a678531bad289a8cbcf1ffa80879431f4e9f` | igual | 2956 |
| `evals.json` | `595c00ec2fe6169b656c8b99927475182164e075` | igual | 5463 |
| `references/boundaries.md` | `1651fe394e981731227ff1f574a084fb4ccb18f6` | igual | 7446 |
| `references/component-principles.md` | `108d50fa47c8af51147b45cca6a603911c0c3796` | igual | 6655 |
| `references/dependency-rule.md` | `6dfc0a065e24f886b0cb39286ad254212e83e813` | igual | 6362 |
| `references/layer-patterns.md` | `36a1feb5246dae5497dfae599a40345408c0fdc6` | igual | 8957 |

Para volver a sacar la versión original: `git -C <clone> show 1c8c79a:skills/clean-architecture/SKILL.md`.
