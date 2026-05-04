from typing import Optional

from afd import ALFABETO, simular_afd
from kmp import buscar_patron
from modelos import (
    CoincidenciasPatrones,
    RegistroFasta,
    ResultadoValidacion,
)


# ============================================================
# REGLAS BIOLÓGICAS DE VALIDACIÓN
# Una ORF válida debe:
# - empezar con ATG
# - terminar con TAA, TAG o TGA
# - tener longitud múltiplo de 3
# - no tener codones stop intermedios
# - contener solo símbolos del alfabeto {A,C,G,T}
# ============================================================

CODON_INICIO = "ATG"
CODONES_STOP = {"TAA", "TAG", "TGA"}


class SimboloInvalido:
    """
    Representa el primer símbolo inválido encontrado en la secuencia.
    """

    def __init__(self, simbolo: str, posicion: int) -> None:
        self.simbolo = simbolo
        self.posicion = posicion


def validar_registro(registro: RegistroFasta) -> ResultadoValidacion:
    """
    Aplica todas las reglas del problema a un registro FASTA.
    """
    secuencia = registro.secuencia.upper()
    coincidencias = buscar_codones_relevantes(secuencia)

    simbolo_invalido = encontrar_simbolo_invalido(secuencia)
    if simbolo_invalido is not None:
        return construir_resultado(
            registro=registro,
            secuencia_normalizada=secuencia,
            es_valida=False,
            motivo=(
                f"Contiene símbolo inválido '{simbolo_invalido.simbolo}' "
                f"en la posición {simbolo_invalido.posicion}."
            ),
            coincidencias=coincidencias,
        )

    if not secuencia.startswith(CODON_INICIO):
        return construir_resultado(
            registro=registro,
            secuencia_normalizada=secuencia,
            es_valida=False,
            motivo="No empieza con ATG.",
            coincidencias=coincidencias,
        )

    if len(secuencia) < 6:
        return construir_resultado(
            registro=registro,
            secuencia_normalizada=secuencia,
            es_valida=False,
            motivo="Secuencia incompleta: no alcanza para codón de inicio y codón stop.",
            coincidencias=coincidencias,
        )

    if len(secuencia) % 3 != 0:
        return construir_resultado(
            registro=registro,
            secuencia_normalizada=secuencia,
            es_valida=False,
            motivo="No respeta el marco de lectura: la longitud no es múltiplo de 3.",
            coincidencias=coincidencias,
        )

    if secuencia[-3:] not in CODONES_STOP:
        return construir_resultado(
            registro=registro,
            secuencia_normalizada=secuencia,
            es_valida=False,
            motivo="No termina con un codón stop válido.",
            coincidencias=coincidencias,
        )

    posicion_stop_intermedio = encontrar_stop_intermedio(secuencia)
    if posicion_stop_intermedio is not None:
        return construir_resultado(
            registro=registro,
            secuencia_normalizada=secuencia,
            es_valida=False,
            motivo=f"Tiene un codón stop intermedio en la posición {posicion_stop_intermedio}.",
            coincidencias=coincidencias,
        )

    recorrido_afd = simular_afd(secuencia)
    if recorrido_afd.aceptada:
        return ResultadoValidacion(
            nombre_registro=registro.nombre,
            secuencia=secuencia,
            es_valida=True,
            motivo="ORF válida.",
            coincidencias=coincidencias,
            recorrido_afd=recorrido_afd,
        )

    return ResultadoValidacion(
        nombre_registro=registro.nombre,
        secuencia=secuencia,
        es_valida=False,
        motivo="La cadena fue rechazada por el AFD.",
        coincidencias=coincidencias,
        recorrido_afd=recorrido_afd,
    )


def buscar_codones_relevantes(secuencia: str) -> CoincidenciasPatrones:
    """
    Usa KMP para localizar el codón de inicio y los codones stop.
    """
    return CoincidenciasPatrones(
        posiciones_atg=buscar_patron(secuencia, "ATG"),
        posiciones_taa=buscar_patron(secuencia, "TAA"),
        posiciones_tag=buscar_patron(secuencia, "TAG"),
        posiciones_tga=buscar_patron(secuencia, "TGA"),
    )


def construir_resultado(
    registro: RegistroFasta,
    secuencia_normalizada: str,
    es_valida: bool,
    motivo: str,
    coincidencias: CoincidenciasPatrones,
) -> ResultadoValidacion:
    """
    Centraliza la construcción del resultado final y deja el AFD
    siempre disponible para trazabilidad.
    """
    recorrido_afd = simular_afd(secuencia_normalizada)

    return ResultadoValidacion(
        nombre_registro=registro.nombre,
        secuencia=secuencia_normalizada,
        es_valida=es_valida,
        motivo=motivo,
        coincidencias=coincidencias,
        recorrido_afd=recorrido_afd,
    )


def encontrar_simbolo_invalido(secuencia: str) -> Optional[SimboloInvalido]:
    """
    Devuelve el primer símbolo que no pertenece al alfabeto del ADN.
    """
    for posicion, simbolo in enumerate(secuencia):
        if simbolo not in ALFABETO:
            return SimboloInvalido(simbolo=simbolo, posicion=posicion)
    return None


def encontrar_stop_intermedio(secuencia: str) -> Optional[int]:
    """
    Busca un codón stop interno en el mismo marco de lectura.

    Se empieza desde la posición 3 porque los primeros 3 caracteres son ATG.
    Se excluye el último codón porque ese sí debe ser el stop final válido.
    """
    for indice in range(3, len(secuencia) - 3, 3):
        codon = secuencia[indice:indice + 3]
        if codon in CODONES_STOP:
            return indice
    return None