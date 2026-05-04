import os
from lector_fasta import leer_registros_fasta
from orf import validar_registro

# Leer el FASTA, validar cada registro y mostrar el resumen final

RUTA_ARCHIVO_FASTA = os.path.join(os.path.dirname(__file__), "secuencias.fasta")


def imprimir_resumen(resultados) -> None:
    """
    Imprime el estado de cada registro y el total de cadenas válidas.
    """
    total_validas = 0

    print("\n========== RESULTADOS DE VALIDACIÓN ==========")

    for resultado in resultados:
        estado = "válido" if resultado.es_valida else "inválido"

        print(f"{resultado.nombre_registro} -> {estado}")
        print(f"Secuencia: {resultado.secuencia}")
        print(f"Motivo: {resultado.motivo}")
        print(f"ATG encontrado en: {resultado.coincidencias.posiciones_atg}")
        print(f"TAA encontrado en: {resultado.coincidencias.posiciones_taa}")
        print(f"TAG encontrado en: {resultado.coincidencias.posiciones_tag}")
        print(f"TGA encontrado en: {resultado.coincidencias.posiciones_tga}")
        print(f"Recorrido del AFD: {' -> '.join(resultado.recorrido_afd.estados_visitados)}")
        print("-" * 60)

        if resultado.es_valida:
            total_validas += 1

    print(f"Total de cadenas válidas: {total_validas}")


def main() -> None:
    """
    Ejecuta el flujo principal del programa usando una ruta fija.
    Si quieres probar otro archivo, cambia el valor de RUTA_ARCHIVO_FASTA.
    """
    registros = leer_registros_fasta(RUTA_ARCHIVO_FASTA)
    resultados = [validar_registro(registro) for registro in registros]
    imprimir_resumen(resultados)


if __name__ == "__main__":
    main()