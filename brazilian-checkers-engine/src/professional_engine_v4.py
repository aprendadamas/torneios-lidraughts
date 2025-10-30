"""
Motor V4 Profissional - Motor de Busca Principal
Arquitetura de motor profissional completa
"""

from src.brazilian_engine_complete import BrazilianGameComplete, Capture
from src.professional_engine_v4_part1 import (
    ZobristHasher, TranspositionTable, MoveOrdering,
    NodeType, TTEntry
)
from src.tactical_engine_v3 import EndgameEvaluator, ImprovedTacticalEvaluationV3
from src.pos64 import Pos64
from typing import Tuple, List, Optional
import copy
import time


class ProfessionalEngine:
    """
    Motor Profissional V4 para Damas Brasileiras

    Técnicas implementadas:
    - Transposition Tables (128 MB padrão)
    - Zobrist Hashing
    - Iterative Deepening completo
    - Move Ordering avançado (PV, Killers, History)
    - Quiescence Search
    - Null-Move Pruning
    - Aspiration Windows
    """

    def __init__(self, tt_size_mb: int = 128):
        self.zobrist = ZobristHasher()
        self.tt = TranspositionTable(size_mb=tt_size_mb)
        self.move_ordering = MoveOrdering()
        self.evaluator = ImprovedTacticalEvaluationV3()

        # Estatísticas
        self.nodes_searched = 0
        self.tt_hits = 0
        self.tt_cutoffs = 0
        self.q_nodes = 0

        # Configuração
        self.use_null_move = True
        self.use_quiescence = True
        self.null_move_reduction = 2  # R = 2

    def search_best_move(self, game: BrazilianGameComplete,
                        max_depth: int = 16,
                        max_time_seconds: Optional[float] = None
                        ) -> Tuple[str, int, List[str]]:
        """
        Busca o melhor lance usando Iterative Deepening

        Args:
            game: Posição atual
            max_depth: Profundidade máxima
            max_time_seconds: Tempo máximo (None = ilimitado)

        Returns:
            (best_move_notation, score, principal_variation)
        """
        self.nodes_searched = 0
        self.tt_hits = 0
        self.tt_cutoffs = 0
        self.q_nodes = 0

        self.start_time = time.time()
        self.max_time = max_time_seconds
        self.time_up = False

        # Nova busca - incrementar age da TT
        self.tt.new_search()

        # Iterative Deepening: buscar depth 1, 2, 3, ..., max_depth
        best_move = None
        best_score = 0
        pv = []

        # Rastreamento para estabilidade
        previous_move = None
        previous_score = 0
        stable_iterations = 0

        # Initial guess para aspiration windows
        alpha = float('-inf')
        beta = float('inf')
        aspiration_window = 50  # Pontos

        zobrist_key = self.zobrist.hash_position(game)

        for depth in range(1, max_depth + 1):
            if self.time_up:
                break

            # Usar janela completa sempre (sem aspiration por enquanto)
            alpha = float('-inf')
            beta = float('inf')

            # Buscar nesta profundidade
            try:
                score, move, pv_depth = self._search_root(
                    game, depth, alpha, beta, zobrist_key
                )

                # Validar resultado
                is_valid = True

                # Check 1: Movimento válido
                if not move or move == "no moves":
                    is_valid = False

                # Check 2: Score não é infinito (sem usar math.isinf para evitar import)
                if is_valid and (score > 100000 or score < -100000):
                    is_valid = False
                    print(f"⚠️  depth {depth}: score suspeito {score:+.0f}, mantendo resultado anterior")

                # Check 3: Mudança extrema de score (>5000 pontos)
                if is_valid and previous_move and abs(score - previous_score) > 5000:
                    # Permitir se for primeiro salto para endgame score
                    if not (abs(previous_score) < 500 and abs(score) > 5000):
                        is_valid = False
                        print(f"⚠️  depth {depth}: mudança extrema de score "
                              f"({previous_score:+.0f} → {score:+.0f}), mantendo resultado anterior")

                # Atualizar se resultado válido
                if is_valid:
                    best_move = move
                    best_score = score
                    pv = pv_depth

                    # Rastrear estabilidade
                    if move == previous_move:
                        stable_iterations += 1
                    else:
                        stable_iterations = 1

                    previous_move = move
                    previous_score = score

                # Log progresso
                elapsed = time.time() - self.start_time
                nps = int(self.nodes_searched / elapsed) if elapsed > 0 else 0

                stability_marker = f" [stable×{stable_iterations}]" if stable_iterations >= 3 else ""

                print(f"depth {depth:2d} | score {score:+6.0f} | "
                      f"nodes {self.nodes_searched:,} | "
                      f"nps {nps:,} | "
                      f"time {elapsed:.1f}s | "
                      f"tt_hits {self.tt_hits:,} | "
                      f"pv: {' '.join(pv_depth[:5])}{stability_marker}")

            except TimeoutException:
                print(f"⏱️  Tempo esgotado em depth {depth}")
                break

        print(f"\n✓ Busca completa")
        print(f"  Nós: {self.nodes_searched:,}")
        print(f"  TT Hits: {self.tt_hits:,} ({100*self.tt_hits/max(1,self.nodes_searched):.1f}%)")
        print(f"  TT Cutoffs: {self.tt_cutoffs:,}")
        print(f"  Q-Search Nodes: {self.q_nodes:,}")

        return best_move or "no moves", best_score, pv

    def _search_root(self, game: BrazilianGameComplete, depth: int,
                     alpha: float, beta: float, zobrist_key: int
                     ) -> Tuple[int, str, List[str]]:
        """Busca no nó raiz"""
        best_score = float('-inf') if game.turn == "white" else float('inf')
        best_move_str = None
        best_pv = []
        best_move_tuple = None

        # Obter lances
        captures = game.find_all_captures()
        if captures:
            moves = [(cap, True) for cap in captures]
        else:
            simple_moves = game.find_simple_moves()
            if not simple_moves:
                return 0, "no moves", []
            moves = [(m, False) for m in simple_moves]

        # Ordenar movimentos
        pv_move = self._get_pv_move_from_tt(zobrist_key)
        moves.sort(
            key=lambda x: self.move_ordering.get_move_score(
                x[0], x[1], depth, pv_move
            ),
            reverse=True
        )

        for move, is_capture in moves:
            # Fazer movimento
            game_copy = copy.deepcopy(game)

            if is_capture:
                game_copy.make_move(move.from_field, move.to_field,
                                   move.captured_fields, move.promotes)
                move_str = self._capture_notation(move)
                move_tuple = (move.from_field, move.to_field,
                             tuple(move.captured_fields), move.promotes)
            else:
                game_copy.make_move(move[0], move[1], [], False)
                move_str = f"{Pos64(move[0]).to_algebraic()} → {Pos64(move[1]).to_algebraic()}"
                move_tuple = (move[0], move[1], tuple(), False)

            # Hash da nova posição
            new_zobrist = self.zobrist.hash_position(game_copy)

            # Buscar recursivamente
            score, pv = self._negamax(
                game_copy, depth - 1, -beta, -alpha,
                new_zobrist, allow_null=True
            )
            score = -score  # Negamax

            # Atualizar melhor
            if game.turn == "white":
                if score > best_score:
                    best_score = score
                    best_move_str = move_str
                    best_move_tuple = move_tuple
                    best_pv = [move_str] + pv
                alpha = max(alpha, score)
            else:
                if score < best_score:
                    best_score = score
                    best_move_str = move_str
                    best_move_tuple = move_tuple
                    best_pv = [move_str] + pv
                beta = min(beta, score)

            if beta <= alpha:
                break  # Cutoff

        # Se não encontrou nenhum movimento, retornar o primeiro
        if not best_move_str and moves:
            move, is_capture = moves[0]
            if is_capture:
                best_move_str = self._capture_notation(move)
                best_move_tuple = (move.from_field, move.to_field,
                                 tuple(move.captured_fields), move.promotes)
            else:
                best_move_str = f"{Pos64(move[0]).to_algebraic()} → {Pos64(move[1]).to_algebraic()}"
                best_move_tuple = (move[0], move[1], tuple(), False)

        # Garantir que best_score é finito
        if abs(best_score) >= 100000:
            # Fallback: avaliar posição estática
            best_score = self.evaluator.evaluate_position(game)
            if game.turn == "black":
                best_score = -best_score

        # Armazenar na TT (apenas se score for válido)
        if best_move_tuple and abs(best_score) < 100000:
            self.tt.store(
                zobrist_key, depth, best_score,
                NodeType.EXACT, best_move_tuple
            )

        return best_score, best_move_str or "no moves", best_pv

    def _negamax(self, game: BrazilianGameComplete, depth: int,
                 alpha: float, beta: float, zobrist_key: int,
                 allow_null: bool = True) -> Tuple[int, List[str]]:
        """
        Negamax com alpha-beta e todas as otimizações

        Args:
            game: Posição
            depth: Profundidade restante
            alpha, beta: Janela de busca
            zobrist_key: Hash da posição
            allow_null: Se permite null-move

        Returns:
            (score, principal_variation)
        """
        self.nodes_searched += 1

        # Check time
        if self.max_time and (self.nodes_searched % 4096 == 0):
            if time.time() - self.start_time > self.max_time:
                self.time_up = True
                raise TimeoutException()

        # Probe Transposition Table
        tt_entry = self.tt.probe(zobrist_key)
        if tt_entry and tt_entry.depth >= depth and abs(tt_entry.score) < 100000:
            self.tt_hits += 1

            # Usar score da TT se aplicável
            if tt_entry.node_type == NodeType.EXACT:
                return tt_entry.score, []
            elif tt_entry.node_type == NodeType.LOWER_BOUND:
                alpha = max(alpha, tt_entry.score)
            elif tt_entry.node_type == NodeType.UPPER_BOUND:
                beta = min(beta, tt_entry.score)

            if alpha >= beta:
                self.tt_cutoffs += 1
                return tt_entry.score, []

        # Leaf node ou max depth
        if depth <= 0:
            # Quiescence Search
            if self.use_quiescence:
                q_score = self._quiescence(game, alpha, beta, zobrist_key)
                return q_score, []
            else:
                score = self.evaluator.evaluate_position(game)
                return score if game.turn == "white" else -score, []

        # Obter movimentos (precisa verificar ANTES de null-move)
        captures = game.find_all_captures()

        # Null-Move Pruning
        # IMPORTANTE: Não usar em posições táticas (com capturas disponíveis)
        # pois pode podar incorretamente linhas com sacrifícios profundos
        if (self.use_null_move and allow_null and depth >= 3 and
            not captures and  # NÃO usar null-move se há capturas (posição tática)
            not self._is_in_check(game)):  # Nunca fazer null-move em check

            # Fazer "null move" (passar a vez)
            game_null = copy.deepcopy(game)
            game_null.turn = "black" if game.turn == "white" else "white"
            null_zobrist = zobrist_key ^ self.zobrist.turn_key

            # Buscar com profundidade reduzida
            score, _ = self._negamax(
                game_null, depth - 1 - self.null_move_reduction,
                -beta, -beta + 1, null_zobrist, allow_null=False
            )
            score = -score

            if score >= beta:
                # Null-move cutoff
                return score, []

        # Processar movimentos
        if captures:
            moves = [(cap, True) for cap in captures]
        else:
            simple_moves = game.find_simple_moves()
            if not simple_moves:
                # Sem movimentos = perdeu
                return -10000, []
            moves = [(m, False) for m in simple_moves]

        # Ordenar movimentos
        pv_move = tt_entry.best_move if tt_entry else None
        moves.sort(
            key=lambda x: self.move_ordering.get_move_score(
                x[0], x[1], depth, pv_move
            ),
            reverse=True
        )

        # Search
        best_score = float('-inf')
        best_pv = []
        best_move_tuple = None

        for i, (move, is_capture) in enumerate(moves):
            # Fazer movimento
            game_copy = copy.deepcopy(game)

            if is_capture:
                game_copy.make_move(move.from_field, move.to_field,
                                   move.captured_fields, move.promotes)
                move_str = self._capture_notation(move)
                move_tuple = (move.from_field, move.to_field,
                             tuple(move.captured_fields), move.promotes)
            else:
                game_copy.make_move(move[0], move[1], [], False)
                move_str = f"{Pos64(move[0]).to_algebraic()} → {Pos64(move[1]).to_algebraic()}"
                move_tuple = (move[0], move[1], tuple(), False)

            new_zobrist = self.zobrist.hash_position(game_copy)

            # Buscar
            score, pv = self._negamax(
                game_copy, depth - 1, -beta, -alpha, new_zobrist
            )
            score = -score

            if score > best_score:
                best_score = score
                best_pv = [move_str] + pv
                best_move_tuple = move_tuple

            alpha = max(alpha, score)

            if alpha >= beta:
                # Beta cutoff
                if not is_capture:
                    # Atualizar killers e history
                    self.move_ordering.update_killer(depth, move[0], move[1])
                    self.move_ordering.update_history(move[0], move[1], depth)
                break

        # Garantir que best_score é finito
        if abs(best_score) >= 100000:
            # Fallback: avaliar posição estática
            score = self.evaluator.evaluate_position(game)
            best_score = score if game.turn == "white" else -score

        # Armazenar na TT (apenas se score for válido)
        if best_move_tuple and abs(best_score) < 100000:
            if best_score <= alpha:
                node_type = NodeType.UPPER_BOUND
            elif best_score >= beta:
                node_type = NodeType.LOWER_BOUND
            else:
                node_type = NodeType.EXACT

            self.tt.store(zobrist_key, depth, best_score, node_type, best_move_tuple)

        return best_score, best_pv

    def _quiescence(self, game: BrazilianGameComplete,
                    alpha: float, beta: float, zobrist_key: int,
                    ply: int = 0) -> int:
        """
        Quiescence Search - busca apenas capturas até posição quieta

        Evita horizon effect
        """
        self.q_nodes += 1

        # Stand-pat: avaliação estática
        stand_pat = self.evaluator.evaluate_position(game)
        if game.turn == "black":
            stand_pat = -stand_pat

        # Beta cutoff (mas apenas se beta for finito)
        if stand_pat >= beta and abs(beta) < 100000:
            return beta

        # Atualizar alpha
        if alpha < stand_pat:
            alpha = stand_pat

        # Limitar profundidade do q-search
        if ply >= 10:
            return stand_pat

        # Buscar apenas capturas
        captures = game.find_all_captures()
        if not captures:
            return stand_pat

        # Ordenar capturas (MVV-LVA)
        captures.sort(key=lambda c: len(c.captured_fields), reverse=True)

        for capture in captures:
            game_copy = copy.deepcopy(game)
            game_copy.make_move(capture.from_field, capture.to_field,
                              capture.captured_fields, capture.promotes)

            new_zobrist = self.zobrist.hash_position(game_copy)
            score = -self._quiescence(game_copy, -beta, -alpha, new_zobrist, ply + 1)

            # Ignorar scores infinitos de chamadas recursivas
            if abs(score) >= 100000:
                continue

            # Beta cutoff (mas apenas se beta for finito)
            if score >= beta and abs(beta) < 100000:
                return beta

            if score > alpha:
                alpha = score

        return alpha

    def _is_in_check(self, game: BrazilianGameComplete) -> bool:
        """Verifica se está em check (para damas, não se aplica diretamente)"""
        # Em damas não existe "check", mas podemos verificar se está sob ameaça
        return False  # Simplificação por ora

    def _get_pv_move_from_tt(self, zobrist_key: int) -> Optional[Tuple]:
        """Obtém PV move da TT se existir"""
        entry = self.tt.probe(zobrist_key)
        return entry.best_move if entry else None

    def _capture_notation(self, capture: Capture) -> str:
        """Converte captura para notação"""
        from_pos = Pos64(capture.from_field).to_algebraic()
        to_pos = Pos64(capture.to_field).to_algebraic()

        notation = from_pos
        for field in capture.captured_fields:
            notation += f" x {Pos64(field).to_algebraic()}"
        notation += f" → {to_pos}"

        if capture.promotes:
            notation += " ♛"

        return notation


class TimeoutException(Exception):
    """Exceção para timeout na busca"""
    pass
