# Bug Fix: Promoção Durante Multi-Captura

**Data**: 2025-10-29
**Status**: ✅ **CORRIGIDO**

---

## Resumo do Bug

O motor `BrazilianGameComplete` parava e promovia imediatamente quando um peão alcançava a linha de coroação durante uma captura múltipla, **SEM** verificar se havia mais capturas disponíveis "no mesmo curso" (como peão).

### Exemplo

**Exercício #18 - Lance 5**: `h2 x g3 x e5 x e7 x g7 → h6`

**ANTES DO FIX**:
- Motor encontrava: `h2 x g3 x e5 x e7 → f8 ♛` (3 capturas, para em f8)
- Para em f8 (linha 8) e promove imediatamente
- **Perde a 4ª captura!**

**DEPOIS DO FIX**:
- Motor encontra: `h2 x g3 x e5 x e7 x g7 → h6` (4 capturas)
- Passa por f8 (linha 8) mas continua capturando
- Para em h6 (linha 6) como peão
- ✅ **Solução correta!**

---

## Regra FMJD

> **Artigo 3.7**: "If a man reaches the last horizontal line and can continue capture pieces in the same course, it continues as a man and only promotes to a king when it stops."

**Tradução**: Se um peão alcança a última linha horizontal e pode continuar capturando peças no mesmo curso, ele continua como peão e só promove a dama quando para.

### Interpretação

1. Peão alcança linha de coroação **DURANTE** uma multi-captura
2. **PRIMEIRO**: Verificar se há mais capturas como peão (movimentos adjacentes)
3. **SE HÁ**: Continuar capturando SEM promover
4. **SE NÃO HÁ**: Promover e parar

---

## Localização do Bug

**Arquivo**: `src/brazilian_engine_complete.py`
**Método**: `_find_man_captures()`
**Linhas**: 190-217 (após correção)

### Código ANTES da Correção

```python
# BUGADO - Promovia imediatamente
promotes = self.is_promotion_square(beyond.field, self.turn)

if promotes and not is_promoted:
    # BUG: Para e promove SEM verificar mais capturas!
    captures.append(Capture(
        from_field=original_from,
        to_field=beyond.field,
        captured_fields=new_captured,
        promotes=True
    ))
else:
    # Continua buscando capturas adicionais
    further_captures = self._find_man_captures(...)
    if further_captures:
        captures.extend(further_captures)
    else:
        captures.append(Capture(...))
```

### Código DEPOIS da Correção

```python
# CORRIGIDO - Verifica mais capturas ANTES de promover
promotes = self.is_promotion_square(beyond.field, self.turn)

if promotes and not is_promoted:
    # REGRA FMJD: PRIMEIRO tenta continuar capturando como peão
    further_captures = self._find_man_captures(
        beyond.field,
        original_from,
        new_occupied,
        new_captured,
        is_promoted=False  # Tenta continuar como peão!
    )

    if further_captures:
        # Há mais capturas como peão - continua SEM promover
        captures.extend(further_captures)
    else:
        # Sem mais capturas - promove e para
        captures.append(Capture(
            from_field=original_from,
            to_field=beyond.field,
            captured_fields=new_captured,
            promotes=True
        ))
else:
    # Não é linha de promoção ou já é dama
    further_captures = self._find_man_captures(
        beyond.field,
        original_from,
        new_occupied,
        new_captured,
        is_promoted or promotes
    )

    if further_captures:
        captures.extend(further_captures)
    else:
        captures.append(Capture(
            from_field=original_from,
            to_field=beyond.field,
            captured_fields=new_captured,
            promotes=promotes
        ))
```

---

## Teste de Verificação

**Arquivo**: `test_bug_fix_ex18.py`

Testa especificamente o lance 5 do Exercício #18:

```bash
python test_bug_fix_ex18.py
```

**Resultado esperado**:
```
✅ BUG FIX FUNCIONOU!

O motor agora encontra corretamente:
  - Captura QUÁDRUPLA (4 peças)
  - Passa por f8 (linha 8) sem promover
  - Para em h6 (linha 6) como PEÃO

Regra FMJD aplicada corretamente:
  'Se alcança linha de coroação mas pode continuar
   capturando no mesmo curso, continua SEM promover'
```

---

## Impacto do Bug

### Antes da Correção

❌ **Exercício #18**: Não encontrava captura de 4 peças (parava com 3)
❌ **Qualquer posição** com multi-captura através da linha de coroação
❌ **Táticas complexas** que dependem de continuar capturando após alcançar linha 8/1

### Depois da Correção

✅ **Exercício #18**: Encontra captura quádrupla corretamente
✅ **Motor encontra a5→b6** como primeiro lance (score +100)
✅ **Regra FMJD** implementada corretamente

---

## Taxa de Sucesso Atualizada

| Exercício | Dificuldade | Motor V2 (antes) | Motor V2 (depois) | Status |
|-----------|-------------|------------------|-------------------|---------|
| #1 | Básico | ✅ Correto | ✅ Correto | Resolvido |
| #13 | Intermediário | ✅ Correto | ✅ Correto | Resolvido |
| #14 | Avançado | ✅ Correto | ✅ Correto | Resolvido |
| #16 | Avançado | ✅ Correto | ✅ Correto | Resolvido |
| #17 | Avançado | ✅ Correto | ✅ Correto | Empate |
| **#18** | **Avançado** | **❌ Bug** | **✅ CORRIGIDO** | **Resolvido** |

**Taxa**: 6/6 corretos (100%)! 🎉

---

## Referências

1. **FMJD Rules** - Article 3.7 (Promotion during multi-capture)
2. **SOLUTION_EXERCISE_18.md** - Análise completa do exercício
3. **BUG_PROMOTION_DURING_CAPTURE.md** - Documentação original do bug

---

## Conclusão

O bug foi identificado no Exercício #18 e corrigido aplicando corretamente a **Regra FMJD 3.7**:

> "Se um peão alcança a linha de coroação durante uma captura múltipla e pode continuar capturando no mesmo curso (como peão), ele continua SEM promover."

A correção permite que o motor encontre sequências de captura mais longas e complexas, melhorando significativamente sua força tática.

**Data de correção**: 2025-10-29
**Testado e verificado**: ✅ Sim
