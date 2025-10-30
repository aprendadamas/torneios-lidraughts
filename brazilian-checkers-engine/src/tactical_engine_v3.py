"""
Motor Tático V3 - Com detecção de bloqueio e avaliação de finais
Melhorias para resolver Exercício #1 (4800 Avançado)
"""

from src.brazilian_engine_complete import BrazilianGameComplete, Capture
from src.pos64 import Pos64
from typing import Tuple, List, Optional
import copy


class EndgameEvaluator:
    """Avalia posições de finais (damas vs peões)"""

    @staticmethod
    def is_pawn_blocked(game: BrazilianGameComplete, field: int, color: str) -> bool:
        """
        Detecta se um peão está bloqueado (sem mobilidade)

        Peão bloqueado = não pode avançar E não pode capturar
        """
        pos = Pos64(field)
        all_occupied = game.white_men | game.black_men | game.white_kings | game.black_kings

        # Usar os métodos de movimentação do Pos64
        if color == "white":
            # Brancos avançam para cima (y menor)
            forward_moves = [pos.move_up_left(), pos.move_up_right()]
        else:
            # Pretos avançam para baixo (y maior)
            forward_moves = [pos.move_down_left(), pos.move_down_right()]

        # Verificar se pode avançar
        can_advance = False
        for next_pos in forward_moves:
            if next_pos and next_pos.field not in all_occupied:
                can_advance = True
                break

        # Se pode avançar, não está bloqueado
        if can_advance:
            return False

        # Verificar se pode capturar (regras brasileiras: pode capturar em todas as 4 direções)
        enemy_pieces = game.black_men | game.black_kings if color == "white" else game.white_men | game.white_kings

        # Todas as 4 direções diagonais
        all_directions = [
            (pos.move_up_left, "up_left"),
            (pos.move_up_right, "up_right"),
            (pos.move_down_left, "down_left"),
            (pos.move_down_right, "down_right")
        ]

        for move_func, direction in all_directions:
            adjacent = move_func()
            if not adjacent:
                continue

            # Verificar se há peça inimiga adjacente
            if adjacent.field in enemy_pieces:
                # Há inimigo adjacente, verificar se espaço além está livre
                # Continuar na mesma direção
                beyond = getattr(Pos64(adjacent.field), f"move_{direction}")()

                if beyond and beyond.field not in all_occupied:
                    return False  # Pode capturar, não está bloqueado

        # Não pode avançar nem capturar = BLOQUEADO
        return True

    @staticmethod
    def count_blocked_pawns(game: BrazilianGameComplete, color: str) -> int:
        """Conta quantos peões de uma cor estão bloqueados"""
        pawns = game.white_men if color == "white" else game.black_men
        blocked_count = 0

        for field in pawns:
            if EndgameEvaluator.is_pawn_blocked(game, field, color):
                blocked_count += 1

        return blocked_count

    @staticmethod
    def evaluate_endgame(game: BrazilianGameComplete) -> Optional[int]:
        """
        Avalia posições de final
        Retorna score especial se for final conhecido, None caso contrário

        Conhecimento de finais:
        - 1 dama vs poucos peões (≤3) = vitória forçada
        - 1 dama vs peões bloqueados = vitória forçada (score maior)
        """
        white_total = len(game.white_men) + len(game.white_kings)
        black_total = len(game.black_men) + len(game.black_kings)

        # Final: 1 dama branca vs apenas peões pretos
        if (len(game.white_kings) == 1 and len(game.white_men) == 0 and
            len(game.black_kings) == 0 and len(game.black_men) > 0):

            num_pawns = len(game.black_men)

            # 1 dama vs 1-3 peões = vitória forçada
            if num_pawns <= 3:
                # Verificar se peões estão bloqueados para score mais alto
                blocked = EndgameEvaluator.count_blocked_pawns(game, "black")
                if blocked == num_pawns:
                    return 9999  # Peões bloqueados - vitória imediata
                else:
                    # Peões não bloqueados mas ainda vitória forçada
                    # Score alto mas menor que 9999 para distinguir
                    return 8000 + (3 - num_pawns) * 500  # 8500-9000 dependendo de quantos peões

            # 1 dama vs 4+ peões = vantagem mas não vitória garantida
            elif num_pawns <= 6:
                return 5000  # Grande vantagem

        # Final: 1 dama preta vs apenas peões brancos
        if (len(game.black_kings) == 1 and len(game.black_men) == 0 and
            len(game.white_kings) == 0 and len(game.white_men) > 0):

            num_pawns = len(game.white_men)

            # 1 dama vs 1-3 peões = vitória forçada
            if num_pawns <= 3:
                blocked = EndgameEvaluator.count_blocked_pawns(game, "white")
                if blocked == num_pawns:
                    return -9999
                else:
                    return -(8000 + (3 - num_pawns) * 500)

            # 1 dama vs 4+ peões = vantagem
            elif num_pawns <= 6:
                return -5000

        return None  # Não é um final conhecido


class ImprovedTacticalEvaluationV3:
    """Avaliação tática melhorada com conhecimento de finais"""

    @staticmethod
    def evaluate_position(game: BrazilianGameComplete, depth: int = 0,
                         sacrifice_count: int = 0) -> int:
        """
        Avalia uma posição do tabuleiro

        Melhorias V3:
        - Detecção de peões bloqueados
        - Avaliação de finais
        - Maior tolerance para sacrifícios profundos
        """
        # Primeiro: verificar se é um final conhecido
        endgame_score = EndgameEvaluator.evaluate_endgame(game)
        if endgame_score is not None:
            return endgame_score

        # Material base
        white_material = 0
        black_material = 0

        # Peões brancos
        for field in game.white_men:
            if EndgameEvaluator.is_pawn_blocked(game, field, "white"):
                white_material += 10  # Peão bloqueado vale quase nada
            else:
                white_material += 100  # Peão móvel

        # Damas brancas
        white_material += len(game.white_kings) * 300

        # Peões pretos
        for field in game.black_men:
            if EndgameEvaluator.is_pawn_blocked(game, field, "black"):
                black_material += 10  # Peão bloqueado vale quase nada
            else:
                black_material += 100  # Peão móvel

        # Damas pretas
        black_material += len(game.black_kings) * 300

        material = white_material - black_material

        # Tolerância a sacrifícios AUMENTADA para táticas profundas
        if sacrifice_count > 0:
            # V2 era: 150pts por sacrifício
            # V3: 300pts por sacrifício
            material_tolerance = sacrifice_count * 300

            # Bonus adicional para táticas MUITO profundas (4+ sacrifícios)
            if sacrifice_count >= 4:
                material_tolerance += 800  # Confiança em táticas extremas

            if game.turn == "white" and material < 0:
                material = max(material, -material_tolerance)
            elif game.turn == "black" and material > 0:
                material = min(material, material_tolerance)

        # Bonus por capturas de damas
        king_capture_bonus = 0
        if hasattr(game, '_last_capture_info'):
            kings_captured = game._last_capture_info.get('kings_captured', 0)
            king_capture_bonus = kings_captured * 200

        # Bonus posicional
        positional = 0

        # Peões avançados valem mais
        for field in game.white_men:
            pos = Pos64(field)
            if pos.y <= 3:  # Linhas 1-3 (avançados para brancos)
                positional += 20

        for field in game.black_men:
            pos = Pos64(field)
            if pos.y >= 6:  # Linhas 6-8 (avançados para pretos)
                positional -= 20

        # Centralização de damas
        center_fields = {18, 19, 22, 23}  # d4, e4, c5, d5 aproximadamente
        for field in game.white_kings:
            if field in center_fields:
                positional += 15

        for field in game.black_kings:
            if field in center_fields:
                positional -= 15

        return material + king_capture_bonus + positional


class ImprovedTacticalSearchEngineV3:
    """Motor de busca tática V3 com melhorias para exercícios avançados"""

    def __init__(self):
        self.nodes_searched = 0
        self.evaluator = ImprovedTacticalEvaluationV3()

    def search_best_move(self, game: BrazilianGameComplete, max_depth: int = 10) -> Tuple[str, int, List[str]]:
        """
        Busca o melhor lance usando minimax com alpha-beta pruning

        Returns:
            (best_move_notation, score, principal_variation)
        """
        self.nodes_searched = 0

        # Aumentar profundidade para posições complexas
        # Se há damas e poucos peões, pode ser final profundo
        total_pieces = (len(game.white_men) + len(game.white_kings) +
                       len(game.black_men) + len(game.black_kings))
        has_kings = len(game.white_kings) > 0 or len(game.black_kings) > 0

        if has_kings and total_pieces <= 8:
            # Posições de final podem precisar busca mais profunda
            max_depth = min(max_depth + 2, 12)  # Aumentar um pouco

        best_score = float('-inf') if game.turn == "white" else float('inf')
        best_move = None
        principal_variation = []

        # Obter todos os lances possíveis
        captures = game.find_all_captures()

        if captures:
            moves = [(cap, True) for cap in captures]
        else:
            simple_moves = game.find_simple_moves()
            moves = [(move, False) for move in simple_moves]

        # Ordenar movimentos (capturas longas primeiro)
        if captures:
            moves.sort(key=lambda x: len(x[0].captured_fields) if x[1] else 0, reverse=True)

        for move, is_capture in moves:
            # Fazer o lance
            game_copy = copy.deepcopy(game)

            if is_capture:
                game_copy.make_move(move.from_field, move.to_field,
                                   move.captured_fields, move.promotes)
                move_notation = self._capture_notation(move)
            else:
                game_copy.make_move(move[0], move[1], [], False)
                move_notation = f"{Pos64(move[0]).to_algebraic()} → {Pos64(move[1]).to_algebraic()}"

            # Avaliar recursivamente
            score, pv = self._minimax(game_copy, max_depth - 1, float('-inf'),
                                     float('inf'), sacrifice_count=0)

            # Atualizar melhor lance
            if game.turn == "white":
                if score > best_score:
                    best_score = score
                    best_move = move_notation
                    principal_variation = [move_notation] + pv
            else:
                if score < best_score:
                    best_score = score
                    best_move = move_notation
                    principal_variation = [move_notation] + pv

        return best_move or "no moves", best_score, principal_variation

    def _minimax(self, game: BrazilianGameComplete, depth: int, alpha: float,
                 beta: float, sacrifice_count: int = 0) -> Tuple[int, List[str]]:
        """Busca minimax com alpha-beta pruning"""
        self.nodes_searched += 1

        # Condição de parada
        if depth == 0:
            score = self.evaluator.evaluate_position(game, depth, sacrifice_count)
            return score, []

        # Obter lances possíveis
        captures = game.find_all_captures()

        if captures:
            moves = [(cap, True) for cap in captures]
        else:
            simple_moves = game.find_simple_moves()
            if not simple_moves:
                # Sem lances = perdeu
                return (-10000, []) if game.turn == "white" else (10000, [])
            moves = [(move, False) for move in simple_moves]

        # Ordenar (capturas longas primeiro)
        if captures:
            moves.sort(key=lambda x: len(x[0].captured_fields) if x[1] else 0, reverse=True)

        best_pv = []

        if game.turn == "white":
            max_eval = float('-inf')

            for move, is_capture in moves:
                game_copy = copy.deepcopy(game)

                # Detectar sacrifício
                new_sacrifice_count = sacrifice_count
                if is_capture:
                    # Verificar se é um sacrifício (capturamos menos do que perdemos)
                    captured_value = len(move.captured_fields) * 100
                    # Simplificação: assumir que sacrificamos 1 peça
                    # (análise completa seria muito complexa)
                    game_copy.make_move(move.from_field, move.to_field,
                                       move.captured_fields, move.promotes)
                    move_notation = self._capture_notation(move)
                else:
                    game_copy.make_move(move[0], move[1], [], False)
                    move_notation = f"{Pos64(move[0]).to_algebraic()} → {Pos64(move[1]).to_algebraic()}"

                eval_score, pv = self._minimax(game_copy, depth - 1, alpha, beta, new_sacrifice_count)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_pv = [move_notation] + pv

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Poda beta

            return max_eval, best_pv

        else:  # black's turn
            min_eval = float('inf')

            for move, is_capture in moves:
                game_copy = copy.deepcopy(game)

                if is_capture:
                    game_copy.make_move(move.from_field, move.to_field,
                                       move.captured_fields, move.promotes)
                    move_notation = self._capture_notation(move)
                else:
                    game_copy.make_move(move[0], move[1], [], False)
                    move_notation = f"{Pos64(move[0]).to_algebraic()} → {Pos64(move[1]).to_algebraic()}"

                eval_score, pv = self._minimax(game_copy, depth - 1, alpha, beta, sacrifice_count)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_pv = [move_notation] + pv

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Poda alfa

            return min_eval, best_pv

    def _capture_notation(self, capture: Capture) -> str:
        """Converte captura para notação legível"""
        from_pos = Pos64(capture.from_field).to_algebraic()
        to_pos = Pos64(capture.to_field).to_algebraic()

        notation = from_pos
        for field in capture.captured_fields:
            notation += f" x {Pos64(field).to_algebraic()}"
        notation += f" → {to_pos}"

        if capture.promotes:
            notation += " ♛"

        return notation
