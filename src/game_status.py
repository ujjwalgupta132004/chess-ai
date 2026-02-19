import state
from move_physics import is_king_in_check
import move_logic

def has_no_legal_moves(color):
    """Determines if the game should end due to lack of valid moves."""
    for r in range(8):
        for col in range(8):
            p = state.board[r][col]
            if p and p.color == color:
                if move_logic.get_fully_legal_moves(p, r, col):
                    return False
    return True

def is_stalemate(color):
    """Returns True if the current color is in stalemate (no moves, not in check)."""
    return has_no_legal_moves(color) and not is_king_in_check(color)

def is_checkmate(color):
    """Returns True if the current color is in checkmate (no moves, in check)."""
    return has_no_legal_moves(color) and is_king_in_check(color)
