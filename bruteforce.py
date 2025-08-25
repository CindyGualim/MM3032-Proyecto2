#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bruteforce.py — Programa 1 (Fuerza bruta) para SAT en forma clausal (CNF).

Qué hace (requisitos del PDF “Algoritmo_DPLL.pdf” - Programa 1):
- Entrada: fórmula booleana en **forma clausal (CNF)** representada como lista de cláusulas;
  cada cláusula es un conjunto (o lista) de literales.
  * Literal positivo: "p"
  * Literal negado  : "~p"
  Ej.: (p ∨ q) ∧ (¬p ∨ r)  =>  [{"p","q"}, {"~p","r"}]
- Salida:
  * Si es insatisfacible: (False, {})  -> "False" y asignación vacía
  * Si es satisfacible  : (True,  I )  -> "True" y un modelo (diccionario var->bool)

Cómo se evalúa una CNF:
- Una **cláusula** (OR) es verdadera si **algún** literal es verdadero.
- La **fórmula** (AND) es verdadera si **todas** las cláusulas son verdaderas.

Este archivo también incluye una interfaz de línea de comandos para correrlo desde terminal.
Ejemplos de uso (sin instalar nada):
    # 1) Pasando la CNF como JSON en una sola línea:
    python bruteforce.py --expr '[["p","q"],["~p","r"]]'

    # 2) Pasando la CNF en un archivo JSON (lista de listas de strings):
    python bruteforce.py --input ejemplos_cnf.json

    # 3) Leer desde stdin (pegar JSON y presionar Ctrl+D/Ctrl+Z):
    python bruteforce.py

Formato JSON esperado por la CLI:
- Una lista de cláusulas; cada cláusula es una lista de literales.
  Ej.: [["p","q"],["~p","r"]]   ó   [["p"],["~p"]]

Complejidad aproximada:
- Si hay n variables, se prueban 2^n asignaciones;
  cada verificación evalúa todas las cláusulas y literales dentro de ellas.
- En notación grande: O( 2^n * (m * k) ), donde m=#cláusulas, k=tamaño promedio de cláusula.

NOTA: Este programa es independiente del DPLL (Programa 2). Aquí solo resolvemos por fuerza bruta.
"""

from __future__ import annotations

import argparse
import itertools
import json
from typing import Dict, Iterable, List, Sequence, Set, Tuple


Literal = str               # "p" o "~p"
Clause = Set[Literal]       # p.ej. {"p", "~q", "r"}
CNF = List[Clause]          # p.ej. [{"p","q"}, {"~p","r"}]
Assignment = Dict[str, bool]


# -------------------------------
# Utilidades sobre literales
# -------------------------------

def base_var(lit: Literal) -> str:
    """Devuelve el nombre base de la variable de un literal.
    - base_var("p")  -> "p"
    - base_var("~p") -> "p"
    """
    return lit[1:] if lit.startswith("~") else lit


def is_negated(lit: Literal) -> bool:
    """Indica si el literal está negado (tiene prefijo '~')."""
    return lit.startswith("~")


# -------------------------------
# Evaluación de CNF
# -------------------------------

def eval_literal(lit: Literal, I: Assignment) -> bool:
    """Evalúa un literal bajo una asignación I.
    Requiere que la variable base exista en I.
    - "p"  es True  si I["p"] es True
    - "~p" es True  si I["p"] es False
    """
    v = I[base_var(lit)]
    return (not v) if is_negated(lit) else v


def eval_clause(clause: Clause, I: Assignment) -> bool:
    """Una cláusula (OR) es verdadera si algún literal es verdadero."""
    # Convención: una cláusula *vacía* es FALSA (no hay literal que la haga verdadera).
    if len(clause) == 0:
        return False
    return any(eval_literal(lit, I) for lit in clause)


def eval_cnf(cnf: CNF, I: Assignment) -> bool:
    """La fórmula CNF (AND de cláusulas) es verdadera si TODAS las cláusulas son verdaderas."""
    return all(eval_clause(c, I) for c in cnf)


# -------------------------------
# Pre-simplificación ligera (opcional pero útil)
# -------------------------------

def simplify_cnf(cnf: CNF) -> CNF:
    """Realiza limpiezas seguras:
    - Elimina cláusulas tautológicas (contienen p y ~p).
    - Elimina literales duplicados dentro de una cláusula (al ser sets, ya viene sin duplicados).
    - Elimina cláusulas duplicadas.
    Estas transformaciones no cambian la satisfacibilidad.
    """
    simplified: List[Clause] = []
    for clause in cnf:
        # Si es lista, conviértela a set; si ya es set, cópiala
        cset = set(clause)
        # ¿Tautológica? (contiene variable y su negación)
        bases = {base_var(l) for l in cset}
        is_tautology = any((v in bases and ("~" + v) in cset and v in cset)  # (p y ~p explícitos)
                           or (("~" + v) in cset and v in cset)              # forma estándar
                           for v in bases)
        if is_tautology:
            continue  # quitar cláusula tautológica

        simplified.append(cset)

    # Quitar cláusulas duplicadas (congelándolas)
    unique = list({frozenset(c) for c in simplified})
    # Restaurar a sets mutables
    return [set(fc) for fc in unique]


def variables_from_cnf(cnf: CNF) -> List[str]:
    """Extrae y devuelve la lista ORDENADA de variables presentes en la CNF."""
    vars_set = {base_var(lit) for clause in cnf for lit in clause}
    return sorted(vars_set)


# -------------------------------
# Algoritmo de fuerza bruta
# -------------------------------

def bruteforce_sat(cnf: CNF) -> Tuple[bool, Assignment]:
    """Resuelve SAT por enumeración exhaustiva.

    Entrada:
        cnf: fórmula en forma clausal (lista de cláusulas; cada cláusula es un set/lista de literales).

    Salida:
        (False, {}) si la CNF es insatisfacible.
        (True,  I ) si la CNF es satisfacible, con I un diccionario {variable: bool}.

    Casos límite tratados:
    - CNF vacía (sin cláusulas): True con asignación vacía (fórmula "verdadera" por convención).
    - Alguna cláusula vacía: no hay manera de satisfacerla -> UNSAT inmediato.
    """
    cnf = simplify_cnf(cnf)

    # Caso: CNF vacía (tras quitar tautologías) => verdadera
    if len(cnf) == 0:
        return True, {}

    # Si existe una cláusula vacía, la fórmula es imposible
    if any(len(c) == 0 for c in cnf):
        return False, {}

    vars_list = variables_from_cnf(cnf)
    n = len(vars_list)

    # Enumerar TODAS las asignaciones posibles de n variables (2^n combinaciones)
    for values in itertools.product([False, True], repeat=n):
        I = dict(zip(vars_list, values))
        if eval_cnf(cnf, I):
            return True, I

    # Ninguna asignación satisfizo la fórmula
    return False, {}


# -------------------------------
# CLI (interfaz de línea de comandos)
# -------------------------------

def _load_cnf_from_json_like(obj: Iterable[Iterable[str]]) -> CNF:
    """Convierte una estructura tipo JSON (lista de listas de strings) a la representación interna (List[Set[str]])."""
    cnf: CNF = []
    for clause in obj:
        cnf.append(set(clause))
    return cnf


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Programa 1 — SAT por fuerza bruta sobre fórmulas en forma clausal (CNF)."
    )
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--input", "-i", type=str, help="Ruta a archivo JSON con la CNF (lista de listas de literales).")
    g.add_argument("--expr", "-e", type=str, help="CNF en JSON inline. Ej.: '[[\"p\",\"q\"],[\"~p\",\"r\"]]'")

    args = parser.parse_args(argv)

    # Leer CNF según el origen elegido
    if args.expr:
        data = json.loads(args.expr)
    elif args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        # Leer desde stdin
        data = json.load(sys.stdin)

    cnf = _load_cnf_from_json_like(data)

    sat, model = bruteforce_sat(cnf)
    out = {"satisfiable": sat, "assignment": model}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main())
