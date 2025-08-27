#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dpll.py — Programa 2 (Algoritmo DPLL sencillo) para SAT en forma clausal (CNF).

Apegado al PDF “Algoritmo_DPLL.pdf”:
- Caso base: B (CNF) vacía  → True y la asignación parcial I
- Caso base: existe cláusula vacía en B → False y asignación vacía
- Seleccionar literal L **en forma positiva** ("pone en forma positiva")
- Ramificar:
    1) Asignar L=True, simplificar y llamar recursivo.
    2) Si falla, asignar L=False (equivalente a afirmar ~L), simplificar y llamar recursivo.
- Si ambas ramas fallan → False.

Nota: DPLL es no determinista (la elección de L puede variar). Aquí usamos una
heurística mínima: tomamos la **primera cláusula no vacía** y de ella el primer
literal, pero devolviéndolo en forma **positiva** (su variable base).
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Dict, List, Set, Tuple, Sequence

Literal = str
Clause = Set[Literal]
CNF     = List[Clause]
Assignment = Dict[str, bool]


# -------------------------------
# Utilidades
# -------------------------------

def base_var(lit: Literal) -> str:
    return lit[1:] if lit.startswith("~") else lit

def is_negated(lit: Literal) -> bool:
    return lit.startswith("~")

def negate(lit: Literal) -> Literal:
    return base_var(lit) if is_negated(lit) else f"~{lit}"


# -------------------------------
# Simplificación B | L=True
# -------------------------------

def simplify(B: CNF, L: Literal) -> CNF:
    """
    Simplifica la CNF B asumiendo que el literal L es VERDADERO:
      - Elimina todas las cláusulas que contienen L (ya satisfechas).
      - En el resto, elimina la ocurrencia de ~L.
    """
    comp = negate(L)
    new_B: CNF = []
    for clause in B:
        if L in clause:
            continue  # satisfecha
        if comp in clause:
            c2 = set(clause)
            c2.remove(comp)
            new_B.append(c2)
        else:
            new_B.append(set(clause))
    return new_B


# -------------------------------
# Selección de literal (positiva)
# -------------------------------

def pick_literal_positive(B: CNF, I: Assignment) -> Literal:
    """
    Devuelve el nombre de variable (literal positivo) a partir de la primera cláusula no vacía.
    Mantiene la sencillez pedida por el PDF y la indicación de “poner en forma positiva”.
    """
    for clause in B:
        if len(clause) == 0:
            continue
        # primer literal de la cláusula → devolver su variable base en forma positiva
        raw = next(iter(clause))
        return base_var(raw)
    # fallback (no debería ocurrir si se llama correctamente)
    return "p"


# -------------------------------
# DPLL recursivo
# -------------------------------

def dpll(B: CNF, I: Assignment) -> Tuple[bool, Assignment]:
    # Caso 1: fórmula vacía → satisfecha
    if len(B) == 0:
        return True, I

    # Caso 2: existe cláusula vacía → insatisfecha
    if any(len(c) == 0 for c in B):
        return False, {}

    # Elegir literal L en forma positiva (variable base)
    L = pick_literal_positive(B, I)     # e.g. "p"

    # Rama L = True
    I_true = dict(I)
    I_true[L] = True
    B_true = simplify(B, L)             # afirma "p"
    sat, model = dpll(B_true, I_true)
    if sat:
        return True, model

    # Rama L = False  (equivale a afirmar "~p")
    I_false = dict(I)
    I_false[L] = False
    B_false = simplify(B, f"~{L}")
    return dpll(B_false, I_false)


# -------------------------------
# CLI
# -------------------------------

def _load_cnf_from_json_like(obj) -> CNF:
    return [set(clause) for clause in obj]

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Programa 2 — SAT con DPLL sencillo (CNF).")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--input", "-i", type=str, help="Ruta a archivo JSON con la CNF (lista de listas).")
    g.add_argument("--expr", "-e",  type=str, help="CNF en JSON inline. Ej.: '[[\"p\",\"q\"],[\"~p\",\"r\"]]'")
    args = parser.parse_args(argv)

    # cargar datos
    if args.expr:
        data = json.loads(args.expr)
    elif args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    B = _load_cnf_from_json_like(data)

    sat, model = dpll(B, {})
    print(json.dumps({"satisfiable": sat, "assignment": model}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())