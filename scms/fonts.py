from pathlib import Path
import pygame

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = PROJECT_ROOT / "assets" / "fonts"

REGULAR_FONT = FONT_DIR / "Inter_24pt-Regular.ttf"
BOLD_FONT = FONT_DIR / "Inter_24pt-SemiBold.ttf"

def load_font(size, bold=False):
    font_path = BOLD_FONT if bold else REGULAR_FONT

    if font_path.exists():
        return pygame.font.Font(str(font_path), size)
    
    return pygame.font.SysFont("Arial", size, bold=bold)