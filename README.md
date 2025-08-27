# Proyecto 2 – SAT por Fuerza Bruta y DPLL (Python)

Este repositorio contiene dos programas para resolver Satisfacibilidad Booleana (SAT) sobre fórmulas en **Forma Normal Conjuntiva (CNF)**:

- **Programa 1:** `bruteforce.py` — Enumeración exhaustiva (fuerza bruta).
- **Programa 2:** `dpll.py` — Implementación sencilla del algoritmo **DPLL**.

> **Nota:** Ambos programas cumplen el enunciado del proyecto: leer una fórmula en **forma clausal (CNF)** y devolver si es **satisfacible** junto con una **asignación (modelo)**, o **insatisfacible** con asignación vacía.

---

## ¿Qué es la entrada en forma clausal (CNF)?

La CNF se representa como **lista de cláusulas**, donde cada cláusula es una **lista de literales**.

- Literal positivo: `"p"`
- Literal negado: `"~p"`

**Ejemplo:**  
\[(p \lor q) \land (\lnot p \lor r)\]  
en JSON se escribe como:

```json
[["p","q"],["~p","r"]]
```

---

## Uso rápido (CLI)

### 1) Pasar la CNF en línea (`--expr`)
```bash
python bruteforce.py --expr '[["p","q"],["~p","r"]]'
python dpll.py       --expr '[["p","q"],["~p","r"]]'
```

### 2) Leer desde archivo (`--input`)
```bash
python bruteforce.py --input entrada.json
python dpll.py       --input entrada.json
```

### 3) Leer desde `stdin`
```bash
# Pega el JSON y termina con Ctrl+D (Linux/Mac) o Ctrl+Z y Enter (Windows)
python bruteforce.py
[["p","q"],["~p","r"]]
```

---

## Estructura del repositorio

```
.
├─ bruteforce.py   # Programa 1: Fuerza bruta (SAT)
├─ dpll.py         # Programa 2: DPLL sencillo
├─ entrada.json    # (Ejemplo) CNF: [["p","q"],["~p","r"]]
└─ README.md
```

---

## Programa 1 — `bruteforce.py` (Fuerza bruta)

### ¿Qué hace?
- Extrae variables de la CNF.
- Genera **todas las combinaciones** posibles (2^n).
- Evalúa cada cláusula (OR) y la fórmula (AND).
- Devuelve el **primer modelo** que satisface la fórmula o UNSAT si no existe.

### Salida (ejemplo real)
Entrada: `entrada.json` con `[[\"p\",\"q\"],[\"~p\",\"r\"]]`

```json
{
  "satisfiable": true,
  "assignment": {
    "p": false,
    "q": true,
    "r": false
  }
}
```

> **Nota:** este modelo puede variar (hay más de una solución). La fuerza bruta devuelve la **primera** que encuentra.

### Complejidad
- En el peor caso, **O(2^n)** asignaciones, donde *n* es el número de variables.

---

## Programa 2 — `dpll.py` (Algoritmo DPLL sencillo)

### ¿Qué hace?
- Aplica **casos base**: fórmula vacía ⇒ SAT; cláusula vacía ⇒ UNSAT.
- **Selecciona** un literal en forma positiva.
- **Simplifica** la CNF al afirmar el literal (elimina cláusulas satisfechas y borra el literal complementario en el resto).
- **Ramifica**: prueba primero con L=True; si falla, prueba con L=False (backtracking).

### Salida (ejemplo real)
Misma entrada `entrada.json` con `[[\"p\",\"q\"],[\"~p\",\"r\"]]`

```json
{
  "satisfiable": true,
  "assignment": {
    "q": true,
    "p": true,
    "r": true
  }
}
```

> **Nota:** Puede devolver **otro modelo** distinto al de fuerza bruta, y sigue siendo válido si satisface la CNF.

---

## Formato de entrada (JSON)

- **Lista** de **cláusulas** (listas de literales como strings).  
- Literales: `"x"` o `"~x"`.

Ejemplos:
```json
[["p"]]                   // p
[["p","q"],["~p","r"]]    // (p ∨ q) ∧ (¬p ∨ r)
[["p","~p"]]              // cláusula tautológica: siempre verdadera
[["p"],["~p"]]            // UNSAT: {p} ∧ {¬p}
```

---

## Detalles de implementación

### `bruteforce.py`
- `simplify_cnf`: elimina tautologías y duplicados (no altera satisfacibilidad).
- `eval_literal / eval_clause / eval_cnf`: evaluación booleana bajo una asignación.
- `bruteforce_sat`: recorre todas las asignaciones (con `itertools.product`).

### `dpll.py`
- `simplify(B, L)`: condiciona la CNF con L=True (elimina cláusulas con L y quita ~L en las demás).
- `pick_literal_positive`: elige un literal **positivo** (heurística simple, alineada al enunciado).
- `dpll(B, I)`: Recursión con casos base + ramificación y poda.

---

## Diferencias clave (Brute Force vs DPLL)

| Aspecto           | Fuerza Bruta                      | DPLL                                 |
|-------------------|-----------------------------------|--------------------------------------|
| Estrategia        | Prueba **todas** las combinaciones| **Poda** y **simplifica** en cada paso |
| Complejidad       | Exponencial (2^n)                 | Mucho menor en práctica               |
| Modelo devuelto   | El primero que encuentre          | El primero que satisfaga tras poda   |
| Implementación    | Simple                            | Recursiva con backtracking           |

> Ambos pueden devolver **modelos distintos**, y todos son correctos si satisfacen la CNF.


