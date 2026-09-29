import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

NIVELES = ("INFO", "WARNING", "ERROR")

# [NIVEL] + resto de la linea (R2)
PATRON_LINEA = re.compile(r"^\[(INFO|WARNING|ERROR)\]\s*(.*)$")
# Algo que "parece" fecha al inicio del resto: 2025-01-10, 2025-1-10, 10/01/2025...
PATRON_PARECE_FECHA = re.compile(r"^(\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4})(?:\s+(.*))?$")
# Formato estricto exigido (R4)
PATRON_FECHA_ESTRICTA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def seleccionar_archivo():
    """Argumento de consola > ventana de seleccion > input manual."""
    if len(sys.argv) > 1:
        return sys.argv[1]
    try:
        import tkinter as tk
        from tkinter import filedialog
        raiz = tk.Tk()
        raiz.withdraw()
        ruta = filedialog.askopenfilename(
            title="Selecciona el archivo de log",
            filetypes=[("Archivos de texto", "*.txt *.log"), ("Todos", "*.*")],
        )
        raiz.destroy()
        if ruta:
            return ruta
    except Exception:
        pass  # sin entorno grafico: pedimos la ruta por consola
    return input("Ruta del archivo de log: ").strip().strip('"')


def fecha_es_valida(texto):
    """Formato AAAA-MM-DD estricto Y fecha real del calendario."""
    if not PATRON_FECHA_ESTRICTA.match(texto):
        return False
    try:
        datetime.strptime(texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def analizar_linea(linea):
    """
    Devuelve (estado, nivel):
      estado: 'ok' | 'sin_fecha' | 'fecha_invalida' | 'malformada'
      nivel : INFO/WARNING/ERROR, o None si es malformada
    """
    m = PATRON_LINEA.match(linea)
    if not m:
        return "malformada", None                      # R2

    nivel, resto = m.group(1), m.group(2).strip()
    if not resto:
        return "malformada", None                      # R3

    f = PATRON_PARECE_FECHA.match(resto)
    if f:
        fecha, mensaje = f.group(1), (f.group(2) or "").strip()
        if not mensaje:
            return "malformada", None                  # R5
        if fecha_es_valida(fecha):
            return "ok", nivel
        return "fecha_invalida", nivel                 # R4
    return "sin_fecha", nivel                          # R4


def analizar_archivo(ruta):
    resumen = {
        "lineas_vacias": 0,
        "por_nivel": Counter({n: 0 for n in NIVELES}),
        "estados": Counter(),
        "malformadas": [],       # (numero_linea, texto)
        "sin_fecha": [],
        "fecha_invalida": [],
    }
    with open(ruta, "r", encoding="utf-8", errors="replace") as f:
        for num, cruda in enumerate(f, start=1):
            linea = cruda.strip()
            if not linea:
                resumen["lineas_vacias"] += 1          # R1
                continue
            estado, nivel = analizar_linea(linea)
            resumen["estados"][estado] += 1
            if nivel:
                resumen["por_nivel"][nivel] += 1
            if estado in ("malformada", "sin_fecha", "fecha_invalida"):
                resumen[estado if estado != "malformada" else "malformadas"].append((num, linea))
    return resumen


def mostrar_resumen(ruta, r):
    total_eventos = sum(r["por_nivel"].values())
    print("=" * 50)
    print(f" RESUMEN DE LOG: {Path(ruta).name}")
    print("=" * 50)
    print(f" Total de eventos (con nivel valido): {total_eventos}")
    for n in NIVELES:
        print(f"   - {n:<8}: {r['por_nivel'][n]}")
    print("-" * 50)
    print(f" Eventos con fecha valida : {r['estados']['ok']}")
    print(f" Eventos sin fecha        : {r['estados']['sin_fecha']}")
    print(f" Eventos con fecha invalida: {r['estados']['fecha_invalida']}")
    print(f" Lineas mal formateadas   : {r['estados']['malformada']}")
    print(f" Lineas vacias ignoradas  : {r['lineas_vacias']}")

    for titulo, clave in (("MAL FORMATEADAS", "malformadas"),
                          ("SIN FECHA", "sin_fecha"),
                          ("FECHA INVALIDA", "fecha_invalida")):
        if r[clave]:
            print("-" * 50)
            print(f" Detalle - {titulo}:")
            for num, texto in r[clave]:
                print(f"   linea {num}: {texto}")
    print("=" * 50)


def main():
    ruta = seleccionar_archivo()
    if not ruta:
        print("No se selecciono ningun archivo.")
        return
    try:
        resumen = analizar_archivo(ruta)
    except FileNotFoundError:
        print(f"Error: no existe el archivo '{ruta}'.")
        return
    except PermissionError:
        print(f"Error: sin permisos para leer '{ruta}'.")
        return
    if not resumen["estados"]:
        print("Advertencia: el archivo esta vacio o solo tiene lineas en blanco.")
        return
    mostrar_resumen(ruta, resumen)


if __name__ == "__main__":
    main()
