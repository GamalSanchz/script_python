# Analizador de logs en Python — Semana 2 (KODIGO)

## Cómo ejecutarlo
    python analizador_logs.py                # abre selector de archivos
    python analizador_logs.py log_bueno.txt  # ruta directa

## Reglas de validación (decisiones mías)
| Regla | Decisión | Por qué |
|---|---|---|
| Línea vacía | Se ignora | No es un evento ni un error |
| Nivel | Solo `[INFO]`, `[WARNING]`, `[ERROR]` en mayúsculas | Prefiero un criterio estricto y predecible; cualquier otro nivel se considera mal formateado |
| Sin fecha | Cuenta como evento, marcado "sin fecha" | Tiene severidad y mensaje, sigue siendo útil |
| Fecha inválida | Cuenta como evento, marcado "fecha inválida" | Igual: falla solo la marca de tiempo |
| Sin mensaje / sin nivel | Línea mal formateada | Información incompleta |

Casos borde que NO manejo: logs multilínea, horas (HH:MM:SS), niveles extra (DEBUG).

## Evidencia de pruebas

### Archivo 1: log_bueno.txt (5 líneas válidas)
- Esperado: 5 eventos (3 INFO, 1 WARNING, 1 ERROR) y 0 malformadas.
- Obtenido: coincide.

### Archivo 2: log_con_errores.txt (12 líneas con casos mezclados)
- Esperado: 5 eventos (2 INFO, 2 WARNING, 1 ERROR), 1 sin fecha, 2 con fecha inválida, 6 malformadas y 1 vacía ignorada.
- Obtenido: coincide.

### Archivo 3: archivo inexistente
- Esperado: mensaje de error sin que el programa se caiga.
- Obtenido: coincide.

## Reflexión técnica

### 1. Qué apoyó la IA
La IA me ayudó más que todo a arrancar. Le pedí ideas para reconocer el nivel de cada línea (INFO, WARNING, ERROR) y la fecha, y me sugirió cómo ordenar el programa en funciones pequeñas en lugar de hacer todo en un solo bloque. También me ayudó con la ventana para escoger el archivo, que era algo que no había hecho antes. Y cuando había una parte del código que no entendía, le pedía que me explicara para qué servía, no necesariamente cómo funcionaba por dentro.

### 2. Qué decidí yo
Todas las reglas de qué está bien y qué está mal las decidí yo. Lo pensé así: si a una línea le falta la fecha pero tiene el nivel y el mensaje, igual es un evento útil, así que la cuento pero la marco como "sin fecha". Lo mismo con una fecha imposible, como el mes 13. En cambio, si a la línea le falta el nivel o el mensaje, la considero mal formateada, porque le falta información importante. También decidí ser estricto con los niveles: solo acepto los tres en mayúsculas, y cualquier otro (como DEBUG) cuenta como mal formateado. Dejé fuera casos más complicados, como errores de varias líneas o horas exactas, porque la tarea no los pide y solo iban a complicar el código.

### 3. Ejemplo concreto: la IA se equivocó y yo lo corregí
Cuando le pedí a la IA una forma de revisar las fechas, me dio una fórmula que se veía bien y funcionaba con las fechas normales. Pero al probar con mi archivo de errores me di cuenta de que aceptaba una fecha como 2025-13-45 como si fuera válida, aunque no existe el mes 13 ni el día 45. Lo que pasaba es que solo revisaba que "se viera como una fecha", no que lo fuera de verdad. Lo corregí agregando una segunda revisión que confirma que la fecha realmente exista en el calendario. Con eso, esa línea ahora aparece como "fecha inválida".

### 4. Qué aprendí sobre usar IA
Aprendí que la IA es como un compañero rápido que propone cosas, pero no siempre acierta y no sabe qué quiero yo exactamente. Lo que me dio funcionaba en los casos normales, y los problemas solo aparecieron cuando probé con datos malos a propósito. Si hubiera copiado y pegado sin probar, habría entregado algo que parecía bien y no lo estaba. Me quedo con que la IA me ahorra tiempo escribiendo, pero yo soy quien decide qué es un error y quien tiene que comprobar que todo funcione.