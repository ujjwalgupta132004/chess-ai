import state

def uci_to_grid(uci):
    """Translates UCI string (e2e4) to ((start_r, start_c), (end_r, end_c))."""
    if len(uci) < 4: return None
    start_c = ord(uci[0]) - ord('a')
    start_r = 8 - int(uci[1])
    end_c = ord(uci[2]) - ord('a')
    end_r = 8 - int(uci[3])
    return (start_r, start_c), (end_r, end_c)

def generate_fen():
    """Generates the FEN string for the current board state."""
    fen_parts = []
    
    # 1. Piece placement
    piece_map = {
        ('white', 'pawn'): 'P', ('white', 'knight'): 'N', ('white', 'bishop'): 'B',
        ('white', 'rook'): 'R', ('white', 'queen'): 'Q', ('white', 'king'): 'K',
        ('black', 'pawn'): 'p', ('black', 'knight'): 'n', ('black', 'bishop'): 'b',
        ('black', 'rook'): 'r', ('black', 'queen'): 'q', ('black', 'king'): 'k'
    }
    
    rows = []
    for r in range(8):
        empty_count = 0
        row_str = ""
        for c in range(8):
            p = state.board[r][c]
            if p:
                if empty_count > 0:
                    row_str += str(empty_count)
                    empty_count = 0
                row_str += piece_map[(p.color, p.type)]
            else:
                empty_count += 1
        if empty_count > 0:
            row_str += str(empty_count)
        rows.append(row_str)
    fen_parts.append("/".join(rows))
    
    # 2. Side to move
    fen_parts.append('w' if state.current_turn_color == 'white' else 'b')
    
    # 3. Castling ability
    castling = ""
    # White
    wk = state.board[7][4]
    if wk and wk.type == 'king' and wk.color == 'white' and not wk.has_moved:
        # Kingside
        wr_k = state.board[7][7]
        if wr_k and wr_k.type == 'rook' and wr_k.color == 'white' and not wr_k.has_moved:
            castling += "K"
        # Queenside
        wr_q = state.board[7][0]
        if wr_q and wr_q.type == 'rook' and wr_q.color == 'white' and not wr_q.has_moved:
            castling += "Q"
    # Black
    bk = state.board[0][4]
    if bk and bk.type == 'king' and bk.color == 'black' and not bk.has_moved:
        # Kingside
        br_k = state.board[0][7]
        if br_k and br_k.type == 'rook' and br_k.color == 'black' and not br_k.has_moved:
            castling += "k"
        # Queenside
        br_q = state.board[0][0]
        if br_q and br_q.type == 'rook' and br_q.color == 'black' and not br_q.has_moved:
            castling += "q"
    
    fen_parts.append(castling if castling else "-")
    
    # 4. En passant target square
    if state.pawn_en_passant_target:
        r, c = state.pawn_en_passant_target
        col_char = chr(ord('a') + c)
        row_char = str(8 - r)
        fen_parts.append(f"{col_char}{row_char}")
    else:
        fen_parts.append("-")
    
    # 5. Halfmove clock
    fen_parts.append("0")
    
    # 6. Fullmove number
    fen_parts.append("1")
    
    return " ".join(fen_parts)
