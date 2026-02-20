import state

def find_king(color):
    """Utility to quickly find the King's current coordinates."""
    for r in range(8):
        for c in range(8):
            p = state.board[r][c]
            if p and p.type == 'king' and p.color == color:
                return (r, c)
    return None

def get_raw_piece_moves(piece, row, col):
    """Calculates basic physics-based moves, ignoring specialized rules like 'Check'."""
    moves = []
    
    # Pawn-specific movement logic
    if piece.type == 'pawn':
        move_dir = -1 if piece.color == 'white' else 1
        # Forward move (blocked by any piece)
        if 0 <= row + move_dir < 8 and state.board[row + move_dir][col] is None:
            moves.append((row + move_dir, col))
            start_row = 6 if piece.color == 'white' else 1
            # Double move from start rank
            if row == start_row and state.board[row + 2 * move_dir][col] is None:
                moves.append((row + 2 * move_dir, col))
        # Captures
        for direction_col in [-1, 1]:
            targeted_row, targeted_col = row + move_dir, col + direction_col
            if 0 <= targeted_row < 8 and 0 <= targeted_col < 8:
                target = state.board[targeted_row][targeted_col]
                if target and target.color != piece.color:
                    moves.append((targeted_row,targeted_col))
                elif (targeted_row, targeted_col) == state.pawn_en_passant_target:
                    moves.append((targeted_row,targeted_col))
        return moves

    # Sliding logic for Rooks, Bishops, and Queens
    is_sliding = piece.type in ['rook', 'bishop', 'queen']
    directions = []
    if piece.type in ['rook', 'queen']:
        directions += [(1,0), (-1,0), (0,1), (0,-1)]
    if piece.type in ['bishop', 'queen']:
        directions += [(1,1), (1,-1), (-1,1), (-1,-1)]
    if piece.type == 'knight':
        directions = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
    if piece.type == 'king':
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

    for direction_row, direction_col in directions:
        curr_r, curr_c = row + direction_row, col + direction_col
        while 0 <= curr_r < 8 and 0 <= curr_c < 8:
            blocking_p = state.board[curr_r][curr_c]
            # Valid if empty or contains an enemy
            if blocking_p is None or blocking_p.color != piece.color:
                moves.append((curr_r, curr_c))
            
            # Stop if the path is blocked OR if piece doesn't slide (Knight/King)
            if not is_sliding or blocking_p:
                break
            curr_r += direction_row
            curr_c += direction_col
    return moves

def is_cell_attacked(target_row, target_col, defender_color):
    """Returns True if the specified square is reachable by ANY enemy piece."""
    opponent_color = 'black' if defender_color == 'white' else 'white'
    for r in range(8):
        for c in range(8):
            piece = state.board[r][c]
            if piece and piece.color == opponent_color:
                if (target_row, target_col) in get_raw_piece_moves(piece, r, c):
                    return True
    return False

def is_king_in_check(color):
    """Boolean check for whether the current color's King is under threat."""
    k_pos = find_king(color)
    if k_pos:
        return is_cell_attacked(k_pos[0], k_pos[1], color)
    return False
