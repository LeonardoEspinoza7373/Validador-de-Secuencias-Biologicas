from dataclasses import dataclass
from typing import List


# ============================================================
# MODELOS DE DATOS
# Estos dataclasses permiten que el proyecto sea más claro,
# fácil de mantener y fácil de probar.
# ============================================================

@dataclass(frozen=True)
class RegistroFasta:
    """
    Representa un registro individual del archivo FASTA.
    """
    nombre: str
    secuencia: str


@dataclass(frozen=True)
class CoincidenciasPatrones:
    """
    Guarda las posiciones donde KMP encontró los patrones relevantes.
    """
    posiciones_atg: List[int]
    posiciones_taa: List[int]
    posiciones_tag: List[int]
    posiciones_tga: List[int]


@dataclass(frozen=True)
class RecorridoMaquina:
    """
    Guarda el resultado de la simulación del AFD.
    """
    aceptada: bool
    estado_final: str
    estados_visitados: List[str]


@dataclass(frozen=True)
class ResultadoValidacion:
    """
    Resultado completo de validar una secuencia como ORF.
    """
    nombre_registro: str
    secuencia: str
    es_valida: bool
    motivo: str
    coincidencias: CoincidenciasPatrones
    recorrido_afd: RecorridoMaquina