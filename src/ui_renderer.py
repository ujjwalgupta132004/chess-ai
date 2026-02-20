import pygame
import constants
import state
from move_physics import is_king_in_check

def get_sq_rect(row, col):
    """Returns the pygame.Rect for a board square."""
    x = constants.BOARD_OFFSET_X + col * constants.SQUARE_SIZE
    y = constants.BOARD_OFFSET_Y + row * constants.SQUARE_SIZE
    return pygame.Rect(x, y, constants.SQUARE_SIZE, constants.SQUARE_SIZE)

def wrap_text(text, font, max_width):
    """Simple word wrap for Pygame surfaces."""
    words = str(text).split(' ')
    lines = []
    while words:
        line_words = []
        while words:
            line_words.append(words.pop(0))
            fw, _ = font.size(' '.join(line_words + words[:1]))
            if fw > max_width:
                break
        lines.append(' '.join(line_words))
    return lines

def format_time(seconds):
    """Formats seconds into MM:SS."""
    s = max(0, int(seconds))
    mins = s // 60
    secs = s % 60
    return f"{mins:02d}:{secs:02d}"

def draw_topbar():
    """Draws the top toolbar with board theme switcher."""
    pygame.draw.rect(state.screen, constants.BG_DARK, (0, 0, constants.WINDOW_W, constants.TOPBAR_HEIGHT))
    # Bottom border line
    pygame.draw.line(state.screen, constants.ACCENT, (0, constants.TOPBAR_HEIGHT - 1), (constants.WINDOW_W, constants.TOPBAR_HEIGHT - 1), 2)

    font = pygame.font.SysFont('Segoe UI', 17, bold=True)
    label = font.render("BOARD THEME:", True, constants.TEXT_DIM)
    state.screen.blit(label, (10, 15))

    btn_w, btn_h = 80, 28
    btn_y = (constants.TOPBAR_HEIGHT - btn_h) // 2
    x = 150
    for i, name in enumerate(constants.THEME_NAMES):
        color = constants.ACCENT if i == state.current_theme_idx else (50, 52, 70)
        rect = pygame.Rect(x, btn_y, btn_w, btn_h)
        pygame.draw.rect(state.screen, color, rect, border_radius=6)
        txt = font.render(name, True, constants.WHITE)
        state.screen.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))
        x += btn_w + 8

def draw_chess_board():
    """Renders the grid, highlights, coordinate labels."""
    light, dark = constants.BOARD_THEMES[state.current_theme_idx]

    for row in range(8):
        for col in range(8):
            sq_rect = get_sq_rect(row, col)
            square_color = light if (row + col) % 2 == 0 else dark

            # Highlight king in check
            p = state.board[row][col]
            if p and p.type == 'king' and p.color == state.current_turn_color:
                if is_king_in_check(state.current_turn_color):
                    square_color = (210, 60, 60)

            pygame.draw.rect(state.screen, square_color, sq_rect)

    # Selected piece highlight
    if state.active_selected_pos:
        sel_r, sel_c = state.active_selected_pos
        sel_rect = get_sq_rect(sel_r, sel_c)
        highlight = pygame.Surface((constants.SQUARE_SIZE, constants.SQUARE_SIZE), pygame.SRCALPHA)
        highlight.fill((255, 215, 0, 120))
        state.screen.blit(highlight, sel_rect.topleft)

    # Legal move dots
    for move_row, move_col in state.legal_moves_for_selected:
        sq_r = get_sq_rect(move_row, move_col)
        center = sq_r.center
        pygame.draw.circle(state.screen, (0, 0, 0, 160), center, constants.SQUARE_SIZE // 7)
        pygame.draw.circle(state.screen, (255, 255, 255, 80), center, constants.SQUARE_SIZE // 7 - 2)

    # Board border
    board_rect = pygame.Rect(constants.BOARD_OFFSET_X, constants.BOARD_OFFSET_Y, constants.BOARD_PX, constants.BOARD_PX)
    pygame.draw.rect(state.screen, constants.ACCENT, board_rect, 2)

    # --- Coordinate Labels ---
    lbl_font = pygame.font.SysFont('Segoe UI', 14, bold=True)
    files = 'ABCDEFGH'
    for col in range(8):
        # Column letters (A-H) below board
        sq_r = get_sq_rect(7, col)
        txt = lbl_font.render(files[col], True, constants.TEXT_DIM)
        x = sq_r.centerx - txt.get_width() // 2
        y = constants.BOARD_OFFSET_Y + constants.BOARD_PX + 4
        state.screen.blit(txt, (x, y))
        # Also draw at top
        txt2 = lbl_font.render(files[col], True, constants.TEXT_DIM)
        state.screen.blit(txt2, (x, constants.BOARD_OFFSET_Y - constants.BOARD_LABEL_SIZE + 2))

    for row in range(8):
        # Row numbers (8-1 from top) left of board
        sq_r = get_sq_rect(row, 0)
        num = str(8 - row)
        txt = lbl_font.render(num, True, constants.TEXT_DIM)
        x = constants.BOARD_OFFSET_X - txt.get_width() - 3
        y = sq_r.centery - txt.get_height() // 2
        state.screen.blit(txt, (x, y))

def draw_all_pieces():
    """Draws piece images on top of the squares."""
    for row in range(8):
        for col in range(8):
            p = state.board[row][col]
            if p:
                sq_rect = get_sq_rect(row, col)
                state.screen.blit(p.image, sq_rect.topleft)

def draw_bottom_bar():
    """Draws the bottom bar showing the last hint move."""
    bar_y = constants.TOPBAR_HEIGHT + constants.BOARD_LABEL_SIZE + constants.BOARD_PX
    bar_w = constants.BOARD_OFFSET_X + constants.BOARD_PX
    pygame.draw.rect(state.screen, constants.BG_DARK, (0, bar_y, bar_w, constants.BOTTOM_BAR_HEIGHT))
    pygame.draw.line(state.screen, constants.ACCENT, (0, bar_y), (bar_w, bar_y), 1)

    font = pygame.font.SysFont('Segoe UI', 16, bold=True)
    if state.last_hint_move:
        prefix = font.render("Best Move:  ", True, constants.TEXT_DIM)
        move_txt = font.render(state.last_hint_move.upper(), True, constants.YELLOW)
        state.screen.blit(prefix, (12, bar_y + 10))
        state.screen.blit(move_txt, (12 + prefix.get_width(), bar_y + 10))
    else:
        hint_txt = font.render("Click \"GET HINT\" to see the best move.", True, constants.TEXT_DIM)
        state.screen.blit(hint_txt, (12, bar_y + 10))

def draw_sidebar():
    """Renders the AI coach panel and Timer controls."""
    sb_y = 0
    sb_h = constants.WINDOW_H
    pygame.draw.rect(state.screen, constants.BG_SIDEBAR, (constants.SIDEBAR_X, sb_y, constants.SIDEBAR_WIDTH, sb_h))
    pygame.draw.line(state.screen, constants.ACCENT, (constants.SIDEBAR_X, 0), (constants.SIDEBAR_X, sb_h), 2)

    pad = 16
    font_title  = pygame.font.SysFont('Segoe UI', 24, bold=True)
    font_med    = pygame.font.SysFont('Segoe UI', 18, bold=True)
    font_small  = pygame.font.SysFont('Segoe UI', 15)
    font_hint   = pygame.font.SysFont('Segoe UI', 13)
    font_timer  = pygame.font.SysFont('Consolas', 26, bold=True)

    y = 12

    # --- Title ---
    title_surf = font_title.render("\u265e  AI COACH", True, constants.ACCENT)
    state.screen.blit(title_surf, (constants.SIDEBAR_X + pad, y))
    y += title_surf.get_height() + 4
    pygame.draw.line(state.screen, constants.ACCENT, (constants.SIDEBAR_X + pad, y), (constants.SIDEBAR_X + constants.SIDEBAR_WIDTH - pad, y), 1)
    y += 10

    # --- Timers (Top Section) ---
    if state.timer_active:
        # Black Timer
        b_col = constants.DANGER if state.current_turn_color == 'black' else constants.TEXT_DIM
        b_lbl = font_hint.render("BLACK TIME", True, b_col)
        b_val = font_timer.render(format_time(state.black_time), True, b_col)
        state.screen.blit(b_lbl, (constants.SIDEBAR_X + pad, y))
        state.screen.blit(b_val, (constants.SIDEBAR_X + constants.SIDEBAR_WIDTH - b_val.get_width() - pad, y - 5))
        y += b_lbl.get_height() + 20

    # --- Engine Status ---
    import ai_interface
    status_text = ai_interface.AI_STATUS
    status_color = constants.SUCCESS if "Ready" in status_text else (constants.DANGER if "Error" in status_text else constants.YELLOW)
    lbl = font_hint.render("ENGINE STATUS", True, constants.TEXT_DIM)
    val = font_med.render(status_text, True, status_color)
    state.screen.blit(lbl, (constants.SIDEBAR_X + pad, y))
    y += lbl.get_height() + 2
    state.screen.blit(val, (constants.SIDEBAR_X + pad, y))
    y += val.get_height() + 10

    # --- Evaluation ---
    eval_s = str(state.ai_eval_score)
    eval_color = constants.SUCCESS if eval_s.startswith('+') else (constants.DANGER if eval_s.startswith('-') else constants.YELLOW)
    lbl_eval = font_hint.render("EVALUATION (White \u2192)", True, constants.TEXT_DIM)
    eval_font = pygame.font.SysFont('Segoe UI', 30, bold=True)
    val_eval = eval_font.render(eval_s, True, eval_color)
    state.screen.blit(lbl_eval, (constants.SIDEBAR_X + pad, y))
    y += lbl_eval.get_height() + 2
    state.screen.blit(val_eval, (constants.SIDEBAR_X + pad, y))
    y += val_eval.get_height() + 10
    pygame.draw.line(state.screen, (50, 55, 80), (constants.SIDEBAR_X + pad, y), (constants.SIDEBAR_X + constants.SIDEBAR_WIDTH - pad, y), 1)
    y += 8

    # --- Timer Settings ---
    lbl = font_hint.render("TIMER SETTINGS", True, constants.TEXT_DIM)
    state.screen.blit(lbl, (constants.SIDEBAR_X + pad, y))
    y += lbl.get_height() + 4
    
    # Toggle button
    tog_text = "CLOCK: ON" if state.timer_active else "CLOCK: OFF"
    tog_col  = constants.SUCCESS if state.timer_active else (60, 65, 80)
    tog_rect = pygame.Rect(constants.SIDEBAR_X + pad, y, 110, 26)
    pygame.draw.rect(state.screen, tog_col, tog_rect, border_radius=5)
    t_surf = font_hint.render(tog_text, True, constants.WHITE)
    state.screen.blit(t_surf, (tog_rect.centerx - t_surf.get_width() // 2, tog_rect.centery - t_surf.get_height() // 2))
    
    # Preset buttons
    presets = [("5m", 300), ("10m", 600), ("30m", 1800)]
    preset_rects = []
    px = tog_rect.right + 8
    for label, secs in presets:
        p_rect = pygame.Rect(px, y, 45, 26)
        p_col  = constants.ACCENT if state.timer_initial_seconds == secs else (50, 52, 70)
        pygame.draw.rect(state.screen, p_col, p_rect, border_radius=5)
        p_surf = font_hint.render(label, True, constants.WHITE)
        state.screen.blit(p_surf, (p_rect.centerx - p_surf.get_width() // 2, p_rect.centery - p_surf.get_height() // 2))
        preset_rects.append((p_rect, secs))
        px += p_rect.width + 6
        
    y += tog_rect.height + 12
    pygame.draw.line(state.screen, (50, 55, 80), (constants.SIDEBAR_X + pad, y), (constants.SIDEBAR_X + constants.SIDEBAR_WIDTH - pad, y), 1)
    y += 10

    # --- Mode ---
    bot_active = state.ai_opponent_enabled
    lbl = font_hint.render("GAME MODE", True, constants.TEXT_DIM)
    state.screen.blit(lbl, (constants.SIDEBAR_X + pad, y))
    y += lbl.get_height() + 2
    mode_txt = "\u25cf  Bot Playing Black" if bot_active else "\u25cb  Local 2-Player"
    mode_col  = constants.SUCCESS if bot_active else constants.TEXT_DIM
    mode_surf = font_med.render(mode_txt, True, mode_col)
    state.screen.blit(mode_surf, (constants.SIDEBAR_X + pad, y))
    y += mode_surf.get_height() + 8

    # --- Action Buttons ---
    btn_w = constants.SIDEBAR_WIDTH - pad * 2
    btn_h = 36
    btn_x = constants.SIDEBAR_X + pad

    # Hint button
    h_rect = pygame.Rect(btn_x, y, btn_w, btn_h)
    pygame.draw.rect(state.screen, constants.ACCENT, h_rect, border_radius=8)
    h_txt = font_med.render("\u2192 GET HINT", True, constants.WHITE)
    state.screen.blit(h_txt, (h_rect.centerx - h_txt.get_width() // 2, h_rect.centery - h_txt.get_height() // 2))
    y += btn_h + 8

    # Bot toggle button
    t_color = constants.DANGER if bot_active else (60, 65, 90)
    t_rect = pygame.Rect(btn_x, y, btn_w, btn_h)
    pygame.draw.rect(state.screen, t_color, t_rect, border_radius=8)
    t_label = "DISABLE BOT" if bot_active else "ENABLE BOT"
    t_txt = font_med.render(t_label, True, constants.WHITE)
    state.screen.blit(t_txt, (t_rect.centerx - t_txt.get_width() // 2, t_rect.centery - t_txt.get_height() // 2))
    y += btn_h + 12
    pygame.draw.line(state.screen, (50, 55, 80), (constants.SIDEBAR_X + pad, y), (constants.SIDEBAR_X + constants.SIDEBAR_WIDTH - pad, y), 1)
    y += 10

    # --- White Timer (Bottom of Section) ---
    if state.timer_active:
        w_col = constants.SUCCESS if state.current_turn_color == 'white' else constants.TEXT_DIM
        w_lbl = font_hint.render("WHITE TIME", True, w_col)
        w_val = font_timer.render(format_time(state.white_time), True, w_col)
        state.screen.blit(w_lbl, (constants.SIDEBAR_X + pad, y))
        state.screen.blit(w_val, (constants.SIDEBAR_X + constants.SIDEBAR_WIDTH - w_val.get_width() - pad, y - 5))
        y += w_lbl.get_height() + 20

    # --- Advice Section ---
    lbl = font_hint.render("COACH ADVICE", True, constants.TEXT_DIM)
    state.screen.blit(lbl, (constants.SIDEBAR_X + pad, y))
    y += lbl.get_height() + 6
    wrapped = wrap_text(state.ai_coach_message, font_small, constants.SIDEBAR_WIDTH - pad * 2)
    for line in wrapped:
        if y + font_small.get_height() > constants.WINDOW_H - 10:
            break
        surf = font_small.render(line, True, constants.TEXT_BRIGHT)
        state.screen.blit(surf, (constants.SIDEBAR_X + pad, y))
        y += surf.get_height() + 3

    return {
        'hint': h_rect,
        'bot_tog': t_rect,
        'clock_tog': tog_rect,
        'presets': preset_rects
    }

def draw_history_panel():
    """Renders the move history log on the rightmost side."""
    hx = constants.HISTORY_X
    pygame.draw.rect(state.screen, constants.BG_DARK, (hx, 0, constants.HISTORY_WIDTH, constants.WINDOW_H))
    pygame.draw.line(state.screen, constants.ACCENT, (hx, 0), (hx, constants.WINDOW_H), 2)
    
    pad = 16
    y = 12
    font_title = pygame.font.SysFont('Segoe UI', 20, bold=True)
    font_log   = pygame.font.SysFont('Consolas', 14)
    
    title = font_title.render("MOVE HISTORY", True, constants.TEXT_DIM)
    state.screen.blit(title, (hx + pad, y))
    y += title.get_height() + 8
    pygame.draw.line(state.screen, (50, 52, 70), (hx + pad, y), (hx + constants.HISTORY_WIDTH - pad, y), 1)
    y += 12
    
    # Show last 30 moves
    log_slice = state.game_move_log[-30:]
    for entry in log_slice:
        entry_surf = font_log.render(entry, True, constants.TEXT_BRIGHT)
        state.screen.blit(entry_surf, (hx + pad, y))
        y += entry_surf.get_height() + 5
        if y > constants.WINDOW_H - 20:
            break
