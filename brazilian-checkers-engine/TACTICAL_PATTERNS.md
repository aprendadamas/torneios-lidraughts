# Padrões Táticos Identificados

Este documento cataloga os padrões táticos encontrados ao resolver exercícios de Damas Brasileiras, com o objetivo de melhorar o motor de cálculo tático.

## Status dos Exercícios

| Exercício | Status | Padrão Tático | Dificuldade |
|-----------|--------|---------------|-------------|
| #1 | ✅ RESOLVIDO | Sacrifício para captura múltipla | Básico |
| #13 | ✅ RESOLVIDO | Sacrifício forçando promoção armadilha | Básico |
| #14 | ❌ NÃO RESOLVIDO | ? | Intermediário |
| #15 | ✅ RESOLVIDO | Sequência de capturas forçadas | Básico |

---

## Padrão 1: Sacrifício para Captura Múltipla

**Identificado em**: Exercício #1

### Descrição

Sacrificar uma peça para forçar o adversário a uma posição onde uma captura múltipla se torna possível.

### Exemplo: Exercício #1

**Posição Inicial**:
- Brancas: a1, b2, c3
- Pretas: a5, e5, g7

**Solução**:
1. **c3 → b4** (SACRIFÍCIO!)
2. a5 x b4 → c3 (captura forçada)
3. **b2 x c3 x e5 x g7 → h8** (captura tripla com promoção!)

### Características

- Lance inicial parece ruim (entregar peça de graça)
- Resposta do adversário é FORÇADA (captura obrigatória)
- Lance seguinte captura múltiplas peças, recuperando material com vantagem
- Frequentemente leva à promoção

### Implementação no Motor

```python
def is_tactical_sacrifice(game, from_field, to_field) -> Tuple[bool, float]:
    """
    Detecta se um movimento é um sacrifício tático

    1. Simula o movimento
    2. Verifica se adversário pode capturar
    3. Simula melhor captura do adversário
    4. Verifica se há contra-ataque vencedor
    """
    # Simular movimento
    new_game = game.copy()
    new_game.make_move(from_field, to_field)

    # Verificar capturas do adversário
    enemy_captures = new_game.find_all_captures()

    if not enemy_captures:
        return (False, 0.0)  # Não é sacrifício se não pode ser capturado

    # Simular melhor captura
    best_capture = max(enemy_captures, key=lambda c: len(c.captured_fields))
    new_game.make_move(best_capture.from_field, best_capture.to_field,
                       best_capture.captured_fields, best_capture.promotes)

    # Verificar se temos contra-ataque forte
    counter_captures = new_game.find_all_captures()

    if counter_captures:
        best_counter = max(counter_captures, key=lambda c: len(c.captured_fields))
        if len(best_counter.captured_fields) >= 2:
            return (True, len(best_counter.captured_fields) * 100)

    return (False, 0.0)
```

### Avaliação Tática

O motor deve:
- Aumentar profundidade de busca (+2) quando detectar sacrifício
- Dar bônus de avaliação para capturas múltiplas (50 pontos por peça)
- Considerar promoção resultante (+100 bônus se promove)

---

## Padrão 2: Sacrifício Forçando Promoção Armadilha

**Identificado em**: Exercício #13

### Descrição

Sacrificar uma peça para forçar o adversário a promover em uma posição ruim, onde a dama recém-promovida fica armadilhada e leva à derrota.

### Exemplo: Exercício #13

**Posição Inicial**:
- Brancas: c1, e3, h4
- Pretas: a3, h6, e7

**Solução**:
1. **c1 → b2** (SACRIFÍCIO!)
2. a3 x b2 → **c1 ♛** (captura forçada com PROMOÇÃO)
3. e3 → f4
4. **c1 x f4 → g5** (dama FORÇADA a capturar)
5. **h4 x g5 x e7 → d8 ♛** (captura múltipla, brancas vencem!)

### Características

- Lance inicial entrega peça na borda do tabuleiro
- Adversário é forçado a capturar e promover
- Promoção ocorre em casa ruim (c1 = borda)
- Dama recém-promovida fica com poucas opções
- Configuração de peças força a dama a uma captura desvantajosa
- Contra-ataque captura a dama e outras peças

### Reconhecimento no Motor

Para reconhecer este padrão, verificar:

1. **Peça está perto da linha de promoção do adversário?**
   - Brancas: campos 25-32 (linhas 1-2)
   - Pretas: campos 1-8 (linhas 7-8)

2. **Captura leva à promoção forçada?**
   - Verificar se o campo de destino da captura é casa de promoção

3. **Dama promovida fica em posição ruim?**
   - Casas de canto: c1, a1 (campos 29-32) para pretas
   - Casas de canto: c8, a8 (campos 1-4) para brancas
   - Poucas casas livres ao redor

4. **Há capturas forçadas para a dama?**
   - Verificar se próximo lance força a dama a capturar

5. **Captura da dama leva à vitória?**
   - Simular sequência e avaliar

### Implementação

```python
def is_promotion_trap(game, from_field, to_field):
    """Detecta armadilha de promoção"""
    new_game = game.copy()
    new_game.make_move(from_field, to_field)

    enemy_captures = new_game.find_all_captures()

    for cap in enemy_captures:
        if cap.promotes:  # Captura leva à promoção
            # Verificar se promove em casa ruim (canto/borda)
            if is_corner_or_edge(cap.to_field):
                # Simular promoção
                test_game = new_game.copy()
                test_game.make_move(cap.from_field, cap.to_field,
                                   cap.captured_fields, True)

                # Verificar se há sequência vencedora
                score = evaluate_position_deeply(test_game, depth=4)
                if score >= 1000:  # Vitória detectada
                    return True

    return False
```

---

## Padrão 3: Sequência de Capturas Forçadas

**Identificado em**: Exercício #15

### Descrição

Uma sequência onde cada lance é uma captura forçada (ou há apenas um lance razoável), levando a uma vitória matemática.

### Características

- Todas as capturas são obrigatórias (regra do jogo)
- Adversário não tem escolha significativa
- Sequência leva à captura de todas as peças ou posição vencedora
- Pode ser longa (10+ lances)

### Implementação

Este padrão é o mais fácil para o motor, pois basta:
1. Busca em profundidade suficiente
2. Priorizar linhas forçadas (capturas obrigatórias)
3. Não requer reconhecimento especial

---

## Melhorias Necessárias no Motor

### 1. Função de Avaliação Tática

```python
class TacticalEvaluation:
    # Valores de material
    MAN_VALUE = 100
    KING_VALUE = 300

    # Bônus táticos
    MULTIPLE_CAPTURE_BONUS = 50  # por peça capturada além da primeira
    WINNING_CAPTURE_BONUS = 500  # captura que elimina adversário
    PROMOTION_BONUS_PER_SQUARE = 10  # proximidade à promoção
    KING_ACTIVITY_BONUS = 20  # mobilidade da dama
```

### 2. Detecção de Sacrifícios

- Implementado em `TacticalSearchEngine.is_tactical_sacrifice()`
- Aumenta profundidade em +2 para linhas de sacrifício
- Avalia continuação após captura forçada

### 3. Profundidade Adaptativa

- Linhas táticas: profundidade +2
- Capturas forçadas: continuar até posição quieta
- Sequências de captura múltipla: buscar até o fim

---

## Padrões Ainda Não Identificados

Baseado no fato de que Exercício #14 não foi resolvido, pode haver padrões adicionais:

### Possíveis Padrões Faltando

1. **Zugzwang Tático**: Forçar adversário a movimento ruim
2. **Rede de Mate**: Coordenação de múltiplas peças para armadilha
3. **Ataque Duplo**: Ameaçar duas peças simultaneamente
4. **Cravada**: Peça não pode mover sem expor outra
5. **Rompimento**: Sacrifício para abrir linhas de captura

### Estratégia de Aprendizado

1. Resolver exercícios #2-#12 (nível básico)
2. Catalogar padrão de cada exercício resolvido
3. Implementar reconhecimento de novos padrões
4. Testar em exercícios não resolvidos
5. Iterar até resolver todos os básicos

---

## Resultados do Motor Tático Atual

### Exercícios Resolvidos Automaticamente

✅ **Exercício #1**:
- Motor encontrou: `c3 → b4`
- Avaliação: 10997 (vitória clara)
- Nós pesquisados: 162
- Profundidade: 6

✅ **Exercício #13**:
- Motor encontrou: `c1 → b2`
- Avaliação: 750 (vantagem decisiva)
- Nós pesquisados: 564
- Profundidade: 6

### Exercícios Não Resolvidos

❌ **Exercício #14**:
- Motor sugeriu: `c1 → b2`
- Avaliação: 300 (não indica vitória)
- Nós pesquisados: 8213
- Profundidade: 8
- Busca até profundidade 10 também não encontrou vitória

---

## Próximos Passos

1. **Testar exercícios #2-#12** para identificar mais padrões
2. **Implementar reconhecimento de padrões faltantes**
3. **Aumentar eficiência da busca** (alpha-beta, transposition tables)
4. **Melhorar avaliação posicional** (estrutura de peões, controle central)
5. **Retornar ao Exercício #14** com padrões aprendidos

---

## Referências

- Livro: "1800 Combinações - Do Básico ao Avançado"
- Regras: Lidraughts.org (variante Russian/Brazilian)
- Implementação: Motor Python (protótipo para futuro C++)
