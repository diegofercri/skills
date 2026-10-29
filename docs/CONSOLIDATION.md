# Matriz de consolidación

| Fuente y capacidad | Destino | Decisión |
|---|---|---|
| `clean-code`: nombres, legibilidad y errores | `code-quality` | Conservar criterios, reescribir sin imponer convenciones de otro lenguaje ni prohibir null/result types |
| `clean-code`: comentarios + `antislop-code` | `code-quality/references/comments.md` | Una guía original; preservar contratos, directivas, licencias y contexto útil sin límites de dos líneas |
| `clean-code`: SOLID | `architecture/references/decisions.md` | Un propietario para responsabilidad, sustitución e inversión de dependencias |
| `clean-code`: smells + `refactoring-patterns` | `refactoring/references/moves.md` | Un catálogo de movimientos con riesgos; no duplicar el procedimiento en calidad |
| `clean-code`: TDD | `testing/references/design.md` | Bajo demanda; no imponer TDD a cada cambio |
| Arquitectura local: capas, dependencias, boundaries | `architecture` | Consolidar con la fuente de nathankim0 |
| Arquitectura local: componentes, ciclos y cohesión | `architecture/references/decisions.md` | Conservar decisiones prácticas, retirar ratios y estructuras universales |
| nathankim0: Clean Architecture | `architecture` | Distinguir llamadas de dependencias; un solo contrato puede justificar un puerto |
| nathankim0: Kent Beck, simplificación incremental | `refactoring` | Preservar comportamiento; no crear commits automáticamente |
| `test-strategy`: niveles, ROI, contratos y cobertura | `testing` | Selección por riesgo, sin 60/30/10 ni umbrales universales |
| `test-strategy`: fixtures, dobles, reloj, aislamiento y flaky tests | `testing/references/design.md` | Mantener límites de los fakes, commits reales y diagnóstico de flakiness |
| `code-review-mastery`: diff, contexto, severidad y reporte | `review` | Una entrada, solo lectura; severidad por impacto, no por etiqueta de categoría |
| Thermos: bugs, seguridad, flags y devex | `review/references/deep-review.md` | Primera pasada exhaustiva, solo cuando se solicita |
| Thermos: mantenibilidad y simplificación | `review` + referencias canónicas | Segunda pasada; crecimiento de archivos es señal, no fallo automático a 1000 líneas |
| Thermos: coordinación y síntesis | `review` | Secuencial en v1, un informe; sin dependencia de subagentes Cursor |
| antislop core, UI, copywriting, human/accessibility | Archivo privado | Excluir del catálogo por elección de alcance; no sustituye herramientas de accesibilidad del proyecto |
| Wizards, companion checks, instrucciones de instalación en skills | `manage.py` y README | Retirar de los procedimientos que carga el modelo |
| `CLAUDE.md` original | `preferences/COMMON.md` | Conservar preferencias y añadir alcance de uso; generar bloques para cada cliente |

Las referencias entre skills son relativas y se distribuyen juntas. El instalador selecciona clientes, no subconjuntos de skills, para mantener esas referencias válidas. Compartir conceptos no obliga a cargar varias skills: la revisión consulta solo el criterio especializado que necesita.

Los ejemplos extensos originales se conservan en el ZIP; no se copian porque mezclaban convenciones de lenguajes, repetían conceptos o imponían reglas que esta colección ha descartado. Las nuevas referencias explican decisiones y riesgos en lugar de reproducir tutoriales.
