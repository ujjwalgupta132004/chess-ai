import pygame
import sys

# 1. Foundation
import constants
import state

# 2. Logic & Models
import models
import board_manager
import move_physics
import move_logic
import game_status
import engine
import uci_utils
import ai_agent
import input_handler

# Connect engine and ai_agent to avoid circularity
engine.set_ai_agent_module(ai_agent)

def start_chess_game():
    """Initializes and runs the main game loop."""
    board_manager.initialize_game_board()
    throttle = pygame.time.Clock()

    ui_rects = {
        'hint': pygame.Rect(0, 0, 1, 1),
        'bot_tog': pygame.Rect(0, 0, 1, 1),
        'clock_tog': pygame.Rect(0, 0, 1, 1),
        'presets': []
    }

    import ui_renderer # Import inside to ensure state.screen is ready

    while True:
        # --- Timer Logic ---
        dt = throttle.tick(60) / 1000.0  # seconds
        if state.timer_active:
            if state.current_turn_color == 'white':
                state.white_time -= dt
            else:
                state.black_time -= dt
            
            # Check for Time Out
            if state.white_time <= 0:
                print("--- TIME OUT! Black wins on time ---")
                state.timer_active = False # Stop clock
            elif state.black_time <= 0:
                print("--- TIME OUT! White wins on time ---")
                state.timer_active = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                input_handler.handle_mouse_input(pygame.mouse.get_pos(), ui_rects)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    engine.undo_move()

        # --- Poll for pending AI move (set by background thread) ---
        if state.pending_ai_move is not None:
            start_pos, end_pos = state.pending_ai_move
            state.pending_ai_move = None          # Consume it immediately
            
            piece = state.board[start_pos[0]][start_pos[1]]
            if piece and piece.color == 'black':
                # Set globals for engine to consume
                state.active_selected_piece = piece
                state.active_selected_pos = start_pos
                state.legal_moves_for_selected = []
                
                engine.execute_move(end_pos[0], end_pos[1])
                
                state.active_selected_piece = None
                state.active_selected_pos = None
                print(f"--- AI moved: {start_pos} -> {end_pos} ---")

        # --- Rendering ---
        state.screen.fill(constants.BG_DARK)
        
        ui_renderer.draw_topbar()
        ui_renderer.draw_chess_board()
        ui_renderer.draw_all_pieces()
        ui_renderer.draw_bottom_bar()
        
        new_rects = ui_renderer.draw_sidebar()
        if new_rects:
            ui_rects = new_rects
            
        ui_renderer.draw_history_panel()
            
        pygame.display.flip()

if __name__ == "__main__":
    start_chess_game()