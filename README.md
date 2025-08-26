# Proyecto 2 – Programa 1: Fuerza Bruta SAT

##  Lo que pide el enunciado

“Realice un programa en Python que implemente un algoritmo utilizando fuerza bruta, donde la entrada sea una fórmula booleana en forma de cláusula y devuelva falsa con asignación vacía o nula (en caso de ser insatisfacible) o devuelva verdadero con la asignación correspondiente (en caso de ser satisfacible)”.

---

##  Cómo lo cumple el código (`bruteforce.py`)

### Entrada en forma clausal (CNF)
El archivo `entrada.json` contiene:

```json
[["p","q"],["~p","r"]]
Eso corresponde a la fórmula:

(𝑝∨𝑞)∧(¬𝑝∨𝑟)


En el código, la función _load_cnf_from_json_like convierte esa lista en la estructura interna CNF (listas de conjuntos de literales).

