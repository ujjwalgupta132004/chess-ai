import threading
import state
import models
import game_status
import uci_utils
from ai_interface import get_evaluation_and_move

# Forward declaration for ai_agent trigger
_ai_agent_module = None

def set_ai_agent_module(mod):
    global _ai_agent_module
    _ai_agent_module = mod

def execute_move(target_row, target_col):
    """Applies a move to the board, handling captures and special side effects."""
    moving_piece = state.active_selected_piece
    if moving_piece is None or state.active_selected_pos is None:
        return

    # --- Execute the Move ---
    start_row, start_col = state.active_selected_pos
    captured_piece = state.board[target_row][target_col]
    prev_en_passant = state.pawn_en_passant_target
    is_en_passant = False
    is_castle_move = False
    rook_move_info = None

    # --- Side Effect: Castling ---
    if moving_piece.type == 'king' and abs(target_col - start_col) == 2:
        is_castle_move = True
        old_rook_col = 7 if target_col == 6 else 0
        new_rook_col = 5 if target_col == 6 else 3
        rook = state.board[target_row][old_rook_col]
        rook_move_info = (rook, (target_row, old_rook_col), (target_row, new_rook_col))
        
        state.board[target_row][new_rook_col] = state.board[target_row][old_rook_col]
        state.board[target_row][old_rook_col] = None
        if rook:
            rook.has_moved = True

    # --- Side Effect: En Passant Capture ---
    if moving_piece.type == 'pawn' and (target_row, target_col) == state.pawn_en_passant_target:
        is_en_passant = True
        captured_piece = state.board[start_row][target_col] # The captured pawn
        state.board[start_row][target_col] = None

    # --- Setup next turn's En Passant state ---
    state.pawn_en_passant_target = None
    if moving_piece.type == 'pawn' and abs(target_row - start_row) == 2:
        state.pawn_en_passant_target = ((target_row + start_row) // 2, start_col)

    # --- Finalize the Move ---
    state.board[target_row][target_col] = moving_piece
    state.board[start_row][start_col] = None
    moving_piece.has_moved = True

    # --- Auto-Promotion to Queen ---
    promoted_from = None
    is_promo = False
    if moving_piece.type == 'pawn' and (target_row == 0 or target_row == 7):
        is_promo = True
        promoted_from = moving_piece
        p_color = moving_piece.color
        state.board[target_row][target_col] = models.ChessPiece(p_color, 'queen', f'src/images/{p_color}_queen.png')

    # --- Store Move for Undo ---
    move_rec = models.MoveRecord(
        (start_row, start_col), (target_row, target_col), 
        state.board[target_row][target_col], # Could be promoted piece
        captured_piece, 
        prev_en_passant,
        is_en_passant=is_en_passant,
        is_castle=is_castle_move,
        rook_move=rook_move_info,
        is_promotion=is_promo,
        promoted_from=promoted_from
    )
    state.move_history.append(move_rec)

    # --- Log to Game Move Log ---
    move_count = (len(state.move_history) + 1) // 2
    color_name = "White" if state.current_turn_color == "white" else "Black"
    
    def get_coord_str(r, c):
        return f"{chr(ord('a') + c)}{8 - r}"

    s_str = get_coord_str(start_row, start_col)
    e_str = get_coord_str(target_row, target_col)
    log_entry = f"Move {move_count} {color_name}: {s_str.upper()} - {e_str.upper()}"
    state.game_move_log.append(log_entry)

    # Switch turns
    state.current_turn_color = 'black' if state.current_turn_color == 'white' else 'white'
    
    # Update Board Evaluation (Live)
    def update_eval():
        _, eval_val = get_evaluation_and_move(uci_utils.generate_fen())
        state.ai_eval_score = eval_val

    threading.Thread(target=update_eval, daemon=True).start()

    # Trigger AI if enabled
    if state.ai_opponent_enabled and state.current_turn_color == 'black':
        if _ai_agent_module:
            _ai_agent_module.perform_ai_turn()

    # Check for Checkmate or Stalemate
    if game_status.is_checkmate(state.current_turn_color):
        print(f"CHECKMATE! {state.current_turn_color.upper()} player has lost.")
    elif game_status.is_stalemate(state.current_turn_color):
        print("STALEMATE! The game ends in a draw.")

def undo_move():
    """Reverses the last move made using the move history stack."""
    if not state.move_history:
        print("No moves to undo.")
        return

    move = state.move_history.pop()
    if state.game_move_log:
        state.game_move_log.pop()
    selected_row, selected_col = move.start_pos
    target_row, target_col = move.end_pos

    # Restore piece position
    state.board[selected_row][selected_col] = move.piece_moved
    state.board[target_row][target_col] = move.captured_piece
    move.piece_moved.has_moved = move.piece_moved_had_moved

    # Restore En Passant capture
    if move.is_en_passant:
        # The captured pawn was at (selected_row, target_col)
        state.board[selected_row][target_col] = move.captured_piece
        state.board[target_row][target_col] = None

    # Restore Castling Rook
    if move.is_castle:
        rook, r_start, r_end = move.rook_move
        state.board[r_start[0]][r_start[1]] = rook
        state.board[r_end[0]][r_end[1]] = None
        if rook:
            rook.has_moved = move.rook_had_moved

    # Restore Promotion
    if move.is_promotion:
        state.board[selected_row][selected_col] = move.promoted_from

    # Restore global state
    state.pawn_en_passant_target = move.prev_en_passant
    state.current_turn_color = 'white' if state.current_turn_color == 'black' else 'black'
    print(f"Undo successful. Now it's {state.current_turn_color}'s turn.")
