from typing import Dict, List

from modelos import RecorridoMaquina


# ============================================================
# AFD PARA ORFs
# Este autómata es el determinista obtenido por subconjuntos.
# Estados:
# {q0}, {q1}, {q2}, {q3,q9}, {q4}, {q5}, {q6,q10},
# {q7,q11}, {q8,q12}, {qf}, ∅
# ============================================================

ALFABETO = frozenset({"A", "C", "G", "T"})
ESTADO_INICIAL = "{q0}"
ESTADOS_DE_ACEPTACION = frozenset({"{qf}"})
ESTADO_MUERTO = "∅"

TRANSICIONES: Dict[str, Dict[str, str]] = {
    "{q0}": {
        "A": "{q1}",
        "C": "∅",
        "G": "∅",
        "T": "∅",
    },
    "{q1}": {
        "A": "∅",
        "C": "∅",
        "G": "∅",
        "T": "{q2}",
    },
    "{q2}": {
        "A": "∅",
        "C": "∅",
        "G": "{q3,q9}",
        "T": "∅",
    },
    "{q3,q9}": {
        "A": "{q4}",
        "C": "{q4}",
        "G": "{q4}",
        "T": "{q6,q10}",
    },
    "{q4}": {
        "A": "{q5}",
        "C": "{q5}",
        "G": "{q5}",
        "T": "{q5}",
    },
    "{q5}": {
        "A": "{q3,q9}",
        "C": "{q3,q9}",
        "G": "{q3,q9}",
        "T": "{q3,q9}",
    },
    "{q6,q10}": {
        "A": "{q7,q11}",
        "C": "{q5}",
        "G": "{q8,q12}",
        "T": "{q5}",
    },
    "{q7,q11}": {
        "A": "{qf}",
        "C": "{q3,q9}",
        "G": "{qf}",
        "T": "{q3,q9}",
    },
    "{q8,q12}": {
        "A": "{qf}",
        "C": "{q3,q9}",
        "G": "{q3,q9}",
        "T": "{q3,q9}",
    },
    "{qf}": {
        "A": "∅",
        "C": "∅",
        "G": "∅",
        "T": "∅",
    },
    "∅": {
        "A": "∅",
        "C": "∅",
        "G": "∅",
        "T": "∅",
    },
}


def simular_afd(secuencia: str) -> RecorridoMaquina:
    """
    Recorre la secuencia símbolo por símbolo usando la tabla de transición.
    Si aparece un símbolo fuera del alfabeto, la máquina cae al estado muerto.
    """
    estado_actual = ESTADO_INICIAL
    estados_visitados: List[str] = [estado_actual]

    for simbolo in secuencia:
        if simbolo not in ALFABETO:
            estado_actual = ESTADO_MUERTO
            estados_visitados.append(estado_actual)
            return RecorridoMaquina(
                aceptada=False,
                estado_final=estado_actual,
                estados_visitados=estados_visitados,
            )

        estado_actual = TRANSICIONES[estado_actual][simbolo]
        estados_visitados.append(estado_actual)

    return RecorridoMaquina(
        aceptada=estado_actual in ESTADOS_DE_ACEPTACION,
        estado_final=estado_actual,
        estados_visitados=estados_visitados,
    )