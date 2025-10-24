# Solução do Exercício 1 - Damas Brasileiras

## Problema Identificado

**FEN Original:** `W:Wa1,b2,c3:Ba5,e5,g7`

**Solução Original (INCORRETA):**
```
d2-e3 → g7-f6 → a1-b2 → f6-g5 → e3-d4 → e5-f4 → b2-a3 → g5-h4 →
d4-c5 → h4-g3 → c3-d4 → g3-f2 → c5-d6 → f2-e1 → d4-e5 → f4-e3 →
e5-f6 → e3-d2 → d6-c7 → d2-c1
```

### Erro Encontrado

A solução original começa com `d2-e3`, mas **não existe nenhuma peça em d2** na posição FEN fornecida.

**Peças na posição:**
- Brancas: a1, b2, c3
- Pretas: a5, e5, g7

## Posição Inicial

```
   |   |   |   |   |   |   |
-------------------------------
   |   |   |   |   |   | b |   (g7)
-------------------------------
   |   |   |   |   |   |   |
-------------------------------
 b |   |   |   | b |   |   |   (a5, e5)
-------------------------------
   |   |   |   |   |   |   |
-------------------------------
   |   | w |   |   |   |   |   (c3)
-------------------------------
   | w |   |   |   |   |   |   (b2)
-------------------------------
 w |   |   |   |   |   |   |   (a1)
```

## Solução Correta

**Motor:** Brazilian Draughts Solver baseado em pydraughts library
**Método:** Minimax com avaliação posicional (profundidade 2)

### Notação PDN (Numérica)
```
5-9 → 17-13 → 9x18 → 19-14 → 18x11 → 28-23 → 10-13 → 23-19 → 13-18 → 19-15 → 11x20
```

### Notação Algébrica
```
b2-a3 → a5-b4 → a3xc5 → e5-d4 → c5xe3 → g7-f6 → c3-b4 → f6-e5 → b4-c5 → e5-f4 → e3xg5
```

### Sequência Detalhada

| Jogada | PDN    | Algébrica  | Jogador |
|--------|--------|------------|---------|
| 1      | 5-9    | b2-a3      | Brancas |
| 2      | 17-13  | a5-b4      | Pretas  |
| 3      | 9x18   | a3xc5      | Brancas (captura) |
| 4      | 19-14  | e5-d4      | Pretas  |
| 5      | 18x11  | c5xe3      | Brancas (captura) |
| 6      | 28-23  | g7-f6      | Pretas  |
| 7      | 10-13  | c3-b4      | Brancas |
| 8      | 23-19  | f6-e5      | Pretas  |
| 9      | 13-18  | b4-c5      | Brancas |
| 10     | 19-15  | e5-f4      | Pretas  |
| 11     | 11x20  | e3xg5      | Brancas (captura) |

### Resultado

**As Brancas vencem!**

Após a jogada 11, as Pretas não têm mais movimentos legais.

## Sistema de Numeração

O sistema PDN numera as casas escuras de 1 a 32:

```
Linha 8: 29  30  31  32
Linha 7: 25  26  27  28
Linha 6: 21  22  23  24
Linha 5: 17  18  19  20
Linha 4: 13  14  15  16
Linha 3:  9  10  11  12
Linha 2:  5   6   7   8
Linha 1:  1   2   3   4
         a   b   c   d   e   f   g   h
```

## Implementação

Os seguintes arquivos foram criados:

1. **brazilian_draughts_solver.py** - Motor completo com minimax
2. **simple_solver.py** - Solver simplificado e eficiente
3. **notation_converter.py** - Conversor PDN ↔ Algébrica
4. **test_pydraughts.py** - Testes da API pydraughts

### Uso

```bash
# Resolver o exercício
python3 simple_solver.py

# Converter notações
python3 notation_converter.py
```

## Dependências

```bash
pip install pydraughts
```

A biblioteca pydraughts implementa todas as regras oficiais de damas brasileiras baseadas no Lidraughts.org.
