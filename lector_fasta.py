from pathlib import Path
from typing import List, Optional

from modelos import RegistroFasta


def leer_registros_fasta(ruta_archivo: str) -> List[RegistroFasta]:
    """
    Lee un archivo FASTA y devuelve una lista de registros.
    """
    # Se verifica que el archivo realmente exista antes de intentar procesarlo
    ruta = Path(ruta_archivo)

    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo FASTA: {ruta_archivo}")

    # Se inicializa la lista final de registros y las variables temporales para ir construyendo cada registro iterativamente
    registros: List[RegistroFasta] = []
    nombre_actual: Optional[str] = None
    lineas_secuencia: List[str] = []

    # Se lee el archivo línea por línea asegurando su correcta codificación
    with ruta.open("r", encoding="utf-8") as archivo_fasta:
        for linea_cruda in archivo_fasta:
            # Se limpian los caracteres de salto de línea al final de cada cadena
            linea = linea_cruda.rstrip("\n").rstrip("\r")

            if not linea:
                continue

            # Las líneas que inician con '>' indican un nuevo registro
            if linea.startswith(">"):
                # Si ya se estaba procesando una secuencia anterior, se ensambla y se guarda
                if nombre_actual is not None:
                    registros.append(
                        RegistroFasta(
                            nombre=nombre_actual,
                            secuencia="".join(lineas_secuencia),
                        )
                    )

                # Se extrae el nombre del nuevo registro y se reinicia el acumulador de secuencias
                nombre_actual = linea[1:].strip()
                lineas_secuencia = []
                continue

            # Las líneas que contienen la secuencia biológica se van guardando temporalmente
            lineas_secuencia.append(linea)

    # Al terminar de leer el archivo, es necesario guardar el último registro que quedó en memoria
    if nombre_actual is not None:
        registros.append(
            RegistroFasta(
                nombre=nombre_actual,
                secuencia="".join(lineas_secuencia),
            )
        )

    # Retorno de resultados
    return registros