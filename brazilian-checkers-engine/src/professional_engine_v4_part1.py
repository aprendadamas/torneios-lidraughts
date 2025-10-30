"""
Motor V4 - Arquitetura Profissional
Baseado em técnicas de motores campeões: Scan (damas), Stockfish (xadrez)

Implementa:
1. Transposition Tables (Hash Tables)
2. Zobrist Hashing
3. Iterative Deepening completo
4. Move Ordering avançado (PV, Killer moves, History)
5. Quiescence Search
6. Null-Move Pruning
"""

from src.brazilian_engine_complete import BrazilianGameComplete, Capture
from src.pos64 import Pos64
from typing import Tuple, List, Optional, Dict
from dataclasses import dataclass
from enum import Enum
import copy
import random


class NodeType(Enum):
    """Tipo de nó na árvore de busca"""
    EXACT = 1      # Valor exato
    LOWER_BOUND = 2  # Alpha cutoff (≥ valor real)
    UPPER_BOUND = 3  # Beta cutoff (≤ valor real)


@dataclass
class TTEntry:
    """Entrada na Transposition Table"""
    zobrist_key: int
    depth: int
    score: int
    node_type: NodeType
    best_move: Optional[Tuple]  # (from_field, to_field, captured, promotes)
    age: int  # Para replacement strategy


class ZobristHasher:
    """
    Zobrist Hashing para gerar hash único de posições

    Cada peça em cada casa tem um número aleatório único.
    Hash da posição = XOR de todos os números das peças.
    """

    def __init__(self):
        # Gerar números aleatórios para cada combinação (peça, casa)
        random.seed(12345)  # Seed fixo para reprodutibilidade

        # 32 casas × 4 tipos (white_man, white_king, black_man, black_king)
        self.piece_keys = {}

        for field in range(1, 33):
            self.piece_keys[('white_man', field)] = random.getrandbits(64)
            self.piece_keys[('white_king', field)] = random.getrandbits(64)
            self.piece_keys[('black_man', field)] = random.getrandbits(64)
            self.piece_keys[('black_king', field)] = random.getrandbits(64)

        # Key para indicar quem joga
        self.turn_key = random.getrandbits(64)

    def hash_position(self, game: BrazilianGameComplete) -> int:
        """Gera hash Zobrist da posição"""
        h = 0

        # XOR de todas as peças
        for field in game.white_men:
            h ^= self.piece_keys[('white_man', field)]

        for field in game.white_kings:
            h ^= self.piece_keys[('white_king', field)]

        for field in game.black_men:
            h ^= self.piece_keys[('black_man', field)]

        for field in game.black_kings:
            h ^= self.piece_keys[('black_king', field)]

        # XOR do turno
        if game.turn == "black":
            h ^= self.turn_key

        return h

    def update_hash_after_move(self, current_hash: int, game_before: BrazilianGameComplete,
                               from_field: int, to_field: int,
                               captured_fields: List[int], promotes: bool) -> int:
        """
        Atualiza hash incrementalmente após um movimento
        Muito mais rápido que recalcular do zero
        """
        h = current_hash

        # Determinar tipo da peça que moveu
        if from_field in game_before.white_men:
            piece_type = 'white_man'
            is_white = True
        elif from_field in game_before.white_kings:
            piece_type = 'white_king'
            is_white = True
        elif from_field in game_before.black_men:
            piece_type = 'black_man'
            is_white = False
        else:  # black_kings
            piece_type = 'black_king'
            is_white = False

        # Remover peça da posição origem
        h ^= self.piece_keys[(piece_type, from_field)]

        # Remover peças capturadas
        for cap_field in captured_fields:
            if cap_field in game_before.white_men:
                h ^= self.piece_keys[('white_man', cap_field)]
            elif cap_field in game_before.white_kings:
                h ^= self.piece_keys[('white_king', cap_field)]
            elif cap_field in game_before.black_men:
                h ^= self.piece_keys[('black_man', cap_field)]
            else:  # black_kings
                h ^= self.piece_keys[('black_king', cap_field)]

        # Adicionar peça na posição destino
        if promotes:
            # Promoveu a dama
            new_piece_type = 'white_king' if is_white else 'black_king'
        else:
            new_piece_type = piece_type

        h ^= self.piece_keys[(new_piece_type, to_field)]

        # Inverter turno
        h ^= self.turn_key

        return h


class TranspositionTable:
    """
    Transposition Table (Hash Table) para cache de posições

    Tamanho típico: 64 MB - 1 GB
    """

    def __init__(self, size_mb: int = 128):
        """
        Inicializa TT com tamanho especificado

        Args:
            size_mb: Tamanho em megabytes (padrão 128 MB)
        """
        # Cada entrada tem ~48 bytes (zobrist_key=8, depth=4, score=4, etc)
        bytes_per_entry = 48
        self.size = (size_mb * 1024 * 1024) // bytes_per_entry

        # Usar potência de 2 para indexação rápida com &
        self.size = 2 ** (self.size.bit_length() - 1)

        self.table: Dict[int, TTEntry] = {}
        self.current_age = 0

        print(f"Transposition Table: {self.size:,} entradas (~{size_mb} MB)")

    def probe(self, zobrist_key: int) -> Optional[TTEntry]:
        """
        Busca entrada no cache

        Returns:
            TTEntry se encontrado, None caso contrário
        """
        index = zobrist_key & (self.size - 1)
        entry = self.table.get(index)

        if entry and entry.zobrist_key == zobrist_key:
            return entry

        return None

    def store(self, zobrist_key: int, depth: int, score: int,
              node_type: NodeType, best_move: Optional[Tuple] = None):
        """
        Armazena entrada no cache

        Usa replacement strategy: sempre substituir se profundidade >= existente
        """
        index = zobrist_key & (self.size - 1)
        existing = self.table.get(index)

        # Always-replace se:
        # 1. Não existe entrada
        # 2. Nova profundidade >= profundidade existente
        # 3. Entrada antiga (age diferente)
        if (not existing or
            depth >= existing.depth or
            existing.age != self.current_age):

            self.table[index] = TTEntry(
                zobrist_key=zobrist_key,
                depth=depth,
                score=score,
                node_type=node_type,
                best_move=best_move,
                age=self.current_age
            )

    def new_search(self):
        """Incrementa age para nova busca"""
        self.current_age += 1

    def clear(self):
        """Limpa toda a tabela"""
        self.table.clear()
        self.current_age = 0


class MoveOrdering:
    """
    Ordenação inteligente de movimentos para melhorar cutoffs

    Ordem:
    1. PV move (da Transposition Table)
    2. Capturas (ordenadas por MVV-LVA)
    3. Killer moves
    4. History heuristic
    5. Demais movimentos
    """

    def __init__(self):
        # Killer moves: 2 melhores movimentos não-captura que causaram cutoff
        # killer_moves[depth] = [(from, to), (from, to)]
        self.killer_moves: Dict[int, List[Tuple[int, int]]] = {}

        # History heuristic: rastreia quais movimentos causam cutoffs
        # history[from][to] = score
        self.history: Dict[int, Dict[int, int]] = {}

        for i in range(1, 33):
            self.history[i] = {}
            for j in range(1, 33):
                self.history[i][j] = 0

    def update_killer(self, depth: int, from_field: int, to_field: int):
        """Atualiza killer moves para esta profundidade"""
        if depth not in self.killer_moves:
            self.killer_moves[depth] = []

        move = (from_field, to_field)

        # Se não está na lista, adiciona
        if move not in self.killer_moves[depth]:
            self.killer_moves[depth].insert(0, move)
            # Manter apenas 2 killers
            if len(self.killer_moves[depth]) > 2:
                self.killer_moves[depth].pop()

    def update_history(self, from_field: int, to_field: int, depth: int):
        """Atualiza history heuristic"""
        self.history[from_field][to_field] += depth * depth

    def get_move_score(self, move, is_capture: bool, depth: int,
                       pv_move: Optional[Tuple] = None) -> int:
        """
        Retorna score do movimento para ordenação

        Score maior = melhor movimento (será avaliado primeiro)
        """
        # PV move tem prioridade máxima
        if pv_move and self._moves_equal(move, pv_move, is_capture):
            return 1_000_000

        if is_capture:
            # Ordenar capturas por MVV-LVA (Most Valuable Victim - Least Valuable Aggressor)
            # Capturar dama = melhor, capturar com peão = melhor
            num_captured = len(move.captured_fields)
            return 900_000 + num_captured * 100

        # Movimentos simples
        from_field, to_field = move[0], move[1]

        # Base score
        base_score = 0

        # Killer moves
        if depth in self.killer_moves:
            if (from_field, to_field) in self.killer_moves[depth]:
                idx = self.killer_moves[depth].index((from_field, to_field))
                base_score = 800_000 - idx * 1000
        else:
            # History heuristic
            base_score = self.history.get(from_field, {}).get(to_field, 0)

        # NOVO: Bonus para avanço de peões (crucial para táticas de promoção!)
        # Detectar se é avanço de peão calculando diferença de campo
        # Sistema: campos 1-32, menores = mais avançados para brancos
        # Brancos avançam de campos maiores para menores
        # Pretos avançam de campos menores para maiores
        pawn_advance_bonus = 0
        if from_field > to_field:
            # Branco avançando (campo diminui)
            # Calcular quantas linhas avança
            from_y = ((from_field - 1) // 4) + 1
            to_y = ((to_field - 1) // 4) + 1
            lines_advanced = from_y - to_y

            # Bonus progressivo por linha - MÁXIMA PRIORIDADE!
            if to_y == 2:  # Chegando na linha 7 (penúltima)
                pawn_advance_bonus = 850_000  # Maior que killers!
            elif to_y == 3:  # Chegando na linha 6
                pawn_advance_bonus = 820_000
            elif to_y == 4:  # Chegando na linha 5
                pawn_advance_bonus = 810_000

            # Bonus adicional para colunas centrais (mais táticas!)
            # Campos centrais: 6,7,10,11,14,15,18,19,22,23,26,27
            if to_field in [7, 11, 15, 19, 23, 27]:  # Colunas d/e
                pawn_advance_bonus += 10_000
        elif to_field > from_field:
            # Preto avançando (campo aumenta)
            from_y = ((from_field - 1) // 4) + 1
            to_y = ((to_field - 1) // 4) + 1
            lines_advanced = to_y - from_y

            if to_y == 7:  # Chegando na linha 2 (penúltima para pretos)
                pawn_advance_bonus = 850_000
            elif to_y == 6:  # Chegando na linha 3
                pawn_advance_bonus = 820_000
            elif to_y == 5:  # Chegando na linha 4
                pawn_advance_bonus = 810_000

            if to_field in [6, 10, 14, 18, 22, 26]:  # Colunas d/e para pretos
                pawn_advance_bonus += 10_000

        return base_score + pawn_advance_bonus

    def _moves_equal(self, move1, move2, is_capture: bool) -> bool:
        """Verifica se dois movimentos são iguais"""
        if is_capture:
            return (move1.from_field == move2[0] and
                    move1.to_field == move2[1])
        else:
            return move1[0] == move2[0] and move1[1] == move2[1]

    def clear_history(self):
        """Limpa history (útil entre jogos)"""
        for i in range(1, 33):
            for j in range(1, 33):
                self.history[i][j] = 0

    def age_history(self, factor: float = 0.9):
        """
        Envelhecer history (reduzir valores antigos)
        Útil para dar mais peso a movimentos recentes
        """
        for i in range(1, 33):
            for j in range(1, 33):
                self.history[i][j] = int(self.history[i][j] * factor)


# Continua no próximo arquivo...
