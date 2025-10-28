"""
Verificar mapeamento de campos
"""

from src.pos64 import Pos64

print("=" * 70)
print("MAPEAMENTO DE CAMPOS")
print("=" * 70)
print()

# Verificar campos relevantes
fields_to_check = [
    'a1', 'b2', 'c1', 'd2', 'e1', 'f2', 'g1', 'h2',
    'a3', 'b4', 'c3', 'd4', 'e3', 'f4', 'g3', 'h4',
    'a5', 'b6', 'c5', 'd6', 'e5', 'f6', 'g5', 'h6',
    'a7', 'b8', 'c7', 'd8', 'e7', 'f8', 'g7', 'h8'
]

print("Mapeamento campo → número:")
print()
for alg in fields_to_check:
    pos = Pos64.from_algebraic(alg)
    if pos:
        print(f"  {alg} → campo {pos.field}")
    else:
        print(f"  {alg} → INVÁLIDO")

print()
print("=" * 70)
print("VERIFICAÇÃO ESPECÍFICA: f4 → g5")
print("=" * 70)
print()

f4 = Pos64.from_algebraic('f4')
g5 = Pos64.from_algebraic('g5')
h6 = Pos64.from_algebraic('h6')
e3 = Pos64.from_algebraic('e3')

print(f"f4 = campo {f4.field}")
print(f"g5 = campo {g5.field}")
print(f"h6 = campo {h6.field}")
print(f"e3 = campo {e3.field}")
print()

# Verificar distância
print("Distâncias:")
print(f"  f4 → g5: Δx={g5.x - f4.x}, Δy={g5.y - f4.y}")
print(f"  h6 → g5: Δx={g5.x - h6.x}, Δy={g5.y - h6.y}")
print(f"  g5 → e3: Δx={e3.x - g5.x}, Δy={e3.y - g5.y}")
print()

# Mostrar tabuleiro com numeração
print("=" * 70)
print("TABULEIRO COM NUMERAÇÃO DOS CAMPOS")
print("=" * 70)
print()

print("    a  b  c  d  e  f  g  h")
print("  ┌─────────────────────────┐")

for rank in range(8, 0, -1):
    line = f"{rank} │ "
    for file_char in 'abcdefgh':
        alg = f"{file_char}{rank}"
        pos = Pos64.from_algebraic(alg)
        if pos:
            line += f"{pos.field:2d} "
        else:
            line += " · "
    line += "│"
    print(line)

print("  └─────────────────────────┘")
