import pygame
import state
import constants
import ai_agent
import move_logic
import engine

def handle_mouse_input(position, hint_btn_rect, toggle_btn_rect):
    """Translates a user click into a selection or a move execution."""
    mx, my = position

    # 1. Top-bar theme clicks
    if my < constants.TOPBAR_HEIGHT:
        btn_w, btn_h = 80, 28
        btn_y = (constants.TOPBAR_HEIGHT - btn_h) // 2
        x = 150
        for i in range(len(constants.THEME_NAMES)):
            rect = pygame.Rect(x, btn_y, btn_w, btn_h)
            if rect.collidepoint(mx, my):
                state.current_theme_idx = i
                return
            x += btn_w + 8
        return

    # 2. Sidebar button clicks
    if hint_btn_rect.collidepoint(mx, my):
        ai_agent.get_ai_hint()
        return
    if toggle_btn_rect.collidepoint(mx, my):
        state.ai_opponent_enabled = not state.ai_opponent_enabled
        if state.ai_opponent_enabled and state.current_turn_color == 'black':
            ai_agent.perform_ai_turn()
        state.active_selected_piece = None
        state.active_selected_pos = None
        state.legal_moves_for_selected = []
        return

    # 3. Board coordinate calculation (accounting for offsets)
    if mx < constants.SIDEBAR_X and my >= constants.BOARD_OFFSET_Y and my < constants.BOARD_OFFSET_Y + constants.BOARD_PX:
        col = (mx - constants.BOARD_OFFSET_X) // constants.SQUARE_SIZE
        row = (my - constants.BOARD_OFFSET_Y) // constants.SQUARE_SIZE

        if not (0 <= row < 8 and 0 <= col < 8):
            return

        # Phase 1: Picking up a piece
        if state.active_selected_piece is None:
            p = state.board[row][col]
            if p and p.color == state.current_turn_color:
                state.active_selected_piece = p
                state.active_selected_pos = (row, col)
                state.legal_moves_for_selected = move_logic.get_fully_legal_moves(p, row, col)
        
        # Phase 2: Placing the selected piece
        else:
            if (row, col) in state.legal_moves_for_selected:
                engine.execute_move(row, col)
            
            # Reset selection state
            state.active_selected_piece = None
            state.active_selected_pos = None
            state.legal_moves_for_selected = []
