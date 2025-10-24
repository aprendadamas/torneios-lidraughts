# Motor de Damas Brasileiras

Motor de jogo de damas implementando as regras oficiais brasileiras.

## Regras Implementadas

### Tabuleiro
- Tabuleiro 8x8 (64 casas)
- Cada jogador começa com 12 peças
- Peças brancas começam na parte inferior (linhas 0-2)
- Peças pretas começam na parte superior (linhas 5-7)

### Movimentação
- **Peças simples**: movem apenas para frente na diagonal (uma casa)
- **Damas**: movem em qualquer direção na diagonal (quantas casas quiser)
- Captura é **obrigatória**
- Quando há múltiplas capturas possíveis, deve-se escolher a que captura o maior número de peças
- Peças simples capturam para frente e para trás
- Damas capturam em qualquer direção diagonal

### Coroação (virar Dama)
- Peça simples vira dama ao alcançar a última linha do adversário
- Se uma peça vira dama durante uma captura, ela **deve parar** (não continua a captura)

### Vitória
- Capturar todas as peças do adversário
- Bloquear todas as peças adversárias (sem movimentos legais)

## Estrutura do Projeto

```
brazilian-checkers-engine/
├── src/
│   ├── __init__.py
│   ├── board.py       # Tabuleiro e lógica de posições
│   ├── piece.py       # Peças (simples e damas)
│   ├── game.py        # Controle do jogo e regras
│   └── utils.py       # Funções auxiliares
├── tests/
│   ├── __init__.py
│   ├── test_board.py
│   ├── test_piece.py
│   └── test_game.py
├── examples/
│   └── simple_game.py # Exemplo de uso
├── docs/
│   └── rules.md       # Documentação detalhada das regras
└── README.md

```

## Instalação

```bash
# Clonar o repositório
git clone [url-do-repositorio]
cd brazilian-checkers-engine

# Instalar dependências (se houver)
pip install -r requirements.txt
```

## Uso Básico

```python
from src.game import Game

# Criar novo jogo
game = Game()

# Fazer um movimento
game.move((2, 1), (3, 2))  # Move peça de (2,1) para (3,2)

# Verificar estado do jogo
print(game.get_winner())  # None, 'white', ou 'black'
print(game.get_legal_moves((3, 2)))  # Lista de movimentos legais

# Exibir tabuleiro
game.display_board()
```

## Testes

```bash
# Executar todos os testes
python -m pytest tests/

# Executar testes específicos
python -m pytest tests/test_board.py
```

## Desenvolvimento

Este motor foi desenvolvido para:
- Análise de partidas de damas brasileiras
- Desenvolvimento de IAs para jogar damas
- Plataforma educacional para aprender as regras
- Integração com interfaces gráficas

## Roadmap

- [x] Implementação básica do tabuleiro
- [x] Movimentação de peças simples
- [x] Movimentação de damas
- [x] Captura obrigatória
- [x] Coroação
- [ ] Integração com Lidraughts API
- [ ] Interface gráfica
- [ ] IA básica (Minimax)
- [ ] IA avançada (Alpha-Beta, MCTS)

## Contribuindo

Contribuições são bem-vindas! Por favor:
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## Licença

MIT License - veja LICENSE para detalhes.

## Contato

Desenvolvido por [Aprenda Damas](https://www.aprendadamas.org)

WhatsApp: (27) 98875-0076
