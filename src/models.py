import pygame
import constants

class ChessPiece:
    def __init__(self, color, type_name, image_path):
        self.color = color
        self.type = type_name
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (constants.SQUARE_SIZE, constants.SQUARE_SIZE))
        self.has_moved = False

class MoveRecord:
    """Stores all information needed to reverse a chess move."""
    def __init__(self, start_pos, end_pos, piece_moved, captured_piece, 
                 prev_en_passant, is_en_passant=False, 
                 is_castle=False, rook_move=None, 
                 is_promotion=False, promoted_from=None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.piece_moved = piece_moved
        self.captured_piece = captured_piece
        self.prev_en_passant = prev_en_passant
        self.is_en_passant = is_en_passant
        self.is_castle = is_castle
        self.rook_move = rook_move # (rook_piece, r_start, r_end)
        self.is_promotion = is_promotion
        self.promoted_from = promoted_from
        
        # Save 'has_moved' states
        self.piece_moved_had_moved = piece_moved.has_moved
        if rook_move:
            self.rook_had_moved = rook_move[0].has_moved
