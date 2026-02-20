# --- Layout Constants ---
TOPBAR_HEIGHT = 50      # Header toolbar height
BOTTOM_BAR_HEIGHT = 40  # Bottom hint display height
BOARD_LABEL_SIZE = 22   # Width/height of coordinate labels strip
SIDEBAR_WIDTH = 300
HISTORY_WIDTH = 240

# Board renders inside the label strip, starting offset
BOARD_LABEL_SIZE_OFFSET = BOARD_LABEL_SIZE
BOARD_OFFSET_X = BOARD_LABEL_SIZE
BOARD_OFFSET_Y = TOPBAR_HEIGHT + BOARD_LABEL_SIZE
BOARD_PX = 690        # Board pixel size (divisible by 8)
SQUARE_SIZE = BOARD_PX // 8

WINDOW_W = BOARD_OFFSET_X + BOARD_PX + SIDEBAR_WIDTH + HISTORY_WIDTH
WINDOW_H = TOPBAR_HEIGHT + BOARD_LABEL_SIZE + BOARD_PX + BOTTOM_BAR_HEIGHT

# Alias for sidebar x start
SIDEBAR_X = BOARD_OFFSET_X + BOARD_PX
HISTORY_X = SIDEBAR_X + SIDEBAR_WIDTH

# --- Color Palette ---
WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
YELLOW = (255, 215,   0)
RED    = (220,  50,  50)

# Board themes: (light_square, dark_square)
BOARD_THEMES = [
    ((240, 217, 181), (181, 136, 99)),   # Classic Wood
    ((238, 238, 210), (118, 150,  86)),  # Green & Cream
    ((200, 200, 200), ( 80,  80,  80)),  # Grey Slate
    ((255, 235, 205), (139,  90,  43)),  # Warm Tan
    ((173, 216, 230), ( 70, 130, 180)),  # Ocean Blue
]
THEME_NAMES = ["Classic", "Green", "Slate", "Warm Tan", "Ocean"]

# UI palette
BG_DARK    = ( 22,  22,  30)
BG_SIDEBAR = ( 28,  28,  40)
ACCENT     = ( 90, 130, 255)
SUCCESS    = ( 70, 200, 120)
DANGER     = (200,  70,  70)
TEXT_DIM   = (160, 160, 180)
TEXT_BRIGHT= (240, 240, 255)
