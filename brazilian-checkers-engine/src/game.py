"""
Módulo principal do jogo de damas brasileiro
Implementa as regras completas e controle do jogo
"""

from typing import List, Tuple, Optional, Dict
from .board import Board
from .piece import Piece, Color, PieceType


class Move:
    """Representa um movimento no jogo"""

    def __init__(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int],
                 captures: List[Tuple[int, int]] = None, is_promotion: bool = False):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.captures = captures or []
        self.is_promotion = is_promotion

    def is_capture(self) -> bool:
        """Verifica se é um movimento de captura"""
        return len(self.captures) > 0

    def __repr__(self) -> str:
        capture_str = f" (captures: {len(self.captures)})" if self.is_capture() else ""
        promo_str = " [PROMOTION]" if self.is_promotion else ""
        return f"Move({self.from_pos} -> {self.to_pos}{capture_str}{promo_str})"


class Game:
    """
    Controla o jogo de damas brasileiro
    Implementa todas as regras oficiais
    """

    def __init__(self):
        """Inicializa um novo jogo"""
        self.board = Board()
        self.board.setup_initial_position()
        self.current_player = Color.WHITE
        self.move_history: List[Move] = []
        self.winner: Optional[Color] = None

    def get_current_player(self) -> Color:
        """Retorna o jogador atual"""
        return self.current_player

    def switch_player(self):
        """Alterna o jogador atual"""
        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE

    def get_simple_moves(self, piece: Piece) -> List[Move]:
        """
        Retorna movimentos simples (sem captura) para uma peça

        Args:
            piece: Peça para verificar movimentos

        Returns:
            Lista de movimentos simples possíveis
        """
        moves = []
        row, col = piece.position

        # Direções diagonais: (-1,-1), (-1,+1), (+1,-1), (+1,+1)
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        if piece.is_king():
            # Damas podem mover quantas casas quiser na diagonal
            for dr, dc in directions:
                distance = 1
                while True:
                    new_row = row + (dr * distance)
                    new_col = col + (dc * distance)
                    new_pos = (new_row, new_col)

                    if not self.board.is_valid_position(new_pos):
                        break

                    if not self.board.is_empty(new_pos):
                        break  # Bloqueado por outra peça

                    moves.append(Move(piece.position, new_pos))
                    distance += 1
        else:
            # Peças simples movem apenas 1 casa para frente
            forward_dir = piece.get_forward_direction()

            for dc in [-1, 1]:
                new_row = row + forward_dir
                new_col = col + dc
                new_pos = (new_row, new_col)

                if self.board.is_valid_position(new_pos) and self.board.is_empty(new_pos):
                    # Verificar se há coroação
                    is_promotion = (new_row == 0 and piece.color == Color.BLACK) or \
                                   (new_row == self.board.size - 1 and piece.color == Color.WHITE)
                    moves.append(Move(piece.position, new_pos, is_promotion=is_promotion))

        return moves

    def get_capture_moves(self, piece: Piece, current_pos: Optional[Tuple[int, int]] = None,
                          captured_so_far: Optional[List[Tuple[int, int]]] = None) -> List[Move]:
        """
        Retorna movimentos de captura para uma peça (recursivo para múltiplas capturas)

        Args:
            piece: Peça para verificar capturas
            current_pos: Posição atual (para capturas em sequência)
            captured_so_far: Lista de peças já capturadas nesta sequência

        Returns:
            Lista de movimentos de captura possíveis
        """
        if current_pos is None:
            current_pos = piece.position
        if captured_so_far is None:
            captured_so_far = []

        moves = []
        row, col = current_pos

        # Direções diagonais
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Peças simples só capturam para frente (mas podem capturar nas 2 diagonais frontais)
        # E também podem capturar para trás na regra brasileira!
        if not piece.is_king():
            # Na regra brasileira, peças simples podem capturar para trás também
            pass  # Usar todas as direções

        for dr, dc in directions:
            if piece.is_king():
                # Damas podem capturar a qualquer distância
                distance = 1
                enemy_pos = None
                enemy_distance = None

                # Procurar por inimigo na diagonal
                while True:
                    check_row = row + (dr * distance)
                    check_col = col + (dc * distance)
                    check_pos = (check_row, check_col)

                    if not self.board.is_valid_position(check_pos):
                        break

                    target_piece = self.board.get_piece(check_pos)

                    if target_piece:
                        if target_piece.color != piece.color and check_pos not in captured_so_far:
                            # Encontrou inimigo
                            enemy_pos = check_pos
                            enemy_distance = distance
                        else:
                            # Bloqueado por peça amiga ou já capturada
                            break
                        break
                    distance += 1

                # Se encontrou inimigo, verificar casas de pouso após ele
                if enemy_pos:
                    landing_distance = enemy_distance + 1
                    while True:
                        land_row = row + (dr * landing_distance)
                        land_col = col + (dc * landing_distance)
                        land_pos = (land_row, land_col)

                        if not self.board.is_valid_position(land_pos):
                            break

                        if not self.board.is_empty(land_pos):
                            break  # Bloqueado

                        # Captura válida encontrada
                        new_captured = captured_so_far + [enemy_pos]

                        # Verificar capturas em sequência
                        # Criar cópia temporária do tabuleiro para simular
                        temp_board = self.board.copy()
                        temp_piece = temp_board.get_piece(current_pos)

                        # Simular a captura
                        temp_board.remove_piece(enemy_pos)
                        temp_board.move_piece(current_pos, land_pos)

                        # Se virou dama nesta captura, não pode continuar
                        promoted = temp_piece.should_be_crowned(temp_board.size)

                        if not promoted:
                            # Recursivamente buscar mais capturas
                            further_moves = self.get_capture_moves(piece, land_pos, new_captured)

                            if further_moves:
                                # Tem capturas adicionais
                                moves.extend(further_moves)
                            else:
                                # Não tem mais capturas, este é um movimento final
                                moves.append(Move(piece.position, land_pos, new_captured, is_promotion=promoted))
                        else:
                            # Promovido, deve parar
                            moves.append(Move(piece.position, land_pos, new_captured, is_promotion=True))

                        landing_distance += 1

            else:
                # Peças simples capturam saltando 1 casa
                enemy_row = row + dr
                enemy_col = col + dc
                enemy_pos = (enemy_row, enemy_col)

                land_row = row + (dr * 2)
                land_col = col + (dc * 2)
                land_pos = (land_row, land_col)

                # Verificar se é captura válida
                if self.board.is_valid_position(enemy_pos) and \
                   self.board.is_valid_position(land_pos) and \
                   enemy_pos not in captured_so_far:

                    enemy_piece = self.board.get_piece(enemy_pos)

                    if enemy_piece and enemy_piece.color != piece.color and \
                       self.board.is_empty(land_pos):

                        new_captured = captured_so_far + [enemy_pos]

                        # Verificar se vira dama
                        promoted = (land_row == 0 and piece.color == Color.BLACK) or \
                                   (land_row == self.board.size - 1 and piece.color == Color.WHITE)

                        if not promoted:
                            # Buscar capturas adicionais
                            further_moves = self.get_capture_moves(piece, land_pos, new_captured)

                            if further_moves:
                                moves.extend(further_moves)
                            else:
                                moves.append(Move(piece.position, land_pos, new_captured, is_promotion=False))
                        else:
                            # Promovido, deve parar
                            moves.append(Move(piece.position, land_pos, new_captured, is_promotion=True))

        return moves

    def get_legal_moves(self, pos: Tuple[int, int]) -> List[Move]:
        """
        Retorna todos os movimentos legais para uma peça

        Args:
            pos: Posição da peça

        Returns:
            Lista de movimentos legais
        """
        piece = self.board.get_piece(pos)
        if not piece or piece.color != self.current_player:
            return []

        # Verificar se existem capturas disponíveis para qualquer peça do jogador atual
        all_captures = []
        for p in self.board.get_pieces_by_color(self.current_player):
            captures = self.get_capture_moves(p)
            all_captures.extend(captures)

        # Se existem capturas, elas são obrigatórias
        if all_captures:
            # Retornar apenas capturas desta peça
            piece_captures = self.get_capture_moves(piece)

            # Filtrar para retornar apenas as capturas com o maior número de peças
            if piece_captures:
                max_captures = max(len(m.captures) for m in piece_captures)
                return [m for m in piece_captures if len(m.captures) == max_captures]
            return []
        else:
            # Sem capturas, retornar movimentos simples
            return self.get_simple_moves(piece)

    def get_all_legal_moves(self) -> Dict[Tuple[int, int], List[Move]]:
        """Retorna todos os movimentos legais para o jogador atual"""
        all_moves = {}

        # Verificar se há capturas obrigatórias
        all_captures = []
        for piece in self.board.get_pieces_by_color(self.current_player):
            captures = self.get_capture_moves(piece)
            if captures:
                all_captures.extend(captures)
                all_moves[piece.position] = captures

        if all_captures:
            # Capturas obrigatórias - filtrar apenas as com maior número de capturas
            max_captures = max(len(m.captures) for m in all_captures)
            filtered_moves = {}
            for pos, moves in all_moves.items():
                valid = [m for m in moves if len(m.captures) == max_captures]
                if valid:
                    filtered_moves[pos] = valid
            return filtered_moves
        else:
            # Sem capturas, retornar movimentos simples
            for piece in self.board.get_pieces_by_color(self.current_player):
                simple_moves = self.get_simple_moves(piece)
                if simple_moves:
                    all_moves[piece.position] = simple_moves
            return all_moves

    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """
        Executa um movimento

        Args:
            from_pos: Posição de origem
            to_pos: Posição de destino

        Returns:
            True se o movimento foi executado, False se inválido
        """
        legal_moves = self.get_legal_moves(from_pos)

        # Encontrar o movimento correspondente
        move = None
        for m in legal_moves:
            if m.to_pos == to_pos:
                move = m
                break

        if not move:
            return False  # Movimento inválido

        # Executar o movimento
        piece = self.board.get_piece(from_pos)

        # Remover peças capturadas
        for capture_pos in move.captures:
            self.board.remove_piece(capture_pos)

        # Mover a peça
        self.board.move_piece(from_pos, to_pos)

        # Adicionar ao histórico
        self.move_history.append(move)

        # Verificar fim de jogo
        self.check_game_over()

        # Alternar jogador
        if not self.winner:
            self.switch_player()

        return True

    def check_game_over(self):
        """Verifica se o jogo terminou"""
        # Verificar se um jogador não tem mais peças
        white_count = self.board.count_pieces(Color.WHITE)
        black_count = self.board.count_pieces(Color.BLACK)

        if white_count == 0:
            self.winner = Color.BLACK
            return

        if black_count == 0:
            self.winner = Color.WHITE
            return

        # Verificar se o próximo jogador tem movimentos legais
        # (trocar temporariamente para verificar)
        original_player = self.current_player
        self.switch_player()
        has_moves = len(self.get_all_legal_moves()) > 0
        self.current_player = original_player

        if not has_moves:
            # Jogador atual venceu (adversário não tem movimentos)
            self.winner = self.current_player

    def get_winner(self) -> Optional[Color]:
        """Retorna o vencedor do jogo, ou None se ainda em andamento"""
        return self.winner

    def is_game_over(self) -> bool:
        """Verifica se o jogo terminou"""
        return self.winner is not None

    def display_board(self):
        """Exibe o tabuleiro"""
        self.board.display()

    def __repr__(self) -> str:
        """Representação em string do jogo"""
        return f"Game(Current: {self.current_player.value}, Moves: {len(self.move_history)}, Winner: {self.winner})"
