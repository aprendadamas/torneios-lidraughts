"""
Motor Tático MELHORADO v2
Reconhece padrões de duplo sacrifício e capturas de damas
"""

from typing import List, Tuple, Optional
from src.brazilian_engine_complete import BrazilianGameComplete, Capture
from src.pos64 import Pos64


class ImprovedTacticalEvaluation:
    """Avaliação tática melhorada"""

    @staticmethod
    def evaluate_position(game: BrazilianGameComplete, depth: int = 0, sacrifice_count: int = 0) -> float:
        """
        Avalia uma posição com reconhecimento de sacrifícios múltiplos

        sacrifice_count: número de sacrifícios na linha atual (para tolerância)
        """
        # Material básico
        white_men = len(game.white_men)
        white_kings = len(game.white_kings)
        black_men = len(game.black_men)
        black_kings = len(game.black_kings)

        # Pesos
        MAN_VALUE = 100
        KING_VALUE = 350  # Aumentado de 300 para 350

        material = (white_men * MAN_VALUE + white_kings * KING_VALUE) - \
                   (black_men * MAN_VALUE + black_kings * KING_VALUE)

        # Verificar vitória
        if black_men + black_kings == 0:
            return 10000 - depth
        if white_men + white_kings == 0:
            return -10000 + depth

        # NOVO: Tolerância a material negativo se houver sacrifícios na linha
        if sacrifice_count > 0:
            # Se fizemos sacrifícios, ser mais tolerante com material negativo
            # Cada sacrifício permite -150 de material temporário
            material_tolerance = sacrifice_count * 150
            if game.turn == "white" and material < 0:
                # Material negativo para brancas, mas há sacrifícios
                material = max(material, -material_tolerance)
            elif game.turn == "black" and material > 0:
                material = min(material, material_tolerance)

        # Bonificação por capturas múltiplas disponíveis
        capture_bonus = 0
        king_capture_bonus = 0

        if game.turn == "white":
            caps = game.find_all_captures()
            if caps:
                max_captures = max(len(c.captured_fields) for c in caps)
                capture_bonus = max_captures * 60  # Aumentado de 50 para 60

                # NOVO: Bônus extra para captura de damas
                for cap in caps:
                    kings_captured = 0
                    for cf in cap.captured_fields:
                        if cf in game.black_kings:
                            kings_captured += 1
                    king_capture_bonus += kings_captured * 200  # 200 pts por dama capturada

                    # Bonificação extra se captura elimina todas as pretas
                    pieces_after = (black_men + black_kings) - len(cap.captured_fields)
                    if pieces_after == 0:
                        capture_bonus += 600  # Aumentado de 500 para 600
        else:
            caps = game.find_all_captures()
            if caps:
                max_captures = max(len(c.captured_fields) for c in caps)
                capture_bonus = -max_captures * 60

                # Bônus para pretas capturarem damas brancas
                for cap in caps:
                    kings_captured = 0
                    for cf in cap.captured_fields:
                        if cf in game.white_kings:
                            kings_captured += 1
                    king_capture_bonus -= kings_captured * 200

                    pieces_after = (white_men + white_kings) - len(cap.captured_fields)
                    if pieces_after == 0:
                        capture_bonus -= 600

        # Bonificação por promoção
        promotion_bonus = 0
        if game.turn == "white":
            for field in game.white_men:
                distance_to_promo = field
                if distance_to_promo <= 4:
                    promotion_bonus += 35  # Aumentado de 30
                elif distance_to_promo <= 8:
                    promotion_bonus += 25
                elif distance_to_promo <= 12:
                    promotion_bonus += 15
        else:
            for field in game.black_men:
                distance_to_promo = 33 - field
                if distance_to_promo <= 4:
                    promotion_bonus -= 35
                elif distance_to_promo <= 8:
                    promotion_bonus -= 25
                elif distance_to_promo <= 12:
                    promotion_bonus -= 15

        total = material + capture_bonus + king_capture_bonus + promotion_bonus

        return total


class ImprovedTacticalSearchEngine:
    """Motor de busca tático melhorado"""

    def __init__(self):
        self.evaluator = ImprovedTacticalEvaluation()
        self.nodes_searched = 0

    def search_best_move(self, game: BrazilianGameComplete, max_depth: int = 6) -> Tuple[Optional[str], float, List[str]]:
        """
        Busca o melhor movimento com reconhecimento de sacrifícios

        Retorna: (movimento, avaliação, sequência_principal)
        """
        self.nodes_searched = 0

        best_score = -999999 if game.turn == "white" else 999999
        best_move = None
        best_sequence = []

        # Capturas obrigatórias
        caps = game.find_all_captures()

        if caps:
            for cap in caps:
                test_game = game.copy()

                notation = Pos64(cap.from_field).to_algebraic()
                for cf in cap.captured_fields:
                    notation += f" x {Pos64(cf).to_algebraic()}"
                notation += f" → {Pos64(cap.to_field).to_algebraic()}"
                if cap.promotes:
                    notation += " ♛"

                test_game.make_move(cap.from_field, cap.to_field, cap.captured_fields, cap.promotes)

                # Verificar se captura inclui damas
                kings_captured = sum(1 for cf in cap.captured_fields
                                   if cf in (game.white_kings if game.turn == "black" else game.black_kings))

                score, seq = self._minimax(test_game, max_depth - 1, -999999, 999999,
                                           game.turn == "black", 1, sacrifice_count=0)

                if game.turn == "white":
                    if score > best_score:
                        best_score = score
                        best_move = notation
                        best_sequence = [notation] + seq
                else:
                    if score < best_score:
                        best_score = score
                        best_move = notation
                        best_sequence = [notation] + seq

            return (best_move, best_score, best_sequence)

        # Movimentos simples - DETECTAR SACRIFÍCIOS
        moves = game.find_simple_moves()

        for from_f, to_f, promotes in moves:
            test_game = game.copy()

            notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
            if promotes:
                notation += " ♛"

            test_game.make_move(from_f, to_f, [], promotes)

            # NOVO: Detectar se é sacrifício
            is_sacrifice = False
            sacrifice_count = 0

            enemy_caps = test_game.find_all_captures()
            for enemy_cap in enemy_caps:
                if to_f in enemy_cap.captured_fields:
                    is_sacrifice = True
                    sacrifice_count = 1
                    break

            # NOVO: Se é sacrifício, aumentar profundidade
            extra_depth = 0
            if is_sacrifice:
                extra_depth = 3  # +3 profundidade para sacrifícios

            score, seq = self._minimax(test_game, max_depth - 1 + extra_depth, -999999, 999999,
                                       game.turn == "black", 1, sacrifice_count=sacrifice_count)

            if game.turn == "white":
                if score > best_score:
                    best_score = score
                    best_move = notation
                    best_sequence = [notation] + seq
            else:
                if score < best_score:
                    best_score = score
                    best_move = notation
                    best_sequence = [notation] + seq

        return (best_move, best_score, best_sequence)

    def _minimax(self, game: BrazilianGameComplete, depth: int, alpha: float, beta: float,
                 maximizing: bool, current_depth: int, sacrifice_count: int = 0) -> Tuple[float, List[str]]:
        """
        Busca minimax com alpha-beta pruning e contagem de sacrifícios
        """
        self.nodes_searched += 1

        if depth <= 0:
            return (self.evaluator.evaluate_position(game, current_depth, sacrifice_count), [])

        # Verificar fim de jogo
        if len(game.white_men) + len(game.white_kings) == 0:
            return (-10000 + current_depth, [])
        if len(game.black_men) + len(game.black_kings) == 0:
            return (10000 - current_depth, [])

        # Capturas obrigatórias
        caps = game.find_all_captures()

        if caps:
            if maximizing:
                max_eval = -999999
                best_seq = []

                for cap in caps:
                    notation = Pos64(cap.from_field).to_algebraic()
                    for cf in cap.captured_fields:
                        notation += f" x {Pos64(cf).to_algebraic()}"
                    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
                    if cap.promotes:
                        notation += " ♛"

                    new_game = game.copy()
                    new_game.make_move(cap.from_field, cap.to_field, cap.captured_fields, cap.promotes)

                    eval_score, seq = self._minimax(new_game, depth - 1, alpha, beta, False,
                                                    current_depth + 1, sacrifice_count)

                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_seq = [notation] + seq

                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break

                return (max_eval, best_seq)
            else:
                min_eval = 999999
                best_seq = []

                for cap in caps:
                    notation = Pos64(cap.from_field).to_algebraic()
                    for cf in cap.captured_fields:
                        notation += f" x {Pos64(cf).to_algebraic()}"
                    notation += f" → {Pos64(cap.to_field).to_algebraic()}"
                    if cap.promotes:
                        notation += " ♛"

                    new_game = game.copy()
                    new_game.make_move(cap.from_field, cap.to_field, cap.captured_fields, cap.promotes)

                    eval_score, seq = self._minimax(new_game, depth - 1, alpha, beta, True,
                                                    current_depth + 1, sacrifice_count)

                    if eval_score < min_eval:
                        min_eval = eval_score
                        best_seq = [notation] + seq

                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break

                return (min_eval, best_seq)

        # Movimentos simples
        moves = game.find_simple_moves()

        if not moves:
            # Sem movimentos = derrota
            if maximizing:
                return (-10000 + current_depth, [])
            else:
                return (10000 - current_depth, [])

        if maximizing:
            max_eval = -999999
            best_seq = []

            for from_f, to_f, promotes in moves:
                notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
                if promotes:
                    notation += " ♛"

                new_game = game.copy()
                new_game.make_move(from_f, to_f, [], promotes)

                # NOVO: Detectar se próximo jogador pode capturar (= é sacrifício)
                new_sacrifice_count = sacrifice_count
                next_caps = new_game.find_all_captures()
                for next_cap in next_caps:
                    if to_f in next_cap.captured_fields:
                        new_sacrifice_count += 1
                        break

                eval_score, seq = self._minimax(new_game, depth - 1, alpha, beta, False,
                                                current_depth + 1, new_sacrifice_count)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_seq = [notation] + seq

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break

            return (max_eval, best_seq)
        else:
            min_eval = 999999
            best_seq = []

            for from_f, to_f, promotes in moves:
                notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"
                if promotes:
                    notation += " ♛"

                new_game = game.copy()
                new_game.make_move(from_f, to_f, [], promotes)

                # Detectar sacrifício
                new_sacrifice_count = sacrifice_count
                next_caps = new_game.find_all_captures()
                for next_cap in next_caps:
                    if to_f in next_cap.captured_fields:
                        new_sacrifice_count += 1
                        break

                eval_score, seq = self._minimax(new_game, depth - 1, alpha, beta, True,
                                                current_depth + 1, new_sacrifice_count)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_seq = [notation] + seq

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break

            return (min_eval, best_seq)
