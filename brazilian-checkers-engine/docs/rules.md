# Regras Oficiais das Damas Brasileiras

Este documento descreve detalhadamente as regras implementadas no motor de damas brasileiro.

## 1. Tabuleiro e Peças

### Tabuleiro
- Tabuleiro quadrado de 8x8 casas (64 casas no total)
- Alternância de casas claras e escuras
- Apenas as **casas escuras** são utilizadas no jogo
- Total de 32 casas escuras jogáveis

### Peças Iniciais
- Cada jogador começa com **12 peças**
- **Peças brancas**: ocupam as linhas 0, 1 e 2 (parte inferior do tabuleiro)
- **Peças pretas**: ocupam as linhas 5, 6 e 7 (parte superior do tabuleiro)
- As peças são colocadas apenas nas casas escuras

### Tipos de Peças
1. **Peça simples (Pedra)**: representada por `w` (branca) ou `b` (preta)
2. **Dama**: representada por `W` (branca) ou `B` (preta)

## 2. Movimentação

### Peças Simples
- Movem **apenas para frente** na diagonal
- Movem **uma casa por vez**
- Não podem mover para trás em jogadas normais
- **Podem capturar para trás** (característica da regra brasileira)

### Damas
- Movem em **qualquer direção diagonal** (frente, trás, direita, esquerda)
- Podem mover **quantas casas quiser** na diagonal
- Não podem "saltar" peças próprias
- Podem capturar em qualquer direção

## 3. Capturas

### Regras Gerais de Captura
- Captura é feita **saltando** sobre a peça adversária
- A peça adversária é **removida do tabuleiro**
- Capturas são **OBRIGATÓRIAS**
- Quando há múltiplas opções de captura, deve-se escolher a que **captura o maior número de peças**

### Captura de Peças Simples
- Peças simples capturam saltando uma casa na diagonal
- **Podem capturar para frente E para trás** (regra brasileira)
- Após a captura, a peça pousa na casa imediatamente após a peça capturada

### Captura de Damas
- Damas capturam em qualquer direção diagonal
- Podem capturar peças a **qualquer distância**
- Após a captura, podem pousar em qualquer casa livre após a peça capturada
- A distância percorrida após a captura não é limitada

### Capturas Múltiplas (Sopro)
- Se após uma captura for possível capturar outra peça, **deve-se continuar capturando**
- Isso se repete até que não haja mais capturas possíveis
- Todas as peças capturadas são removidas após a sequência completa
- Uma peça não pode ser capturada duas vezes na mesma jogada

### Captura Obrigatória Máxima
- Quando há múltiplas capturas possíveis, deve-se escolher a que captura **o maior número de peças**
- Se houver empate no número de capturas, o jogador pode escolher qualquer uma

## 4. Coroação (Promoção a Dama)

### Quando Ocorre
- Peça simples vira dama ao **alcançar a última linha do adversário**
- Brancas viram dama ao chegar na linha 7 (topo)
- Pretas viram dama ao chegar na linha 0 (base)

### Regra Importante
- Se uma peça vira dama **durante uma captura múltipla**, ela **DEVE PARAR**
- A peça recém-coroada não pode continuar capturando na mesma jogada
- Esta é uma regra característica das damas brasileiras

### Após Coroação
- A dama passa a ter todos os poderes de movimentação de dama
- Pode mover e capturar em qualquer direção diagonal
- Pode percorrer múltiplas casas

## 5. Vitória e Fim de Jogo

### Condições de Vitória
1. **Capturar todas as peças do adversário**
2. **Bloquear todas as peças adversárias** (adversário sem movimentos legais)

### Empate
- **Acordo mútuo**: ambos os jogadores concordam com o empate
- **Repetição de posições**: mesma posição ocorre 3 vezes
- **50 movimentos sem captura**: após 50 movimentos consecutivos sem capturas ou movimentos de peças simples
- **Insuficiência de material**: quando é impossível dar xeque-mate (raro em damas)

## 6. Regras Específicas da Variante Brasileira

### Diferenças de Outras Variantes
1. **Captura para trás**: peças simples podem capturar para trás (não presente em todas as variantes)
2. **Parada obrigatória na coroação**: peça que vira dama durante captura deve parar
3. **Tabuleiro 8x8**: algumas variantes usam 10x10
4. **Captura máxima**: obrigatório escolher a captura com mais peças

### Notação
- **Notação algébrica**: a1, b2, c3, etc. (colunas a-h, linhas 1-8)
- **Notação numérica**: 1-32 (numerando apenas casas escuras)
- **Notação de coordenadas**: (linha, coluna) começando em (0,0)

## 7. Casos Especiais

### Dama vs Peça Simples
- Dama pode capturar peça simples a qualquer distância
- Peça simples só pode capturar dama se estiver adjacente

### Sopro (Penalização por não capturar)
- Em algumas modalidades, se um jogador não realiza uma captura obrigatória, a peça pode ser "soprada" (removida)
- **Esta regra NÃO é implementada na versão atual** (considerada obsoleta)

### Empate por Inferioridade
- Se um jogador com vantagem material não consegue vencer em 20 movimentos, pode ser declarado empate
- Esta regra é opcional e não implementada por padrão

## 8. Estratégia Básica

### Princípios Fundamentais
1. **Controle do centro**: controlar as casas centrais dá mais mobilidade
2. **Progressão coordenada**: avançar peças em conjunto, protegendo-se mutuamente
3. **Coroação**: priorizar transformar peças em damas
4. **Troca vantajosa**: trocar peças quando se tem vantagem numérica
5. **Oposição**: posicionar damas em oposição ao rei adversário

### Fases do Jogo
1. **Abertura**: desenvolvimento das peças, controle do centro
2. **Meio-jogo**: trocas táticas, criação de vantagens
3. **Final**: conversão da vantagem em vitória, técnicas de damas

## 9. Implementação no Motor

### Validação de Movimentos
O motor valida automaticamente:
- Se o movimento é legal segundo as regras
- Se há capturas obrigatórias disponíveis
- Se a captura escolhida é a máxima possível
- Se houve coroação
- Se o jogo terminou

### Interface de Programação
```python
# Criar novo jogo
game = Game()

# Fazer movimento
game.make_move((2, 1), (3, 2))

# Obter movimentos legais
moves = game.get_legal_moves((3, 2))

# Verificar fim de jogo
if game.is_game_over():
    winner = game.get_winner()
```

## 10. Referências

- Confederação Brasileira de Damas (CBD)
- Federação Internacional de Damas (FMJD)
- Regulamento Oficial de Damas Brasileiras
- Lidraughts.org - Plataforma online de damas

---

**Observações:**
- Este documento descreve as regras implementadas no motor
- Pequenas variações podem existir em diferentes regiões do Brasil
- Para competições oficiais, consulte sempre o regulamento da CBD
