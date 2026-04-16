import os
import sys
from datetime import datetime

# ─── Configuración ───────────────────────────────────────────────
ARCHIVO_ENTRADA = "datos.txt"
ARCHIVO_SALIDA  = "resultado.txt"
ARCHIVO_LOG     = "backup.log"
VERSION         = os.environ.get("VERSION", "v1.0")   # se puede pasar por variable de entorno


def leer_archivo(path):
    """Lee el archivo .txt y retorna las líneas."""
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


def limpiar_datos(lineas):
    """
    Limpia y transforma cada línea:
      - Elimina espacios extra en cada campo
      - Descarta filas vacías o sin nombre
      - Descarta filas sin correo
    Retorna (registros_validos, registros_descartados)
    """
    validos    = []
    descartados = 0

    for linea in lineas:
        linea = linea.strip()
        if not linea:
            descartados += 1
            continue

        partes = [p.strip() for p in linea.split(",")]

        # Aseguramos exactamente 3 campos: nombre, edad, correo
        while len(partes) < 3:
            partes.append("")

        nombre, edad, correo = partes[0], partes[1], partes[2]

        # Descartar si falta nombre o correo
        if not nombre or not correo:
            descartados += 1
            continue

        # Normalizar nombre (Title Case)
        nombre = nombre.title()

        # Validar edad numérica; si no es número dejar vacío
        if not edad.isdigit():
            edad = "N/A"

        validos.append(f"{nombre},{edad},{correo}")

    return validos, descartados


def guardar_resultado(path, registros):
    """Escribe el archivo de resultados."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("NOMBRE,EDAD,CORREO\n")
        for r in registros:
            f.write(r + "\n")


def escribir_log(path, archivo_entrada, total_leidos, total_validos, total_descartados, version):
    """Agrega una entrada al backup.log."""
    ahora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    entrada = (
        f"[{ahora}] "
        f"Archivo procesado: {archivo_entrada} | "
        f"Versión: {version} | "
        f"Total leídos: {total_leidos} | "
        f"Válidos: {total_validos} | "
        f"Descartados: {total_descartados} | "
        f"Resultado: Se transformaron/limpiaron {total_validos} registros\n"
    )
    with open(path, "a", encoding="utf-8") as f:
        f.write(entrada)
    print(entrada.strip())


# ─── Main ────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("   Procesador de datos - Transformación/Limpieza")
    print("=" * 55)

    # 1. Leer
    lineas = leer_archivo(ARCHIVO_ENTRADA)
    print(f"✔ Archivo leído: {ARCHIVO_ENTRADA}  ({len(lineas)} líneas)")

    # 2. Limpiar
    registros_validos, descartados = limpiar_datos(lineas)
    print(f"✔ Registros válidos  : {len(registros_validos)}")
    print(f"✔ Registros descartados: {descartados}")

    # 3. Guardar resultado
    guardar_resultado(ARCHIVO_SALIDA, registros_validos)
    print(f"✔ Resultado guardado en: {ARCHIVO_SALIDA}")

    # 4. Registrar en log
    escribir_log(
        ARCHIVO_LOG,
        ARCHIVO_ENTRADA,
        len(lineas),
        len(registros_validos),
        descartados,
        VERSION,
    )
    print(f"✔ Log actualizado en: {ARCHIVO_LOG}")
    print("=" * 55)
