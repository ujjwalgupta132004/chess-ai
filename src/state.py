import pygame
import constants

# --- Initial Setup ---
pygame.init()

# The 8x8 chess board. It stores ChessPiece objects or None for empty squares.
board = [[None for _ in range(8)] for _ in range(8)]

# --- Global Game State ---
current_turn_color = 'white'  # Current player color: 'white' or 'black'
active_selected_piece = None  # The piece object selected by the player
active_selected_pos = None    # The (row, col) position of that piece
legal_moves_for_selected = [] # Highlighted target squares for the UI
pawn_en_passant_target = None # Square targeting an en passant capture
move_history = []             # Stack to store move history for undoing

# --- AI State ---
ai_opponent_enabled = False
ai_coach_message = "I am your coach. Make a move or click 'Hint'!"
ai_eval_score = "0.0"
is_ai_thinking = False
last_hint_move = ""   # e.g. "e2e4" – displayed below board
pending_ai_move = None  # Set by background thread: ((sr,sc),(er,ec))

# --- Timer & History State ---
timer_active = False
timer_initial_seconds = 600.0  # Default 10 mins
white_time = 600.0
black_time = 600.0
game_move_log = []            # List of strings: "1. White: E2-E4"

# --- UI State ---
current_theme_idx = 0

# Create the screen
# Create the screen (re-calculate width with new constants)
screen = pygame.display.set_mode((constants.WINDOW_W, constants.WINDOW_H))
pygame.display.set_caption("Chess AI — Grandmaster Coach")
