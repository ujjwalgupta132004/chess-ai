import state
from models import ChessPiece

def initialize_game_board():
    """Starts a new game by placing all 32 pieces in their standard positions."""
    # Reset board to all empty squares first
    for r in range(8):
        for c in range(8):
            state.board[r][c] = None

    # Place Pawns
    for col in range(8):
        state.board[1][col] = ChessPiece('black', 'pawn', 'src/images/black_pawn.png')
        state.board[6][col] = ChessPiece('white', 'pawn', 'src/images/white_pawn.png')

    # Place Rooks
    state.board[0][0] = state.board[0][7] = ChessPiece('black', 'rook', 'src/images/black_rook.png')
    state.board[7][0] = state.board[7][7] = ChessPiece('white', 'rook', 'src/images/white_rook.png')

    # Place Knights
    state.board[0][1] = state.board[0][6] = ChessPiece('black', 'knight', 'src/images/black_knight.png')
    state.board[7][1] = state.board[7][6] = ChessPiece('white', 'knight', 'src/images/white_knight.png')

    # Place Bishops
    state.board[0][2] = state.board[0][5] = ChessPiece('black', 'bishop', 'src/images/black_bishop.png')
    state.board[7][2] = state.board[7][5] = ChessPiece('white', 'bishop', 'src/images/white_bishop.png')

    # Place Queens
    state.board[0][3] = ChessPiece('black', 'queen', 'src/images/black_queen.png')
    state.board[7][3] = ChessPiece('white', 'queen', 'src/images/white_queen.png')

    # Place Kings
    state.board[0][4] = ChessPiece('black', 'king', 'src/images/black_king.png')
    state.board[7][4] = ChessPiece('white', 'king', 'src/images/white_king.png')
