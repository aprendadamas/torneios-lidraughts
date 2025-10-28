"""
Motor Tático de Damas Brasileiras
Implementa avaliação tática que reconhece padrões como sacrifícios
"""

from typing import List, Tuple, Optional
from src.brazilian_engine_complete import BrazilianGameComplete, Capture
from src.pos64 import Pos64


class TacticalEvaluation:
    """Avaliação tática de posições"""

    @staticmethod
    def evaluate_position(game: BrazilianGameComplete, depth: int = 0) -> float:
        """
        Avalia uma posição considerando fatores táticos

        Retorna: score positivo = brancas melhor, negativo = pretas melhor
        """
        # Material básico
        white_men = len(game.white_men)
        white_kings = len(game.white_kings)
        black_men = len(game.black_men)
        black_kings = len(game.black_kings)

        # Pesos
        MAN_VALUE = 100
        KING_VALUE = 300

        material = (white_men * MAN_VALUE + white_kings * KING_VALUE) - \
                   (black_men * MAN_VALUE + black_kings * KING_VALUE)

        # Verificar vitória
        if black_men + black_kings == 0:
            return 10000 - depth  # Vitória mais rápida é melhor
        if white_men + white_kings == 0:
            return -10000 + depth

        # Bonificação por capturas múltiplas disponíveis
        capture_bonus = 0
        if game.turn == "white":
            caps = game.find_all_captures()
            if caps:
                max_captures = max(len(c.captured_fields) for c in caps)
                capture_bonus = max_captures * 50

                # Bonificação extra se captura múltipla elimina todas as pretas
                for cap in caps:
                    pieces_after = (black_men + black_kings) - len(cap.captured_fields)
                    if pieces_after == 0:
                        capture_bonus += 500  # Captura que vence o jogo!

        else:
            caps = game.find_all_captures()
            if caps:
                max_captures = max(len(c.captured_fields) for c in caps)
                capture_bonus = -max_captures * 50

                for cap in caps:
                    pieces_after = (white_men + white_kings) - len(cap.captured_fields)
                    if pieces_after == 0:
                        capture_bonus -= 500

        # Bonificação por promoção
        promotion_bonus = 0
        if game.turn == "white":
            for field in game.white_men:
                pos = Pos64(field)
                # Quanto mais perto da promoção, melhor
                distance_to_promo = field  # Campos menores = mais perto da linha 1-4
                if distance_to_promo <= 4:
                    promotion_bonus += 30
                elif distance_to_promo <= 8:
                    promotion_bonus += 20
                elif distance_to_promo <= 12:
                    promotion_bonus += 10
        else:
            for field in game.black_men:
                distance_to_promo = 33 - field  # Campos maiores = mais perto da linha 29-32
                if distance_to_promo <= 4:
                    promotion_bonus -= 30
                elif distance_to_promo <= 8:
                    promotion_bonus -= 20
                elif distance_to_promo <= 12:
                    promotion_bonus -= 10

        total = material + capture_bonus + promotion_bonus

        return total

    @staticmethod
    def is_tactical_sacrifice(game: BrazilianGameComplete, from_field: int, to_field: int) -> Tuple[bool, float]:
        """
        Detecta se um movimento é um sacrifício tático válido

        Retorna: (é_sacrifício, valor_tático)
        """
        # Simular o movimento
        test_game = BrazilianGameComplete(
            game.white_men.copy(), game.black_men.copy(),
            game.white_kings.copy(), game.black_kings.copy(),
            game.turn
        )

        test_game.make_move(from_field, to_field, [], False)

        # Verificar se oponente pode capturar
        opponent_caps = test_game.find_all_captures()

        if not opponent_caps:
            return (False, 0.0)

        # É um sacrifício se perde a peça
        piece_lost = False
        for cap in opponent_caps:
            if to_field in cap.captured_fields:
                piece_lost = True
                break

        if not piece_lost:
            return (False, 0.0)

        # Avaliar se o sacrifício é tático (leva a ganho)
        tactical_value = 0.0

        # Para cada possível resposta do oponente
        for cap in opponent_caps:
            if to_field not in cap.captured_fields:
                continue

            # Simular captura do oponente
            test_game2 = BrazilianGameComplete(
                test_game.white_men.copy(), test_game.black_men.copy(),
                test_game.white_kings.copy(), test_game.black_kings.copy(),
                test_game.turn
            )

            test_game2.make_move(cap.from_field, cap.to_field, cap.captured_fields, cap.promotes)

            # Verificar contra-ataques disponíveis
            counter_caps = test_game2.find_all_captures()

            if counter_caps:
                # Avaliar melhor contra-ataque
                best_counter = max(counter_caps, key=lambda c: len(c.captured_fields))

                # Se contra-ataque captura múltiplas peças, é tático!
                if len(best_counter.captured_fields) >= 2:
                    tactical_value = max(tactical_value, len(best_counter.captured_fields) * 100)

                # Se contra-ataque leva à vitória, é MUITO tático!
                pieces_after_counter = (len(test_game2.black_men) + len(test_game2.black_kings)) - \
                                      len(best_counter.captured_fields)
                if pieces_after_counter == 0:
                    tactical_value = max(tactical_value, 1000)

        return (tactical_value > 0, tactical_value)


class TacticalSearchEngine:
    """Motor de busca que reconhece táticas"""

    def __init__(self):
        self.evaluator = TacticalEvaluation()
        self.nodes_searched = 0

    def search_best_move(self, game: BrazilianGameComplete, max_depth: int = 6) -> Tuple[Optional[str], float, List[str]]:
        """
        Busca o melhor movimento considerando táticas

        Retorna: (movimento, avaliação, sequência_principal)
        """
        self.nodes_searched = 0

        best_score = -999999 if game.turn == "white" else 999999
        best_move = None
        best_sequence = []

        # Verificar capturas obrigatórias
        caps = game.find_all_captures()

        if caps:
            # Avaliar cada captura
            for cap in caps:
                test_game = BrazilianGameComplete(
                    game.white_men.copy(), game.black_men.copy(),
                    game.white_kings.copy(), game.black_kings.copy(),
                    game.turn
                )

                notation = Pos64(cap.from_field).to_algebraic()
                for cf in cap.captured_fields:
                    notation += f" x {Pos64(cf).to_algebraic()}"
                notation += f" → {Pos64(cap.to_field).to_algebraic()}"

                test_game.make_move(cap.from_field, cap.to_field, cap.captured_fields, cap.promotes)

                score, seq = self._minimax(test_game, max_depth - 1, -999999, 999999,
                                           game.turn == "black", 1)

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

        # Movimentos simples - INCLUIR SACRIFÍCIOS TÁTICOS
        moves = game.find_simple_moves()

        for from_f, to_f, promotes in moves:
            # Verificar se é sacrifício tático
            is_sacrifice, tactical_value = self.evaluator.is_tactical_sacrifice(game, from_f, to_f)

            test_game = BrazilianGameComplete(
                game.white_men.copy(), game.black_men.copy(),
                game.white_kings.copy(), game.black_kings.copy(),
                game.turn
            )

            notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"

            test_game.make_move(from_f, to_f, [], promotes)

            # Se é sacrifício tático, aumentar profundidade de busca
            search_depth = max_depth + 2 if is_sacrifice else max_depth - 1

            score, seq = self._minimax(test_game, search_depth, -999999, 999999,
                                       game.turn == "black", 1)

            # Bonificar sacrifícios táticos
            if is_sacrifice and game.turn == "white":
                score += tactical_value

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
                 maximizing: bool, current_depth: int) -> Tuple[float, List[str]]:
        """Minimax com alpha-beta pruning"""

        self.nodes_searched += 1

        # Verificar condições de parada
        white_total = len(game.white_men) + len(game.white_kings)
        black_total = len(game.black_men) + len(game.black_kings)

        if white_total == 0:
            return (-10000 + current_depth, [])
        if black_total == 0:
            return (10000 - current_depth, [])

        if depth == 0:
            return (self.evaluator.evaluate_position(game, current_depth), [])

        # Capturas obrigatórias
        caps = game.find_all_captures()

        if caps:
            if maximizing:
                max_eval = -999999
                best_seq = []

                for cap in caps:
                    test_game = BrazilianGameComplete(
                        game.white_men.copy(), game.black_men.copy(),
                        game.white_kings.copy(), game.black_kings.copy(),
                        game.turn
                    )

                    notation = Pos64(cap.from_field).to_algebraic()
                    for cf in cap.captured_fields:
                        notation += f" x {Pos64(cf).to_algebraic()}"
                    notation += f" → {Pos64(cap.to_field).to_algebraic()}"

                    test_game.make_move(cap.from_field, cap.to_field, cap.captured_fields, cap.promotes)

                    eval_score, seq = self._minimax(test_game, depth - 1, alpha, beta, False, current_depth + 1)

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
                    test_game = BrazilianGameComplete(
                        game.white_men.copy(), game.black_men.copy(),
                        game.white_kings.copy(), game.black_kings.copy(),
                        game.turn
                    )

                    notation = Pos64(cap.from_field).to_algebraic()
                    for cf in cap.captured_fields:
                        notation += f" x {Pos64(cf).to_algebraic()}"
                    notation += f" → {Pos64(cap.to_field).to_algebraic()}"

                    test_game.make_move(cap.from_field, cap.to_field, cap.captured_fields, cap.promotes)

                    eval_score, seq = self._minimax(test_game, depth - 1, alpha, beta, True, current_depth + 1)

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
            # Sem movimentos disponíveis
            if maximizing:
                return (-10000 + current_depth, [])
            else:
                return (10000 - current_depth, [])

        if maximizing:
            max_eval = -999999
            best_seq = []

            for from_f, to_f, promotes in moves:
                test_game = BrazilianGameComplete(
                    game.white_men.copy(), game.black_men.copy(),
                    game.white_kings.copy(), game.black_kings.copy(),
                    game.turn
                )

                notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"

                test_game.make_move(from_f, to_f, [], promotes)

                eval_score, seq = self._minimax(test_game, depth - 1, alpha, beta, False, current_depth + 1)

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
                test_game = BrazilianGameComplete(
                    game.white_men.copy(), game.black_men.copy(),
                    game.white_kings.copy(), game.black_kings.copy(),
                    game.turn
                )

                notation = f"{Pos64(from_f).to_algebraic()} → {Pos64(to_f).to_algebraic()}"

                test_game.make_move(from_f, to_f, [], promotes)

                eval_score, seq = self._minimax(test_game, depth - 1, alpha, beta, True, current_depth + 1)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_seq = [notation] + seq

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break

            return (min_eval, best_seq)
