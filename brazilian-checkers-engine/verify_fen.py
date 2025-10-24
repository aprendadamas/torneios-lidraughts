"""
Verificar se o FEN está correto e explorar diferentes interpretações
"""

from src.pos64 import Pos64

print("="*70)
print("VERIFICAÇÃO DO FEN")
print("="*70)
print()

# FEN original: W:Wc1,b2,d2,f4,h4:Ba3,d6,h6,e7,f8
print("FEN: W:Wc1,b2,d2,f4,h4:Ba3,d6,h6,e7,f8")
print()

# Verificar se faz sentido posicional
white_positions = ['c1', 'b2', 'd2', 'f4', 'h4']
black_positions = ['a3', 'd6', 'h6', 'e7', 'f8']

print("Linhas ocupadas:")
print("  Brancas:", [p[1] for p in white_positions])
print("  Pretas:", [p[1] for p in black_positions])
print()

# Mostrar tabuleiro com números de campo
print("Tabuleiro com numeração de campos (1-32):")
print()
print("    a  b  c  d  e  f  g  h")
print("  ┌─────────────────────────┐")

for row in range(8, 0, -1):
    print(f"{row} │", end="")

    for col in 'abcdefgh':
        alg = f"{col}{row}"
        pos = Pos64.from_algebraic(alg)

        if pos:
            # Casa escura
            field = pos.field

            # Verificar se há peça
            piece = ""
            if alg in white_positions:
                piece = "w"
            elif alg in black_positions:
                piece = "b"
            else:
                piece = "·"

            # Mostrar campo (2 dígitos)
            if piece in ['w', 'b']:
                print(f"{field:2}", end="")
            else:
                print(" ·", end="")
        else:
            # Casa clara
            print("  ", end="")

    print(" │")

print("  └─────────────────────────┘")
print("    a  b  c  d  e  f  g  h")
print()

# Mostrar campos das peças
print("Peças por campo:")
white_fields = {}
black_fields = {}

for alg in white_positions:
    pos = Pos64.from_algebraic(alg)
    if pos:
        white_fields[alg] = pos.field

for alg in black_positions:
    pos = Pos64.from_algebraic(alg)
    if pos:
        black_fields[alg] = pos.field

print("  Brancas:", white_fields)
print("  Pretas:", black_fields)
print()

# Análise posicional
print("="*70)
print("ANÁLISE POSICIONAL")
print("="*70)
print()

# Verificar se brancas podem coroar
print("Peças próximas à coroação:")
print("  Brancas coroam na linha 8 (campos 1-4)")
print("  Pretas coroam na linha 1 (campos 29-32)")
print()

for alg, field in white_fields.items():
    if field <= 4:
        print(f"  ⚠️  Branca em {alg} (campo {field}) está NA LINHA DE COROAÇÃO!")
    elif field <= 8:
        print(f"  ✨ Branca em {alg} (campo {field}) está a 1 lance da coroação")

for alg, field in black_fields.items():
    if field >= 29:
        print(f"  ⚠️  Preta em {alg} (campo {field}) está NA LINHA DE COROAÇÃO!")
    elif field >= 25:
        print(f"  ✨ Preta em {alg} (campo {field}) está a 1 lance da coroação")

print()
print("="*70)
print("INVESTIGAÇÃO: POSSÍVEL ERRO NO FEN?")
print("="*70)
print()

# Talvez o FEN use notação diferente?
# Testar se "c1" poderia ser "campo 1" em vez de notação algébrica
print("Testando interpretação alternativa:")
print("  Se o FEN usar campos numéricos em vez de algébrica...")
print()

# Tentar interpretar como campos
alt_white = [1, 2, 2, 4, 4]  # c1, b2, d2, f4, h4 como se fossem campos?
print("  Isso não faz sentido (campos repetidos)")
print()

print("CONCLUSÃO: O FEN parece usar notação algébrica padrão.")
print("O tabuleiro está correto conforme mostrado acima.")
