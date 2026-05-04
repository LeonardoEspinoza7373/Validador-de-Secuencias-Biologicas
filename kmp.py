from typing import List


# ============================================================
# LPS + KMP
# Este módulo implementa exactamente la lógica pedida:
# 1. construir el arreglo LPS
# 2. buscar patrones dentro de una cadena
# ============================================================

def construir_lps(patron: str) -> List[int]:
    """
    Construye el arreglo LPS (Longest Prefix Suffix).

    LPS[i] guarda la longitud del prefijo propio más largo
    que también es sufijo en patron[0:i+1].
    """
    # Tamaño del patrón (m)
    longitud_patron = len(patron)

    # lps[i] = longitud del prefijo propio más largo que también es sufijo
    # dentro de patron[0:i+1]. Se inicializa en 0 porque para i=0 siempre vale 0.
    lps = [0] * longitud_patron

    # longitud_prefijo = cuántos caracteres (desde el inicio del patrón)
    # ya sabemos que coinciden como prefijo/sufijo.
    longitud_prefijo = 0

    # indice recorre el patrón; empieza en 1 porque lps[0] se queda en 0.
    indice = 1

    while indice < longitud_patron:
        # Caso 1: el siguiente carácter continúa el prefijo actual.
        if patron[indice] == patron[longitud_prefijo]:
            longitud_prefijo += 1
            lps[indice] = longitud_prefijo
            indice += 1
            continue

        # Caso 2: hay desacuerdo, pero ya teníamos un prefijo parcial.
        # Retrocedemos longitud_prefijo usando la información de LPS.
        # Importante: NO movemos 'indice' para reintentar con un prefijo más corto.
        if longitud_prefijo != 0:
            longitud_prefijo = lps[longitud_prefijo - 1]
            continue

        # Caso 3: hay desacuerdo y no hay prefijo parcial.
        # Entonces lps[indice] debe ser 0 y avanzamos.
        lps[indice] = 0
        indice += 1

    return lps


def buscar_patron(texto: str, patron: str) -> List[int]:
    """
    Busca todas las ocurrencias de 'patron' dentro de 'texto'
    usando el algoritmo KMP.

    Retorna una lista con los índices iniciales de cada coincidencia.
    """
    # Por convención de este proyecto: patrón vacío no devuelve coincidencias.
    if not patron:
        return []

    longitud_texto = len(texto)
    longitud_patron = len(patron)

    # Preprocesamiento: construimos el arreglo LPS del patrón.
    lps = construir_lps(patron)

    # Lista con los índices (0-based) donde inicia cada coincidencia.
    posiciones_encontradas: List[int] = []

    # índice en el texto (i)
    indice_texto = 0

    # índice en el patrón (j)
    indice_patron = 0

    while indice_texto < longitud_texto:
        # Si el carácter actual coincide, avanzamos en ambos.
        if texto[indice_texto] == patron[indice_patron]:
            indice_texto += 1
            indice_patron += 1

        # Si ya consumimos todo el patrón, encontramos una ocurrencia.
        if indice_patron == longitud_patron:
            # El inicio de la coincidencia es (i - j)
            posiciones_encontradas.append(indice_texto - indice_patron)

            # Para permitir coincidencias solapadas, no reiniciamos a 0;
            # saltamos al mejor prefijo posible usando LPS.
            indice_patron = lps[indice_patron - 1]
            continue

        # Si hay desacuerdo (mismatch) y todavía hay texto por analizar...
        if indice_texto < longitud_texto and texto[indice_texto] != patron[indice_patron]:
            # Si ya habíamos avanzado algo en el patrón, retrocedemos j usando LPS.
            # Esto evita retroceder en el texto: KMP es O(n).
            if indice_patron != 0:
                indice_patron = lps[indice_patron - 1]
            else:
                # Si j==0, no hay nada que “reutilizar” del patrón: avanzamos i.
                indice_texto += 1

    return posiciones_encontradas
