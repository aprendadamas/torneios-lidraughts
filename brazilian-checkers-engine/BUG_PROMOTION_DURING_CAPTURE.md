# BUG: Promoção durante captura múltipla

## Descrição

O motor está incorretamente promovendo peças quando elas **passam** pela linha de coroação durante uma captura múltipla, em vez de apenas promover quando **param** na linha de coroação.

## Exercício #18 - Exemplo do Bug

### Posição antes do lance 5:
- Brancas: h2, h4
- Pretas: g3 (peão), e5, e7, g7, b8, d8

### Captura esperada:
```
h2 x g3 x e5 x e7 x g7 → h6 ♛
```
- Captura 4 peças
- Passa por f8 (linha 8) mas **não para**
- Continua e captura g7
- **Para em h6** → promove aqui!

### Captura encontrada pelo motor:
```
h2 x g3 x e5 x e7 → f8 ♛
```
- Captura apenas 3 peças
- **Para em f8** e promove
- **NÃO continua** para capturar g7

## Regra Brasileira (FMJD)

> A man is crowned when it **stops** at the last eighth (counting from himself) line.
> If a man reaches the last horizontal line when it is captured pieces and it have the opportunity to continue capture pieces, it is obliged to continue capture the same course.

**Ou seja**: Só promove se **PARA** na linha de coroação!

## Localização do Bug

Arquivo: `src/brazilian_engine_complete.py`
Método: `_find_man_captures()`
Linhas: 188-197

```python
# Verificar se promove (REGRA BRASILEIRA: para quando promove!)
promotes = self.is_promotion_square(beyond.field, self.turn)

if promotes and not is_promoted:
    # Promove a dama - PARA a captura (regra brasileira)  ← BUG AQUI!
    captures.append(Capture(
        from_field=original_from,
        to_field=beyond.field,
        captured_fields=new_captured,
        promotes=True
    ))
```

### Problema:

O código **para** e promove imediatamente quando chega na linha de coroação, **SEM** verificar se há mais capturas disponíveis.

### Correção necessária:

1. Ao chegar na linha de coroação, **primeiro** verificar se há mais capturas possíveis
2. Se **SIM**: continuar capturando SEM promover
3. Se **NÃO**: promover e parar

## Algoritmo Correto

```python
promotes = self.is_promotion_square(beyond.field, self.turn)

if promotes and not is_promoted:
    # NOVO: Tentar continuar capturando ANTES de promover
    further_captures = self._find_man_captures(
        beyond.field,
        original_from,
        new_occupied,
        new_captured,
        is_promoted=False  # Continua como peão!
    )

    if further_captures:
        # Há mais capturas! Continuar SEM promover
        captures.extend(further_captures)
    else:
        # Sem mais capturas - promover e parar
        captures.append(Capture(
            from_field=original_from,
            to_field=beyond.field,
            captured_fields=new_captured,
            promotes=True
        ))
else:
    # Não está na linha de promoção, continuar normalmente
    further_captures = self._find_man_captures(...)
    ...
```

## Impacto

- **Exercício #18**: Motor não encontra a solução correta (captura de 4 peças)
- Qualquer posição onde uma captura múltipla passa pela linha de coroação será mal avaliada
- Motor pode perder vitórias táticas que dependem deste padrão

## Prioridade

**ALTA** - Afeta corretude do motor em padrões táticos comuns

## Status

- [x] Bug identificado
- [x] Localizado no código
- [x] Solução proposta
- [ ] Correção implementada
- [ ] Testes adicionados
- [ ] Verificado com Exercício #18
