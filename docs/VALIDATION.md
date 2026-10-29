# Validación

Fecha: 2026-10-29. Entorno ejecutado: Windows, Python 3.12.14 del runtime local de Codex.

## Resultados ejecutados

- `python manage.py validate`: cinco skills, metadatos y referencias relativos válidos, sin dependencias antiguas o instrucciones exclusivas de un cliente.
- `python -m unittest discover -s tests -v`: **23 tests**, incluyendo instalación repetida, copias idénticas, vista previa sin escrituras, actualización de contenido/referencias, desinstalación parcial, preservación byte a byte de preferencias ajenas, conflictos, enlaces, rutas con espacios, recuperación ante fallo intermedio y protección ante cambios posteriores a la comprobación inicial.
- `tests/smoke_codex.py`: **Codex CLI 0.165.0** abrió su app-server en un home temporal y respondió a `skills/list`: una entrada para cada skill, cero errores. No se inició ningún turno de modelo. Se comprobó descubrimiento y parseo real, no la calidad de respuestas del modelo.
- Respaldo: **47 archivos, 385275 bytes** originales, comprimidos y verificados individualmente por SHA256. ZIP y manifiesto en `archive/`; las diez carpetas también están disponibles para consulta en `archive/legacy-source/`.

El validador externo `skill-creator/scripts/quick_validate.py` se intentó ejecutar, pero requiere PyYAML, ausente en el runtime. No se ha presentado ese intento como aprobado. El validador propio no necesita paquetes y Codex ha parseado los cinco manifiestos reales.

## Revisión de comportamiento

`tests/behavior-cases.json` contiene 13 escenarios de aceptación y sus resultados esperados. Las descripciones y procedimientos se revisaron contra estos casos: alcance, elección del procedimiento, exclusión de UI/prosa, preservación de comentarios útiles, revisión sin editar y deduplicación entre pasadas.

Esta es una comprobación editorial; no son 13 ejecuciones de modelo ni una medición de precisión del selector. Para evaluar comportamiento, usar una copia desechable de un proyecto, ejecutar cada prompt en una sesión nueva y guardar: cliente/versión/modelo, skills cargadas, respuesta, cambios de archivos y resultado frente al criterio. Una revisión debe dejar el código intacto. El caso Thermos debe producir un único hallazgo por causa/remedio.

## Límites y comprobaciones pendientes

- Claude Code y OpenCode no estaban disponibles en PATH ni en las ubicaciones de ejecutables comprobadas. Sus rutas y capacidades se contrastaron con documentación oficial; queda comprobar descubrimiento y carga en sesiones reales.
- En OpenCode, ejecutar `python /ruta/manage.py run-opencode -- debug skill` tras instalar: verificar un nombre por skill. El lanzador desactiva descubrimiento externo también para otras skills de `.claude`/`.agents`; usar rutas nativas para las skills de proyecto necesarias.
- En Claude, iniciar una sesión nueva y verificar el menú de skills y `/review`. En Codex, el smoke test ya verificó descubrimiento; queda evaluar la selección contextual y el uso de referencias durante tareas reales.
- Los tests se ejecutaron en Windows. La implementación usa Python estándar y rutas portables, pero no se ha declarado una ejecución en Linux/macOS. Repetir la misma suite allí antes de dar soporte validado a esos sistemas.
- El control de conflictos cubre las rutas globales estándar. No inspecciona automáticamente todos tus proyectos ni plugins instalados; sus homónimos deben comprobarse en el catálogo real del cliente.
- Los commits inmutables de las fuentes remotas nuevas no pudieron recuperarse. `sources.json` identifica URLs, fecha de lectura y esta limitación; no se inventan SHAs. Las licencias verificadas y los avisos pendientes figuran en `NOTICE.md`.

No se ha instalado, desinstalado ni actualizado ninguna skill en el home real del usuario.
