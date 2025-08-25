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
    python bruteforce.py --input entrada.json

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
