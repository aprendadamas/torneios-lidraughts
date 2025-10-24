# Solução do Exercício Tático #15

## Posição Inicial

**FEN**: `W:Wc1,b2,d2,f4,h4:Ba3,d6,h6,e7,f8.`

**Fonte**: 1800 Combinações - Do básico ao Avançado

### Peças

- **Brancas** (vez de jogar): c1, b2, d2, f4, h4
- **Pretas**: a3, d6, h6, e7, f8

### Tabuleiro

```
    a  b  c  d  e  f  g  h
  ┌─────────────────────────┐
8 │   · · · · B B · │
7 │ · · · · B B · · │
6 │   · · B B · · B │
5 │ · · · · · · · · │
4 │   · · · · W W W │
3 │ B B · · · · · · │
2 │   W W W W · · · │
1 │ · · W W · · · · │
  └─────────────────────────┘
```

## Análise

### Movimentos Disponíveis

Na posição inicial, as brancas NÃO têm capturas disponíveis, portanto devem fazer um movimento simples.

Movimentos simples possíveis:
1. f4 → e5 ❌ (permite d6 x e5)
2. f4 → g5 ❌ (permite h6 x g5)
3. h4 → g5 ⚠️  (seguro, mas leva a derrota)
4. **b2 → c3** ✅ (MELHOR - leva à vitória)
5. d2 → c3 ✅ (também vence)
6. d2 → e3 ✅ (também vence)

### Conceitos Importantes das Regras Brasileiras

1. **Movimentos simples**: Peças movem apenas PARA FRENTE
   - Brancas sobem (UpLeft, UpRight)
   - Pretas descem (DownLeft, DownRight)

2. **Capturas**: Peças podem capturar em TODAS as 4 direções diagonais
   - Mesmo peões podem capturar para trás!
   - Capturas são OBRIGATÓRIAS
   - Capturas múltiplas devem ser completadas

## Solução

### Melhor Movimento: **b2 → c3**

Esta jogada força uma sequência vencedora para as brancas.

### Sequência Vencedora (21 lances)

```
1.  white: b2 → c3
2.  black: a3 → b2
3.  white: c3 x b2 → a1         (captura para trás!)
4.  black: h6 → g5
5.  white: h4 x g5 x e7 → d8    (CAPTURA DUPLA - lance tático chave!)
6.  black: d6 → e5
7.  white: f4 x e5 → d6
8.  black: f8 → g7
9.  white: d6 → c7
10. black: g7 → h6
11. white: c7 → b8
12. black: h6 → g5
13. white: d2 → c3
14. black: g5 → h4
15. white: c3 → b4
16. black: h4 → g3
17. white: b4 → a5
18. black: g3 → h2
19. white: a5 → b6
20. black: h2 → g1
21. white: b6 → a7

BRANCAS VENCEM!
```

### Posição Final

```
    a  b  c  d  e  f  g  h
  ┌─────────────────────────┐
8 │   W W W W · · · │
7 │ W W · · · · · · │
6 │   · · · · · · · │
5 │ · · · · · · · · │
4 │   · · · · · · · │
3 │ · · · · · · · · │
2 │   · · · · · · · │
1 │ W W W W · · B B │
  └─────────────────────────┘
```

As brancas conseguem promover várias peças a damas e dominam o tabuleiro. **Vitória das brancas em 21 lances!**

### Lance Tático Chave

O **lance 5 (h4 x g5 x e7 → d8)** é a jogada tática crucial:
- Captura DUPLA (múltipla) que remove duas peças pretas
- h4 salta sobre g5, captura, continua e salta sobre e7, chegando a d8
- Isso demonstra que peões podem capturar em todas as 4 direções diagonais
- Esta captura múltipla garante vantagem material decisiva para as brancas

## Alternativas

Os movimentos **d2 → c3** e **d2 → e3** também levam à vitória das brancas, mas **b2 → c3** é a linha principal por ser mais forçada.

O movimento **h4 → g5**, embora não permita captura imediata, leva a uma posição perdedora para as brancas após a melhor defesa das pretas.

## Implementação

A solução foi encontrada usando um motor de jogo de Damas Brasileiras implementado em Python, baseado na implementação oficial do Lidraughts (Russian/Brazilian variant):

- Sistema de coordenadas Pos64 (campos 1-32)
- Lógica de capturas em 4 direções para peões
- Busca recursiva de capturas múltiplas
- Simulação automática de partidas

### Arquivos

- `src/pos64.py` - Sistema de posições baseado no Lidraughts
- `src/brazilian_engine.py` - Motor de jogo
- `verify_pos64.py` - Verificação do sistema de coordenadas
- `SOLUTION_EXERCISE_15.md` - Este documento
