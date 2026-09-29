# Analizador de logs en Python — Semana 2 (KODIGO)

## Cómo ejecutarlo
    python analizador_logs.py                # abre selector de archivos
    python analizador_logs.py log_bueno.txt  # ruta directa

## Reglas de validación (decisiones mías)
| Regla | Decisión | Por qué |
|---|---|---|
| Línea vacía | Se ignora | No es un evento ni un error |
| Nivel | Solo `[INFO]`, `[WARNING]`, `[ERROR]` en mayúsculas | [COMPLETAR: tu razón] |
| Sin fecha | Cuenta como evento, marcado "sin fecha" | Tiene severidad y mensaje, sigue siendo útil |
| Fecha inválida | Cuenta como evento, marcado "fecha inválida" | Igual: falla solo la marca de tiempo |
| Sin mensaje / sin nivel | Línea mal formateada | Información incompleta |

Casos borde que NO manejo: logs multilínea, horas (HH:MM:SS), niveles extra (DEBUG).

## Evidencia de pruebas
**log_bueno.txt** — 5 líneas válidas.
- Esperado: 5 eventos (3 INFO, 1 WARNING, 1 ERROR), 0 malformadas.
- Obtenido: coincide.

**log_con_errores.txt** — 12 líneas con casos mezclados.
- Esperado: 5 eventos (2 INFO, 2 WARNING, 1 ERROR); 1 sin fecha; 2 con fecha inválida; 6 malformadas; 1 vacía ignorada.
- Obtenido: coincide.

**Archivo inexistente** — muestra mensaje de error sin romper el programa.

## Reflexión técnica
### 1. Qué apoyó la IA
[COMPLETAR con tu experiencia real: por ejemplo, la propuesta de regex, la estructura en funciones, el selector con tkinter...]

### 2. Qué decidí yo
[COMPLETAR: las reglas de la tabla, qué cuenta como línea inválida, qué casos borde dejé fuera...]

### 3. Ejemplo concreto: la IA se equivocó y yo lo corregí
[COMPLETAR con un caso REAL que hayas visto al probar. Ideas para buscar uno:
 - ¿La regex aceptaba `2025-13-45` como fecha válida? (una regex sola no valida el calendario)
 - ¿Contaba `[ERROR] 2025-01-11` (sin mensaje) como evento bueno?
 - ¿Aceptaba `[info]` en minúscula sin que tú lo decidieras?
 Describe: qué sugirió, cómo lo detectaste, cómo lo corregiste.]

### 4. Qué aprendí
[COMPLETAR con tus palabras: IA como herramienta, no como reemplazo]
