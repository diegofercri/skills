# Skills personales de programación

Una fuente editable para OpenCode, Claude Code y Codex CLI. Cinco skills bajo demanda, sin agentes ni instalaciones automáticas durante una tarea.

| Skill | Responsabilidad | Ejemplo |
|---|---|---|
| `code-quality` | Implementación, nombres, errores y comentarios | «Limpia solo los comentarios» |
| `architecture` | Límites, contratos, dependencias y SOLID | «Separa esta regla del SDK» |
| `refactoring` | Simplificación preservando comportamiento | «Refactoriza sin cambiar el contrato» |
| `testing` | Riesgos, niveles y calidad de tests | «Qué tests detectarían este fallo» |
| `review` | Revisión de cambios sin editar | «Revisa lo staged» o «Revisión exhaustiva contra develop» |

La revisión normal es ligera. La exhaustiva/Thermos es explícita y realiza dos pasadas secuenciales (corrección/seguridad y mantenibilidad), con un informe sin hallazgos repetidos. No implica independencia entre revisores.

## Instalación

Requisito: Python **3.10+**, sin paquetes adicionales. En Windows puede ser `py -3` y en Linux/macOS `python3`, según tu instalación. Los ejemplos usan `python`. Ejecuta desde esta carpeta o utiliza la ruta absoluta a `manage.py`.

```sh
python manage.py validate
python manage.py install --client all --dry-run
python manage.py install --client all
python manage.py check
```

Selecciona un cliente con `--client opencode`, `--client claude` o `--client codex`; puedes repetir la opción. Se instalan las cinco skills juntas para conservar sus referencias relativas.

| Cliente | Copias generadas | Preferencias |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `~/.claude/CLAUDE.md` |
| Codex CLI | `~/.agents/skills/` | `~/.codex/AGENTS.md` |
| OpenCode | `~/.config/opencode/skills/` | `~/.config/opencode/AGENTS.md` |

Edita **`skills/`** y **`preferences/COMMON.md`**, no las copias instaladas. Los bloques de preferencias preservan el contenido ajeno y sus cambios posteriores fuera del bloque.

El instalador se detiene ante skills antiguas o homónimas no gestionadas, archivos modificados, enlaces/junctions y marcadores ajenos. Primero archiva las antiguas fuera de las rutas de descubrimiento; renombrarlas dentro de `skills/` no basta. Esta implementación no ha tocado tu instalación global existente.

Las rutas personalizadas mediante `CODEX_HOME`, `CLAUDE_CONFIG_DIR`, `XDG_CONFIG_HOME` u `OPENCODE_CONFIG_DIR` no se gestionan automáticamente: si están definidas, el instalador se detiene. `--home` sirve para probar una instalación aislada con la estructura estándar, no para cambiar el home real de los clientes.

## OpenCode sin duplicados

OpenCode también escanea `.claude/skills` y `.agents/skills`. Si instalas más de un cliente, inicia OpenCode desde tu proyecto con:

```sh
python /ruta/a/esta/coleccion/manage.py run-opencode --
```

Cita las rutas con espacios. El lanzador conserva el directorio de trabajo y pasa los argumentos después de `--`. Activa `OPENCODE_DISABLE_EXTERNAL_SKILLS=1` y `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=1` solo para ese proceso. No modifica variables globales.

**Consecuencia:** tampoco se cargan otras skills de proyecto o usuario alojadas en `.claude`/`.agents` en esa sesión. Usa `.opencode/skills` para las específicas que necesites allí. No se desactivan instrucciones de proyecto ni plugins. Con el comando directo `opencode` y las tres copias instaladas puede reaparecer el descubrimiento de homónimos; el lanzador evita ese escaneo. Si solo instalas OpenCode y no tienes otras copias, puedes usar el comando habitual.

Comprueba su catálogo real con:

```sh
python /ruta/a/esta/coleccion/manage.py run-opencode -- debug skill
```

Claude permite `/review`; Codex permite `$review`. En OpenCode pide «usa la skill review». La selección contextual depende del cliente y del modelo; no se promete comportamiento idéntico.

## Actualizar y desinstalar

Tras editar la fuente, ejecuta `install` otra vez. También actualiza los clientes ya registrados para mantener las copias sincronizadas. `check` detecta diferencias con la fuente. Reinicia sesiones si el cliente no recarga cambios.

```sh
python manage.py uninstall --client claude --dry-run
python manage.py uninstall --client claude
python manage.py uninstall --client all
```

Solo se retiran archivos registrados sin modificaciones y el bloque propio de preferencias. Se conservan ficheros ajenos y pueden quedar directorios vacíos. El manifiesto con hashes está en `~/.personal-dev-skills/state.json`; no lo borres para eludir conflictos.

Si editaste una copia instalada, conserva el cambio y trasládalo a la fuente o restaura la copia registrada antes de actualizar. Para volver a una versión anterior, recupera aquella fuente y ejecuta `install`. Guarda versiones con tu control de versiones: esta carpeta de entrada no tenía Git y no se ha creado un repositorio ni hecho commits automáticamente.

Las escrituras son atómicas por archivo y hay reversión ante errores durante el proceso. No es una transacción resistente a apagones: una interrupción abrupta puede dejar una instalación parcial o un bloqueo. Conserva el manifiesto y revisa el estado antes de retirar un `install.lock` obsoleto.

## Validación y mantenimiento

```sh
python manage.py validate
python -m unittest discover -s tests -v
python manage.py install --client all --home .sandbox-home --dry-run
```

La [validación](docs/VALIDATION.md) distingue tests ejecutados de comprobaciones pendientes en clientes reales. Consulta también la [matriz de consolidación](docs/CONSOLIDATION.md), [procedencia](sources.json) y [atribuciones](NOTICE.md). Las actualizaciones externas requieren revisión editorial, no sustitución automática de las skills.

Documentación contrastada el 2026-10-29: [OpenCode skills](https://opencode.ai/docs/skills/), [OpenCode CLI y variables](https://opencode.ai/docs/cli/), [Claude skills](https://code.claude.com/docs/en/skills), [Claude memory](https://code.claude.com/docs/en/memory), [Codex skills](https://learn.chatgpt.com/docs/build-skills) y [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
