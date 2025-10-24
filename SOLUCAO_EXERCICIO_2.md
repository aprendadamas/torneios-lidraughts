# Solução do Exercício 2 - Damas Brasileiras

## Informações do Exercício

**Origem:** 1800 Combinações - Do Básico ao Avançado
**Site:** www.cursodedamas.com.br
**Ano:** 2024
**FEN:** `W:Wa1,b2,c3,h4:Ba5,e5,f6,g7`

## Posição Inicial

**Peças:**
- **Brancas (4):** a1, b2, c3, h4
- **Pretas (4):** a5, e5, f6, g7

```
8  |   |   |   |   |   |   |
   -------------------------------
7  |   |   |   |   |   | b |
   -------------------------------
6  |   |   |   |   | b |   |
   -------------------------------
5  b |   |   |   | b |   |   |
   -------------------------------
4  |   |   |   |   |   |   | w
   -------------------------------
3  |   |   | w |   |   |   |
   -------------------------------
2  |   | w |   |   |   |   |
   -------------------------------
1  w |   |   |   |   |   |   |
   a   b   c   d   e   f   g   h
```

## Solução - MATE IN 5

### Notação Completa

**Algébrica:**
```
1. h4-g5    f6xh4
2. c3-b4    a5xc3
3. b2xd4xf6xh8    h4-g3
4. h8-d4    g3-f2
5. d4xg1#
```

**PDN (Numérica):**
```
1. 16-20    23x16
2. 10-13    17x10
3. 5x32     16-12
4. 32-14    12-7
5. 14x4#
```

## Análise Lance a Lance

### Lance 1: SACRIFÍCIO DUPLO COMEÇA

**1. h4-g5!**

Brancas sacrificam a peça em h4 movendo para g5. Este é o primeiro sacrifício tático.

```
Após 1. h4-g5:
4  |   |   |   |   |   | w |   ← sacrifício oferecido
   -------------------------------
3  |   |   | w |   |   |   |
```

**1... f6xh4** (FORÇADA)

Pretas devem capturar (captura obrigatória nas damas brasileiras).

```
Após 1... f6xh4:
5  b |   |   |   | b |   |   |   (a5, e5 restam)
4  |   |   |   |   |   |   | b  (f6 capturou e está agora em h4)
```

### Lance 2: SEGUNDO SACRIFÍCIO (Tema do Exercício 1!)

**2. c3-b4!**

Exatamente como no Exercício 1! Segundo sacrifício.

**2... a5xc3** (FORÇADA)

```
Após 2... a5xc3:
Pretas em: c3 (recém capturada), e5, g7, h4
Brancas em: a1, b2
```

### Lance 3: CAPTURA TRIPLA COM PROMOÇÃO!

**3. b2xd4xf6xh8**

A mesma captura tripla do Exercício 1!
- b2 captura c3 → d4
- d4 captura e5 → f6
- f6 captura g7 → h8 (PROMOÇÃO A DAMA!)

```
Após 3. b2xd4xf6xh8:
8  |   |   |   |   |   |   | W  ← DAMA BRANCA!
4  |   |   |   |   |   |   | b  (h4 é a única preta restante)
1  w |   |   |   |   |   |   |
```

**3... h4-g3**

Única peça preta restante tenta fugir.

### Lance 4: DAMA PERSEGUE

**4. h8-d4**

Dama branca desce a diagonal para perseguir.

```
Após 4. h8-d4:
4  |   |   | W |   |   |   |   ← Dama em d4
3  |   |   |   |   |   | b |
```

**4... g3-f2**

Peça preta continua fugindo.

### Lance 5: CAPTURA FINAL - MATE!

**5. d4xg1#**

Dama captura a última peça preta chegando em g1.

```
Posição Final:
1  w |   |   |   |   |   | W |
   a   b   c   d   e   f   g   h

FEN: B:Wa1,Kg1:B
```

**XEQUE-MATE!** Pretas não têm peças nem movimentos legais.

## Padrões Táticos Importantes

### 1. Sacrifício Duplo
Este exercício demonstra **dois sacrifícios consecutivos**:
- Primeiro: h4-g5 (sacrifica h4)
- Segundo: c3-b4 (sacrifica c3)

Ambos são necessários para preparar a captura tripla devastadora.

### 2. Captura Tripla (Repetição do Exercício 1)
A sequência b2xd4xf6xh8 é **idêntica** ao Exercício 1:
- 3 capturas consecutivas
- Promoção a dama na última fileira
- Uso eficiente da regra de captura obrigatória

### 3. Perseguição com Dama
Após a promoção:
- Dama usa sua mobilidade superior
- Caça a última peça inimiga
- Força o mate

## Comparação com Exercício 1

| Aspecto | Exercício 1 | Exercício 2 |
|---------|-------------|-------------|
| Sacrifícios | 1 (c3-b4) | 2 (h4-g5, c3-b4) |
| Mate em | 2 movimentos | 5 movimentos |
| Captura tripla | Sim (lance 2) | Sim (lance 3) |
| Promoção a dama | Sim (mate imediato) | Sim (perseguição necessária) |
| Dificuldade | Básico | Intermediário |

## Estatísticas da Busca

**Solver Performance:**
- **Nós explorados:** 4,197
- **Profundidade:** 10 movimentos (5 lances completos)
- **Tempo:** < 1 segundo
- **Primeiro movimento testado:** 16-20 (h4-g5) ✓ CORRETO!

## Lições Táticas

1. **Sacrifícios múltiplos:** Às vezes é necessário sacrificar mais de uma peça
2. **Preparação:** O primeiro sacrifício (h4-g5) prepara o segundo (c3-b4)
3. **Tema recorrente:** A captura tripla é um padrão tático importante
4. **Técnica de dama:** Saber usar a dama para caçar peças isoladas
5. **Visualização:** Calcular 5 lances à frente requer boa visualização

## Uso dos Solvers

```bash
# Resolver exercício 2
python3 solve_exercise_2.py

# Output esperado:
# Trying 16-20 (h4-g5)... MATE IN 5! (4197 nodes)
```

## Arquivos Relacionados

- `solve_exercise_2.py` - Script para resolver este exercício
- `final_solver.py` - Solver tático principal
- `SOLUCAO_EXERCICIO_2.md` - Esta documentação

---

**Status:** ✓ RESOLVIDO
**Motor:** TacticalSolver v1.0
**Método:** Busca de mate forçado com verificação completa
