import state
from move_physics import get_raw_piece_moves, is_king_in_check, is_cell_attacked

def get_fully_legal_moves(piece, row, col):
    """Refines raw moves with safety checks to ensure the King isn't left in Check."""
    raw_moves = get_raw_piece_moves(piece, row, col)
    legal_moves = []

    # Filter out moves that would cause self-check
    for target_r, target_c in raw_moves:
        original_piece = state.board[target_r][target_c]
        
        # Simulate move
        state.board[target_r][target_c] = piece
        state.board[row][col] = None
        is_safe = not is_king_in_check(piece.color)
        
        if is_safe:
            legal_moves.append((target_r, target_c))
            
        # Revert simulation
        state.board[row][col] = piece
        state.board[target_r][target_c] = original_piece

    # Specialized Castling Logic
    if piece.type == 'king' and not piece.has_moved and not is_king_in_check(piece.color):
        # Kingside (Right)
        rook_r = state.board[row][7]
        if rook_r and rook_r.type == 'rook' and not rook_r.has_moved:
            if state.board[row][5] is None and state.board[row][6] is None:
                if not is_cell_attacked(row, 5, piece.color) and not is_cell_attacked(row, 6, piece.color):
                    legal_moves.append((row, 6))
        # Queenside (Left)
        rook_l = state.board[row][0]
        if rook_l and rook_l.type == 'rook' and not rook_l.has_moved:
            if state.board[row][1] is None and state.board[row][2] is None and state.board[row][3] is None:
                if not is_cell_attacked(row, 2, piece.color) and not is_cell_attacked(row, 3, piece.color):
                    legal_moves.append((row, 2))

    return legal_moves
