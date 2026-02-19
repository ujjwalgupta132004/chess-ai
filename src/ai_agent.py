import threading
import state
import uci_utils
from ai_interface import get_best_move_from_stockfish, get_evaluation_and_move, get_ai_coach_commentary

def perform_ai_turn():
    """Fetches move from Stockfish and stores it in pending_ai_move."""
    if state.is_ai_thinking: return
    
    fen = uci_utils.generate_fen()
    print(f"--- AI Turn Started ---")
    state.is_ai_thinking = True
    
    def fetch_and_move():
        try:
            move_uci = get_best_move_from_stockfish(fen)
            if move_uci:
                print(f"--- Stockfish chose: {move_uci} ---")
                coords = uci_utils.uci_to_grid(move_uci)
                if coords:
                    state.pending_ai_move = coords  # Main loop picks this up
            else:
                print("--- Stockfish returned no move (Game over?) ---")
        except Exception as e:
            print(f"--- AI Turn Error: {e} ---")
        finally:
            state.is_ai_thinking = False

    threading.Thread(target=fetch_and_move, daemon=True).start()

def get_ai_hint():
    """Asks for a hint and updates the coach message."""
    if state.is_ai_thinking: return
    
    fen = uci_utils.generate_fen()
    print(f"--- Requesting Hint ---")
    state.is_ai_thinking = True
    
    def fetch_hint():
        try:
            move, eval_val = get_evaluation_and_move(fen)
            state.ai_eval_score = eval_val if eval_val else "?"
            if move:
                state.last_hint_move = move   # Store raw UCI for bottom bar
                # Format as e2-e4 for sidebar
                move_fmt = f"{move[0]}{move[1]}-{move[2]}{move[3]}" if len(move) >= 4 else move
                print(f"--- Best Move: {move_fmt}  |  Eval: {eval_val} ---")
                state.ai_coach_message = f"Best move is {move_fmt.upper()}. Analyzing..."
                get_ai_coach_commentary(fen, move, eval_val, update_coach_text)
            else:
                state.ai_coach_message = "No clear best move found."
        except Exception as e:
            print(f"--- Hint Logic Error: {e} ---")
            state.ai_coach_message = "Coach had an error."
        finally:
            state.is_ai_thinking = False

    threading.Thread(target=fetch_hint, daemon=True).start()

def update_coach_text(text):
    """Callback to update coach message with LLM commentary + move notation."""
    if state.last_hint_move and len(state.last_hint_move) >= 4:
        move_fmt = f"{state.last_hint_move[0]}{state.last_hint_move[1]}-{state.last_hint_move[2]}{state.last_hint_move[3]}".upper()
        state.ai_coach_message = f"{text}\n\nBest Move: {move_fmt}"
    else:
        state.ai_coach_message = text
