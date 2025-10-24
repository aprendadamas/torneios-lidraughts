# Soluções dos Exercícios de Damas Brasileiras

## Exercício 1
**FEN:** `W:Wa1,b2,c3:Ba5,e5,g7.`

**Posição Inicial:**
- Brancas: Dama em a1, peões em b2 e c3
- Pretas: peões em a5, e5 e g7

**Solução:**
```
6-11 → 28-23 → 1-5 → 23-20 → 11-14 → 19-15 → 5-9 → 20-16 → 14-18 → 16-12 →
10-14 → 12-7 → 18-22 → 7-3 → 14-19 → 15-11 → 19-23 → 11-6 → 22-26 → 6-2
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
1-5 → 24-20 → 5-9 → 28-24 → 6-11 → 20-15 → 11x20 → 24x15 → 9-13 → 15-11 →
13-18 → 11-7 → 18-22 → 19x26 → 17-21 → 26-22 → 21-25 → 22-18 → 25-29 → 7-3
```
**Total de lances:** 20

**Capturas nesta linha:** 11x20, 24x15, 19x26

---

## Exercício 3
**FEN:** `W:Wa1,g1,b2,c3,b4,h4:Bd4,a5,e5,f6,g7,f8.`

**Posição Inicial:**
- Brancas: Damas em a1 e g1, peões em b2, c3, b4 e h4
- Pretas: peões em d4, a5, e5, f6, g7 e f8

**Solução:**
```
14x23 → 28x19 → 1-5 → 32-28 → 17-21 → 17x26 → 4-7 → 24-20 → 5-9 → 20-16 →
9-13 → 15-12 → 10-14 → 12x17 → 14x32 → 16-12 → 32-28 → 17-13 → 28-23 → 26-21
```
**Total de lances:** 20

**Capturas nesta linha:** 14x23, 28x19, 17x26, 12x17, 14x32

---

## Exercício 4
**FEN:** `W:Wa1,g1,b2,f2,c3,h4:Bd4,a5,e5,d6,f6,e7.`

**Posição Inicial:**
- Brancas: Damas em a1 e g1, peões em b2, f2, c3 e h4
- Pretas: peões em d4, a5, e5, d6, f6 e e7

**Solução:**
```
1-5 → 27-22 → 4-7 → 23-20 → 7-12 → 15-11 → 6x15 → 20x11 → 5-9 → 22-18 →
17-21 → 17x26 → 12-15 → 11x20 → 8-12 → 26-22 → 12-16 → 20-15 → 10-13 → 15-11
```
**Total de lances:** 20

**Capturas nesta linha:** 6x15, 20x11, 17x26, 11x20

---

## Exercício 5
**FEN:** `W:We1,f2:Bb4,f4,b6,d6.`

**Posição Inicial:**
- Brancas: Dama em e1, peão em f2
- Pretas: peões em b4, f4, b6 e d6

**Solução:**
```
8-12
```
**Total de lances:** 1

---

## Observações

Este solver foi desenvolvido especificamente para resolver exercícios de damas brasileiras (8x8) usando algoritmo minimax com poda alpha-beta. As soluções apresentadas representam as melhores sequências de movimentos encontradas pelo motor a uma profundidade de busca de 12 níveis.

**Notação utilizada:**
- `X-Y`: movimento simples da casa X para casa Y
- `XxY`: captura da casa X para casa Y
- As casas são numeradas de 1 a 32 no sistema padrão de damas brasileiras

**Gerado em:** 2025-10-24
**Motor:** Solver Damas Brasileiras v1.0
