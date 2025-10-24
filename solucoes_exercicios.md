# Soluções dos Exercícios de Damas Brasileiras

## Exercício 1
**FEN:** `W:Wa1,b2,c3:Ba5,e5,g7.`

**Posição Inicial:**
- Brancas: Dama em a1, peões em b2 e c3
- Pretas: peões em a5, e5 e g7

**Solução:**
```
d2-e3 → g7-f6 → a1-b2 → f6-g5 → e3-d4 → e5-f4 → b2-a3 → g5-h4 →
d4-c5 → h4-g3 → c3-d4 → g3-f2 → c5-d6 → f2-e1 → d4-e5 → f4-e3 →
e5-f6 → e3-d2 → d6-c7 → d2-c1
```
**Total de lances:** 20

---

## Exercício 2
**FEN:** `W:Wa1,b2,c3,h4:Ba5,e5,f6,g7.`

**Posição Inicial:**
- Brancas: Dama em a1, peões em b2, c3 e h4
- Pretas: peões em a5, e5, f6 e g7

**Solução:**
```
a1-b2 → h6-g5 → b2-a3 → g7-h6 → d2-e3 → g5-f4 → e3xg5 → h6xf4 →
a3-b4 → f4-e3 → b4-c5 → e3-f2 → c5-d6 → e5xc7 → a5-b6 → c7-d6 →
b6-a7 → d6-c5 → a7-b8 → f2-e1
```
**Total de lances:** 20

**Capturas nesta linha:** e3xg5, h6xf4, e5xc7

---

## Exercício 3
**FEN:** `W:Wa1,g1,b2,c3,b4,h4:Bd4,a5,e5,f6,g7,f8.`

**Posição Inicial:**
- Brancas: Damas em a1 e g1, peões em b2, c3, b4 e h4
- Pretas: peões em d4, a5, e5, f6, g7 e f8

**Solução:**
```
d4xf6 → g7xe5 → a1-b2 → h8-g7 → a5-b6 → a5xc7 → g1-f2 → h6-g5 →
b2-a3 → g5-h4 → a3-b4 → f4-g3 → c3-d4 → g3xa5 → d4xh8 → h4-g3 →
h8-g7 → a5-b4 → g7-f6 → c7-b6
```
**Total de lances:** 20

**Capturas nesta linha:** d4xf6, g7xe5, a5xc7, g3xa5, d4xh8

---

## Exercício 4
**FEN:** `W:Wa1,g1,b2,f2,c3,h4:Bd4,a5,e5,d6,f6,e7.`

**Posição Inicial:**
- Brancas: Damas em a1 e g1, peões em b2, f2, c3 e h4
- Pretas: peões em d4, a5, e5, d6, f6 e e7

**Solução:**
```
a1-b2 → e7-d6 → g1-f2 → f6-g5 → f2-g3 → f4-e3 → d2xf4 → g5xe3 →
b2-a3 → d6-c5 → a5-b6 → a5xc7 → g3-f4 → e3xg5 → h2-g3 → c7-d6 →
g3-h4 → g5-f4 → c3-b4 → f4-e3
```
**Total de lances:** 20

**Capturas nesta linha:** d2xf4, g5xe3, a5xc7, e3xg5

---

## Exercício 5
**FEN:** `W:We1,f2:Bb4,f4,b6,d6.`

**Posição Inicial:**
- Brancas: Dama em e1, peão em f2
- Pretas: peões em b4, f4, b6 e d6

**Solução:**
```
h2-g3
```
**Total de lances:** 1

---

## Observações

Este solver foi desenvolvido especificamente para resolver exercícios de damas brasileiras (8x8) usando algoritmo minimax com poda alpha-beta. As soluções apresentadas representam as melhores sequências de movimentos encontradas pelo motor a uma profundidade de busca de 12 níveis.

**Notação utilizada:**
- `a1-b2`: movimento simples da casa a1 para casa b2
- `e3xg5`: captura da casa e3 para casa g5 (com "x")
- As casas são identificadas por letra (a-h) + número (1-8)

**Gerado em:** 2025-10-24
**Motor:** Solver Damas Brasileiras v1.0
